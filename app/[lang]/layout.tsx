import "@/app/global.css"
import { RootProvider } from 'fumadocs-ui/provider';
import type { Translations } from 'fumadocs-ui/i18n';

const cn: Partial<Translations> = {
  search: '搜索',
  searchNoResult: '未找到',
  toc: '目录',
  tocNoHeadings: '目录',
  lastUpdate: '最后更新',
  chooseLanguage: '选择语言',
  nextPage: '下一页',
  previousPage: '上一页',
  chooseTheme: '选择主题',
  editOnGithub: '编辑',
};

const locales = [
  {
    name: 'English',
    locale: 'en',
  },
  {
    name: '简体中文',
    locale: 'cn',
  },
];

export default async function RootLayout({
  params,
  children,
}: {
  params: Promise<{ lang: string }>;
  children: React.ReactNode;
}) {
  const lang = (await params).lang;

  return (
    <html lang={lang} suppressHydrationWarning>
      <body>
        <RootProvider
          i18n={{
            locale: lang,
            locales,
            translations: { cn }[lang],
          }}

        >
          {children}
        </RootProvider>
      </body>
    </html>
  );
}