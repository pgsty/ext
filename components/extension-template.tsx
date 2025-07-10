import { File, Folder, Files } from 'fumadocs-ui/components/files';
import { Package, Box } from 'lucide-react';
import { Callout } from 'fumadocs-ui/components/callout';
import { Badge } from '@/components/ui/badge';
import { TooltipIconButton } from '@/components/ui/tooltip-icon-button';
import { DynamicCodeBlock } from 'fumadocs-ui/components/dynamic-codeblock';
import { Tab, Tabs } from 'fumadocs-ui/components/tabs';
import Link from 'next/link';
import {
    Scale, Clock, Globe, Brain, Search, ChartNoAxesCombined,
    Sparkles, BookA, Boxes, Wrench, Variable, Landmark,
    Activity, Shield, FileInput, FileCode2, Shell, Truck, Blocks
} from 'lucide-react';

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
  pkg_repo: string | null;
  pkg_ver: string | null;
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

const DEFAULT_OS = ['el8.x86_64', 'el8.aarch64', 'el9.x86_64', 'el9.aarch64', 'd12.x86_64', 'd12.aarch64', 'u22.x86_64', 'u22.aarch64', 'u24.x86_64', 'u24.aarch64'];
const DEFAULT_PG = [17, 16, 15, 14, 13];

function formatBool(value: boolean | null, trueText: string = "Yes", falseText: string = "No"): string {
  if (value === null) return "Unknown";
  return value ? trueText : falseText;
}

function formatRepoTag(repo: string): React.JSX.Element {
  const badges: Record<string, React.JSX.Element> = {
    'PGDG': <Badge variant="blue-subtle"><span className="font-bold">PGDG</span></Badge>,
    'PIGSTY': <Badge variant="amber-subtle"><span className="font-bold">PIGSTY</span></Badge>,
    'CONTRIB': <Badge variant="green-subtle"><span className="font-bold">CONTRIB</span></Badge>,
    'MIXED': <Badge variant="gray-subtle"><span className="font-bold">MIXED</span></Badge>
  };
  return badges[repo] || <Badge variant="gray-subtle"><span className="font-bold">{repo}</span></Badge>;
}

function formatLicenseTag(license: string): React.JSX.Element {
  const licenseMapping: Record<string, { name: string; anchor: string; variant: string }> = {
    'PostgreSQL': { name: 'PostgreSQL', anchor: 'postgresql', variant: 'blue-subtle' },
    'MIT': { name: 'MIT', anchor: 'mit', variant: 'blue-subtle' },
    'ISC': { name: 'ISC', anchor: 'isc', variant: 'blue-subtle' },
    'BSD-0': { name: 'BSD 0-Clause', anchor: 'bsd-0-clause', variant: 'blue-subtle' },
    'BSD 0-Clause': { name: 'BSD 0-Clause', anchor: 'bsd-0-clause', variant: 'blue-subtle' },
    'BSD-2': { name: 'BSD 2-Clause', anchor: 'bsd-2-clause', variant: 'blue-subtle' },
    'BSD 2-Clause': { name: 'BSD 2-Clause', anchor: 'bsd-2-clause', variant: 'blue-subtle' },
    'BSD-3': { name: 'BSD 3-Clause', anchor: 'bsd-3-clause', variant: 'blue-subtle' },
    'BSD 3-Clause': { name: 'BSD 3-Clause', anchor: 'bsd-3-clause', variant: 'blue-subtle' },
    'Artistic': { name: 'Artistic', anchor: 'artistic', variant: 'green-subtle' },
    'Apache-2.0': { name: 'Apache-2.0', anchor: 'apache-20', variant: 'green-subtle' },
    'MPL-2.0': { name: 'MPL-2.0', anchor: 'mpl-20', variant: 'green-subtle' },
    'MPLv2': { name: 'MPL-2.0', anchor: 'mpl-20', variant: 'green-subtle' },
    'GPL-2.0': { name: 'GPL-2.0', anchor: 'gpl-20', variant: 'amber-subtle' },
    'GPLv2': { name: 'GPL-2.0', anchor: 'gpl-20', variant: 'amber-subtle' },
    'GPL-3.0': { name: 'GPL-3.0', anchor: 'gpl-30', variant: 'amber-subtle' },
    'GPLv3': { name: 'GPL-3.0', anchor: 'gpl-30', variant: 'amber-subtle' },
    'LGPL-2.1': { name: 'LGPL-2.1', anchor: 'lgpl-21', variant: 'amber-subtle' },
    'LGPLv2': { name: 'LGPL-2.1', anchor: 'lgpl-21', variant: 'amber-subtle' },
    'LGPL-3.0': { name: 'LGPL-3.0', anchor: 'lgpl-30', variant: 'amber-subtle' },
    'LGPLv3': { name: 'LGPL-3.0', anchor: 'lgpl-30', variant: 'amber-subtle' },
    'AGPL-3.0': { name: 'AGPL-3.0', anchor: 'agpl-30', variant: 'red-subtle' },
    'AGPLv3': { name: 'AGPL-3.0', anchor: 'agpl-30', variant: 'red-subtle' },
    'Timescale': { name: 'Timescale', anchor: 'timescale', variant: 'gray-subtle' }
  };
  
  const info = licenseMapping[license] || { name: license, anchor: license.toLowerCase().replace(/[^a-z0-9]/g, ''), variant: 'gray-subtle' };
  
  return (
    <a href={`/ext/list/license#${info.anchor}`} className="no-underline">
      <Badge icon={<Scale />} variant={info.variant as any}>{info.name}</Badge>
    </a>
  );
}

function formatLanguageTag(language: string): React.JSX.Element {
  const langMap: Record<string, { variant: string; anchor: string }> = {
    'Python': { variant: 'blue-subtle', anchor: '/list/lang#python' },
    'Rust': { variant: 'amber-subtle', anchor: '/list/lang#rust' },
    'SQL': { variant: 'green-subtle', anchor: '/list/lang#sql' },
    'Java': { variant: 'pink-subtle', anchor: '/list/lang#java' },
    'Data': { variant: 'teal-subtle', anchor: '/list/lang#data' },
    'C++': { variant: 'purple-subtle', anchor: '/list/lang#c-1' },
    'C': { variant: 'blue-subtle', anchor: '/list/lang#c' },
  };
  
  const info = langMap[language] || { variant: 'gray-subtle', anchor: '/list/lang#other' };
  
  return (
    <a href={`/ext${info.anchor}`}>
      <Badge icon={<FileCode2 />} variant={info.variant as any}>{language || "N/A"}</Badge>
    </a>
  );
}

function formatCategoryTag(category: string): React.JSX.Element {
  const categoryMeta: Record<string, { icon: string; color: string }> = {
    'TIME': { icon: 'Clock', color: 'blue-subtle' },
    'GIS': { icon: 'Globe', color: 'green-subtle' }, 
    'RAG': { icon: 'Brain', color: 'purple-subtle' },
    'FTS': { icon: 'Search', color: 'amber-subtle' },
    'OLAP': { icon: 'ChartNoAxesCombined', color: 'red-subtle' },
    'FEAT': { icon: 'Sparkles', color: 'pink-subtle' },
    'LANG': { icon: 'BookA', color: 'teal-subtle' },
    'TYPE': { icon: 'Boxes', color: 'gray-subtle' },
    'UTIL': { icon: 'Wrench', color: 'amber-subtle' },
    'FUNC': { icon: 'Variable', color: 'pink-subtle' },
    'ADMIN': { icon: 'Landmark', color: 'gray-subtle' },
    'STAT': { icon: 'Activity', color: 'green-subtle' },
    'SEC': { icon: 'Shield', color: 'red-subtle' },
    'FDW': { icon: 'FileInput', color: 'blue-subtle' },
    'SIM': { icon: 'Shell', color: 'teal-subtle' },
    'ETL': { icon: 'Truck', color: 'purple-subtle' }
  };
  
  const meta = categoryMeta[category] || { icon: 'Blocks', color: 'gray-subtle' };
  const iconComponentMap = {
    Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, 
    Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck, Blocks
  };
  const IconComponent = iconComponentMap[meta.icon as keyof typeof iconComponentMap] || Blocks;
  
  return (
    <a href={`/ext/cate/${category.toLowerCase()}`} className="no-underline">
      <Badge icon={<IconComponent />} variant={meta.color as any}>{category}</Badge>
    </a>
  );
}

function PackageInfoSection({ ext }: { ext: ExtensionData }) {
  const rows = [];
  
  // Check if has RPM packages
  const hasRpm = ext.rpm_repo && ext.rpm_repo.trim() !== '';
  if (hasRpm) {
    const rpmPgBadges = DEFAULT_PG.map(pg => {
      const isSupported = ext.rpm_pg.includes(String(pg));
      return (
        <Badge key={pg} variant={isSupported ? "green-subtle" : "red-subtle"}>
          {pg}
        </Badge>
      );
    });
    
    const rpmDepsElements = ext.rpm_deps.length > 0 ? (
      <div className="space-y-1">
        {ext.rpm_deps.map((dep, idx) => (
          <div key={idx}><code>{dep}</code></div>
        ))}
      </div>
    ) : '-';
    
    rows.push(
      <tr key="rpm">
        <td className="text-center"><strong>EL</strong></td>
        <td className="text-center">{formatRepoTag(ext.rpm_repo)}</td>
        <td className="text-center"><code>{ext.rpm_pkg || '-'}</code></td>
        <td className="text-center"><code>{ext.rpm_ver || '-'}</code></td>
        <td className="text-center">{rpmDepsElements}</td>
        <td className="text-center">{rpmPgBadges}</td>
      </tr>
    );
  }
  
  // Check if has DEB packages
  const hasDeb = ext.deb_repo && ext.deb_repo.trim() !== '';
  if (hasDeb) {
    const debPgBadges = DEFAULT_PG.map(pg => {
      const isSupported = ext.deb_pg.includes(String(pg));
      return (
        <Badge key={pg} variant={isSupported ? "green-subtle" : "red-subtle"}>
          {pg}
        </Badge>
      );
    });
    
    const debDepsElements = ext.deb_deps.length > 0 ? (
      <div className="space-y-1">
        {ext.deb_deps.map((dep, idx) => (
          <div key={idx}><code>{dep}</code></div>
        ))}
      </div>
    ) : '-';
    
    rows.push(
      <tr key="deb">
        <td className="text-center"><strong>Debian</strong></td>
        <td className="text-center">{formatRepoTag(ext.deb_repo)}</td>
        <td className="text-center"><code>{ext.deb_pkg || '-'}</code></td>
        <td className="text-center"><code>{ext.deb_ver || '-'}</code></td>
        <td className="text-center">{debDepsElements}</td>
        <td className="text-center">{debPgBadges}</td>
      </tr>
    );
  }
  
  if (rows.length === 0) {
    rows.push(
      <tr key="none">
        <td colSpan={6} className="text-center">No package information available</td>
      </tr>
    );
  }
  
  return (
    <table className="w-full border-collapse border">
      <thead>
        <tr>
          <th className="text-center"><TooltipIconButton tooltip="Linux distribution family, EL or Debian" side="top">Distro</TooltipIconButton></th>
          <th className="text-center"><TooltipIconButton tooltip="Package repository" side="top">Repo</TooltipIconButton></th>
          <th className="text-center"><TooltipIconButton tooltip="The RPM/DEB Package Name Pattern (replace $v with real pg major)" side="top">Package Name</TooltipIconButton></th>
          <th className="text-center"><TooltipIconButton tooltip="Latest package version" side="top">Version</TooltipIconButton></th>
          <th className="text-center"><TooltipIconButton tooltip="RPM/DEB Package dependencies" side="top">Deps</TooltipIconButton></th>
          <th className="text-center"><TooltipIconButton tooltip="Available in these PostgreSQL Major Versions" side="top">PG Major</TooltipIconButton></th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  );
}

function AvailabilityMatrix({ ext }: { ext: ExtensionData }) {
  const pgHeaders = DEFAULT_PG.map(pg => {
    const isSupported = ext.pg_ver.includes(String(pg));
    return (
      <th key={pg} className={`text-center ${isSupported ? '' : 'text-red-500'}`}>
        <strong>PG{pg}</strong>
      </th>
    );
  });
  
  const rows = DEFAULT_OS.map(os => {
    const cells = DEFAULT_PG.map(pg => {
      // Find matrix entry for this os/pg combination
      const matrixEntry = ext.matrix.find(m => m.os === os && m.pg === pg);
      
      if (matrixEntry && matrixEntry.pkg_ver && !matrixEntry.miss) {
        const { pkg_ver, pkg_repo } = matrixEntry;
        let variant = 'purple-subtle';
        if (pkg_repo === 'pigsty') variant = 'amber-subtle';
        else if (pkg_repo === 'pgdg') variant = 'blue-subtle';
        else if (pkg_repo === 'contrib') variant = 'green-subtle';
        
        return (
          <td key={pg} className="text-center">
            <Badge variant={variant as any}>{pkg_ver}</Badge>
          </td>
        );
      } else if (ext.contrib && ext.pg_ver.includes(String(pg))) {
        return (
          <td key={pg} className="text-center">
            <Badge variant="green-subtle">{ext.version}</Badge>
          </td>
        );
      } else {
        return (
          <td key={pg} className="text-center">
            <Badge variant="red-subtle">✗</Badge>
          </td>
        );
      }
    });
    
    return (
      <tr key={os}>
        <td className="text-center"><code>{os}</code></td>
        {cells}
      </tr>
    );
  });
  
  return (
    <table className="w-full border-collapse border">
      <thead>
        <tr>
          <th className="text-center"><TooltipIconButton tooltip="Linux Distro Arch / PostgreSQL Major Version" side="top">Linux / PostgreSQL</TooltipIconButton></th>
          {pgHeaders}
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  );
}

function DependenciesSection({ ext }: { ext: ExtensionData }) {
  const sections = [];
  
  // Dependencies (what this extension requires)
  if (ext.requires.length > 0) {
    const depsLinks = ext.requires.map((dep, index) => (
      <span key={dep}>
        {index > 0 && ', '}
        <Link href={`/e/${dep}`}><code>{dep}</code></Link>
      </span>
    ));
    sections.push(
      <Callout key="deps" title="Dependencies" type="warn">
        <div>This extension depends on: {depsLinks}</div>
      </Callout>
    );
  }
  
  // Reverse dependencies (what depends on this extension)
  if (ext.require_by.length > 0) {
    const dependentLinks = ext.require_by.map((dep, index) => (
      <span key={dep}>
        {index > 0 && ', '}
        <Link href={`/e/${dep}`}><code>{dep}</code></Link>
      </span>
    ));
    sections.push(
      <Callout key="dependents" title="Dependent Extensions" type="info">
        <div>The following extensions depend on this extension: {dependentLinks}</div>
      </Callout>
    );
  }
  
  // Comments (if extension has comment field)
  if (ext.comment && ext.comment.trim()) {
    sections.push(
      <Callout key="comments" title="Comments" type="info">
        <div>{ext.comment}</div>
      </Callout>
    );
  }
  
  return <div className="space-y-4">{sections}</div>;
}

function DownloadSection({ ext }: { ext: ExtensionData }) {
  if (ext.contrib) {
    return (
      <div>
        This extension is built-in with PostgreSQL and does not need separate download.
      </div>
    );
  }
  
  return (
    <div className="space-y-4">
      <div>
        To add the required PGDG / PIGSTY upstream repository, use:
      </div>
      
      <Tabs items={['pig', 'pigsty']}>
        <Tab value="pig">
          <DynamicCodeBlock
            lang="bash"
            code={`pig repo add pgdg -u    # add PGDG repo and update cache (leave existing repos)
pig repo add pigsty -u  # add PIGSTY repo and update cache (leave existing repos)
pig repo add pgsql -u   # add PGDG + Pigsty repo and update cache (leave existing repos)
pig repo set all -u     # set repo to all = NODE + PGSQL + INFRA  (remove existing repos)`}
          />
        </Tab>
        <Tab value="pigsty">
          <DynamicCodeBlock
            lang="bash"
            code={`./node.yml -t node_repo -e node_repo_modules=node,pgsql # -l <cluster>`}
          />
        </Tab>
      </Tabs>
      
      <div>Or download the latest packages directly:</div>
      
      <Files>
        {DEFAULT_OS.map(os => {
          const [osName, expectedArch] = os.split('.');
          
          // Map arch names: x86_64 <-> amd, aarch64 <-> arm
          const archMapping: Record<string, string[]> = {
            'x86_64': ['x86_64', 'amd', 'amd64'],
            'aarch64': ['aarch64', 'arm', 'arm64']
          };
          
          const possibleArchs = archMapping[expectedArch] || [expectedArch];
          
          const hasPackages = ext.package.some(pkg => {
            const [pkgOsCode, pkgArch] = pkg.os.split('.');
            return pkgOsCode === osName && possibleArchs.includes(pkgArch);
          });
          
          if (!hasPackages) return null;
          
          return (
            <Folder key={os} name={`${osName}.${expectedArch}`}>
              {DEFAULT_PG.filter(pg => ext.pg_ver.includes(String(pg))).map(pg => {
                const pkg = ext.package.find(p => {
                  const [pkgOsCode, pkgArch] = p.os.split('.');
                  return pkgOsCode === osName && possibleArchs.includes(pkgArch) && p.pg === pg;
                });
                
                if (!pkg) return null;
                
                const iconName = osName.startsWith('el') ? 'Package' : 'Box';
                const iconColor = expectedArch === 'x86_64' ? 'text-emerald-500' : 'text-orange-500';
                const IconComponent = iconName === 'Package' ? Package : Box;
                
                return (
                  <a key={pg} href={pkg.url || '#'}>
                    <File 
                      name={pkg.file || `${ext.name}-${pkg.ver}.rpm`} 
                      icon={<IconComponent className={iconColor} />} 
                    />
                  </a>
                );
              })}
            </Folder>
          );
        })}
      </Files>
    </div>
  );
}


function InstallSection({ ext }: { ext: ExtensionData }) {
  if (ext.contrib) {
    const sections = [];
    
    sections.push(
      <div key="contrib-info" className="space-y-4">
        <div>
          Extension <code>{ext.name}</code> is PostgreSQL Built-in{' '}
          <a href="/ext/list/contrib"><strong>Contrib</strong></a> Extension which is installed along with the kernel/contrib.
        </div>
      </div>
    );
    
    // Add Load section if needed
    if (ext.need_load) {
      sections.push(
        <div key="load" className="space-y-4">
          <div>
            <a href="/ext/usage/load"><strong>Load</strong></a> this extension by adding it to shared_preload_libraries:
          </div>
          
          <DynamicCodeBlock
            lang="ini"
            code={`# postgresql.conf\nshared_preload_libraries = '${ext.name}'  # add to existing extensions if any`}
          />
          
          <div>
            After modifying the configuration, restart PostgreSQL to load the extension.
          </div>
        </div>
      );
    }
    
    // Add Create section
    if (ext.need_ddl) {
      sections.push(
        <div key="create" className="space-y-4">
          <div>
            <a href="/ext/usage/create"><strong>Create</strong></a> this extension with:
          </div>
          
          <DynamicCodeBlock
            lang="sql"
            code={`CREATE EXTENSION ${ext.name}${ext.requires.length > 0 ? ' CASCADE' : ''};`}
          />
        </div>
      );
    }
    
    return <div className="space-y-6">{sections}</div>;
  }
  
  const sections = [];
  
  // Build tab items dynamically
  const tabItems = ['pig'];
  const hasRpm = ext.rpm_repo && ext.rpm_repo.trim() !== '';
  const hasDeb = ext.deb_repo && ext.deb_repo.trim() !== '';
  if (hasRpm) tabItems.push('yum');
  if (hasDeb) tabItems.push('apt');
  tabItems.push('ansible');
  
  // 1. Install section
  sections.push(
    <div key="install" className="space-y-4">
      <div>
        <a href="/ext/usage/install"><strong>Install</strong></a> this extension with:
      </div>
      
      <Tabs items={tabItems}>
        <Tab value="pig">
          <DynamicCodeBlock
            lang="bash"
            code={`pig ext install ${ext.name}; # install by extension name, for the current active PG version${ext.pkg !== ext.name ? `\npig ext install ${ext.pkg}; # install via package alias, for the active PG version` : ''}${DEFAULT_PG.filter(pg => ext.pg_ver.includes(String(pg))).map(pg => 
                `\npig ext install ${ext.name} -v ${pg};   # install for PG ${pg}`
              ).join('')}`}
          />
        </Tab>
        
        {hasRpm && (
          <Tab value="yum">
            <DynamicCodeBlock
              lang="bash"
              code={DEFAULT_PG.filter(pg => ext.pg_ver.includes(String(pg))).map(pg => {
                const pkgName = ext.rpm_pkg.includes('$v') 
                  ? ext.rpm_pkg.replace('$v', String(pg))
                  : ext.rpm_pkg;
                return `dnf install ${pkgName};`;
              }).join('\n')}
            />
          </Tab>
        )}
        
        {hasDeb && (
          <Tab value="apt">
            <DynamicCodeBlock
              lang="bash"
              code={DEFAULT_PG.filter(pg => ext.pg_ver.includes(String(pg))).map(pg => {
                const pkgName = ext.deb_pkg.includes('$v')
                  ? ext.deb_pkg.replace('$v', String(pg))
                  : `postgresql-${pg}-${ext.deb_pkg}`;
                return `apt install ${pkgName};`;
              }).join('\n')}
            />
          </Tab>
        )}
        
        <Tab value="ansible">
          <DynamicCodeBlock
            lang="bash"
            code={`./pgsql.yml -t pg_ext -e '{"pg_extensions": ["${ext.pkg}"]}' # -l <cls>`}
          />
        </Tab>
      </Tabs>
    </div>
  );
  
  // 2. Load section (if needed)
  if (ext.need_load) {
    sections.push(
      <div key="load" className="space-y-4">
        <div>
          <a href="/ext/usage/config"><strong>Load</strong></a> this extension with:
        </div>
        
        <DynamicCodeBlock
          lang="ini"
          code={`shared_preload_libraries = '${ext.name}'  # add to pg config`}
        />

      </div>
    );
  }
  
  // 3. Create section
  if (ext.need_ddl) {
    const createCmd = ext.name.includes('-') ? `"${ext.name}"` : ext.name;
    
    sections.push(
      <div key="create" className="space-y-4">
        <div>
          <a href="/ext/usage/create"><strong>Create</strong></a> this extension with:
        </div>
        
        <DynamicCodeBlock
          lang="sql"
          code={`CREATE EXTENSION ${createCmd}${ext.requires.length > 0 ? ' CASCADE' : ''};`}
        />
      </div>
    );
  } else {
    sections.push(
      <div key="no-ddl" className="space-y-4">
        <div>
          Extension <code>{ext.name}</code>{' '}
          <a href="/pgsql/ext/create#extension-without-ddl"><strong>does not need</strong></a>{' '}
          <code>CREATE EXTENSION</code> command.
        </div>
      </div>
    );
  }
  
  return <div className="space-y-6">{sections}</div>;
}

export default function ExtensionTemplate({ data }: { data: ExtensionData }) {
  const nameLink = data.url ? (
    <a href={data.url}><code>{data.name}</code></a>
  ) : (
    <code>{data.name}</code>
  );
  
  const leadingExtension = data.siblings.find(sibling => sibling !== data.name) || data.lead_ext;
  const packageLink = data.pkg !== data.name && leadingExtension && leadingExtension !== data.name ? (
    <a href={`/e/${leadingExtension}`}><code>{data.pkg}</code></a>
  ) : (
    <code>{data.pkg}</code>
  );
  
  return (
    <div className="space-y-8">
      {/* Overview Section */}
      <section>
        <h2>Overview</h2>
        <table className="w-full border-collapse border">
          <thead>
            <tr>
              <th className="text-center"><TooltipIconButton tooltip="Extension unique identifier" side="top">ID</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Extension name" side="top">Name</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Package name for installation" side="top">Package</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Latest available extension version" side="top">Version</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Extension category" side="top">Category</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Open source license" side="top">License</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Programming language" side="top">Lang</TooltipIconButton></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="text-center"><strong>{data.id}</strong></td>
              <td className="text-center">{nameLink}</td>
              <td className="text-center">{packageLink}</td>
              <td className="text-center">{data.version}</td>
              <td className="text-center">{formatCategoryTag(data.category)}</td>
              <td className="text-center">{formatLicenseTag(data.license)}</td>
              <td className="text-center">{formatLanguageTag(data.lang)}</td>
            </tr>
          </tbody>
        </table>
      </section>

      {/* Attributes Section */}
      <section>
        <h3>Attributes</h3>
        <table className="w-full border-collapse border">
          <thead>
            <tr>
              <th className="text-center"><TooltipIconButton tooltip="The Primary Leading extension in the Package" side="top">Leading</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Contains binary utils" side="top">Has Bin</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Contains .so shared library files" side="top">Has Lib</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Requires preloading via shared_preload_libraries" side="top">PreLoad</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Requires CREATE EXTENSION DDL command" side="top">Need DDL</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Can be installed in any schema" side="top">Relocatable</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Can be created by non-superuser" side="top">Trusted</TooltipIconButton></th>
              <th className="text-center"><TooltipIconButton tooltip="Schemas used by this extension" side="top">Schemas</TooltipIconButton></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="text-center">{formatBool(data.lead)}</td>
              <td className="text-center">{formatBool(data.has_bin)}</td>
              <td className="text-center">{formatBool(data.has_lib)}</td>
              <td className="text-center">{formatBool(data.need_load)}</td>
              <td className="text-center">{formatBool(data.need_ddl)}</td>
              <td className="text-center">{formatBool(data.relocatable)}</td>
              <td className="text-center">{formatBool(data.trusted)}</td>
              <td className="text-center">{data.schemas.length > 0 ? data.schemas.map(s => <code key={s}>{s}</code>).reduce((prev, curr) => [prev, ', ', curr] as any) : '-'}</td>
            </tr>
          </tbody>
        </table>
      </section>

      {/* Packages Section */}
      <section>
        <h3>Packages</h3>
        <PackageInfoSection ext={data} />
      </section>

      {/* Dependencies Section */}
      <DependenciesSection ext={data} />

      <hr />

      {/* Availability Section */}
      <section>
        <h2>Availability</h2>
        <AvailabilityMatrix ext={data} />
        
        <div className="mt-4 space-x-2">
          <Badge variant="green-subtle"><span className="font-black">CONTRIB</span></Badge>
          <Badge variant="blue-subtle"><span className="font-black">PGDG</span></Badge>
          <Badge variant="amber-subtle"><span className="font-black">PIGSTY</span></Badge>
        </div>
      </section>

      <hr />

      {/* Download Section */}
      <section>
        <h2>Download</h2>
        <DownloadSection ext={data} />
      </section>

      <hr />

      {/* Install Section */}
      <section>
        <h2>Install</h2>
        <InstallSection ext={data} />
      </section>
    </div>
  );
}