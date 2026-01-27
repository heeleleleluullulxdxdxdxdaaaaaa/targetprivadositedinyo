const nextConfig = {
  output: 'export',
  distDir: 'dist',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  // Serve static HTML file
  async rewrites() {
    return [
      {
        source: '/',
        destination: '/index.html',
      },
    ];
  }
};

module.exports = nextConfig;