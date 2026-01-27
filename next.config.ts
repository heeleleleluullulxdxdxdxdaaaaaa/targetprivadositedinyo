import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  distDir: 'dist',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  webpack: (config) => {
    config.module.rules.push({
      test: /\.(png|jpe?g|gif|svg|mp3|wav)$/i,
      use: [
        {
          loader: 'file-loader',
          options: {
            publicPath: '/_next/static/media/',
            outputPath: 'static/media/',
            name: '[name].[hash:7].[ext]'
          }
        }
      ]
    });
    return config;
  }
};

export default nextConfig;