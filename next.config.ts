import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://youtube-mp3-converter.up.railway.app/:path*',
      },
    ]
  },
};

export default nextConfig;
