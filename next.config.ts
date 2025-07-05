import { createMDX } from 'fumadocs-mdx/next';
import type { NextConfig } from 'next';

const withMDX = createMDX();

const config: NextConfig = {
  // output: 'export', // static export
  reactStrictMode: true,
  serverExternalPackages: [
    'shiki',
  ],
  eslint: {
    ignoreDuringBuilds: true,
  },
  images: {
    // unoptimized: true, // if using static export
    remotePatterns: [
      {protocol: 'https',hostname: 'pigsty.io',port: '',pathname: '/**'},
      {protocol: 'https',hostname: 'pigsty.cc',port: '',pathname: '/**'}
    ],
  },
  trailingSlash: true, // do it right?
};

export default withMDX(config);
