import { docs, ext } from '@/.source';
import { loader } from 'fumadocs-core/source';
import { i18n } from './i18n';
import { icons } from 'lucide-react';
import { createElement } from 'react';

// See https://fumadocs.vercel.app/docs/headless/source-api for more info
export const source = loader({
  // it assigns a URL to your pages
  i18n,
  baseUrl: '/',
  source: docs.toFumadocsSource(),
  icon(icon) {
    if (!icon) {
      // You may set a default icon
      return;
    }
    if (icon in icons) return createElement(icons[icon as keyof typeof icons]);
  },
  
});

export const extSource = loader({
  i18n,
  baseUrl: '/ext',
  source: ext.toFumadocsSource(),
  icon(icon) {
    if (!icon) {
      return;
    }
    if (icon in icons) return createElement(icons[icon as keyof typeof icons]);
  },
});

