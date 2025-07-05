import type { BaseLayoutProps, LinkItemType } from 'fumadocs-ui/layouts/shared';
import { i18n } from '@/lib/i18n';
import { AlbumIcon } from 'lucide-react';
import { LayoutTemplate } from 'lucide-react';

export const linkItems = (lang: string): LinkItemType[] => [
  {
    text: 'Extension',
    url: `/${lang}/`,
    icon: <LayoutTemplate />,
    active: 'url',
  },
];

export const baseOptions = (lang: string): BaseLayoutProps => {
  return {
    i18n,
    nav: {
      title: (
        <><svg width="24" height="24" viewBox="24 15 25 27" xmlns="http://www.w3.org/2000/svg" aria-label="Logo">
            <g id="PigstyLogo" fillOpacity="1" strokeOpacity="1" stroke="none" fill="none" strokeDasharray="none">
              <g id="PigstyLayer1">
                <g id="Group_17">
                  <g id="Graphic_15">
                    <path d="M 31.73258 28.426406 L 34.130154 24.27369 L 38.9253 24.27369 L 41.322873 28.426406 L 38.9253 32.579122 L 34.130154 32.579122 Z" fill="#bbb" fillOpacity=".9526367"/>
                    <path d="M 31.73258 28.426406 L 34.130154 24.27369 L 38.9253 24.27369 L 41.322873 28.426406 L 38.9253 32.579122 L 34.130154 32.579122 Z" stroke="white" strokeLinecap="round" strokeLinejoin="round" strokeWidth=".7453222"/>
                  </g>
                  <g id="Graphic_14">
                    <path d="M 31.73258 36.735683 L 34.130154 32.582966 L 38.9253 32.582966 L 41.322873 36.735683 L 38.9253 40.8884 L 34.130154 40.8884 Z" fill="#de372c" fillOpacity=".8545852"/>
                    <path d="M 31.73258 36.735683 L 34.130154 32.582966 L 38.9253 32.582966 L 41.322873 36.735683 L 38.9253 40.8884 L 34.130154 40.8884 Z" stroke="white" strokeLinecap="round" strokeLinejoin="round" strokeWidth=".7453222"/>
                  </g>
                  <g id="Graphic_13">
                    <path d="M 38.925406 32.612197 L 41.32298 28.45948 L 46.118125 28.45948 L 48.5157 32.612197 L 46.118125 36.764914 L 41.32298 36.764914 Z" fill="#424242" fillOpacity=".9016462"/>
                    <path d="M 38.925406 32.612197 L 41.32298 28.45948 L 46.118125 28.45948 L 48.5157 32.612197 L 46.118125 36.764914 L 41.32298 36.764914 Z" stroke="white" strokeLinecap="round" strokeLinejoin="round" strokeWidth=".7453222"/>
                  </g>
                  <g id="Graphic_12">
                    <path d="M 38.925406 24.278864 L 41.32298 20.126148 L 46.118125 20.126148 L 48.5157 24.278864 L 46.118125 28.43158 L 41.32298 28.43158 Z" fill="#ffa269" fillOpacity=".8975772"/>
                    <path d="M 38.925406 24.278864 L 41.32298 20.126148 L 46.118125 20.126148 L 48.5157 24.278864 L 46.118125 28.43158 L 41.32298 28.43158 Z" stroke="white" strokeLinecap="round" strokeLinejoin="round" strokeWidth=".7453222"/>
                  </g><g id="Graphic_11">
                    <path d="M 31.73258 20.152717 L 34.130154 16 L 38.9253 16 L 41.322873 20.152717 L 38.9253 24.305433 L 34.130154 24.305433 Z" fill="#419edb" fillOpacity=".8979957"/>
                    <path d="M 31.73258 20.152717 L 34.130154 16 L 38.9253 16 L 41.322873 20.152717 L 38.9253 24.305433 L 34.130154 24.305433 Z" stroke="white" strokeLinecap="round" strokeLinejoin="round" strokeWidth=".7453222"/></g>
                  <g id="Graphic_10">
                    <path d="M 24.5157 24.278864 L 26.913272 20.126148 L 31.70842 20.126148 L 34.10599 24.278864 L 31.70842 28.43158 L 26.913272 28.43158 Z" fill="#2f6793" fillOpacity=".9002511"/>
                    <path d="M 24.5157 24.278864 L 26.913272 20.126148 L 31.70842 20.126148 L 34.10599 24.278864 L 31.70842 28.43158 L 26.913272 28.43158 Z" stroke="white" strokeLinecap="round" strokeLinejoin="round" strokeWidth=".7453222"/>
                  </g>
                  <g id="Graphic_9">
                    <path d="M 24.55213 32.60094 L 26.949702 28.448223 L 31.74485 28.448223 L 34.14242 32.60094 L 31.74485 36.753656 L 26.949702 36.753656 Z" fill="#53ac79" fillOpacity=".9"/>
                    <path d="M 24.55213 32.60094 L 26.949702 28.448223 L 31.74485 28.448223 L 34.14242 32.60094 L 31.74485 36.753656 L 26.949702 36.753656 Z" stroke="white" strokeLinecap="round" strokeLinejoin="round" strokeWidth=".7453222"/>
                  </g>
                </g>
              </g>
            </g>
          </svg>
          PIGSTY
        </>
      ),
    },
    githubUrl: 'https://github.com/pgsty/pigsty',
  }
}
