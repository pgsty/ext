import { notFound } from 'next/navigation';
import { DocsPage, DocsBody, DocsDescription, DocsTitle } from 'fumadocs-ui/page';
import fs from 'fs';
import path from 'path';
import ExtensionTemplate from '@/components/extension-template';

interface MatrixData {
  pg: number;
  os: string;
  type: string;
  os_code: string;
  os_arch: string;
  pkg: string;
  ext: string;
  pname: string;
  miss: boolean;
  hide: boolean;
  pkg_repo: string;
  pkg_ver: string;
  count: number;
}

interface PackageData {
  os: string;
  pg: number;
  name: string;
  ver: string;
  version: string;
  release: string;
  file: string;
  size: number;
  url: string;
  sha256: string;
}

interface ExtensionData {
  id: number;
  name: string;
  pkg: string;
  lead_ext: string;
  category: string;
  state: string;
  url: string;
  license: string;
  tags: string[];
  version: string;
  repo: string;
  lang: string;
  contrib: boolean;
  lead: boolean;
  has_bin: boolean;
  has_lib: boolean;
  need_ddl: boolean;
  need_load: boolean;
  trusted: boolean;
  relocatable: boolean;
  schemas: string[];
  pg_ver: string[];
  requires: string[];
  require_by: string[];
  see_also: string[];
  rpm_ver: string;
  rpm_repo: string;
  rpm_pkg: string;
  rpm_pg: string[];
  rpm_deps: string[];
  deb_ver: string;
  deb_repo: string;
  deb_pkg: string;
  deb_deps: string[];
  deb_pg: string[];
  source: string | null;
  extra: Record<string, any>;
  en_desc: string;
  zh_desc: string;
  comment: string;
  mtime: string;
  siblings: string[];
  matrix: MatrixData[];
  package: PackageData[];
}

async function getExtensionData(name: string): Promise<ExtensionData | null> {
  try {
    const filePath = path.join(process.cwd(), 'data', 'ext', `${name}.json`);
    
    if (!fs.existsSync(filePath)) {
      return null;
    }
    
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const data = JSON.parse(fileContent);
    
    return data as ExtensionData;
  } catch (error) {
    console.error(`Error loading extension data for ${name}:`, error);
    return null;
  }
}

async function getAllExtensions(): Promise<{ name: string; lang: string }[]> {
  try {
    const extDir = path.join(process.cwd(), 'data', 'ext');
    
    if (!fs.existsSync(extDir)) {
      return [];
    }
    
    const files = fs.readdirSync(extDir)
      .filter(file => file.endsWith('.json'))
      .map(file => file.replace('.json', ''));
    
    const langs = ['en', 'cn'];
    const params = [];
    
    for (const lang of langs) {
      for (const extName of files) {
        params.push({ name: extName, lang });
      }
    }
    
    return params;
  } catch (error) {
    console.error('Error loading extension directory:', error);
    return [];
  }
}

export default async function ExtensionPage({
  params,
}: {
  params: Promise<{ extension: string; lang: string }>;
}) {
  const { extension, lang } = await params;
  const extensionData = await getExtensionData(extension);

  if (!extensionData) {
    notFound();
  }

  // Use description based on language
  const description = lang === 'cn' && extensionData.zh_desc 
    ? extensionData.zh_desc 
    : extensionData.en_desc || 'PostgreSQL Extension';

  return (
    <DocsPage toc={[]} full={true}>
      <DocsTitle>{extensionData.name}</DocsTitle>
      <DocsDescription>{description}</DocsDescription>
      <DocsBody>
        <ExtensionTemplate data={extensionData} />
      </DocsBody>
    </DocsPage>
  );
}

export async function generateStaticParams() {
  const allExtensions = await getAllExtensions();
  
  return allExtensions.map(({ name, lang }) => ({
    extension: name,
    lang: lang,
  }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ extension: string; lang: string }>;
}) {
  const { extension, lang } = await params;
  const extensionData = await getExtensionData(extension);

  if (!extensionData) {
    return {
      title: 'Extension Not Found',
      description: 'The requested PostgreSQL extension could not be found.',
    };
  }

  const description = lang === 'cn' && extensionData.zh_desc 
    ? extensionData.zh_desc 
    : extensionData.en_desc || 'PostgreSQL Extension';

  return {
    title: extensionData.name,
    description,
  };
}