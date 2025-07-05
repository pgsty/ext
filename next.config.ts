import { createMDX } from 'fumadocs-mdx/next';
import type { NextConfig } from 'next';

const withMDX = createMDX();

const config: NextConfig = {
  reactStrictMode: true,
    serverExternalPackages: [
    'shiki',
  ],
  eslint: {
    ignoreDuringBuilds: true,
  },
  images: {
    remotePatterns: [
      {protocol: 'https',hostname: 'pigsty.io',port: '',pathname: '/**'},
      {protocol: 'https',hostname: 'pigsty.cc',port: '',pathname: '/**'}
    ],
  },
};

export default withMDX(config);
