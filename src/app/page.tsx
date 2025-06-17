"use client";

import { useState } from "react";
import axios from "axios";
import Image from "next/image";
import YouTubeLogo from "@/app/components/YoutubeLogo";
import Spinner from "@/app/components/Spinner";

export default function Home() {
  const [url, setUrl] = useState("");
  const [mp3Link, setMp3Link] = useState("");
  const [youtubeTitle, setYoutubeTitle] = useState("");
  const [youtubeThumbnail, setYoutubeThumbnail] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMp3Link("");
    setYoutubeTitle("");
    setYoutubeThumbnail(null);

    try {
      const res = await axios.post("/api/download", { url });
      if (res?.data) {
        const { downloadUrl, title, thumbnail } = res.data;
        setMp3Link(downloadUrl);
        setYoutubeTitle(title);
        setYoutubeThumbnail(thumbnail);
        setUrl("");
      }
    } catch (err) {
      console.log(err);
      alert("轉換失敗");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center p-8 bg-gradient-to-l from-zinc-950 via-zinc-900 to-zinc-950 backdrop-blur-sm shadow-inner">
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-4">
        <h1 className="text-xl font-bold flex items-center">
          <YouTubeLogo width={100} /> 轉 MP3
        </h1>
        <input
          type="text"
          placeholder="輸入 YouTube 連結"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full p-2 border rounded focus:ring-2 focus:ring-slate-500 focus:outline-none"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-slate-800 text-slate-400 p-2 rounded hover:bg-slate-800/80 hover:text-slate-600 transition"
        >
          {loading ? <Spinner /> : "轉換"}
        </button>
        {mp3Link && (
          <div>
            {youtubeThumbnail && (
              <Image
                src={youtubeThumbnail}
                alt="YouTube Thumbnail"
                width={480}
                height={360}
                className="w-full rounded mt-10"
              />
            )}
            {youtubeTitle && <p className="my-4 font-bold ">{youtubeTitle}</p>}
            <a
              href={mp3Link}
              className="text-slate-400 border p-2 rounded hover:bg-slate-800 hover:text-slate-500 transition font-bold"
              download
            >
              下載 MP3
            </a>
          </div>
        )}
      </form>
    </main>
  );
}
