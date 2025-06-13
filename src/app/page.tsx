"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [url, setUrl] = useState("");
  const [mp3Link, setMp3Link] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMp3Link("");

    console.log(url);

    try {
      const res = await axios.post("/api/download", { url });
      setMp3Link(res.data.downloadUrl);
    } catch (err) {
      console.log(err);
      alert("轉換失敗");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center p-8">
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-4">
        <h1 className="text-xl font-bold">YouTube 轉 MP3</h1>
        <input
          type="text"
          placeholder="輸入 YouTube 連結"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-500 text-white p-2 rounded"
        >
          {loading ? "轉換中..." : "轉換"}
        </button>
        {mp3Link && (
          <a
            href={mp3Link}
            className="block text-blue-600 underline mt-2"
            download
          >
            下載 MP3
          </a>
        )}
      </form>
    </main>
  );
}
