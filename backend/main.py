from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI()

# CORS 設定（開發中可開放所有來源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.post("/download")
async def download_audio(req: URLRequest, request: Request):
    url = req.url
    unique_id = str(uuid.uuid4())
    filename = unique_id
    output_path = f"downloads/{filename}"  # yt-dlp 會自動加 .mp3

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

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)  # 抓資料＋下載
            title = info.get("title")
            thumbnail = info.get("thumbnail")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    base_url = str(request.base_url).rstrip("/")
    return {
        "downloadUrl": f"{base_url}/file/{filename}.mp3",
        "title": title,
        "thumbnail": thumbnail,
    }

@app.get("/file/{filename}")
async def serve_file(filename: str):
    file_path = f"downloads/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='audio/mpeg', filename=filename)
    return JSONResponse(status_code=404, content={"error": "File not found"})