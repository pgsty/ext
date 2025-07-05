#!/usr/bin/env python3

import os
import psycopg2
from typing import Dict, List, Optional, Any

# Database connection
CONN = psycopg2.connect('postgres:///vonng')

# Global mappings for reverse dependency lookup and leading extensions
EXT_MAP = {}
DEP_MAP = {}
LEADING_MAP = {}  # Maps package names to leading extension names

# Constants
DEFAULT_OS = ['el8.x86_64', 'el8.aarch64', 'el9.x86_64', 'el9.aarch64', 'd12.x86_64', 'd12.aarch64', 'u22.x86_64', 'u22.aarch64', 'u24.x86_64', 'u24.aarch64']
DEFAULT_PG = [17, 16, 15, 14, 13]

# Directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'content', 'docs', 'ext'))
STUB_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'stub'))

# Utility functions
def normalize_arch(arch: str) -> str:
    """Normalize different architecture representations to standard format."""
    if not arch: return 'x86_64'  # default fallback
    arch = arch.lower().strip()
    if arch in ['x86_64', 'amd64', 'x86', 'amd']:return 'x86_64'
    if arch in ['aarch64', 'arm64', 'arm', 'armv8']: return 'aarch64'
    print(f"Warning: Unknown architecture '{arch}', defaulting to x86_64")
    return 'x86_64'

def format_repo_badge(repo: str) -> str:
    """Format repository name as Badge component."""
    repo_badges = {
        'PGDG': '<Badge variant="blue-subtle"><span className="font-bold">PGDG</span></Badge>',
        'PIGSTY': '<Badge variant="amber-subtle"><span className="font-bold">PIGSTY</span></Badge>',
        'CONTRIB': '<Badge variant="green-subtle"><span className="font-bold">CONTRIB</span></Badge>',
        'MIXED': '<Badge variant="gray-subtle"><span className="font-bold">MIXED</span></Badge>'
    }
    return repo_badges.get(repo, f'<Badge variant="gray-subtle"><span className="font-bold">{repo}</span></Badge>' if repo else 'N/A')

def format_license_badge(license_name: str) -> str:
    """Format license as Badge component with standard colors and links."""
    # License mapping to standard names and anchor links
    license_mapping = {
        'PostgreSQL': {'name': 'PostgreSQL', 'anchor': 'postgresql', 'variant': 'blue-subtle'},
        'MIT': {'name': 'MIT', 'anchor': 'mit', 'variant': 'blue-subtle'},
        'ISC': {'name': 'ISC', 'anchor': 'isc', 'variant': 'blue-subtle'},
        'BSD-0': {'name': 'BSD 0-Clause', 'anchor': 'bsd-0-clause', 'variant': 'blue-subtle'},
        'BSD 0-Clause': {'name': 'BSD 0-Clause', 'anchor': 'bsd-0-clause', 'variant': 'blue-subtle'},
        'BSD-2': {'name': 'BSD 2-Clause', 'anchor': 'bsd-2-clause', 'variant': 'blue-subtle'},
        'BSD 2-Clause': {'name': 'BSD 2-Clause', 'anchor': 'bsd-2-clause', 'variant': 'blue-subtle'},
        'BSD-3': {'name': 'BSD 3-Clause', 'anchor': 'bsd-3-clause', 'variant': 'blue-subtle'},
        'BSD 3-Clause': {'name': 'BSD 3-Clause', 'anchor': 'bsd-3-clause', 'variant': 'blue-subtle'},
        'Artistic': {'name': 'Artistic', 'anchor': 'artistic', 'variant': 'green-subtle'},
        'Apache-2.0': {'name': 'Apache-2.0', 'anchor': 'apache-20', 'variant': 'green-subtle'},
        'MPL-2.0': {'name': 'MPL-2.0', 'anchor': 'mpl-20', 'variant': 'green-subtle'},
        'MPLv2': {'name': 'MPL-2.0', 'anchor': 'mpl-20', 'variant': 'green-subtle'},
        'GPL-2.0': {'name': 'GPL-2.0', 'anchor': 'gpl-20', 'variant': 'amber-subtle'},
        'GPLv2': {'name': 'GPL-2.0', 'anchor': 'gpl-20', 'variant': 'amber-subtle'},
        'GPL-3.0': {'name': 'GPL-3.0', 'anchor': 'gpl-30', 'variant': 'amber-subtle'},
        'GPLv3': {'name': 'GPL-3.0', 'anchor': 'gpl-30', 'variant': 'amber-subtle'},
        'LGPL-2.1': {'name': 'LGPL-2.1', 'anchor': 'lgpl-21', 'variant': 'amber-subtle'},
        'LGPLv2': {'name': 'LGPL-2.1', 'anchor': 'lgpl-21', 'variant': 'amber-subtle'},
        'LGPL-3.0': {'name': 'LGPL-3.0', 'anchor': 'lgpl-30', 'variant': 'amber-subtle'},
        'LGPLv3': {'name': 'LGPL-3.0', 'anchor': 'lgpl-30', 'variant': 'amber-subtle'},
        'AGPL-3.0': {'name': 'AGPL-3.0', 'anchor': 'agpl-30', 'variant': 'red-subtle'},
        'AGPLv3': {'name': 'AGPL-3.0', 'anchor': 'agpl-30', 'variant': 'red-subtle'},
        'Timescale': {'name': 'Timescale', 'anchor': 'timescale', 'variant': 'gray-subtle'}
    }
    
    license_info = license_mapping.get(license_name, {
        'name': license_name, 
        'anchor': license_name.lower().replace(' ', '-').replace('.', '') if license_name else 'unknown', 
        'variant': 'gray-subtle'
    })
    
    return f'<a href="/list/license#{license_info["anchor"]}" className="no-underline"><Badge icon={{<Scale />}} variant="{license_info["variant"]}">{license_info["name"]}</Badge></a>'

def format_language_badge(language: str, extra: str = None) -> str:
    """Format programming language as Badge component with appropriate color."""
    language_dict = {
        'Python': { "variant": 'blue-subtle'   ,"anchor": "/list/lang#python" },
        'Rust':   { "variant": 'amber-subtle'  ,"anchor": "/list/lang#rust" },
        'SQL':    { "variant": 'green-subtle'  ,"anchor": "/list/lang#sql" },
        'Java':   { "variant": 'pink-subtle'   ,"anchor": "/list/lang#java" },
        'Data':   { "variant": 'teal-subtle'   ,"anchor": "/list/lang#data" },
        'C++':    { "variant": 'purple-subtle' ,"anchor": "/list/lang#c-1" },
        'C':      { "variant": 'blue-subtle'   ,"anchor": "/list/lang#c" },
    }
    info = language_dict.get(language, 'gray-subtle')
    return f'<a href="{info['anchor']}"><Badge icon={{<FileCode2 />}} variant="{info['variant']}">{language or "N/A"}</Badge></a>'


def format_category_badge(category: str) -> str:
    """Format category as Badge component with icon and color."""
    category_meta = {
        'TIME': {'icon': 'Clock', 'color': 'blue-subtle'},
        'GIS': {'icon': 'Globe', 'color': 'green-subtle'}, 
        'RAG': {'icon': 'Brain', 'color': 'purple-subtle'},
        'FTS': {'icon': 'Search', 'color': 'amber-subtle'},
        'OLAP': {'icon': 'ChartNoAxesCombined', 'color': 'red-subtle'},
        'FEAT': {'icon': 'Sparkles', 'color': 'pink-subtle'},
        'LANG': {'icon': 'BookA', 'color': 'teal-subtle'},
        'TYPE': {'icon': 'Boxes', 'color': 'gray-subtle'},
        'UTIL': {'icon': 'Wrench', 'color': 'amber-subtle'},
        'FUNC': {'icon': 'Variable', 'color': 'pink-subtle'},
        'ADMIN': {'icon': 'Landmark', 'color': 'gray-subtle'},
        'STAT': {'icon': 'Activity', 'color': 'green-subtle'},
        'SEC': {'icon': 'Shield', 'color': 'red-subtle'},
        'FDW': {'icon': 'FileInput', 'color': 'blue-subtle'},
        'SIM': {'icon': 'Shell', 'color': 'teal-subtle'},
        'ETL': {'icon': 'Truck', 'color': 'purple-subtle'}
    }
    meta = category_meta.get(category, {'icon': 'Blocks', 'color': 'gray-subtle'})
    iconstr = '{<%s />}' % meta['icon']
    return f'<a href="/cate/{category.lower()}" className="no-underline"><Badge icon={iconstr} variant="{meta["color"]}">{category}</Badge></a>'

def format_pg_badge(pg_version: int, repo: str = '') -> str:
    """Format PostgreSQL version as Badge with appropriate color."""
    if repo == 'PIGSTY':
        return f'<Badge variant="amber-subtle">**PG{pg_version}**</Badge>'
    else:
        return f'<Badge variant="blue-subtle">**PG{pg_version}**</Badge>'

def parse_array(value: str) -> List[str]:
    """Parse PostgreSQL array string to Python list."""
    # already a list, return it
    if isinstance(value, list):
        return value
    if not value or not value.startswith('{') or not value.endswith('}'):
        return []
    return [item.strip() for item in value[1:-1].split(',') if item.strip()]

# Template for generating extension documentation
EXTENSION_TEMPLATE = '''---
title: {name}
description: {description}
full: true
---

import {{ File, Folder, Files }} from 'fumadocs-ui/components/files';
import {{ Package, Box }} from 'lucide-react';
import {{ Callout }} from 'fumadocs-ui/components/callout';
import {{ Badge }} from '@/components/ui/badge';
import {{ TooltipIconButton }} from '@/components/ui/tooltip-icon-button';
import {{
    Scale, Clock, Globe, Brain, Search, ChartNoAxesCombined,
    Sparkles, BookA, Boxes, Wrench, Variable, Landmark,
    Activity, Shield, FileInput, FileCode2, Shell, Truck, Blocks
}} from 'lucide-react';

## Overview

| <TooltipIconButton tooltip="Extension unique identifier" side="top">ID</TooltipIconButton> | <TooltipIconButton tooltip="Extension name" side="top">Name</TooltipIconButton> | <TooltipIconButton tooltip="Package name for installation" side="top">Package</TooltipIconButton> | <TooltipIconButton tooltip="Latest available extension version" side="top">Version</TooltipIconButton> | <TooltipIconButton tooltip="Extension category" side="top">Category</TooltipIconButton> | <TooltipIconButton tooltip="Open source license" side="top">License</TooltipIconButton> | <TooltipIconButton tooltip="Programming language" side="top">Lang</TooltipIconButton> |
|:--------:|:--------:|:----------:|:--------------:|:---------------------------------------:|:------------------------------------------------------:|:----:|
| **{ext_id}** | {name_link} | {package} | {version} | {category_badge} | {license_badge} | {language} |

### Attributes

| <TooltipIconButton tooltip="The Primary Leading extension in the Package" side="top">Leading</TooltipIconButton> | <TooltipIconButton tooltip="Contains binary utils" side="top">Has Bin</TooltipIconButton> | <TooltipIconButton tooltip="Contains .so shared library files" side="top">Has Lib</TooltipIconButton> | <TooltipIconButton tooltip="Requires preloading via shared_preload_libraries" side="top">PreLoad</TooltipIconButton> | <TooltipIconButton tooltip="Requires CREATE EXTENSION DDL command" side="top">Need DDL</TooltipIconButton> | <TooltipIconButton tooltip="Can be installed in any schema" side="top">Relocatable</TooltipIconButton> | <TooltipIconButton tooltip="Can be created by non-superuser" side="top">Trusted</TooltipIconButton> | <TooltipIconButton tooltip="Schemas used by this extension" side="top">Schemas</TooltipIconButton> |
|:-------:|:-------:|:-------:|:-------:|:--------:|:-----------:|:-------:|:-------:|
| {lead} | {has_bin} | {has_lib} | {need_load} | {need_ddl} | {relocatable} | {trusted} | {schemas} |

### Packages

| <TooltipIconButton tooltip="Linux distribution family, EL or Debian" side="top">Distro</TooltipIconButton> | <TooltipIconButton tooltip="Package repository" side="top">Repo</TooltipIconButton> | <TooltipIconButton tooltip="The RPM/DEB Package Name Pattern (replace $v with real pg major)" side="top">Package Name</TooltipIconButton> | <TooltipIconButton tooltip="Latest package version" side="top">Version</TooltipIconButton> | <TooltipIconButton tooltip="RPM/DEB Package dependencies" side="top">Deps</TooltipIconButton> | <TooltipIconButton tooltip="Available in these PostgreSQL Major Versions" side="top">PG Major</TooltipIconButton> |
|:----------:|:--------:|:------------------------:|:-----------:|:------------:|:------------------:|
{package_info}

{dependencies_section}

------

## Availability

{availability_table}

<Badge variant="green-subtle"><span className="font-black">CONTRIB</span></Badge> <Badge variant="blue-subtle"><span className="font-black">PGDG</span></Badge> <Badge variant="amber-subtle"><span className="font-black">PIGSTY</span></Badge>

------

## Download

{download_section}

------

## Install

{install_section}

{stub_include}
'''


class Package:
    """Represents a PostgreSQL extension package."""
    
    def __init__(self, row):
        (self.pkg, self.pname, self.os, self.pg, self.name, self.ver, self.org, 
         self.type, self.os_code, self.os_arch, self.repo, self.version, 
         self.release, self.file, self.sha256, self.url, self.mirror_url, 
         self.size, self.size_full) = row
    
    def __str__(self):
        return f"{self.pname} @ {self.os}"



class Extension:
    """Represents a PostgreSQL extension with all its metadata and packages."""
    
    def __init__(self, row):
        # Unpack the database row
        (self.id, self.name, self.pkg, self.alias, self.category, self.state, 
         self.url, self.license, self.tags, self.version, self.repo, self.lang, 
         self.contrib, self.lead, self.has_bin, self.has_lib, self.need_ddl, 
         self.need_load, self.trusted, self.relocatable, self.schemas, 
         self.pg_ver, self.requires, self.rpm_ver, self.rpm_repo, self.rpm_pkg, 
         self.rpm_pg, self.rpm_deps, self.deb_ver, self.deb_repo, self.deb_pkg, 
         self.deb_deps, self.deb_pg, self.bad_case, self.extra, self.ctime, 
         self.mtime, self.en_desc, self.zh_desc, self.comment) = row
        
        # Parse array fields
        self.tags = parse_array(self.tags) if self.tags else []
        self.pg_ver = parse_array(self.pg_ver) if self.pg_ver else []
        self.requires = parse_array(self.requires) if self.requires else []
        self.schemas = parse_array(self.schemas) if self.schemas else []
        self.rpm_deps = parse_array(self.rpm_deps) if self.rpm_deps else []
        self.deb_deps = parse_array(self.deb_deps) if self.deb_deps else []
        self.rpm_pg = parse_array(self.rpm_pg) if self.rpm_pg else []
        self.deb_pg = parse_array(self.deb_pg) if self.deb_pg else []
        
        # Computed properties
        self.has_rpm = bool(self.rpm_repo)
        self.has_deb = bool(self.deb_repo)
        self.packages: List[Package] = []
    
    def __str__(self):
        return self.name
    
    def load_packages(self):
        """Load package information from database."""
        with CONN.cursor() as cur:
            cur.execute('SELECT * FROM ext.pkg WHERE pkg = %s ORDER BY type DESC, os, pg DESC;', (self.pkg,))
            res = cur.fetchall()
        self.packages = [Package(row) for row in res]

    def format_bool(self, value: Optional[bool], true_text: str = "Yes", false_text: str = "No") -> str:
        """Format boolean value for display."""
        if value is None:
            return "Unknown"
        return true_text if value else false_text
    
    def generate_dependencies_section(self) -> str:
        """Generate dependencies, reverse dependencies, and comments callout sections."""
        sections = []
        
        # Dependencies (what this extension requires)
        if self.requires:
            deps_links = [f"[{dep}](/ext/{dep})" for dep in self.requires]
            deps_text = ", ".join(deps_links)
            sections.append(f'''
<Callout title="Dependencies" type="warn">
    This extension depends on: {deps_text}
</Callout>
''')
        
        # Reverse dependencies (what depends on this extension)
        if self.name in DEP_MAP:
            dependents = DEP_MAP[self.name]
            dependent_links = [f"[{dep}](/ext/{dep})" for dep in dependents]
            dependent_text = ", ".join(dependent_links)
            sections.append(f'''
<Callout title="Dependent Extensions" type="info">
    The following extensions depend on this extension: {dependent_text}
</Callout>
''')
        
        # Comments (if extension has comment field)
        if self.comment and self.comment.strip():
            sections.append(f'''
<Callout title="Comments" type="info">
    {self.comment}
</Callout>
''')
        
        return ''.join(sections)
    
    def generate_package_info(self) -> str:
        """Generate package information table rows."""
        rows = []
        
        if self.has_rpm:
            # Generate PG version badges for RPM
            rpm_pg_badges = []
            for pg in DEFAULT_PG:
                if str(pg) in (self.rpm_pg or []):
                    rpm_pg_badges.append(f'<Badge variant="green-subtle">{pg}</Badge>')
                else:
                    rpm_pg_badges.append(f'<Badge variant="red-subtle">{pg}</Badge>')
            rpm_pg_versions = "".join(rpm_pg_badges)
            
            rpm_deps = "<br /> ".join([ '`%s`'%i for i in self.rpm_deps]) if self.rpm_deps else "-"
            rows.append(f"|   **EL**   | {format_repo_badge(self.rpm_repo)} | `{self.rpm_pkg or '-'}` | `{self.rpm_ver or '-'}` | {rpm_deps} | {rpm_pg_versions} |")
            
        if self.has_deb:
            # Generate PG version badges for DEB
            deb_pg_badges = []
            for pg in DEFAULT_PG:
                if str(pg) in (self.deb_pg or []):
                    deb_pg_badges.append(f'<Badge variant="green-subtle">{pg}</Badge>')
                else:
                    deb_pg_badges.append(f'<Badge variant="red-subtle">{pg}</Badge>')
            deb_pg_versions = "".join(deb_pg_badges)
            
            deb_deps = "<br /> ".join([ '`%s`'%i for i in self.deb_deps]) if self.deb_deps else "-"
            rows.append(f"| **Debian** | {format_repo_badge(self.deb_repo)} | `{self.deb_pkg or '-'}` | `{self.deb_ver or '-'}` | {deb_deps} | {deb_pg_versions} |")
        
        return "\n".join(rows) if rows else "| - | - | - | - | - | - |"
    
    def generate_availability_table(self) -> str:
        """Generate availability matrix table with merged Linux column and Badge components."""
        self.load_packages()
        
        # Build package matrix with repository information using new DEFAULT_OS format
        matrix = {}
        repo_matrix = {}
        for os in DEFAULT_OS:
            matrix[os] = {}
            repo_matrix[os] = {}
            for pg in DEFAULT_PG:
                matrix[os][pg] = ""
                repo_matrix[os][pg] = ""
        
        # Fill matrix with package versions and repository info
        for pkg in self.packages:
            # Convert package OS info to DEFAULT_OS format for matching
            pkg_os_code = getattr(pkg, 'os_code', getattr(pkg, 'os', '').split('.')[0])
            pkg_arch = normalize_arch(getattr(pkg, 'os_arch', ''))
            pkg_os_key = f"{pkg_os_code}.{pkg_arch}"
            
            if pkg_os_key in matrix and pkg.pg in matrix[pkg_os_key]:
                matrix[pkg_os_key][pkg.pg] = pkg.version
                repo_matrix[pkg_os_key][pkg.pg] = pkg.org.upper()
        
        # Generate PG version headers based on extension support
        pg_headers = []
        for pg in DEFAULT_PG:
            if str(pg) in self.pg_ver:
                pg_headers.append(f'**PG{pg}**')  # Normal text for supported versions
            else:
                pg_headers.append(f'<span className="text-red-500">**PG{pg}**</span>')  # Red for unsupported versions
        
        # Generate table with merged Linux column
        headers = ['<TooltipIconButton tooltip="Linux Distro Arch / PostgreSQL Major Version" side="top">Linux / PostgreSQL </TooltipIconButton>'] + pg_headers
        rows = [f"| {' | '.join(headers)} |"]
        rows.append(f"|{'|'.join([':-----:'] * len(headers))}|")
        
        for os in DEFAULT_OS:
            # DEFAULT_OS is now in format 'el8.x86_64', 'el8.aarch64', etc.
            linux_cell = f'`{os}`'
            
            row_data = [linux_cell]
            for pg in DEFAULT_PG:
                version = matrix[os][pg]
                repo = repo_matrix[os][pg]
                if version:
                    if repo == 'PIGSTY':
                        row_data.append(f'<Badge variant="amber-subtle">{version}</Badge>')
                    elif repo == 'PGDG':
                        row_data.append(f'<Badge variant="blue-subtle">{version}</Badge>')
                    elif repo == 'CONTRIB':
                        row_data.append(f'<Badge variant="green-subtle">{version}</Badge>')
                    else:
                        row_data.append(f'<Badge variant="purple-subtle">{version}</Badge>')

                elif self.contrib:
                    if str(pg) in self.pg_ver:
                        row_data.append('<Badge variant="green-subtle">%s</Badge>'% self.version)
                    else:
                        row_data.append('<Badge variant="red-subtle">✗</Badge>')
                else:
                    row_data.append('<Badge variant="red-subtle">✗</Badge>')
            
            rows.append(f"| {' | '.join(row_data)} |")
        
        return "\n".join(rows)
    
    def generate_download_section(self) -> str:
        """Generate download section with file tree using actual package names from database."""
        if self.contrib:
            return "This extension is built-in with PostgreSQL and does not need separate download."
        
        repo_text = format_repo_badge(self.rpm_repo or self.deb_repo or 'Unknown')
        
        section = f"""To add the required PGDG / PIGSTY upstream repository, use:

```bash tab="pig"
pig repo add pgdg -u    # add PGDG repo and update cache (leave existing repos)
pig repo add pigsty -u  # add PIGSTY repo and update cache (leave existing repos)
pig repo add pgsql -u   # add PGDG + Pigsty repo and update cache (leave existing repos)
pig repo set all -u     # set repo to all = NODE + PGSQL + INFRA  (remove existing repos)
```
```bash tab="pigsty"
./node.yml -t node_repo -e node_repo_modules=node,pgsql # -l <cluster>
```

Or download the latest packages directly:

<Files>"""

        # Load actual package data from database
        self.load_packages()
        
        # Group packages by OS/architecture with proper normalization
        pkg_by_os = {}
        for pkg in self.packages:
            # Create standardized OS key using normalize_arch for consistent matching
            os_code = getattr(pkg, 'os_code', getattr(pkg, 'os', '').split('.')[0])
            normalized_arch = normalize_arch(getattr(pkg, 'os_arch', ''))
            os_key = f"{os_code}.{normalized_arch}"
            
            if os_key not in pkg_by_os:
                pkg_by_os[os_key] = {}
            pkg_by_os[os_key][pkg.pg] = pkg
        
        
        # Generate file tree for each OS
        for os in DEFAULT_OS:
            # Parse the new DEFAULT_OS format (e.g., 'el8.x86_64')
            os_parts = os.split('.')
            if len(os_parts) != 2:
                print(f"Warning: Invalid OS format '{os}', skipping")
                continue
                
            os_name = os_parts[0]
            arch = os_parts[1]  # Already in correct format (x86_64 or aarch64)
            
            section += f"""
    <Folder name="{os_name}.{arch}">"""
            
            # Look for packages for this OS/arch combination  
            os_key = f"{os_name}.{arch}"
            found_packages = False
            
            # Try exact match, then fuzzy matching
            search_keys = [os_key] + [key for key in pkg_by_os if key.endswith(f'.{arch}') and key.startswith(os_name)]
            
            for search_key in search_keys:
                if search_key in pkg_by_os:
                    for pg in DEFAULT_PG:
                        if str(pg) in self.pg_ver and pg in pkg_by_os[search_key]:
                            pkg = pkg_by_os[search_key][pg]
                            found_packages = True
                            
                            # Use actual package data from database
                            file_name = getattr(pkg, 'file', f'{self.name}-{pkg.version}.rpm')
                            url = getattr(pkg, 'url', '#')
                            
                            # Determine icon and color based on distro and architecture
                            icon_name = "Package" if os_name.startswith(('el', 'rocky', 'alma')) else "Box"
                            icon_color = "text-emerald-500" if arch == 'x86_64' else "text-orange-500"
                            
                            section += f"""
        <a href="{url}"><File name="{file_name}" icon={{<{icon_name} className="{icon_color}" />}} /></a>"""
                    if found_packages:
                        break
            
            section += """
    </Folder>"""
        
        section += """
</Files>"""
        
        return section
    
    def generate_install_section(self) -> str:
        """Generate installation instructions."""
        if self.contrib:
            install_text = f"""Extension `{self.name}` is PostgreSQL Built-in [**Contrib**](/list/contrib) Extension which is installed along with the kernel/contrib.

[**Create**](/usage/create) this extension on PostgreSQL database with:

```sql
CREATE EXTENSION {self.name};
```"""
        else:
            install_text = f"""[**Install**](/usage/install) this extension with:

```bash tab="pig"
pig ext install {self.name}; # install by extension name, for the current active PG version
"""
            if self.pkg != self.name:
                install_text += f"""pig ext install {self.pkg}; # install via package alias, for the active PG version"""
            for pg in DEFAULT_PG:
                if str(pg) in self.pg_ver:
                    install_text += f"""
pig ext install {self.name} -v {pg};   # install for PG {pg}"""
            
            install_text += """
```"""
            
            if self.has_rpm:
                install_text += """
```bash tab="yum" """
                for pg in DEFAULT_PG:
                    if str(pg) in self.pg_ver:
                        # Fix package name without wildcards
                        if '$v' in self.rpm_pkg:
                            pkg_name = self.rpm_pkg.replace('$v', str(pg))
                        else:
                            pkg_name = self.rpm_pkg
                        install_text += f"""
dnf install {pkg_name};"""
                install_text += """
```"""
            
            if self.has_deb:
                install_text += """
```bash tab="apt" """
                for pg in DEFAULT_PG:
                    if str(pg) in self.pg_ver:
                        # Fix package name without wildcards
                        if '$v' in self.deb_pkg:
                            pkg_name = self.deb_pkg.replace('$v', str(pg))
                        else:
                            pkg_name = f"postgresql-{pg}-{self.deb_pkg}"
                        install_text += f"""
apt install {pkg_name};"""
                install_text += """
```"""
            
            install_text += f"""
```bash tab="ansible"
./pgsql.yml -t pg_ext -e '{{"pg_extensions": ["{self.pkg}"]}}' # -l <cls>
```"""

            if self.need_load:
                install_text += f"""

[**Preload**](/usage/load) this extension with:

```bash
shared_preload_libraries = '{self.name}'; # add to pg cluster config
```"""

            if self.need_ddl:
                create_cmd = f'"{self.name}"' if '-' in self.name else self.name
                cascade = ' CASCADE' if self.requires else ''
                install_text += f"""

[**Create**](/usage/create) this extension with:

```sql
CREATE EXTENSION {create_cmd}{cascade};
```"""
            else:
                install_text += f"""

Extension `{self.name}` [**does not need**](/usage/create#extensions-without-ddl) `CREATE EXTENSION` command."""
        
        return install_text
    
    def generate_stub_include(self) -> str:
        """Generate include statement for stub content if the file exists."""
        stub_path = os.path.join(STUB_DIR, f"{self.name}.md")
        if os.path.exists(stub_path):
            return f"\n<include>../../../stub/{self.name}.md</include>"
        return ""
    
    def generate_documentation(self) -> str:
        """Generate complete MDX documentation for the extension."""
        # Format template variables with improved name and package linking
        name_link = f'[`{self.name}`]({self.url})' if self.url else f'`{self.name}`'
        
        # Package linking logic: link to leading extension if pkg != name
        if self.pkg != self.name and self.pkg in LEADING_MAP:
            leading_ext = LEADING_MAP[self.pkg]
            package_link = f'[`{self.pkg}`](/ext/{leading_ext})'
        else:
            package_link = f'`{self.pkg}`'
        
        template_vars = {
            'name': self.name,
            'name_link': name_link,
            'description': self.en_desc or 'PostgreSQL Extension',
            'ext_id': self.id,
            'package': package_link,
            'category': self.category,
            'category_lower': self.category.lower(),
            'category_badge': format_category_badge(self.category),
            'license_badge': format_license_badge(self.license),
            'language': format_language_badge(self.lang, self.extra),
            'version': self.version or 'Unknown',
            'lead': self.format_bool(self.lead),
            'has_bin': self.format_bool(self.has_bin),
            'has_lib': self.format_bool(self.has_lib),
            'need_load': self.format_bool(self.need_load),
            'need_ddl': self.format_bool(self.need_ddl),
            'relocatable': self.format_bool(self.relocatable),
            'trusted': self.format_bool(self.trusted),
            'schemas': ', '.join(f'`{s}`' for s in self.schemas) if self.schemas else '-',
            'package_info': self.generate_package_info(),
            'dependencies_section': self.generate_dependencies_section(),
            'availability_table': self.generate_availability_table(),
            'download_section': self.generate_download_section(),
            'install_section': self.generate_install_section(),
            'stub_include': self.generate_stub_include()
        }
        
        return EXTENSION_TEMPLATE.format(**template_vars)
    
    def save_documentation(self):
        """Save the generated documentation to file."""
        content = self.generate_documentation()
        output_path = os.path.join(OUTPUT_DIR, f"{self.name}.mdx")
        
        # Ensure output directory exists
        #os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        #with open(output_path, 'w', encoding='utf-8') as f:
        #    f.write(content)

def build_leading_extension_map(extensions: List['Extension']) -> Dict[str, str]:
    """Build a mapping from package names to their leading extensions."""
    leading_map = {}
    for ext in extensions:
        if ext.lead and ext.pkg:  # This is a leading extension
            leading_map[ext.pkg] = ext.name
    return leading_map

def gen_extension_pages():
    """Main function to generate documentation for all extensions."""
    print("Loading extensions from database...")
    
    with CONN.cursor() as cur:
        cur.execute('SELECT * FROM ext.extension ORDER BY id')
        rows = cur.fetchall()
    
    extensions = [Extension(row) for row in rows]
    
    # Build global dependency and leading extension maps
    print("Building dependency and leading extension maps...")
    global EXT_MAP, DEP_MAP, LEADING_MAP
    LEADING_MAP = build_leading_extension_map(extensions)
    
    for ext in extensions:
        EXT_MAP[ext.name] = ext
        if ext.requires:
            for req in ext.requires:
                if req not in DEP_MAP:
                    DEP_MAP[req] = []
                DEP_MAP[req].append(ext.name)
    
    print(f"Found {len(extensions)} extensions.")
    print(f"Found {len(LEADING_MAP)} leading extensions.")
    print("Generating documentation...")
    
    for ext in extensions:
        try:
            print(f"Processing {ext.name}...")
            ext.save_documentation()
        except Exception as e:
            print(f"Error processing {ext.name}: {e}")
    
    print("Documentation generation complete!")

def gen_category_pages():
    """Generate category pages with meta.json and index.mdx for each category."""
    print("Loading extensions from database for category pages...")
    
    # Category metadata with descriptions and icons
    CATEGORY_META = {
        "TIME": {
            "description": "TimescaleDB, Versioning & Temporal Table, Crontab, Async & Background Job Scheduler",
            "icon": "Clock",
            "color": "blue"
        },
        "GIS": {
            "description": "GeoSpatial Data Types, Operators, and Indexes, Hexagonal Indexing, OGR Data FDW, GeoIP & MobilityDB",
            "icon": "Globe",
            "color": "green"
        },
        "RAG": {
            "description": "Vector Database with IVFFLAT, HNSW, DiskANN Indexes, AI & ML in SQL interface, Similarity Funcs",
            "icon": "Brain",
            "color": "purple"
        },
        "FTS": {
            "description": "ElasticSearch Alternative with BM25, 2-gram/3-gram Fuzzy Search, Zhparser & Hunspell Segregation Dicts",
            "icon": "Search",
            "color": "orange"
        },
        "OLAP": {
            "description": "DuckDB Integration with FDW & PG Lakehouse, Access Parquet from File/S3, Sharding with Citus/Partman/PlProxy",
            "icon": "ChartNoAxesCombined",
            "color": "red"
        },
        "FEAT": {
            "description": "OpenCypher with AGE, GraphQL, JsonSchema, Hints & Hypo Index, HLL, Rum, IVM, ChemRDKit, and Message Queues",
            "icon": "Sparkles",
            "color": "cyan"
        },
        "LANG": {
            "description": "Develop, Test, Package, and Deliver Stored Procedures written in various PL/Languages: Java, Js, Lua, R, Sh, PRQL",
            "icon": "BookA",
            "color": "indigo"
        },
        "TYPE": {
            "description": "Dedicate New Data Types Like: prefix, sember, uint, SIUnit, RoaringBitmap, Rational, Sphere, Hash, RRule",
            "icon": "Boxes",
            "color": "teal"
        },
        "UTIL": {
            "description": "Utilities such as send http request, perform gzip/zstd compress, send mails, Regex, ICU, encoding, docs, Encryption",
            "icon": "Wrench",
            "color": "amber"
        },
        "FUNC": {
            "description": "Function such as id generator, aggregations, sketches, vector functions, mathematical functions and digest functions",
            "icon": "Variable",
            "color": "pink"
        },
        "ADMIN": {
            "description": "Utilities for Bloat Control, DirtyRead, BufferInspect, DDL Generate, ChecksumVerify, Permission, Priority, Catalog",
            "icon": "Landmark",
            "color": "slate"
        },
        "STAT": {
            "description": "Observability Catalogs, Monitoring Metrics & Views, Statistics, Query Plans, WaitSampling, SlowLogs",
            "icon": "Activity",
            "color": "emerald"
        },
        "SEC": {
            "description": "Auditing Logs, Enforce Passwords, Keep Secrets, TDE, SM Algorithm, Login Hooks, Log Erros, Extension White List",
            "icon": "Shield",
            "color": "red"
        },
        "FDW": {
            "description": "Wrappers & Multicorn for FDW Development, Access other DBMS: MySQL, Mongo, SQLite, MSSQL, Oracle, HDFS, DB2",
            "icon": "FileInput",
            "color": "blue"
        },
        "SIM": {
            "description": "Protocol Simulation & heterogeneous DBMS Compatibility: Oracle, MSSQL, DB2, MySQL, Memcached, and Babelfish",
            "icon": "Shell",
            "color": "violet"
        },
        "ETL": {
            "description": "Logical Replication, Decoding, CDC in protobuf/JSON/Mongo format, Copy & Load & Compare Postgres Databases",
            "icon": "Truck",
            "color": "orange"
        }
    }
    
    # Load extensions from database
    with CONN.cursor() as cur:
        cur.execute('SELECT * FROM ext.extension ORDER BY category, id')
        rows = cur.fetchall()
    
    extensions = [Extension(row) for row in rows]
    
    # Group extensions by category
    category_groups = {}
    for ext in extensions:
        if ext.category not in category_groups:
            category_groups[ext.category] = []
        category_groups[ext.category].append(ext)
    
    # Ensure all 16 categories exist
    for category in CATEGORY_META.keys():
        if category not in category_groups:
            category_groups[category] = []
    
    print(f"Found {len(extensions)} extensions in {len(category_groups)} categories")
    
    # Generate category directories
    category_output_dir = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'content', 'docs', 'ext', 'cate'))
    
    for category, category_extensions in category_groups.items():
        category_dir = os.path.join(category_output_dir, category.lower())
        os.makedirs(category_dir, exist_ok=True)
        
        # Generate meta.json
        meta_data = {"pages": [f"[{ext.name}](/e/{ext.name})" for ext in category_extensions]}
        meta_path = os.path.join(category_dir, 'meta.json')
        with open(meta_path, 'w', encoding='utf-8') as f:
            import json
            json.dump(meta_data, f, indent=2, ensure_ascii=False)
        
        # Generate index.mdx
        generate_category_index_mdx(category, category_extensions, CATEGORY_META[category], category_dir)
        print(f"Generated category: {category.lower()}/ ({len(category_extensions)} extensions)")
    print("Category pages generation complete!")

def generate_category_index_mdx(category: str, extensions: List['Extension'], category_meta: dict, output_dir: str):
    """Generate index.mdx file for a category."""
    
    # Generate availability matrix for each extension
    def generate_availability_matrix(ext: 'Extension') -> str:
        """Generate compact availability matrix for extension card."""
        if ext.contrib:
            return '<div className="text-xs"><Badge variant="green-subtle">CONTRIB</Badge></div>'
        
        badges = []
        if ext.has_rpm and ext.rpm_repo:
            badges.append(f'<Badge variant="{"amber-subtle" if ext.rpm_repo == "PIGSTY" else "blue-subtle"}">{ext.rpm_repo}</Badge>')
        if ext.has_deb and ext.deb_repo:
            badges.append(f'<Badge variant="{"amber-subtle" if ext.deb_repo == "PIGSTY" else "blue-subtle"}">{ext.deb_repo}</Badge>')
        
        return f'<div className="text-xs space-x-1">{"".join(badges)}</div>' if badges else '<div className="text-xs"><Badge variant="gray-subtle">N/A</Badge></div>'
    
    # Generate extension cards
    def generate_extension_cards(extensions: List['Extension']) -> str:
        """Generate Callout-style layout for extensions with left-right split design."""
        if not extensions:
            return "<p className='text-muted-foreground'>No extensions available in this category.</p>"

        def generate_metadata_table(ext: 'Extension') -> str:
            """Generate left-side metadata table (6 rows x 3 columns)."""
            # Format RPM and DEB package names
            rpm_pkg = f'`{ext.rpm_pkg or "N/A"}`' if ext.has_rpm else '<span className="text-red-500">N/A</span>'
            deb_pkg = f'`{ext.deb_pkg or "N/A"}`' if ext.has_deb else '<span className="text-red-500">N/A</span>'
            
            # Generate individual attribute badges for each row
            load_badge = '<Badge variant="red-subtle">LOAD</Badge>' if ext.need_load else ''
            ddl_badge = '<Badge variant="blue-subtle">DDL</Badge>' if ext.need_ddl else ''
            lib_badge = '<Badge variant="green-subtle">LIB</Badge>' if ext.has_lib else ''
            bin_badge = '<Badge variant="pink-subtle">BIN</Badge>' if ext.has_bin else ''
            trust_badge = '<Badge variant="green-subtle">TRUST</Badge>' if ext.trusted else ''
            
            # Website link
            extension_cell = f'[Extension](/e/{ext.name})'
            website_cell = f'[Website]({ext.url})' if ext.url else 'N/A'
            package_cell = f'[`{ext.pkg}`](/e/{LEADING_MAP[ext.pkg]})'

            return f'''| {extension_cell} | {website_cell} | Attributes |
|:----:|:---------:|:---------:|
| Package  | {package_cell} | {load_badge} |
| RPM  | {rpm_pkg} | {ddl_badge} |
| DEB  | {deb_pkg} | {lib_badge} |
| Language | {format_language_badge(ext.lang or "N/A", ext.extra)} | {bin_badge} |
| License | {format_license_badge(ext.license or "N/A")} | {trust_badge} |'''

        def generate_availability_matrix(ext: 'Extension') -> str:
            """Generate right-side availability matrix with PG version badges."""
            # Build package matrix
            ext.load_packages()
            pkg_matrix = {}
            repo_matrix = {}
            
            # Initialize matrix for each OS
            for os in DEFAULT_OS:
                pkg_matrix[os] = {}
                repo_matrix[os] = {}
                for pg in DEFAULT_PG:
                    pkg_matrix[os][pg] = ""
                    repo_matrix[os][pg] = ""
            
            # Fill matrix with actual package data
            for pkg in ext.packages:
                pkg_os_code = getattr(pkg, 'os_code', getattr(pkg, 'os', '').split('.')[0])
                pkg_arch = normalize_arch(getattr(pkg, 'os_arch', ''))
                pkg_os_key = f"{pkg_os_code}.{pkg_arch}"
                
                if pkg_os_key in pkg_matrix and pkg.pg in pkg_matrix[pkg_os_key]:
                    pkg_matrix[pkg_os_key][pkg.pg] = pkg.version
                    repo_matrix[pkg_os_key][pkg.pg] = pkg.org.upper()
            
            # Generate matrix table
            os_arch_map = {
                'el8.x86_64': 'el8', 'el8.aarch64': 'el8',
                'el9.x86_64': 'el9', 'el9.aarch64': 'el9', 
                'd12.x86_64': 'd12', 'd12.aarch64': 'd12',
                'u22.x86_64': 'u22', 'u22.aarch64': 'u22',
                'u24.x86_64': 'u24', 'u24.aarch64': 'u24'
            }
            
            rows = []
            # Group by OS, then by architecture
            for os_base in ['el8', 'el9', 'd12', 'u22', 'u24']:
                x86_key = f"{os_base}.x86_64"
                arm_key = f"{os_base}.aarch64"
                
                x86_badges = []
                arm_badges = []
                
                for pg in DEFAULT_PG:
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
            
            header = "| OS/Arch | x86_64 | aarch64 |\n|:-----:|:---:|:---:|"
            return f"{header}\n" + "\n".join(rows)

        callouts = []
        for ext in extensions:
            title = f"{ext.name} - {ext.version or 'Unknown'}"
            description = ext.en_desc or 'No description available'
            
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
    
    # Generate table
    def generate_extension_table(extensions: List['Extension']) -> str:
        """Generate markdown table for extensions."""
        if not extensions:
            return "No extensions found."
        
        headers = ['ID', 'Extension', 'Package', 'Version', 'Description']
        header_row = '| ' + ' | '.join(headers) + ' |'
        separator_row = '|:---:|:---|:---|:---|:---|'
        
        rows = [header_row, separator_row]
        
        for ext in extensions:
            row_data = [
                str(ext.id),
                f'[`{ext.name}`](/e/{ext.name})',
                f'[`{ext.pkg}`](/e/{LEADING_MAP[ext.pkg]})',
                ext.version or 'N/A',
                ext.en_desc or 'No description'
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        return '\n'.join(rows)
    
    # Build the content
    extension_count = len(extensions)
    
    content = f'''---
title: {category}
description: "{category_meta["description"]}"
icon: {category_meta["icon"]}
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Callout }} from 'fumadocs-ui/components/callout';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck, Scale, FileCode2 }} from 'lucide-react';

{category} category contains **{extension_count}** PostgreSQL extension{'s' if extension_count != 1 else ''}.

{generate_extension_table(extensions)}

--------

{generate_extension_cards(extensions)}
'''
    
    # Write to file
    index_path = os.path.join(output_dir, 'index.mdx')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)


def gen_inventory_pages():
    pass

def main():
    gen_extension_pages()
    gen_category_pages()

if __name__ == "__main__":
    main()
