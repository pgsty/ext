#!/usr/bin/env python3

"""
Generate Linux distribution-based PostgreSQL extension list pages.
Generates content/docs/list/linux.mdx and content/docs/list/linux.zh.mdx
"""

import os
import sys
import csv
from collections import defaultdict
from typing import Dict, List, Set
from dataclasses import dataclass

# Add the bin directory to Python path so we can import common_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_utils import (
    Config, DataLoader, TableGenerator, OS_DESCRIPTIONS,
    write_content, build_leading_map
)


@dataclass
class Package:
    """Represents a package in the matrix data."""
    pg: int
    os: str
    type: str
    os_code: str
    os_arch: str
    pkg: str
    ext: str
    pname: str
    miss: bool
    hide: bool
    pkg_repo: str
    pkg_ver: str
    count: int


class LinuxListGenerator:
    """Generate Linux distribution-based extension list."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.extensions = []
        self.packages = []
        self.table_gen = None
    
    def generate(self):
        """Generate Linux distribution list pages."""
        print("Generating Linux distribution list...")
        
        # Load data
        self.extensions = self.data_loader.load_extensions()
        self.packages = self._load_packages()
        
        # Build leading extension map
        leading_map = build_leading_map(self.extensions)
        self.table_gen = TableGenerator(leading_map)
        
        # Generate English version
        self._generate_english_version()
        
        # Generate Chinese version
        self._generate_chinese_version()
        
        print("Linux distribution list generation complete!")
    
    def _load_packages(self) -> List[Package]:
        """Load package data from matrix.csv."""
        packages = []
        csv_path = os.path.join(self.config.DATA_DIR, 'matrix.csv')
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                package = Package(
                    pg=int(row['pg']),
                    os=row['os'],
                    type=row['type'],
                    os_code=row['os_code'],
                    os_arch=row['os_arch'],
                    pkg=row['pkg'],
                    ext=row['ext'],
                    pname=row['pname'],
                    miss=row['miss'].lower() == 't',
                    hide=row['hide'].lower() == 't',
                    pkg_repo=row['pkg_repo'],
                    pkg_ver=row['pkg_ver'],
                    count=int(row['count'])
                )
                packages.append(package)
        
        print(f"Loaded {len(packages)} package entries.")
        return packages
    
    def _get_available_packages_by_os(self) -> Dict[str, Set[str]]:
        """Group available packages by OS."""
        os_groups = defaultdict(set)
        for pkg in self.packages:
            if not pkg.miss:  # Only count non-missing packages
                os_key = f"{pkg.os_code}.{pkg.os_arch}"
                os_groups[os_key].add(pkg.pkg)
        return os_groups
    
    def _generate_english_version(self):
        """Generate English version of Linux distribution list."""
        # Group packages by OS
        os_groups = self._get_available_packages_by_os()
        
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
        
        write_content(self.config, 'linux.mdx', content)
    
    def _generate_chinese_version(self):
        """Generate Chinese version of Linux distribution list."""
        print("Generating Chinese Linux distribution list...")
        
        # Group packages by OS
        os_groups = self._get_available_packages_by_os()
        
        # Chinese OS descriptions
        os_descriptions_zh = {
            'el8': 'Enterprise Linux 8 (RHEL 8, CentOS 8, Rocky 8, Alma 8)',
            'el9': 'Enterprise Linux 9 (RHEL 9, CentOS 9, Rocky 9, Alma 9)',
            'd12': 'Debian 12 (Bookworm)',
            'u22': 'Ubuntu 22.04 LTS (Jammy)',
            'u24': 'Ubuntu 24.04 LTS (Noble)'
        }
        
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

{os_descriptions_zh[os_base]}

<Badge variant="blue-subtle">x86_64</Badge> <Badge variant="gray-subtle">{len(x86_packages)} 个包</Badge>

<Badge variant="orange-subtle">aarch64</Badge> <Badge variant="gray-subtle">{len(arm_packages)} 个包</Badge>

<Badge variant="green-subtle">总计</Badge> <Badge variant="gray-subtle">{len(available_extensions)} 个扩展</Badge>

'''
            os_sections.append(section)

        zh_content = f'''---
title: 按 Linux 系统分类
description: PostgreSQL 扩展在各 Linux 发行版上的可用性
icon: Server
full: true
---

import {{ Badge }} from '@/components/ui/badge';

{''.join(os_sections)}
'''
        
        write_content(self.config, 'linux.zh.mdx', zh_content)




def main():
    """Main entry point."""
    config = Config()
    generator = LinuxListGenerator(config)
    generator.generate()


if __name__ == "__main__":
    main()