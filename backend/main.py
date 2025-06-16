from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI() # 建立 FastAPI 應用實例

# CORS 設定（開發中可開放所有來源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel): # 定義 POST 請求的資料結構，需包含一個 url 字串欄位（YouTube 的連結）
    url: str

@app.post("/download")
async def download_audio(req: URLRequest, request: Request): # 自定義一個 download_audio function
    url = req.url
    unique_id = str(uuid.uuid4())
    filename = unique_id
    output_path = f"downloads/{filename}" # (1)yt-dlp 會自動加 .mp3  (2)f"": Python 的 f-string（formatted string）將變數 filename 插入到字串中的指定位


    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path, # 下載檔案後，存放在後端伺服器的這個 output_path
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3', # yt-dlp 在下載完成後，會立刻轉成 .mp3
            'preferredquality': '192', # 音質設定為 192kbps（適中音質，體積小）
        }],
        'noplaylist': True, # 若 URL 是播放清單，只抓單一影片
        'http_headers': { # 偽裝為一般使用者的 header，避免 bot 檢測
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
    }

    os.makedirs("downloads", exist_ok=True) # 若 downloads/ 資料夾不存在就建立

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # 建立 yt-dlp 實例並下載音訊
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