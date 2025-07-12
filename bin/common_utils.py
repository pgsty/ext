#!/usr/bin/env python3

"""
Common utilities for PostgreSQL extension list generators.
Shared data structures, CSV readers, and template generators.
"""

import os
import csv
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class Config:
    """Configuration for the list generators."""
    
    # Data directory
    DATA_DIR: str = None
    
    # Output directory 
    OUTPUT_DIR: str = None
    
    # Supported operating systems
    OS_VERSIONS: List[str] = None
    
    # Supported PostgreSQL major versions
    PG_VERSIONS: List[int] = None
    
    def __post_init__(self):
        if self.DATA_DIR is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.DATA_DIR = os.path.abspath(os.path.join(script_dir, '..', 'data'))
        
        if self.OUTPUT_DIR is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.OUTPUT_DIR = os.path.abspath(os.path.join(script_dir, '..', 'content', 'docs', 'list'))
        
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


# =============================================================================
# CONSTANTS AND MAPPINGS
# =============================================================================

OS_DESCRIPTIONS = {
    'el8': 'Enterprise Linux 8 (RHEL 8, CentOS 8, Rocky 8, Alma 8)',
    'el9': 'Enterprise Linux 9 (RHEL 9, CentOS 9, Rocky 9, Alma 9)',
    'd12': 'Debian 12 (Bookworm)',
    'u22': 'Ubuntu 22.04 LTS (Jammy)',
    'u24': 'Ubuntu 24.04 LTS (Noble)'
}

# Category color scheme - unified color mapping for categories
CATEGORY_COLORS = {
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
    'Python': {"variant": 'blue-subtle', "anchor": "python"},
    'Rust': {"variant": 'amber-subtle', "anchor": "rust"},
    'SQL': {"variant": 'green-subtle', "anchor": "sql"},
    'Java': {"variant": 'pink-subtle', "anchor": "java"},
    'Data': {"variant": 'teal-subtle', "anchor": "data"},
    'C++': {"variant": 'purple-subtle', "anchor": "c-1"},
    'C': {"variant": 'blue-subtle', "anchor": "c"},
}

REPO_CONFIG = {
    'PIGSTY': {'variant': 'amber-subtle'},
    'PGDG': {'variant': 'blue-subtle'},
    'CONTRIB': {'variant': 'purple-subtle'},
    'OTHER': {'variant': 'gray-subtle'}
}


# =============================================================================
# DATA CLASSES
# =============================================================================

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
    
    @property
    def has_rpm(self) -> bool:
        return bool(self.rpm_repo)
    
    @property
    def has_deb(self) -> bool:
        return bool(self.deb_repo)

@dataclass
class Category:
    """Represents a category with metadata."""
    id: int
    name: str
    icon1: str
    icon2: str
    extra: str
    zh_desc: str
    en_desc: str


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


def normalize_license_name(license_name: str) -> str:
    """Normalize license names to standard format."""
    return LICENSE_NORMALIZATION.get(license_name, license_name)


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
    def format_category(category: str, category_meta: Dict, is_chinese: bool = False, in_cate_page: bool = False) -> str:
        """Format category as Badge component with icon and color."""
        meta = category_meta.get(category)
        if meta:
            iconstr = f'{{<{meta.icon2} />}}'
        else:
            iconstr = '{<Blocks />}'
        
        # Use the unified color scheme
        color = CATEGORY_COLORS.get(category, 'gray-subtle')
        
        # Determine link target
        if in_cate_page:
            # Link to anchor in current page
            href = f"#{category.lower()}"
        else:
            # Link to category page
            path_prefix = '/zh' if is_chinese else ''
            href = f"{path_prefix}/cate/{category.lower()}"
        
        return f'<Badge icon={iconstr} variant="{color}"><a href="{href}" className="no-underline">{category}</a></Badge>'
    
    @staticmethod
    def format_license(license_name: str, is_chinese: bool = False, in_license_page: bool = False) -> str:
        """Format license as Badge component with context-aware links."""
        license_info = LICENSE_INFO.get(license_name, {
            'anchor': license_name.lower().replace(' ', '-').replace('.', ''), 
            'variant': 'gray-subtle'
        })
        
        # Determine link target
        if in_license_page:
            # Link to anchor in current page
            href = f"#{license_info['anchor']}"
        else:
            # Link to license page
            path_prefix = '/zh' if is_chinese else ''
            href = f"{path_prefix}/list/license#{license_info['anchor']}"
        
        return f'<a href="{href}" className="no-underline"><Badge icon={{<Scale />}} variant="{license_info["variant"]}">{license_name}</Badge></a>'
    
    @staticmethod
    def format_language(language: str, is_chinese: bool = False, in_language_page: bool = False) -> str:
        """Format programming language as Badge component with context-aware links."""
        info = LANGUAGE_CONFIG.get(language, {"variant": 'gray-subtle', "anchor": "#"})
        
        # Determine link target
        if in_language_page:
            # Extract anchor from existing config and use for in-page navigation
            if '#' in info.get('anchor', ''):
                anchor = info['anchor'].split('#')[1]
                href = f"#{anchor}"
            else:
                href = f"#{language.lower().replace('+', '-')}"
        else:
            # Link to language page
            path_prefix = '/zh' if is_chinese else ''
            if '#' in info.get('anchor', ''):
                anchor = info['anchor'].split('#')[1]
                href = f"{path_prefix}/list/lang#{anchor}"
            else:
                href = f"{path_prefix}/list/lang#{language.lower().replace('+', '-')}"
        
        return f'<a href="{href}"><Badge icon={{<FileCode2 />}} variant="{info["variant"]}">{language or "N/A"}</Badge></a>'
    
    @staticmethod
    def format_repo(repo: str) -> str:
        """Format repository as Badge component with appropriate color."""
        info = REPO_CONFIG.get(repo, {'variant': 'gray-subtle'})
        return f'<Badge variant="{info["variant"]}">{repo}</Badge>'


# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

class DataLoader:
    """Handles loading data from CSV files."""
    
    def __init__(self, config: Config):
        self.config = config
    
    def load_categories(self) -> Dict[str, Category]:
        """Load category metadata from CSV file."""
        categories = {}
        csv_path = os.path.join(self.config.DATA_DIR, 'category.csv')
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                category = Category(
                    id=int(row['id']),
                    name=row['name'],
                    icon1=row['icon1'],
                    icon2=row['icon2'],
                    extra=row['extra'],
                    zh_desc=row['zh_desc'],
                    en_desc=row['en_desc']
                )
                categories[category.name] = category
        
        print(f"Loaded {len(categories)} categories.")
        return categories
    
    def load_extensions(self) -> List[Extension]:
        """Load all extensions from CSV file."""
        extensions = []
        csv_path = os.path.join(self.config.DATA_DIR, 'extension.csv')
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                extension = Extension(
                    id=int(row['id']),
                    name=row['name'],
                    pkg=row['pkg'],
                    lead_ext=row['lead_ext'] if row['lead_ext'] else None,
                    category=row['category'],
                    state=row['state'],
                    url=row['url'] if row['url'] else None,
                    license=row['license'] if row['license'] else None,
                    tags=parse_array(row['tags']) if row['tags'] else [],
                    version=row['version'] if row['version'] else None,
                    repo=row['repo'],
                    lang=row['lang'] if row['lang'] else None,
                    contrib=row['contrib'].lower() == 't',
                    lead=row['lead'].lower() == 't',
                    has_bin=row['has_bin'].lower() == 't',
                    has_lib=row['has_lib'].lower() == 't',
                    need_ddl=row['need_ddl'].lower() == 't',
                    need_load=row['need_load'].lower() == 't',
                    trusted=row['trusted'].lower() == 't',
                    relocatable=row['relocatable'].lower() == 't',
                    schemas=parse_array(row['schemas']) if row['schemas'] else [],
                    pg_ver=parse_array(row['pg_ver']) if row['pg_ver'] else [],
                    requires=parse_array(row['requires']) if row['requires'] else [],
                    require_by=parse_array(row['require_by']) if row['require_by'] else [],
                    see_also=parse_array(row['see_also']) if row['see_also'] else [],
                    rpm_ver=row['rpm_ver'] if row['rpm_ver'] else None,
                    rpm_repo=row['rpm_repo'] if row['rpm_repo'] else None,
                    rpm_pkg=row['rpm_pkg'] if row['rpm_pkg'] else None,
                    rpm_pg=parse_array(row['rpm_pg']) if row['rpm_pg'] else [],
                    rpm_deps=parse_array(row['rpm_deps']) if row['rpm_deps'] else [],
                    deb_ver=row['deb_ver'] if row['deb_ver'] else None,
                    deb_repo=row['deb_repo'] if row['deb_repo'] else None,
                    deb_pkg=row['deb_pkg'] if row['deb_pkg'] else None,
                    deb_deps=parse_array(row['deb_deps']) if row['deb_deps'] else [],
                    deb_pg=parse_array(row['deb_pg']) if row['deb_pg'] else [],
                    source=row['source'] if row['source'] else None,
                    extra=row['extra'] if row['extra'] else None,
                    en_desc=row['en_desc'] if row['en_desc'] else None,
                    zh_desc=row['zh_desc'] if row['zh_desc'] else None,
                    comment=row['comment'] if row['comment'] else None,
                    mtime=row['mtime']
                )
                extensions.append(extension)
        
        print(f"Loaded {len(extensions)} extensions.")
        return extensions


# =============================================================================
# TABLE GENERATION FUNCTIONS
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
    
    def generate_simple_table_zh(self, extensions: List[Extension]) -> str:
        """Generate simple Chinese extension table."""
        if not extensions:
            return "未找到扩展。"
        
        headers = ['ID', '扩展名', '软件包', '描述']
        rows = [self._format_table_header(headers, [':---:',':---',':---',':---'])]
        
        for ext in extensions:
            package_cell = f'[`{ext.pkg}`](/zh/e/{self.leading_map.get(ext.pkg, ext.name)})'
            row_data = [
                str(ext.id),
                f'[`{ext.name}`](/zh/e/{ext.name})',
                package_cell,
                ext.zh_desc or ext.en_desc or '暂无描述'
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
        
        headers = ['ID', '扩展', '扩展包', '版本', '描述']
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
    
    def generate_repo_table(self, extensions: List[Extension], category_meta: Dict, is_chinese: bool = False) -> str:
        """Generate extension table for repo lists (ID, Name, Category, RPM, DEB, Description)."""
        if not extensions:
            return "未找到扩展。" if is_chinese else "No extensions found."
        
        if is_chinese:
            headers = ['ID', '名称', '分类', 'RPM', 'DEB', '描述']
        else:
            headers = ['ID', 'Name', 'Category', 'RPM', 'DEB', 'Description']
        rows = [self._format_table_header(headers, [':---:',':---',':---',':---:',':---:',':---'])]
        
        path_prefix = '/zh' if is_chinese else ''
        
        for ext in extensions:
            rpm_badge = BadgeFormatter.format_repo(ext.rpm_repo) if ext.rpm_repo else '-'
            deb_badge = BadgeFormatter.format_repo(ext.deb_repo) if ext.deb_repo else '-'
            category_badge = BadgeFormatter.format_category(ext.category, category_meta, is_chinese) if ext.category else '-'
            
            description = (ext.zh_desc or ext.en_desc or '暂无描述') if is_chinese else (ext.en_desc or 'No description')
            
            row_data = [
                str(ext.id),
                f'[`{ext.name}`]({path_prefix}/e/{ext.name})',
                category_badge,
                rpm_badge,
                deb_badge,
                description
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        return '\n'.join(rows)
    
    def _format_table_header(self, headers: List[str], alignments: List[str]) -> str:
        """Format table header with alignment."""
        header_row = '| ' + ' | '.join(headers) + ' |'
        separator_row = '|' + '|'.join(alignments) + '|'
        return header_row + '\n' + separator_row


# =============================================================================
# CONTENT WRITING UTILITY
# =============================================================================

def write_content(config: Config, filename: str, content: str):
    """Write content to file in the output directory."""
    output_path = os.path.join(config.OUTPUT_DIR, filename)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {output_path}")


def build_leading_map(extensions: List[Extension]) -> Dict[str, str]:
    """Build a mapping from package names to their leading extensions."""
    leading_map = {}
    for ext in extensions:
        if ext.lead and ext.pkg:
            leading_map[ext.pkg] = ext.name
    return leading_map