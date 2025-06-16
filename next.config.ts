import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    domains: ['i.ytimg.com'],
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        // destination: 'https://youtube-mp3-converter.up.railway.app/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ]
  },
};

export default nextConfig;
