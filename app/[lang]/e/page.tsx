import { DocsPage, DocsBody, DocsDescription, DocsTitle } from 'fumadocs-ui/page';
import fs from 'fs';
import path from 'path';
import Link from 'next/link';
import { Badge } from '@/components/ui/badge';

interface ExtensionSummary {
  id: number;
  name: string;
  pkg: string;
  category: string;
  version: string;
  en_desc: string;
  zh_desc: string;
  url: string;
  license: string;
  lang: string;
  contrib: boolean;
  lead: boolean;
}

interface ExtensionIndex {
  extensions: ExtensionSummary[];
  total_count: number;
  categories: string[];
  generated_at: string;
}

async function getExtensionIndex(): Promise<ExtensionIndex | null> {
  try {
    const indexPath = path.join(process.cwd(), 'data', 'extensions', 'index.json');
    
    if (!fs.existsSync(indexPath)) {
      return null;
    }
    
    const indexContent = fs.readFileSync(indexPath, 'utf-8');
    const indexData = JSON.parse(indexContent);
    
    return indexData as ExtensionIndex;
  } catch (error) {
    console.error('Error loading extension index:', error);
    return null;
  }
}

function formatCategoryBadge(category: string): React.JSX.Element {
  const categoryColors: Record<string, string> = {
    'TIME': 'blue-subtle',
    'GIS': 'green-subtle',
    'RAG': 'purple-subtle',
    'FTS': 'amber-subtle',
    'OLAP': 'red-subtle',
    'FEAT': 'pink-subtle',
    'LANG': 'teal-subtle',
    'TYPE': 'gray-subtle',
    'UTIL': 'amber-subtle',
    'FUNC': 'pink-subtle',
    'ADMIN': 'gray-subtle',
    'STAT': 'green-subtle',
    'SEC': 'red-subtle',
    'FDW': 'blue-subtle',
    'SIM': 'teal-subtle',
    'ETL': 'purple-subtle'
  };
  
  const color = categoryColors[category] || 'gray-subtle';
  
  return (
    <Link href={`/cate/${category.toLowerCase()}`} className="no-underline">
      <Badge variant={color as any}>{category}</Badge>
    </Link>
  );
}

export default async function ExtensionsPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  const indexData = await getExtensionIndex();

  if (!indexData) {
    return (
      <DocsPage toc={[]} full={true}>
        <DocsTitle>Extensions</DocsTitle>
        <DocsDescription>PostgreSQL Extensions Catalog</DocsDescription>
        <DocsBody>
          <div>Failed to load extension data.</div>
        </DocsBody>
      </DocsPage>
    );
  }

  // Sort extensions by category, then by name
  const sortedExtensions = [...indexData.extensions].sort((a, b) => {
    if (a.category !== b.category) {
      return a.category.localeCompare(b.category);
    }
    return a.name.localeCompare(b.name);
  });

  // Group by category for display
  const extensionsByCategory = sortedExtensions.reduce((acc, ext) => {
    if (!acc[ext.category]) {
      acc[ext.category] = [];
    }
    acc[ext.category].push(ext);
    return acc;
  }, {} as Record<string, ExtensionSummary[]>);

  return (
    <DocsPage toc={[]} full={true}>
      <DocsTitle>PostgreSQL Extensions</DocsTitle>
      <DocsDescription>
        Comprehensive catalog of {indexData.total_count} PostgreSQL extensions
      </DocsDescription>
      <DocsBody>
        <div className="space-y-8">
          {/* Summary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-muted p-4 rounded-lg">
              <div className="text-2xl font-bold">{indexData.total_count}</div>
              <div className="text-muted-foreground">Total Extensions</div>
            </div>
            <div className="bg-muted p-4 rounded-lg">
              <div className="text-2xl font-bold">{indexData.categories.length}</div>
              <div className="text-muted-foreground">Categories</div>
            </div>
            <div className="bg-muted p-4 rounded-lg">
              <div className="text-2xl font-bold">
                {sortedExtensions.filter(ext => ext.contrib).length}
              </div>
              <div className="text-muted-foreground">Built-in Extensions</div>
            </div>
          </div>

          {/* Categories Overview */}
          <div>
            <h2>Categories</h2>
            <div className="flex flex-wrap gap-2">
              {indexData.categories.sort().map(category => (
                <div key={category} className="flex items-center gap-2">
                  {formatCategoryBadge(category)}
                  <span className="text-sm text-muted-foreground">
                    ({extensionsByCategory[category]?.length || 0})
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Extensions Table */}
          <div>
            <h2>All Extensions</h2>
            <div className="overflow-x-auto">
              <table className="w-full border-collapse border">
                <thead>
                  <tr>
                    <th className="text-left p-2 border">ID</th>
                    <th className="text-left p-2 border">Name</th>
                    <th className="text-left p-2 border">Package</th>
                    <th className="text-left p-2 border">Category</th>
                    <th className="text-left p-2 border">Version</th>
                    <th className="text-left p-2 border">Description</th>
                  </tr>
                </thead>
                <tbody>
                  {sortedExtensions.map(ext => {
                    const description = lang === 'cn' && ext.zh_desc 
                      ? ext.zh_desc 
                      : ext.en_desc || 'No description available';
                    
                    return (
                      <tr key={ext.name} className="hover:bg-muted/50">
                        <td className="p-2 border text-center">{ext.id}</td>
                        <td className="p-2 border">
                          <Link href={`/ext/${ext.name}`} className="font-mono hover:underline">
                            {ext.name}
                          </Link>
                        </td>
                        <td className="p-2 border">
                          <code className="text-sm">{ext.pkg}</code>
                        </td>
                        <td className="p-2 border">
                          {formatCategoryBadge(ext.category)}
                        </td>
                        <td className="p-2 border">
                          <code className="text-sm">{ext.version}</code>
                        </td>
                        <td className="p-2 border text-sm">
                          {description.length > 100 
                            ? `${description.substring(0, 100)}...` 
                            : description
                          }
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Generation Info */}
          <div className="text-sm text-muted-foreground">
            Data generated at: {new Date(indexData.generated_at).toLocaleString()}
          </div>
        </div>
      </DocsBody>
    </DocsPage>
  );
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const indexData = await getExtensionIndex();
  
  return {
    title: 'PostgreSQL Extensions',
    description: `Comprehensive catalog of ${indexData?.total_count || 400} PostgreSQL extensions`,
  };
}