from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import os
from fastapi.responses import FileResponse

app = FastAPI()

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.post("/download")
async def download_audio(req: URLRequest):
    url = req.url
    output_path = f"downloads/audio.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    os.makedirs("downloads", exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return {"downloadUrl": f"http://localhost:8000/file/audio.mp3"}

@app.get("/file/audio.mp3")
async def serve_file():
    return FileResponse("downloads/audio.mp3", media_type='audio/mpeg', filename="audio.mp3")