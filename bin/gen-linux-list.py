#!/usr/bin/env python3

"""
Generate Linux distribution-based PostgreSQL extension list pages.
Analyzes extension availability from data/ext/ JSON files to identify
missing or problematic extensions across Linux distributions.
Generates content/docs/list/linux.mdx and content/docs/list/linux.zh.mdx
"""

import os
import sys
import json
from collections import defaultdict
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

# Add the bin directory to Python path so we can import common_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_utils import (
    Config, DataLoader, TableGenerator,
    write_content, build_leading_map
)


@dataclass
class ExtensionAvailability:
    """Represents extension availability status on a Linux distribution."""
    name: str
    pkg: str
    missing_platforms: List[str]
    available_platforms: List[str]
    is_completely_missing: bool
    is_partially_missing: bool


class LinuxListGenerator:
    """Generate Linux distribution-based extension list."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.extensions = []
        self.table_gen = None
        
        # Linux distribution platform mapping (10 total platforms)
        self.all_platforms = [
            'el8.x86_64', 'el8.aarch64',
            'el9.x86_64', 'el9.aarch64', 
            'd12.x86_64', 'd12.aarch64',
            'u22.x86_64', 'u22.aarch64',
            'u24.x86_64', 'u24.aarch64'
        ]
        
        self.platform_descriptions = {
            'el8.x86_64': 'Enterprise Linux 8 (x86_64)',
            'el8.aarch64': 'Enterprise Linux 8 (aarch64)',
            'el9.x86_64': 'Enterprise Linux 9 (x86_64)',
            'el9.aarch64': 'Enterprise Linux 9 (aarch64)',
            'd12.x86_64': 'Debian 12 (x86_64)',
            'd12.aarch64': 'Debian 12 (aarch64)',
            'u22.x86_64': 'Ubuntu 22.04 LTS (x86_64)',
            'u22.aarch64': 'Ubuntu 22.04 LTS (aarch64)',
            'u24.x86_64': 'Ubuntu 24.04 LTS (x86_64)',
            'u24.aarch64': 'Ubuntu 24.04 LTS (aarch64)'
        }
        
        # PostgreSQL versions to check
        self.pg_versions = ['18', '17', '16', '15', '14']
    
    def generate(self):
        """Generate Linux distribution list pages."""
        print("Generating Linux distribution availability analysis...")
        
        # Load extension data
        self.extensions = self.data_loader.load_extensions()
        
        # Build leading extension map
        leading_map = build_leading_map(self.extensions)
        self.table_gen = TableGenerator(leading_map)
        
        # Analyze availability across distributions
        distro_analysis = self._analyze_linux_availability()
        
        # Generate English version
        self._generate_english_version(distro_analysis)
        
        # Generate Chinese version
        self._generate_chinese_version(distro_analysis)
        
        print("Linux distribution analysis complete!")
    
    def _load_extension_matrix_data(self) -> Dict[str, List[Dict]]:
        """Load extension availability data from JSON files in data/ext/."""
        ext_dir = os.path.join(self.config.DATA_DIR, 'ext')
        if not os.path.exists(ext_dir):
            print(f"Warning: {ext_dir} not found")
            return {}
        
        extension_data = {}
        
        for filename in os.listdir(ext_dir):
            if not filename.endswith('.json'):
                continue
                
            ext_name = filename[:-5]  # Remove .json suffix
            filepath = os.path.join(ext_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'matrix' in data:
                        extension_data[ext_name] = {
                            'matrix': data['matrix'],
                            'pkg': data.get('pkg', ext_name)
                        }
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not read {filepath}: {e}")
                continue
                
        print(f"Loaded matrix data for {len(extension_data)} extensions")
        return extension_data
        
    def _analyze_linux_availability(self) -> Dict[str, List]:
        """Analyze extension availability across Linux platforms, excluding Contrib extensions."""
        extension_data = self._load_extension_matrix_data()
        
        # Filter out Contrib extensions
        filtered_extensions = []
        for ext in self.extensions:
            if ext.repo != 'CONTRIB':  # Exclude contrib extensions
                if ext.name in extension_data:
                    filtered_extensions.append(ext)
        
        platform_analysis = {}
        
        for platform in self.all_platforms:
            missing_or_flawed = []
            
            for ext in filtered_extensions:
                ext_data = extension_data[ext.name]
                matrix = ext_data['matrix']
                
                # Find matrix entry for this platform
                platform_entry = None
                for entry in matrix:
                    if f"{entry.get('os_code')}.{entry.get('os_arch')}" == platform:
                        platform_entry = entry
                        break
                
                # Check if extension is missing or has issues on this platform
                is_problematic = False
                availability_status = {}
                
                if not platform_entry:
                    # No entry found - completely missing
                    is_problematic = True
                    for pg_ver in self.pg_versions:
                        availability_status[pg_ver] = 'missing'
                else:
                    # Check for each PostgreSQL version
                    for pg_ver in self.pg_versions:
                        if platform_entry.get('miss', False) or platform_entry.get('hide', False):
                            availability_status[pg_ver] = 'missing'
                            is_problematic = True
                        elif platform_entry.get('warn', False):
                            availability_status[pg_ver] = 'warning'
                            is_problematic = True
                        else:
                            availability_status[pg_ver] = 'available'
                
                if is_problematic:
                    missing_or_flawed.append({
                        'extension': ext,
                        'availability': availability_status
                    })
            
            platform_analysis[platform] = sorted(missing_or_flawed, key=lambda x: x['extension'].id)
        
        return platform_analysis
    
    def _generate_english_version(self, platform_analysis: Dict[str, List]):
        """Generate English version of Linux distribution list."""
        
        # Generate platform sections
        platform_sections = []
        for platform in self.all_platforms:
            if platform not in platform_analysis:
                continue
                
            problematic_exts = platform_analysis[platform]
            if not problematic_exts:
                continue  # Skip platforms with no issues
            
            description = self.platform_descriptions[platform]
            count = len(problematic_exts)
            
            # Generate table for problematic extensions
            table_lines = ['| Extension | Package | 18 | 17 | 16 | 15 | 14 |',
                          '|:----------|:--------|:--:|:--:|:--:|:--:|:--:|']
            
            for item in problematic_exts:
                ext = item['extension']
                availability = item['availability']
                
                # Generate badge for each PostgreSQL version
                version_badges = []
                for pg_ver in self.pg_versions:
                    status = availability[pg_ver]
                    if status == 'missing':
                        version_badges.append('<Badge variant="red-subtle">✗</Badge>')
                    elif status == 'warning':
                        version_badges.append('<Badge variant="amber-subtle">⚠</Badge>')
                    else:
                        version_badges.append('<Badge variant="blue-subtle">✓</Badge>')
                
                table_lines.append(f'| [`{ext.name}`](/e/{ext.name}) | [`{ext.pkg}`](/e/{ext.name}) | {" | ".join(version_badges)} |')
            
            table = '\n'.join(table_lines)
            
            section = f'''
## {platform.upper()}

{description}

<Badge variant="red-subtle">Issues Found</Badge> <Badge variant="gray-subtle">{count} Extensions</Badge>

{table}

'''
            
            platform_sections.append(section)

        content = f'''---
title: By Linux Distribution
description: PostgreSQL extensions with availability issues on Linux platforms
icon: Server
full: true
---

import {{ Badge }} from '@/components/ui/badge';

This page lists PostgreSQL extensions that have availability issues on specific Linux distributions and architectures. Extensions are analyzed across 10 platform combinations (5 distributions × 2 architectures).

**Platform Status Legend:**
- <Badge variant="blue-subtle">✓</Badge> Available
- <Badge variant="amber-subtle">⚠</Badge> Available with warnings  
- <Badge variant="red-subtle">✗</Badge> Missing or hidden

{''.join(platform_sections)}
'''
        
        write_content(self.config, 'linux.mdx', content)
    
    def _generate_chinese_version(self, platform_analysis: Dict[str, List]):
        """Generate Chinese version of Linux distribution list."""
        print("Generating Chinese Linux distribution list...")
        
        # Platform descriptions in Chinese
        platform_descriptions_zh = {
            'el8.x86_64': 'Enterprise Linux 8 (x86_64)',
            'el8.aarch64': 'Enterprise Linux 8 (aarch64)',
            'el9.x86_64': 'Enterprise Linux 9 (x86_64)',
            'el9.aarch64': 'Enterprise Linux 9 (aarch64)',
            'd12.x86_64': 'Debian 12 (x86_64)',
            'd12.aarch64': 'Debian 12 (aarch64)',
            'u22.x86_64': 'Ubuntu 22.04 LTS (x86_64)',
            'u22.aarch64': 'Ubuntu 22.04 LTS (aarch64)',
            'u24.x86_64': 'Ubuntu 24.04 LTS (x86_64)',
            'u24.aarch64': 'Ubuntu 24.04 LTS (aarch64)'
        }
        
        # Generate platform sections
        platform_sections = []
        for platform in self.all_platforms:
            if platform not in platform_analysis:
                continue
                
            problematic_exts = platform_analysis[platform]
            if not problematic_exts:
                continue  # Skip platforms with no issues
            
            description = platform_descriptions_zh[platform]
            count = len(problematic_exts)
            
            # Generate table for problematic extensions
            table_lines = ['| 扩展 | 扩展包 | 18 | 17 | 16 | 15 | 14 |',
                          '|:-----|:-------|:--:|:--:|:--:|:--:|:--:|']
            
            for item in problematic_exts:
                ext = item['extension']
                availability = item['availability']
                
                # Generate badge for each PostgreSQL version
                version_badges = []
                for pg_ver in self.pg_versions:
                    status = availability[pg_ver]
                    if status == 'missing':
                        version_badges.append('<Badge variant="red-subtle">✗</Badge>')
                    elif status == 'warning':
                        version_badges.append('<Badge variant="amber-subtle">⚠</Badge>')
                    else:
                        version_badges.append('<Badge variant="blue-subtle">✓</Badge>')
                
                table_lines.append(f'| [`{ext.name}`](/zh/e/{ext.name}) | [`{ext.pkg}`](/zh/e/{ext.name}) | {" | ".join(version_badges)} |')
            
            table = '\n'.join(table_lines)
            
            section = f'''
## {platform.upper()}

{description}

<Badge variant="red-subtle">发现问题</Badge> <Badge variant="gray-subtle">{count} 个扩展</Badge>

{table}

'''
            
            platform_sections.append(section)

        zh_content = f'''---
title: 按 Linux 发行版分类
description: 在特定 Linux 平台上存在可用性问题的 PostgreSQL 扩展
icon: Server
full: true
---

import {{ Badge }} from '@/components/ui/badge';

本页面列出了在特定 Linux 发行版和架构上存在可用性问题的 PostgreSQL 扩展。扩展在 10 个平台组合（5 个发行版 × 2 个架构）上进行分析。

**平台状态图例：**
- <Badge variant="blue-subtle">✓</Badge> 可用
- <Badge variant="amber-subtle">⚠</Badge> 可用但有警告
- <Badge variant="red-subtle">✗</Badge> 缺失或隐藏

{''.join(platform_sections)}
'''
        
        write_content(self.config, 'linux.zh.mdx', zh_content)


def main():
    """Main entry point."""
    config = Config()
    generator = LinuxListGenerator(config)
    generator.generate()


if __name__ == "__main__":
    main()