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
    }

    os.makedirs("downloads", exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return {"downloadUrl": f"http://localhost:8000/file/audio.mp3"}

@app.get("/file/audio.mp3")
async def serve_file():
    return FileResponse("downloads/audio.mp3", media_type='audio/mpeg', filename="audio.mp3")