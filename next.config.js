const nextConfig = {
  output: 'export',
  distDir: 'out',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  experimental: {
    appDir: false
  }
};

module.exports = nextConfig;
