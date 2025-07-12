#!/usr/bin/env python3

import os
import psycopg2
import re
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass


# =============================================================================
# CONFIGURATION - Easy to modify for new OS/PG versions
# =============================================================================

@dataclass
class Config:
    """Configuration for the list generator."""
    
    # Database connection
    DB_CONNECTION: str = 'postgres:///vonng'
    
    # Supported operating systems
    OS_VERSIONS: List[str] = None
    
    # Supported PostgreSQL major versions
    PG_VERSIONS: List[int] = None
    
    # Output directory
    OUTPUT_DIR: str = None
    
    def __post_init__(self):
        if self.OS_VERSIONS is None:
            self.OS_VERSIONS = [
                'el8.x86_64', 'el8.aarch64', 
                'el9.x86_64', 'el9.aarch64',
                'd12.x86_64', 'd12.aarch64', 
                'u22.x86_64', 'u22.aarch64', 
                'u24.x86_64', 'u24.aarch64'
            ]
        
        if self.PG_VERSIONS is None:
            self.PG_VERSIONS = [17, 16, 15, 14, 13]
        
        if self.OUTPUT_DIR is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.OUTPUT_DIR = os.path.abspath(os.path.join(script_dir, '..', 'content', 'docs', 'list'))


# OS and Language mappings
OS_DESCRIPTIONS = {
    'el8': 'Enterprise Linux 8 (RHEL 8, CentOS 8, Rocky 8, Alma 8)',
    'el9': 'Enterprise Linux 9 (RHEL 9, CentOS 9, Rocky 9, Alma 9)',
    'd12': 'Debian 12 (Bookworm)',
    'u22': 'Ubuntu 22.04 LTS (Jammy)',
    'u24': 'Ubuntu 24.04 LTS (Noble)'
}

LANGUAGE_DESCRIPTIONS = {
    'C': 'The traditional PostgreSQL extension language',
    'C++': 'Extensions leveraging C++ features and libraries',
    'Rust': 'Extensions written in Rust with the pgrx framework',
    'Python': 'Extensions written in Python',
    'SQL': 'Pure SQL extensions and functions',
    'Java': 'Extensions running on JVM',
    'Data': 'Data-only extensions',
}

# Category metadata - loaded from category.csv
CATEGORY_META = {}

LICENSE_INFO = {
    'PostgreSQL': {'url': 'https://opensource.org/licenses/postgresql', 'description': 'Very liberal license based on the BSD license, allowing almost unlimited freedom.', 'anchor': 'postgresql', 'variant': 'blue-subtle'},
    'MIT': {'url': 'https://opensource.org/licenses/MIT', 'description': 'A permissive license that allows commercial use, modification, and private use.', 'anchor': 'mit', 'variant': 'blue-subtle'},
    'ISC': {'url': 'https://opensource.org/licenses/ISC', 'description': 'A permissive license similar to MIT, allowing commercial use and modification.', 'anchor': 'isc', 'variant': 'blue-subtle'},
    'BSD 0-Clause': {'url': 'https://opensource.org/license/0bsd', 'description': 'Public domain equivalent license with no restrictions on use.', 'anchor': 'bsd-0-clause', 'variant': 'blue-subtle'},
    'BSD 2-Clause': {'url': 'https://opensource.org/license/bsd-2-clause', 'description': 'Permissive license requiring attribution but allowing commercial use.', 'anchor': 'bsd-2-clause', 'variant': 'blue-subtle'},
    'BSD 3-Clause': {'url': 'https://opensource.org/license/bsd-3-clause', 'description': 'Permissive license with attribution and endorsement restriction clauses.', 'anchor': 'bsd-3-clause', 'variant': 'blue-subtle'},
    'Artistic': {'url': 'https://opensource.org/license/artistic-2-0', 'description': 'Copyleft license allowing modification with certain distribution requirements.', 'anchor': 'artistic', 'variant': 'green-subtle'},
    'Apache-2.0': {'url': 'https://opensource.org/licenses/Apache-2.0', 'description': 'Permissive license with patent protection and attribution requirements.', 'anchor': 'apache-20', 'variant': 'green-subtle'},
    'MPL-2.0': {'url': 'https://opensource.org/licenses/MPL-2.0', 'description': 'Weak copyleft license allowing proprietary combinations with file-level copyleft.', 'anchor': 'mpl-20', 'variant': 'green-subtle'},
    'GPL-2.0': {'url': 'https://opensource.org/licenses/GPL-2.0', 'description': 'Strong copyleft license requiring derivative works to be open source.', 'anchor': 'gpl-20', 'variant': 'amber-subtle'},
    'GPL-3.0': {'url': 'https://opensource.org/licenses/GPL-3.0', 'description': 'Strong copyleft license with additional patent and hardware restrictions.', 'anchor': 'gpl-30', 'variant': 'amber-subtle'},
    'LGPL-2.1': {'url': 'https://opensource.org/licenses/LGPL-2.1', 'description': 'Weak copyleft license allowing proprietary applications to link dynamically.', 'anchor': 'lgpl-21', 'variant': 'amber-subtle'},
    'LGPL-3.0': {'url': 'https://opensource.org/licenses/LGPL-3.0', 'description': 'Weak copyleft license with additional patent and hardware provisions.', 'anchor': 'lgpl-30', 'variant': 'amber-subtle'},
    'AGPL-3.0': {'url': 'https://opensource.org/licenses/AGPL-3.0', 'description': 'Network copyleft license extending GPL to cover network-distributed software.', 'anchor': 'agpl-30', 'variant': 'red-subtle'},
    'Timescale': {'url': 'https://www.timescale.com/legal/licenses', 'description': 'Proprietary license with restrictions on commercial use and distribution.', 'anchor': 'timescale', 'variant': 'gray-subtle'}
}

LICENSE_NORMALIZATION = {
    'BSD-0': 'BSD 0-Clause', 'BSD-2': 'BSD 2-Clause', 'BSD-3': 'BSD 3-Clause',
    'GPLv2': 'GPL-2.0', 'GPLv3': 'GPL-3.0', 'LGPLv2': 'LGPL-2.1', 
    'LGPLv3': 'LGPL-3.0', 'AGPLv3': 'AGPL-3.0', 'MPLv2': 'MPL-2.0'
}

LANGUAGE_CONFIG = {
    'Python': {"variant": 'blue-subtle', "anchor": "/list/lang#python"},
    'Rust': {"variant": 'amber-subtle', "anchor": "/list/lang#rust"},
    'SQL': {"variant": 'green-subtle', "anchor": "/list/lang#sql"},
    'Java': {"variant": 'pink-subtle', "anchor": "/list/lang#java"},
    'Data': {"variant": 'teal-subtle', "anchor": "/list/lang#data"},
    'C++': {"variant": 'purple-subtle', "anchor": "/list/lang#c-1"},
    'C': {"variant": 'blue-subtle', "anchor": "/list/lang#c"},
}

REPO_CONFIG = {
    'PIGSTY': {'variant': 'amber-subtle'},
    'PGDG': {'variant': 'blue-subtle'},
    'CONTRIB': {'variant': 'purple-subtle'},
    'OTHER': {'variant': 'gray-subtle'}
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def parse_array(value: str) -> List[str]:
    """Parse PostgreSQL array string to Python list."""
    if isinstance(value, list):
        return value
    if not value or not value.startswith('{') or not value.endswith('}'):
        return []
    return [item.strip() for item in value[1:-1].split(',') if item.strip()]


def normalize_os_arch(arch_in: str) -> str:
    """Normalize architecture names."""
    arch_map = {
        'amd': 'x86_64', 'x86_64': 'x86_64', 'amd64': 'x86_64',
        'arm': 'aarch64', 'arm64': 'aarch64', 'aarch64': 'aarch64', 'armv8': 'aarch64'
    }
    return arch_map.get(arch_in.lower(), arch_in.lower())


def normalize_license_name(license_name: str) -> str:
    """Normalize license names to standard format."""
    return LICENSE_NORMALIZATION.get(license_name, license_name)


def format_language_badge(language: str) -> str:
    """Format programming language as Badge component with appropriate color."""
    info = LANGUAGE_CONFIG.get(language, {"variant": 'gray-subtle', "anchor": "#"})
    return f'<a href="{info["anchor"]}"><Badge icon={{<FileCode2 />}} variant="{info["variant"]}">{language or "N/A"}</Badge></a>'


def extract_semantic_version(version: str) -> str:
    """Extract semantic version from package version string."""
    semantic_version = re.split(r'[-_]\d*[A-Z]', version)[0]
    semantic_version = re.split(r'[-_]\d*\w*\.', semantic_version)[0]
    semantic_version = re.split(r'[-+]', semantic_version)[0]
    return semantic_version


# =============================================================================
# BADGE FORMATTING FUNCTIONS
# =============================================================================

class BadgeFormatter:
    """Centralized badge formatting functionality."""
    
    @staticmethod
    def format_category(category: str) -> str:
        """Format category as Badge component with icon and color."""
        meta = CATEGORY_META.get(category, {'icon': 'Blocks', 'color': 'gray-subtle'})
        iconstr = '{<%s />}' % meta['icon']
        return f'<Badge icon={iconstr} variant="{meta["color"]}"><a href="/cate/{category.lower()}" className="no-underline">{category}</a></Badge>'
    
    @staticmethod
    def format_license(license_name: str) -> str:
        """Format license as Badge component with standard colors and links."""
        license_info = LICENSE_INFO.get(license_name, {
            'anchor': license_name.lower().replace(' ', '-').replace('.', ''), 
            'variant': 'gray-subtle'
        })
        return f'<a href="/list/license#{license_info["anchor"]}" className="no-underline"><Badge icon={{<Scale />}} variant="{license_info["variant"]}">{license_name}</Badge></a>'
    
    @staticmethod
    def format_language(language: str) -> str:
        """Format programming language as Badge component with appropriate color."""
        info = LANGUAGE_CONFIG.get(language, {"variant": 'gray-subtle', "anchor": "#"})
        return f'<a href="{info["anchor"]}"><Badge icon={{<FileCode2 />}} variant="{info["variant"]}">{language or "N/A"}</Badge></a>'
    
    @staticmethod
    def format_repo(repo: str) -> str:
        """Format repository as Badge component with appropriate color."""
        info = REPO_CONFIG.get(repo, {'variant': 'gray-subtle'})
        return f'<Badge variant="{info["variant"]}">{repo}</Badge>'


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Package:
    """Represents a PostgreSQL extension package."""
    pg: int
    os: str
    pname: str
    org: str
    type: str
    os_code: str
    os_arch: str
    repo: str
    name: str
    ver: str
    version: str
    release: str
    file: str
    sha256: str
    url: str
    mirror_url: str
    size: int
    size_full: int
    
    @classmethod
    def from_row(cls, row: Tuple) -> 'Package':
        """Create Package from database row."""
        return cls(*row)


@dataclass
class Extension:
    """Represents a PostgreSQL extension with all its metadata."""
    id: int
    name: str
    pkg: str
    lead_ext: Optional[str]
    category: str
    state: str
    url: Optional[str]
    license: Optional[str]
    tags: List[str]
    version: Optional[str]
    repo: str
    lang: Optional[str]
    contrib: bool
    lead: bool
    has_bin: bool
    has_lib: bool
    need_ddl: bool
    need_load: bool
    trusted: bool
    relocatable: bool
    schemas: List[str]
    pg_ver: List[str]
    requires: List[str]
    require_by: List[str]
    see_also: List[str]
    rpm_ver: Optional[str]
    rpm_repo: Optional[str]
    rpm_pkg: Optional[str]
    rpm_pg: List[str]
    rpm_deps: List[str]
    deb_ver: Optional[str]
    deb_repo: Optional[str]
    deb_pkg: Optional[str]
    deb_deps: List[str]
    deb_pg: List[str]
    source: Optional[str]
    extra: Optional[str]
    en_desc: Optional[str]
    zh_desc: Optional[str]
    comment: Optional[str]
    mtime: str
    packages: List[Package] = None
    
    @classmethod
    def from_row(cls, row: Tuple) -> 'Extension':
        """Create Extension from database row."""
        (id, name, pkg, lead_ext, category, state, url, license, tags, version, repo, lang, 
         contrib, lead, has_bin, has_lib, need_ddl, need_load, trusted, relocatable, schemas, 
         pg_ver, requires, require_by, see_also, rpm_ver, rpm_repo, rpm_pkg, rpm_pg, rpm_deps, 
         deb_ver, deb_repo, deb_pkg, deb_deps, deb_pg, source, extra, en_desc, zh_desc, comment, mtime) = row
        
        # Parse array fields
        tags = parse_array(tags) if tags else []
        pg_ver = parse_array(pg_ver) if pg_ver else []
        requires = parse_array(requires) if requires else []
        require_by = parse_array(require_by) if require_by else []
        see_also = parse_array(see_also) if see_also else []
        schemas = parse_array(schemas) if schemas else []
        rpm_deps = parse_array(rpm_deps) if rpm_deps else []
        deb_deps = parse_array(deb_deps) if deb_deps else []
        rpm_pg = parse_array(rpm_pg) if rpm_pg else []
        deb_pg = parse_array(deb_pg) if deb_pg else []
        
        return cls(
            id=id, name=name, pkg=pkg, lead_ext=lead_ext, category=category, state=state, url=url,
            license=license, tags=tags, version=version, repo=repo, lang=lang, contrib=contrib,
            lead=lead, has_bin=has_bin, has_lib=has_lib, need_ddl=need_ddl, need_load=need_load,
            trusted=trusted, relocatable=relocatable, schemas=schemas, pg_ver=pg_ver,
            requires=requires, require_by=require_by, see_also=see_also, rpm_ver=rpm_ver, 
            rpm_repo=rpm_repo, rpm_pkg=rpm_pkg, rpm_pg=rpm_pg, rpm_deps=rpm_deps, deb_ver=deb_ver, 
            deb_repo=deb_repo, deb_pkg=deb_pkg, deb_deps=deb_deps, deb_pg=deb_pg, source=source,
            extra=extra, en_desc=en_desc, zh_desc=zh_desc, comment=comment, mtime=mtime, packages=[]
        )
    
    @property
    def has_rpm(self) -> bool:
        return bool(self.rpm_repo)
    
    @property
    def has_deb(self) -> bool:
        return bool(self.deb_repo)
    
    def load_packages(self, all_packages: List[Package]):
        """Load package data for this extension from the provided list."""
        if self.packages is None:
            self.packages = []
        
        # Find packages that match this extension's package name
        for pkg in all_packages:
            # Handle different package naming patterns:
            # RPM: pkg_name, pkg_name_XX (where XX is PG version)
            # DEB: postgresql-XX-pkg-name (where XX is PG version)
            if (pkg.pname == self.pkg or 
                pkg.pname.startswith(f'{self.pkg}_') or
                f'-{self.pkg.replace("_", "-")}' in pkg.pname):
                self.packages.append(pkg)


# =============================================================================
# TABLE GENERATOR CLASSES
# =============================================================================

class TableGenerator:
    """Centralized table generation functionality."""
    
    def __init__(self, leading_map: Dict[str, str]):
        self.leading_map = leading_map
    
    def generate_simple_table(self, extensions: List[Extension]) -> str:
        """Generate simple extension table (ID, Name, Package, Description)."""
        if not extensions:
            return "No extensions found."
        
        headers = ['ID', 'Extension', 'Package', 'Description']
        rows = [self._format_table_header(headers, [':---:',':---',':---',':---'])]
        
        for ext in extensions:
            package_cell = f'[`{ext.pkg}`](/e/{self.leading_map.get(ext.pkg, ext.name)})'
            row_data = [
                str(ext.id),
                f'[`{ext.name}`](/e/{ext.name})',
                package_cell,
                ext.en_desc or 'No description'
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        return '\n'.join(rows)
    
    def generate_category_table(self, extensions: List[Extension]) -> str:
        """Generate extension table for category lists (ID, Name, Package, Version, Description)."""
        if not extensions:
            return "No extensions found."
        
        headers = ['ID', 'Extension', 'Package', 'Version', 'Description']
        rows = [self._format_table_header(headers, [':---:',':---',':---',':---',':---'])]
        
        for ext in extensions:
            package_cell = f'[`{ext.pkg}`](/e/{self.leading_map.get(ext.pkg, ext.name)})'
            row_data = [
                str(ext.id),
                f'[`{ext.name}`](/e/{ext.name})',
                package_cell,
                ext.version or 'N/A',
                ext.en_desc or 'No description'
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        return '\n'.join(rows)
    
    def generate_category_table_zh(self, extensions: List[Extension]) -> str:
        """Generate Chinese extension table for category lists."""
        if not extensions:
            return "未找到扩展。"
        
        headers = ['ID', '扩展', '包', '版本', '描述']
        rows = [self._format_table_header(headers, [':---:',':---',':---',':---',':---'])]
        
        for ext in extensions:
            package_cell = f'[`{ext.pkg}`](/zh/e/{self.leading_map.get(ext.pkg, ext.name)})'
            row_data = [
                str(ext.id),
                f'[`{ext.name}`](/zh/e/{ext.name})',
                package_cell,
                ext.version or 'N/A',
                ext.zh_desc or ext.en_desc or '暂无描述'
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        return '\n'.join(rows)
    
    def generate_repo_table(self, extensions: List[Extension]) -> str:
        """Generate extension table for repo lists (ID, Name, Category, RPM, DEB, Description)."""
        if not extensions:
            return "No extensions found."
        
        headers = ['ID', 'Name', 'Category', 'RPM', 'DEB', 'Description']
        rows = [self._format_table_header(headers, [':---:',':---',':---',':---:',':---:',':---'])]
        
        for ext in extensions:
            rpm_badge = BadgeFormatter.format_repo(ext.rpm_repo) if ext.rpm_repo else '-'
            deb_badge = BadgeFormatter.format_repo(ext.deb_repo) if ext.deb_repo else '-'
            category_badge = BadgeFormatter.format_category(ext.category) if ext.category else '-'
            
            row_data = [
                str(ext.id),
                f'[`{ext.name}`](/e/{ext.name})',
                category_badge,
                rpm_badge,
                deb_badge,
                ext.en_desc or 'No description'
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        return '\n'.join(rows)
    
    def _format_table_header(self, headers: List[str], alignments: List[str]) -> str:
        """Format table header with alignment."""
        header_row = '| ' + ' | '.join(headers) + ' |'
        separator_row = '|' + '|'.join(alignments) + '|'
        return header_row + '\n' + separator_row
    
    def generate_extension_cards(self, extensions: List[Extension], config, is_chinese=False) -> str:
        """Generate Callout-style layout for extensions with detailed metadata."""
        if not extensions:
            return "<p className='text-muted-foreground'>No extensions available in this category.</p>"

        def generate_metadata_table(ext: Extension) -> str:
            """Generate left-side metadata table."""
            # Format RPM and DEB package names
            rpm_pkg = f'`{ext.rpm_pkg or "N/A"}`' if ext.has_rpm else '<span className="text-red-500">N/A</span>'
            deb_pkg = f'`{ext.deb_pkg or "N/A"}`' if ext.has_deb else '<span className="text-red-500">N/A</span>'
            
            # Generate individual attribute badges for each row
            load_badge = '<Badge variant="red-subtle">LOAD</Badge>' if ext.need_load else ''
            ddl_badge = '<Badge variant="blue-subtle">DDL</Badge>' if ext.need_ddl else ''
            lib_badge = '<Badge variant="green-subtle">LIB</Badge>' if ext.has_lib else ''
            bin_badge = '<Badge variant="pink-subtle">BIN</Badge>' if ext.has_bin else ''
            trust_badge = '<Badge variant="green-subtle">TRUST</Badge>' if ext.trusted else ''
            
            # Website link with localized labels
            path_prefix = '/zh' if is_chinese else ''
            ext_label = "扩展" if is_chinese else "Extension"
            website_label = "网站" if is_chinese else "Website"
            attrs_label = "属性" if is_chinese else "Attributes"
            package_label = "扩展包" if is_chinese else "Package"
            lang_label = "开发语言" if is_chinese else "Language"
            lic_label = "许可证" if is_chinese else "License"
            
            extension_cell = f'[{ext_label}]({path_prefix}/e/{ext.name})'
            website_cell = f'[{website_label}]({ext.url})' if ext.url else 'N/A'
            package_cell = f'[`{ext.pkg}`]({path_prefix}/e/{self.leading_map.get(ext.pkg, ext.name)})'

            return f'''| {extension_cell} | {website_cell} | {attrs_label} |
|:----:|:---------:|:---------:|
| {package_label}  | {package_cell} | {load_badge} |
| RPM  | {rpm_pkg} | {ddl_badge} |
| DEB  | {deb_pkg} | {lib_badge} |
| {lang_label} | {format_language_badge(ext.lang or "N/A")} | {bin_badge} |
| {lic_label} | {BadgeFormatter.format_license(ext.license or "N/A")} | {trust_badge} |'''

        def generate_availability_matrix(ext: Extension) -> str:

            """Generate right-side availability matrix with PG version badges."""
            # Packages are already loaded in _setup
            
            # Build package matrix
            pkg_matrix = {}
            repo_matrix = {}
            
            # Initialize matrix for each OS
            for os in config.OS_VERSIONS:
                pkg_matrix[os] = {}
                repo_matrix[os] = {}
                for pg in config.PG_VERSIONS:
                    pkg_matrix[os][pg] = ""
                    repo_matrix[os][pg] = ""
            
            # Fill matrix with actual package data
            for pkg in ext.packages:
                pkg_os_key = f"{pkg.os_code}.{normalize_os_arch(pkg.os_arch)}"
                
                if pkg_os_key in pkg_matrix and pkg.pg in pkg_matrix[pkg_os_key]:
                    pkg_matrix[pkg_os_key][pkg.pg] = pkg.version
                    repo_matrix[pkg_os_key][pkg.pg] = pkg.org.upper()
            
            # Generate matrix table
            rows = []
            # Group by OS, then by architecture
            for os_base in ['el8', 'el9', 'd12', 'u22', 'u24']:
                x86_key = f"{os_base}.x86_64"
                arm_key = f"{os_base}.aarch64"
                
                x86_badges = []
                arm_badges = []
                
                for pg in config.PG_VERSIONS:
                    # x86_64 badges
                    if x86_key in pkg_matrix and pg in pkg_matrix[x86_key] and pkg_matrix[x86_key][pg]:
                        repo = repo_matrix[x86_key][pg]
                        if repo == 'PIGSTY':
                            x86_badges.append(f'<Badge variant="amber-subtle">{pg}</Badge>')
                        elif repo == 'PGDG':
                            x86_badges.append(f'<Badge variant="blue-subtle">{pg}</Badge>')
                        elif repo == 'CONTRIB':
                            x86_badges.append(f'<Badge variant="green-subtle">{pg}</Badge>')
                        else:
                            x86_badges.append(f'<Badge variant="gray-subtle">{pg}</Badge>')
                    elif ext.contrib and str(pg) in ext.pg_ver:
                        x86_badges.append(f'<Badge variant="green-subtle">{pg}</Badge>')
                    else:
                        x86_badges.append(f'<Badge variant="red-subtle">{pg}</Badge>')
                    
                    # aarch64 badges
                    if arm_key in pkg_matrix and pg in pkg_matrix[arm_key] and pkg_matrix[arm_key][pg]:
                        repo = repo_matrix[arm_key][pg]
                        if repo == 'PIGSTY':
                            arm_badges.append(f'<Badge variant="amber-subtle">{pg}</Badge>')
                        elif repo == 'PGDG':
                            arm_badges.append(f'<Badge variant="blue-subtle">{pg}</Badge>')
                        elif repo == 'CONTRIB':
                            arm_badges.append(f'<Badge variant="green-subtle">{pg}</Badge>')
                        else:
                            arm_badges.append(f'<Badge variant="gray-subtle">{pg}</Badge>')
                    elif ext.contrib and str(pg) in ext.pg_ver:
                        arm_badges.append(f'<Badge variant="green-subtle">{pg}</Badge>')
                    else:
                        arm_badges.append(f'<Badge variant="red-subtle">{pg}</Badge>')
                
                rows.append(f"| {os_base} | {''.join(x86_badges)} | {''.join(arm_badges)} |")

            header_txt = '系统'  if is_chinese else 'OS/Arch'
            header = f"| {header_txt} | x86_64 | aarch64 |\n|:-----:|:---:|:---:|"
            return f"{header}\n" + "\n".join(rows)

        callouts = []
        for ext in extensions:
            title = f"{ext.name} - {ext.version or 'Unknown'}"
            description = (ext.zh_desc if is_chinese else ext.en_desc) or ext.en_desc or 'No description available'
            
            callout = f'''
<Callout title="{title}">
    <p>{description}</p>
    <div className="grid grid-cols-2 gap-4"><div className="space-y-2">
            {generate_metadata_table(ext)}
        </div>
        <div className="space-y-2">
            {generate_availability_matrix(ext)}
        </div>
    </div>
</Callout>
'''
            callouts.append(callout)

        return "\n".join(callouts)


# =============================================================================
# DATABASE OPERATIONS
# =============================================================================

class DatabaseManager:
    """Handles all database operations."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._conn = None
    
    def get_connection(self):
        if self._conn is None:
            self._conn = psycopg2.connect(self.connection_string)
        return self._conn
    
    def load_category_metadata(self) -> Dict[str, Dict[str, str]]:
        """Load category metadata from CSV file."""
        print("Loading category metadata from CSV...")
        
        import csv
        category_data = {}
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'category.csv')
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                category_data[row['name']] = {
                    'zh_desc': row['zh_desc'],
                    'en_desc': row['en_desc'],
                    'icon': row['icon2'],
                    'color': 'blue-subtle'  # Default color, can be customized
                }
        
        print(f"Loaded {len(category_data)} categories.")
        return category_data
    
    def load_extensions(self) -> List[Extension]:
        """Load all extensions from database."""
        print("Loading extensions from database...")
        
        with self.get_connection().cursor() as cur:
            cur.execute('SELECT * FROM pgext.extension ORDER BY id')
            rows = cur.fetchall()
        
        extensions = [Extension.from_row(row) for row in rows]
        print(f"Found {len(extensions)} extensions.")
        return extensions
    
    def load_packages(self) -> List[Package]:
        """Load all packages from database."""
        print("Loading packages from database...")
        
        with self.get_connection().cursor() as cur:
            cur.execute('SELECT pg, os, pname, org, type, os_code, os_arch, repo, name, ver, version, release, file, sha256, url, mirror_url, size, size_full FROM pgext.package ORDER BY os, pg DESC')
            rows = cur.fetchall()
        
        packages = [Package.from_row(row) for row in rows]
        print(f"Found {len(packages)} packages.")
        return packages


# =============================================================================
# CONTENT GENERATORS
# =============================================================================

class ContentGenerator:
    """Base class for content generators."""
    
    def __init__(self, config: Config, extensions: List[Extension], table_gen: TableGenerator):
        self.config = config
        self.extensions = extensions
        self.table_gen = table_gen
    
    def write_content(self, filename: str, content: str):
        """Write content to file."""
        output_path = os.path.join(self.config.OUTPUT_DIR, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated: {output_path}")


class CategoryListGenerator(ContentGenerator):
    """Generate category-based extension list."""
    
    def generate(self):
        print("Generating category list...")
        
        # Group extensions by category
        category_groups = defaultdict(list)
        for ext in self.extensions:
            category_groups[ext.category].append(ext)
        
        # Generate category overview table
        category_table_rows = []
        for category in CATEGORY_META.keys():
            count = len(category_groups[category])
            meta = CATEGORY_META[category]
            category_table_rows.append(f'| {BadgeFormatter.format_category(category)} | {count} | {meta["en_desc"]} |')
        
        category_overview_table = f'''| Category | Count | Description |
|:---------|:-----:|:------------|
{chr(10).join(category_table_rows)}'''
        
        # Generate category sections
        category_sections = []
        for category in CATEGORY_META.keys():
            if category not in category_groups:
                continue
            
            cat_extensions = sorted(category_groups[category], key=lambda e: e.name)
            count = len(cat_extensions)
            meta = CATEGORY_META[category]
            
            section = f'''
## {category}

{meta["en_desc"]}

{BadgeFormatter.format_category(category)} <Badge variant="gray-subtle">{count} Extensions</Badge>

{self.table_gen.generate_category_table(cat_extensions)}
'''
            category_sections.append(section)
        
        content = f'''---
title: By Category
description: PostgreSQL extensions organized by functionality categories
icon: Shapes
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck }} from 'lucide-react';

<Badge icon={{<Clock />}}               variant="blue-subtle"><a   href="#time" className="no-underline">TIME</a></Badge>
<Badge icon={{<Globe />}}               variant="green-subtle"><a  href="#gis" className="no-underline">GIS</a></Badge>
<Badge icon={{<Brain />}}               variant="purple-subtle"><a href="#rag" className="no-underline">RAG</a></Badge>
<Badge icon={{<Search />}}              variant="amber-subtle"><a  href="#fts" className="no-underline">FTS</a></Badge>
<Badge icon={{<ChartNoAxesCombined />}} variant="red-subtle"><a    href="#olap" className="no-underline">OLAP</a></Badge>
<Badge icon={{<Sparkles />}}            variant="pink-subtle"><a   href="#feat" className="no-underline">FEAT</a></Badge>
<Badge icon={{<BookA />}}               variant="teal-subtle"><a   href="#lang" className="no-underline">LANG</a></Badge>
<Badge icon={{<Boxes />}}               variant="gray-subtle"><a   href="#type" className="no-underline">TYPE</a></Badge><br />
<Badge icon={{<Wrench />}}              variant="amber-subtle"><a  href="#util" className="no-underline">UTIL</a></Badge>
<Badge icon={{<Variable />}}            variant="pink-subtle"><a   href="#func" className="no-underline">FUNC</a></Badge>
<Badge icon={{<Landmark />}}            variant="gray-subtle"><a   href="#admin" className="no-underline">ADMIN</a></Badge>
<Badge icon={{<Activity />}}            variant="green-subtle"><a  href="#stat" className="no-underline">STAT</a></Badge>
<Badge icon={{<Shield />}}              variant="red-subtle"><a    href="#sec" className="no-underline">SEC</a></Badge>
<Badge icon={{<FileInput />}}           variant="blue-subtle"><a   href="#fdw" className="no-underline">FDW</a></Badge>
<Badge icon={{<Shell />}}               variant="teal-subtle"><a   href="#sim" className="no-underline">SIM</a></Badge>
<Badge icon={{<Truck />}}               variant="purple-subtle"><a href="#etl" className="no-underline">ETL</a></Badge>

## Summary

{category_overview_table}

{''.join(category_sections)}
'''
        
        self.write_content('cate.mdx', content)
        self._generate_chinese_version(category_groups, category_overview_table, category_sections)
    
    def _generate_chinese_version(self, category_groups, category_overview_table, category_sections):
        """Generate Chinese version of category list."""
        print("Generating Chinese category list...")
        
        # Generate Chinese category overview table
        zh_category_table_rows = []
        for category in CATEGORY_META.keys():
            count = len(category_groups[category])
            meta = CATEGORY_META[category]
            zh_category_table_rows.append(f'| {BadgeFormatter.format_category(category)} | {count} | {meta["zh_desc"]} |')
        
        zh_category_overview_table = f'''| 分类 | 数量 | 描述 |
|:---------|:-----:|:------------|
{chr(10).join(zh_category_table_rows)}'''
        
        # Generate Chinese category sections
        zh_category_sections = []
        for category in CATEGORY_META.keys():
            if category not in category_groups:
                continue
            
            cat_extensions = sorted(category_groups[category], key=lambda e: e.name)
            count = len(cat_extensions)
            meta = CATEGORY_META[category]
            
            section = f'''
## {category}

{meta["zh_desc"]}

{BadgeFormatter.format_category(category)} <Badge variant="gray-subtle">{count} 个扩展</Badge>

{self.table_gen.generate_category_table_zh(cat_extensions)}
'''
            zh_category_sections.append(section)
        
        zh_content = f'''---
title: 按分类
description: 按功能分类组织的 PostgreSQL 扩展
icon: Shapes
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck }} from 'lucide-react';

<Badge icon={{<Clock />}}               variant="blue-subtle"><a   href="#time" className="no-underline">TIME</a></Badge>
<Badge icon={{<Globe />}}               variant="green-subtle"><a  href="#gis" className="no-underline">GIS</a></Badge>
<Badge icon={{<Brain />}}               variant="purple-subtle"><a href="#rag" className="no-underline">RAG</a></Badge>
<Badge icon={{<Search />}}              variant="amber-subtle"><a  href="#fts" className="no-underline">FTS</a></Badge>
<Badge icon={{<ChartNoAxesCombined />}} variant="red-subtle"><a    href="#olap" className="no-underline">OLAP</a></Badge>
<Badge icon={{<Sparkles />}}            variant="pink-subtle"><a   href="#feat" className="no-underline">FEAT</a></Badge>
<Badge icon={{<BookA />}}               variant="teal-subtle"><a   href="#lang" className="no-underline">LANG</a></Badge>
<Badge icon={{<Boxes />}}               variant="gray-subtle"><a   href="#type" className="no-underline">TYPE</a></Badge><br />
<Badge icon={{<Wrench />}}              variant="amber-subtle"><a  href="#util" className="no-underline">UTIL</a></Badge>
<Badge icon={{<Variable />}}            variant="pink-subtle"><a   href="#func" className="no-underline">FUNC</a></Badge>
<Badge icon={{<Landmark />}}            variant="gray-subtle"><a   href="#admin" className="no-underline">ADMIN</a></Badge>
<Badge icon={{<Activity />}}            variant="green-subtle"><a  href="#stat" className="no-underline">STAT</a></Badge>
<Badge icon={{<Shield />}}              variant="red-subtle"><a    href="#sec" className="no-underline">SEC</a></Badge>
<Badge icon={{<FileInput />}}           variant="blue-subtle"><a   href="#fdw" className="no-underline">FDW</a></Badge>
<Badge icon={{<Shell />}}               variant="teal-subtle"><a   href="#sim" className="no-underline">SIM</a></Badge>
<Badge icon={{<Truck />}}               variant="purple-subtle"><a href="#etl" className="no-underline">ETL</a></Badge>

## 概览

{zh_category_overview_table}

{''.join(zh_category_sections)}
'''
        
        self.write_content('cate.zh.mdx', zh_content)


class LinuxDistroGenerator(ContentGenerator):
    """Generate Linux distro-based extension list."""
    
    def __init__(self, config: Config, extensions: List[Extension], table_gen: TableGenerator, packages: List[Package]):
        super().__init__(config, extensions, table_gen)
        self.packages = packages
    
    def generate(self):
        print("Generating Linux distro list...")
        
        # Group packages by OS
        os_groups = defaultdict(set)
        for pkg in self.packages:
            os_key = f"{pkg.os_code}.{pkg.os_arch}"
            os_groups[os_key].add(pkg.pname)
        
        # Generate OS sections
        os_sections = []
        for os_base in ['el8', 'el9', 'd12', 'u22', 'u24']:
            x86_packages = os_groups.get(f'{os_base}.x86_64', set())
            arm_packages = os_groups.get(f'{os_base}.aarch64', set())
            
            # Get extensions available on this OS  
            all_os_packages = x86_packages | arm_packages
            available_extensions = [ext for ext in self.extensions if ext.pkg in all_os_packages]
            available_extensions.sort(key=lambda e: e.name)
            
            section = f'''
## {os_base.upper()}

{OS_DESCRIPTIONS[os_base]}

<Badge variant="blue-subtle">x86_64</Badge> <Badge variant="gray-subtle">{len(x86_packages)} Packages</Badge>

<Badge variant="orange-subtle">aarch64</Badge> <Badge variant="gray-subtle">{len(arm_packages)} Packages</Badge>

<Badge variant="green-subtle">Total</Badge> <Badge variant="gray-subtle">{len(available_extensions)} Extensions</Badge>

'''
            os_sections.append(section)

        content = f'''---
title: By Linux
description: PostgreSQL extensions availability by Linux distros
icon: Server
full: true
---

import {{ Badge }} from '@/components/ui/badge';

{''.join(os_sections)}
'''
        
        self.write_content('linux.mdx', content)


class PGMajorGenerator(ContentGenerator):
    """Generate PG major version extension list."""
    
    def generate(self):
        print("Generating PG major list...")
        
        pg_sections = []
        for pg in self.config.PG_VERSIONS:
            # Find extensions NOT available for this PG version
            unavailable_extensions = [ext for ext in self.extensions if str(pg) not in ext.pg_ver]
            unavailable_extensions.sort(key=lambda e: e.name)
            
            section = f'''
## PostgreSQL {pg}

Extensions **NOT available** for PostgreSQL {pg}

{self.table_gen.generate_simple_table(unavailable_extensions)}
'''
            pg_sections.append(section)
        
        content = f'''---
title: By PostgreSQL
description: PostgreSQL extensions unavailable by major version
icon: Database
full: true
---

import {{ Badge }} from '@/components/ui/badge';

{''.join(pg_sections)}
'''
        
        self.write_content('pg.mdx', content)


class LicenseListGenerator(ContentGenerator):
    """Generate license-based extension list."""
    
    def generate(self):
        print("Generating license list...")
        
        # Count extensions by license and normalize names
        license_counts = Counter()
        license_extensions_map = defaultdict(list)
        
        for ext in self.extensions:
            if not ext.license:
                continue
            normalized_name = normalize_license_name(ext.license)
            license_counts[normalized_name] += 1
            license_extensions_map[normalized_name].append(ext)
        
        # Generate summary table
        summary_rows = []
        for license_name, count in license_counts.most_common():
            info = LICENSE_INFO.get(license_name, {'url': '#', 'description': 'Open source license.'})
            summary_rows.append(f'| {BadgeFormatter.format_license(license_name)} | {count} | [License Text]({info["url"]}) | {info["description"]} |')
        
        summary_table = f'''| License | Count | Reference |  Description |
|:--------|:-----:|:-------:|:----------|
{chr(10).join(summary_rows)}'''
        
        # Generate license sections
        license_sections = []
        for license_name, count in license_counts.most_common():
            license_extensions = sorted(license_extensions_map[license_name], key=lambda e: e.name)
            info = LICENSE_INFO.get(license_name, {'url': '#', 'description': 'Open source license.'})
            
            section = f'''
## {license_name}

{BadgeFormatter.format_license(license_name)} <Badge icon={{<Package />}} variant="gray-subtle">{count} Extensions</Badge>

[{license_name} License Text]({info["url"]}) : {info["description"]}

{self.table_gen.generate_simple_table(license_extensions)}
'''
            license_sections.append(section)
        
        content = f'''---
title: By License
description: PostgreSQL extensions organized by open source license
icon: Scale
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Scale, Package }} from 'lucide-react';

<a href="#mit"          className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >MIT</Badge></a>
<a href="#isc"          className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >ISC</Badge></a>
<a href="#postgresql"   className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >PostgreSQL</Badge></a>
<a href="#bsd-0-clause" className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >BSD 0-Clause</Badge></a>
<a href="#bsd-2-clause" className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >BSD 2-Clause</Badge></a>
<a href="#bsd-3-clause" className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >BSD 3-Clause</Badge></a>
<a href="#artistic"     className="no-underline"><Badge icon={{<Scale />}} variant="green-subtle" >Artistic</Badge></a>
<a href="#apache-20"    className="no-underline"><Badge icon={{<Scale />}} variant="green-subtle" >Apache-2.0</Badge></a>
<a href="#mpl-20"       className="no-underline"><Badge icon={{<Scale />}} variant="green-subtle" >MPL-2.0</Badge></a><br />
<a href="#gpl-20"       className="no-underline"><Badge icon={{<Scale />}} variant="amber-subtle" >GPL-2.0</Badge></a>
<a href="#gpl-30"       className="no-underline"><Badge icon={{<Scale />}} variant="amber-subtle" >GPL-3.0</Badge></a>
<a href="#lgpl-21"      className="no-underline"><Badge icon={{<Scale />}} variant="amber-subtle" >LGPL-2.1</Badge></a>
<a href="#lgpl-30"      className="no-underline"><Badge icon={{<Scale />}} variant="amber-subtle" >LGPL-3.0</Badge></a>
<a href="#agpl-30"      className="no-underline"><Badge icon={{<Scale />}} variant="red-subtle"   >AGPL-3.0</Badge></a>
<a href="#timescale"    className="no-underline"><Badge icon={{<Scale />}} variant="gray-subtle"  >Timescale</Badge></a>

## Summary

{summary_table}

---------

{''.join(license_sections)}
'''
        
        self.write_content('license.mdx', content)


class LanguageListGenerator(ContentGenerator):
    """Generate language-based extension list."""
    
    def generate(self):
        print("Generating language list...")
        
        # Count extensions by language
        language_counts = Counter(ext.lang for ext in self.extensions if ext.lang)
        
        # Generate summary table
        summary_rows = []
        for lang, count in language_counts.most_common():
            desc = LANGUAGE_DESCRIPTIONS.get(lang, f'Extensions written in {lang}')
            summary_rows.append(f'| {BadgeFormatter.format_language(lang)} | {count} | {desc} |')
        
        summary_table = f'''| Language | Count | Description |
|:-------:|:-----:|:------------|
{chr(10).join(summary_rows)}'''
        
        # Generate language sections
        language_sections = []
        for lang, count in language_counts.most_common():
            lang_extensions = [ext for ext in self.extensions if ext.lang == lang]
            lang_extensions.sort(key=lambda e: e.name)
            
            desc = LANGUAGE_DESCRIPTIONS.get(lang, f'Extensions written in {lang}')
            
            section = f'''
## {lang}

{BadgeFormatter.format_language(lang)} <Badge icon={{<Package />}} variant="gray-subtle">{count} Extensions</Badge>

{desc}

{self.table_gen.generate_simple_table(lang_extensions)}
'''
            language_sections.append(section)
        
        content = f'''---
title: By Language
description: PostgreSQL extensions organized by implementation language
icon: FileCode2
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ FileCode2, Package }} from 'lucide-react';

<a href="/list/lang#c"><Badge      icon={{<FileCode2 />}} variant="blue-subtle">C</Badge></a>
<a href="/list/lang#c-1"><Badge    icon={{<FileCode2 />}} variant="purple-subtle">C++</Badge></a>
<a href="/list/lang#rust"><Badge   icon={{<FileCode2 />}} variant="amber-subtle">Rust</Badge></a>
<a href="/list/lang#java"><Badge   icon={{<FileCode2 />}} variant="pink-subtle">Java</Badge></a>
<a href="/list/lang#python"><Badge icon={{<FileCode2 />}} variant="blue-subtle">Python</Badge></a>
<a href="/list/lang#sql"><Badge    icon={{<FileCode2 />}} variant="green-subtle">SQL</Badge></a>
<a href="/list/lang#data"><Badge   icon={{<FileCode2 />}} variant="teal-subtle">Data</Badge></a>

## Summary

{summary_table}

{''.join(language_sections)}
'''
        
        self.write_content('lang.mdx', content)


class InventoryIndexGenerator(ContentGenerator):
    """Generate overall inventory index."""
    
    def generate(self):
        print("Generating inventory index...")
        
        catalog_summary = f'''There are **{len(self.extensions)}** PostgreSQL extensions available in the catalog'''

        # Generate platform statistics
        el_stats = {'all': 0, 'PGDG': 0, 'PIGSTY': 0, 'CONTRIB': 0, 'OTHER': 0, 'MISS': 0}
        debian_stats = {'all': 0, 'PGDG': 0, 'PIGSTY': 0, 'CONTRIB': 0, 'OTHER': 0, 'MISS': 0}
        el_pg_stats = {f'PG{pg}': 0 for pg in self.config.PG_VERSIONS}
        debian_pg_stats = {f'PG{pg}': 0 for pg in self.config.PG_VERSIONS}
        
        for ext in self.extensions:
            self._update_platform_stats(ext, el_stats, el_pg_stats, 'rpm')
            self._update_platform_stats(ext, debian_stats, debian_pg_stats, 'deb')
        
        # Generate statistics table
        pg_cols = ' | '.join([f'PG{pg}' for pg in self.config.PG_VERSIONS])
        statistics_table = f'''| Distro | All | PGDG | PIGSTY | CONTRIB | OTHER | MISS | {pg_cols} |
| -------------- |:----:|:----:|:----:|:----:|:----:|:----:|{':----:|' * len(self.config.PG_VERSIONS)}
| EL | {el_stats['all']} | {el_stats['PGDG']} | {el_stats['PIGSTY']} | {el_stats['CONTRIB']} | {el_stats['OTHER']} | {el_stats['MISS']} | {' | '.join([str(el_pg_stats[f'PG{pg}']) for pg in self.config.PG_VERSIONS])} |
| Debian | {debian_stats['all']} | {debian_stats['PGDG']} | {debian_stats['PIGSTY']} | {debian_stats['CONTRIB']} | {debian_stats['OTHER']} | {debian_stats['MISS']} | {' | '.join([str(debian_pg_stats[f'PG{pg}']) for pg in self.config.PG_VERSIONS])} |'''

        # Generate extensions by category
        extensions_content = []
        for category in CATEGORY_META.keys():
            cat_extensions = [ext for ext in self.extensions if ext.category == category]
            if not cat_extensions:
                continue
                
            cat_extensions.sort(key=lambda e: e.name)
            extension_badges = [f'[`{ext.name}`](/e/{ext.name})' for ext in cat_extensions]
            extensions_row = f'''| {BadgeFormatter.format_category(category)} | {' '.join(extension_badges)} |'''
            extensions_content.append(extensions_row)
        
        extensions_table = f'''| Category | Extensions |
|:--------:|:-----------|
{chr(10).join(extensions_content)}'''
        
        content = f'''---
title: Catalog
description: List of available PostgreSQL Extensions
icon: BookText
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck }} from 'lucide-react';

{catalog_summary}

## Statistics

{statistics_table}

-------

## Categories

{extensions_table}

------

## Source

This catalog is open-sourced under the [Apache License 2.0](https://github.com/pgsty/ext/blob/main/LICENSE) and maintained by the [PGSTY](https://github.com/pgsty) team.

You can find the RAW CSV data files at [github.com/pgsty/extension/data/extension.csv](https://github.com/pgsty/ext/blob/main/data/extension.csv)

- https://github.com/pgsty/extension



'''
        
        self.write_content('index.mdx', content)
    
    def _update_platform_stats(self, ext: Extension, stats: Dict, pg_stats: Dict, platform: str):
        """Update platform statistics for an extension."""
        repo_attr = f'{platform}_repo'
        pg_attr = f'{platform}_pg'
        
        if getattr(ext, repo_attr):
            stats['all'] += 1
            repo_value = getattr(ext, repo_attr)
            if repo_value in stats:
                stats[repo_value] += 1
            else:
                stats['OTHER'] += 1
            
            # Count PG version availability
            for pg_ver in getattr(ext, pg_attr):
                pg_key = f'PG{pg_ver}'
                if pg_key in pg_stats:
                    pg_stats[pg_key] += 1
        else:
            stats['MISS'] += 1


class RepoListGenerator(ContentGenerator):
    """Generate repository-based extension list."""
    
    def generate(self):
        print("Generating repository list...")
        
        # Categorize extensions by availability
        contrib_extensions = [ext for ext in self.extensions if ext.contrib]
        both_extensions = []
        el_only_extensions = []
        debian_only_extensions = []
        
        for ext in self.extensions:
            if ext.contrib:
                continue
                
            has_rpm = ext.has_rpm
            has_deb = ext.has_deb
            
            if has_rpm and has_deb:
                both_extensions.append(ext)
            elif has_rpm and not has_deb:
                el_only_extensions.append(ext)
            elif not has_rpm and has_deb:
                debian_only_extensions.append(ext)
        
        # Sort all extension lists by ID
        for ext_list in [contrib_extensions, both_extensions, el_only_extensions, debian_only_extensions]:
            ext_list.sort(key=lambda e: e.id)
        
        # Generate content sections
        contrib_table = self.table_gen.generate_simple_table(contrib_extensions)
        both_table = self.table_gen.generate_repo_table(both_extensions)
        el_only_table = self.table_gen.generate_repo_table(el_only_extensions)
        debian_only_table = self.table_gen.generate_repo_table(debian_only_extensions)
        
        # Generate summary
        total_extensions = len(self.extensions)
        summary_text = f'''There are **{total_extensions}** PostgreSQL extensions in total: **{len(contrib_extensions)}** CONTRIB extensions, **{len(both_extensions)}** available on both EL and Debian platforms, **{len(el_only_extensions)}** available only on EL platforms, and **{len(debian_only_extensions)}** available only on Debian platforms.'''
        
        # Generate summary table
        summary_table = f'''| Entry | ALL | [CONTRIB](#contrib) | [Both](#both) | [EL Only](#el) | [Debian Only](#debian) |
|:-----:|:---:|:-------------------:|:-------------:|:--------------:|:----------------------:|
| Count | {total_extensions} | {len(contrib_extensions)} | {len(both_extensions)} | {len(el_only_extensions)} | {len(debian_only_extensions)} |'''
        
        content = f'''---
title: By Repository
description: PostgreSQL Extensions organized by Repository Source
icon: Warehouse
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck }} from 'lucide-react';

{summary_text}

{summary_table}

## CONTRIB

Extensions that come with PostgreSQL core distribution. There are **{len(contrib_extensions)}** contrib extensions.

{contrib_table}

## BOTH

There are **{len(both_extensions)}** non-contrib extensions available in both EL and Debian platforms.

{both_table}

## EL

There are **{len(el_only_extensions)}** non-contrib extensions only available in EL platforms.

{el_only_table}

## Debian

There are **{len(debian_only_extensions)}** non-contrib extensions only available in Debian platforms.

{debian_only_table}
'''
        
        self.write_content('repo.mdx', content)


class DistroListGenerator(ContentGenerator):
    """Generate Linux distribution-based extension list."""
    
    def __init__(self, config: Config, extensions: List[Extension], table_gen: TableGenerator, packages: List[Package]):
        super().__init__(config, extensions, table_gen)
        self.packages = packages
    
    def generate(self):
        print("Generating distro list...")
        
        # Get leading extensions (not contrib)
        leading_extensions = [ext for ext in self.extensions if ext.lead and not ext.contrib]
        leading_extensions.sort(key=lambda e: e.id)
        
        # Build package mapping
        package_map = self._build_package_map()
        
        # Navigation table
        nav_table = '''|  OS   |           x86_64            |            aarch64            |
|:-----:|:---------------------------:|:-----------------------------:|
| `el8` | [`el8.x86_64`](#el8x86_64) | [`el8.aarch64`](#el8aarch64) |
| `el9` | [`el9.x86_64`](#el9x86_64) | [`el9.aarch64`](#el9aarch64) |
| `d12` | [`d12.x86_64`](#d12x86_64) | [`d12.aarch64`](#d12aarch64) |
| `u22` | [`u22.x86_64`](#u22x86_64) | [`u22.aarch64`](#u22aarch64) |
| `u24` | [`u24.x86_64`](#u24x86_64) | [`u24.aarch64`](#u24aarch64) |'''
        
        # Generate distro sections
        distro_sections = []
        for distro in self.config.OS_VERSIONS:
            section = self._generate_distro_section(distro, leading_extensions, package_map)
            distro_sections.append(section)
        
        content = f'''---
title: By Linux Distro
description: PostgreSQL Extensions organized by Linux Distribution
icon: Server
full: true
---

PostgreSQL extensions availability across different Linux distributions and architectures:

{nav_table}

{"".join(distro_sections)}
'''
        
        self.write_content('distro.mdx', content)
    
    def _build_package_map(self) -> Dict:
        """Build package mapping: {os_arch: {pkg: {pg: version}}}"""
        package_map = {}
        for pkg in self.packages:
            os_key = f"{pkg.os_code}.{normalize_os_arch(pkg.os_arch)}"
            if os_key not in package_map:
                package_map[os_key] = {}
            if pkg.pname not in package_map[os_key]:
                package_map[os_key][pkg.pname] = {}
            package_map[os_key][pkg.pname][pkg.pg] = {'version': pkg.ver, 'repo': pkg.repo}
        return package_map
    
    def _generate_distro_section(self, distro: str, leading_extensions: List[Extension], package_map: Dict) -> str:
        """Generate section for a specific distro."""
        # Generate version availability table for this distro
        table_rows = []
        pg_headers = ' | '.join([f'**PG{pg}**' for pg in self.config.PG_VERSIONS])
        header_row = f'|                        Extension / PG Major                         | {pg_headers} |'
        separator_row = '|:-------------------------------------------------------------------:|' + ':-------------------------------------------:|' * len(self.config.PG_VERSIONS)
        table_rows.extend([header_row, separator_row])
        
        distro_packages = package_map.get(distro, {})
        
        for ext in leading_extensions:
            pkg_name = ext.pkg
            ext_packages = distro_packages.get(pkg_name, {})
            
            row_data = [f'[`{ext.pkg}`](/e/{ext.name})']
            
            for pg_ver in self.config.PG_VERSIONS:
                if pg_ver in ext_packages:
                    version = ext_packages[pg_ver]['version']
                    repo = ext_packages[pg_ver]['repo']
                    
                    # Extract semantic version
                    semantic_version = extract_semantic_version(version)
                    
                    # Determine color based on repo
                    if 'pigsty' in repo.lower():
                        color_class = 'text-amber-500'
                    elif 'pgdg' in repo.lower():
                        color_class = 'text-blue-500'
                    else:
                        color_class = 'text-purple-500'
                    badge = f'<span className="{color_class}">{semantic_version}</span>'
                else:
                    badge = '<span className="text-red-500">×</span>'
                
                row_data.append(badge)
            
            table_rows.append('| ' + ' | '.join(row_data) + ' |')
        
        availability_table = '\n'.join(table_rows)
        
        return f'''## {distro}

Version availability for {distro}:

{availability_table}
'''


class AttributeListGenerator(ContentGenerator):
    """Generate attribute-based extension list."""
    
    def generate(self):
        print("Generating attribute list...")
        
        # Generate sections
        need_loading_section = self._generate_need_loading_section()
        without_ddl_section = self._generate_without_ddl_section()
        has_dependency_section = self._generate_has_dependency_section()
        multiple_extension_section = self._generate_multiple_extension_section()
        
        content = f'''---
title: By Attribute
description: PostgreSQL extensions organized by Attribute
icon: Shapes
full: true
---

import {{ Badge }} from '@/components/ui/badge';

------

{need_loading_section}

------

{without_ddl_section}

------

{has_dependency_section}

------

{multiple_extension_section}
'''
        
        self.write_content('attr.mdx', content)
    
    def _generate_need_loading_section(self) -> str:
        """Generate Need Loading section."""
        need_loading_extensions = [ext for ext in self.extensions if ext.need_load]
        need_loading_extensions.sort(key=lambda e: e.name)
        
        return f'''## Need Loading

Extensions that require dynamic loading in [`shared_preload_libraries`](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-SHARED-PRELOAD-LIBRARIES) to work properly.

{self.table_gen.generate_simple_table(need_loading_extensions)}'''
    
    def _generate_without_ddl_section(self) -> str:
        """Generate Without DDL section."""
        without_ddl_extensions = [ext for ext in self.extensions if not ext.need_ddl]
        without_ddl_extensions.sort(key=lambda e: e.name)
        
        return f'''## Without DDL

These extensions do not have DDL, so you don't need to run `CREATE EXTENSION` to use them.

{self.table_gen.generate_simple_table(without_ddl_extensions)}'''
    
    def _generate_has_dependency_section(self) -> str:
        """Generate Has Dependency section."""
        has_dependency_extensions = [ext for ext in self.extensions if ext.requires]
        has_dependency_extensions.sort(key=lambda e: e.name)
        
        if not has_dependency_extensions:
            return '''## Has Dependency

Extensions that have dependencies on other extensions.

No extensions with dependencies found.'''
        
        # Generate dependency table
        headers = ['Extension', 'Dependencies']
        rows = [self.table_gen._format_table_header(headers, [':---', ':---'])]
        
        for ext in has_dependency_extensions:
            dependency_links = []
            for dep in ext.requires:
                # Try to find the dependency extension to create proper links
                dep_ext = next((e for e in self.extensions if e.name == dep), None)
                if dep_ext:
                    dependency_links.append(f'[`{dep}`](/e/{dep})')
                else:
                    dependency_links.append(f'`{dep}`')
            
            dependencies_cell = ', '.join(dependency_links)
            row_data = [
                f'[`{ext.name}`](/e/{ext.name})',
                dependencies_cell
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        dependency_table = '\n'.join(rows)
        
        return f'''## Has Dependency

Extensions that have dependencies on other extensions.

{dependency_table}'''
    
    def _generate_multiple_extension_section(self) -> str:
        """Generate Multiple Extension section."""
        # Group extensions by package
        package_extensions = defaultdict(list)
        for ext in self.extensions:
            if ext.pkg:
                package_extensions[ext.pkg].append(ext)
        
        # Find packages with multiple extensions
        multi_packages = {pkg: exts for pkg, exts in package_extensions.items() if len(exts) > 1}
        
        if not multi_packages:
            return '''## Multiple Extension

These packages contain multiple extensions simultaneously:

No packages with multiple extensions found.'''
        
        # Generate multiple extension table
        headers = ['Package', 'Extensions']
        rows = [self.table_gen._format_table_header(headers, [':---', ':---'])]
        
        # Sort packages by the leading extension ID
        sorted_packages = []
        for pkg, exts in multi_packages.items():
            # Sort extensions within package: leading extension first, then by ID
            sorted_exts = sorted(exts, key=lambda e: (not e.lead, e.id))
            sorted_packages.append((pkg, sorted_exts))
        
        # Sort packages by the ID of their leading extension
        sorted_packages.sort(key=lambda item: item[1][0].id)
        
        for pkg, exts in sorted_packages:
            extension_links = []
            for ext in exts:
                extension_links.append(f'[`{ext.name}`](/e/{ext.name})')
            
            extensions_cell = ', '.join(extension_links)
            leading_ext = next((e for e in exts if e.lead), exts[0])
            
            row_data = [
                f'[`{pkg}`](/e/{leading_ext.name})',
                extensions_cell
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        multiple_table = '\n'.join(rows)
        
        return f'''## Multiple Extension

These packages contain multiple extensions simultaneously:

{multiple_table}'''


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class ExtensionListGenerator:
    """Main application class."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.db_manager = DatabaseManager(self.config.DB_CONNECTION)
        self.extensions = []
        self.packages = []
        self.leading_map = {}
        self.table_gen = None
    
    def run(self):
        """Run the complete generation process."""
        self._setup()
        self._generate_all_lists()
        print("List generation complete!")
    
    def _setup(self):
        """Setup data and dependencies."""
        # Load category metadata from CSV
        global CATEGORY_META
        CATEGORY_META = self.db_manager.load_category_metadata()
        
        # Load data from database
        self.extensions = self.db_manager.load_extensions()
        self.packages = self.db_manager.load_packages()
        
        # Load packages for all extensions
        for ext in self.extensions:
            ext.load_packages(self.packages)
        
        # Build leading extension map
        self.leading_map = self._build_leading_map()
        
        # Initialize table generator
        self.table_gen = TableGenerator(self.leading_map)
        
        # Ensure output directory exists
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)
    
    def _build_leading_map(self) -> Dict[str, str]:
        """Build a mapping from package names to their leading extensions."""
        leading_map = {}
        for ext in self.extensions:
            if ext.lead and ext.pkg:
                leading_map[ext.pkg] = ext.name
        return leading_map
    
    def _generate_all_lists(self):
        """Generate all list pages."""
        generators = [
            CategoryListGenerator(self.config, self.extensions, self.table_gen),
            LinuxDistroGenerator(self.config, self.extensions, self.table_gen, self.packages),
            PGMajorGenerator(self.config, self.extensions, self.table_gen),
            LicenseListGenerator(self.config, self.extensions, self.table_gen),
            LanguageListGenerator(self.config, self.extensions, self.table_gen),
            InventoryIndexGenerator(self.config, self.extensions, self.table_gen),
            RepoListGenerator(self.config, self.extensions, self.table_gen),
            DistroListGenerator(self.config, self.extensions, self.table_gen, self.packages),
            AttributeListGenerator(self.config, self.extensions, self.table_gen),
        ]
        
        for generator in generators:
            generator.generate()
        
        # Generate individual category pages for the 16 categories
        self._generate_category_pages()
    
    def _generate_category_pages(self):
        """Generate individual category pages for the 16 categories."""
        print("Generating individual category pages...")
        
        # Group extensions by category
        category_groups = defaultdict(list)
        for ext in self.extensions:
            category_groups[ext.category].append(ext)
        
        # Generate a page for each category
        for category in CATEGORY_META.keys():
            if category not in category_groups:
                continue
            
            cat_extensions = sorted(category_groups[category], key=lambda e: e.name)
            count = len(cat_extensions)
            meta = CATEGORY_META[category]
            
            # Generate extension table
            extension_table = self.table_gen.generate_category_table(cat_extensions)
            
            # Generate extension cards with detailed information
            extension_cards = self.table_gen.generate_extension_cards(cat_extensions, self.config, is_chinese=False)
            
            # Generate Chinese extension cards
            extension_cards_zh = self.table_gen.generate_extension_cards(cat_extensions, self.config, is_chinese=True)
            
            # Generate meta.json files for navigation
            self._generate_meta_json_files(category, cat_extensions)
            
            # English version
            en_content = f'''---
title: {category}
description: "{meta["en_desc"]}"
icon: {meta["icon"]}
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Callout }} from 'fumadocs-ui/components/callout';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck, Scale, FileCode2 }} from 'lucide-react';

{category} category contains **{count}** PostgreSQL extensions.

{extension_table}

--------

{extension_cards}
'''
            
            # Chinese version  
            zh_content = f'''---
title: {category}
description: "{meta["zh_desc"]}"
icon: {meta["icon"]}
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Callout }} from 'fumadocs-ui/components/callout';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck, Scale, FileCode2 }} from 'lucide-react';

{category} 分类包含 **{count}** 个 PostgreSQL 扩展。

{self.table_gen.generate_category_table_zh(cat_extensions)}

--------

{extension_cards_zh}
'''
            
            # Write category pages
            category_dir = os.path.join(self.config.OUTPUT_DIR, '..', 'cate', category.lower())
            os.makedirs(category_dir, exist_ok=True)
            
            # English version
            en_path = os.path.join(category_dir, 'index.mdx')
            with open(en_path, 'w', encoding='utf-8') as f:
                f.write(en_content)
            print(f"Generated: {en_path}")
            
            # Chinese version
            zh_path = os.path.join(category_dir, 'index.zh.mdx')
            with open(zh_path, 'w', encoding='utf-8') as f:
                f.write(zh_content)
            print(f"Generated: {zh_path}")
    
    def _generate_meta_json_files(self, category: str, extensions: List[Extension]):
        """Generate meta.json and meta.zh.json files for a category."""
        import json
        
        # Create category directory if it doesn't exist
        category_dir = os.path.join(self.config.OUTPUT_DIR, '..', 'cate', category.lower())
        os.makedirs(category_dir, exist_ok=True)
        
        # Generate pages array for English
        en_pages = []
        zh_pages = []
        
        for ext in extensions:
            # English version
            en_pages.append(f"[{ext.name}](/e/{ext.name})")
            
            # Chinese version  
            zh_pages.append(f"[{ext.name}](/zh/e/{ext.name})")
        
        # Generate English meta.json
        en_meta = {
            "pages": en_pages
        }
        
        en_meta_path = os.path.join(category_dir, 'meta.json')
        with open(en_meta_path, 'w', encoding='utf-8') as f:
            json.dump(en_meta, f, indent=2, ensure_ascii=False)
        print(f"Generated: {en_meta_path}")
        
        # Generate Chinese meta.zh.json
        zh_meta = {
            "pages": zh_pages
        }
        
        zh_meta_path = os.path.join(category_dir, 'meta.zh.json')
        with open(zh_meta_path, 'w', encoding='utf-8') as f:
            json.dump(zh_meta, f, indent=2, ensure_ascii=False)
        print(f"Generated: {zh_meta_path}")


def main():
    """Main entry point."""
    config = Config()
    app = ExtensionListGenerator(config)
    app.run()


if __name__ == "__main__":
    main()