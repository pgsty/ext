#!/usr/bin/env python3

"""
Generate license-based PostgreSQL extension list pages.
Generates content/docs/list/license.mdx and content/docs/list/license.zh.mdx
"""

import os
import sys
from collections import Counter
from typing import Dict, List

# Add the bin directory to Python path so we can import common_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_utils import (
    Config, DataLoader, TableGenerator, BadgeFormatter, 
    LICENSE_INFO, normalize_license_name, write_content, build_leading_map
)


class LicenseListGenerator:
    """Generate license-based extension list."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.extensions = []
        self.table_gen = None
    
    def generate(self):
        """Generate license list pages."""
        print("Generating license list...")
        
        # Load data
        self.extensions = self.data_loader.load_extensions()
        
        # Build leading extension map
        leading_map = build_leading_map(self.extensions)
        self.table_gen = TableGenerator(leading_map)
        
        # Generate English version
        self._generate_english_version()
        
        # Generate Chinese version
        self._generate_chinese_version()
        
        print("License list generation complete!")
    
    def _generate_english_version(self):
        """Generate English version of license list."""
        # Count extensions by license and normalize names
        license_counts = Counter()
        license_extensions_map = {}
        
        for ext in self.extensions:
            if not ext.license:
                continue
            normalized_name = normalize_license_name(ext.license)
            license_counts[normalized_name] += 1
            if normalized_name not in license_extensions_map:
                license_extensions_map[normalized_name] = []
            license_extensions_map[normalized_name].append(ext)
        
        # Local function to format license badges with in-page anchors
        def format_license_in_page(license_name: str) -> str:
            """Format license badge with in-page anchor for license list page."""
            return BadgeFormatter.format_license(license_name, is_chinese=False, in_license_page=True)
        
        # Generate summary table
        summary_rows = []
        for license_name, count in license_counts.most_common():
            info = LICENSE_INFO.get(license_name, {'url': '#', 'description': 'Open source license.'})
            summary_rows.append(f'| {format_license_in_page(license_name)} | {count} | [License Text]({info["url"]}) | {info["description"]} |')
        
        summary_table = f'''| License | Count | Reference | Description |
|:--------|:-----:|:---------:|:------------|
{chr(10).join(summary_rows)}'''
        
        # Generate license sections
        license_sections = []
        for license_name, count in license_counts.most_common():
            license_extensions = sorted(license_extensions_map[license_name], key=lambda e: e.name)
            info = LICENSE_INFO.get(license_name, {'url': '#', 'description': 'Open source license.'})
            
            section = f'''
## {license_name}

{BadgeFormatter.format_license(license_name, is_chinese=False, in_license_page=True)} <Badge icon={{<Package />}} variant="gray-subtle">{count} Extensions</Badge>

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
        
        write_content(self.config, 'license.mdx', content)
    
    def _generate_chinese_version(self):
        """Generate Chinese version of license list."""
        print("Generating Chinese license list...")
        
        # Count extensions by license and normalize names
        license_counts = Counter()
        license_extensions_map = {}
        
        for ext in self.extensions:
            if not ext.license:
                continue
            normalized_name = normalize_license_name(ext.license)
            license_counts[normalized_name] += 1
            if normalized_name not in license_extensions_map:
                license_extensions_map[normalized_name] = []
            license_extensions_map[normalized_name].append(ext)
        
        # Chinese license descriptions
        license_descriptions_zh = {
            'PostgreSQL': '基于 BSD 许可证的非常宽松的许可证，允许几乎无限制的自由使用。',
            'MIT': '允许商业使用、修改和私人使用的宽松许可证。',
            'ISC': '类似于 MIT 的宽松许可证，允许商业使用和修改。',
            'BSD 0-Clause': '等同于公共领域的许可证，对使用没有限制。',
            'BSD 2-Clause': '需要署名但允许商业使用的宽松许可证。',
            'BSD 3-Clause': '带有署名和背书限制条款的宽松许可证。',
            'Artistic': '允许在特定分发要求下修改的Copyleft许可证。',
            'Apache-2.0': '带有专利保护和署名要求的宽松许可证。',
            'MPL-2.0': '允许与专有组合的弱Copyleft许可证，文件级Copyleft。',
            'GPL-2.0': '要求衍生作品开源的强Copyleft许可证。',
            'GPL-3.0': '带有额外专利和硬件限制的强Copyleft许可证。',
            'LGPL-2.1': '允许专有应用动态链接的弱Copyleft许可证。',
            'LGPL-3.0': '带有额外专利和硬件条款的弱Copyleft许可证。',
            'AGPL-3.0': '扩展 GPL 覆盖网络分发软件的网络Copyleft许可证。',
            'Timescale': '对商业使用和分发有限制的专有许可证。'
        }
        
        # Local function to format license badges with in-page anchors for Chinese
        def format_license_in_page_zh(license_name: str) -> str:
            """Format license badge with in-page anchor for Chinese license list page."""
            return BadgeFormatter.format_license(license_name, is_chinese=True, in_license_page=True)
        
        # Generate summary table
        summary_rows = []
        for license_name, count in license_counts.most_common():
            info = LICENSE_INFO.get(license_name, {'url': '#', 'description': '开源许可证。'})
            zh_desc = license_descriptions_zh.get(license_name, '开源许可证。')
            summary_rows.append(f'| {format_license_in_page_zh(license_name)} | {count} | [许可证]({info["url"]}) | {zh_desc} |')
        
        summary_table = f'''| 许可证 | 数量 | 参考文本 | 描述 |
|:--------|:-----:|:-----:|:------------|
{chr(10).join(summary_rows)}'''
        
        # Generate license sections
        license_sections = []
        for license_name, count in license_counts.most_common():
            license_extensions = sorted(license_extensions_map[license_name], key=lambda e: e.name)
            info = LICENSE_INFO.get(license_name, {'url': '#', 'description': '开源许可证。'})
            zh_desc = license_descriptions_zh.get(license_name, '开源许可证。')
            
            section = f'''
## {license_name}

{BadgeFormatter.format_license(license_name, is_chinese=True, in_license_page=True)} <Badge icon={{<Package />}} variant="gray-subtle">{count} 个扩展</Badge>

[{license_name} 许可证]({info["url"]}) : {zh_desc}

{self.table_gen.generate_simple_table_zh(license_extensions)}
'''
            license_sections.append(section)
        
        zh_content = f'''---
title: 按许可证分类
description: 按开源许可证分类的 PostgreSQL 扩展
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

## 概览

{summary_table}

---------

{''.join(license_sections)}
'''
        
        write_content(self.config, 'license.zh.mdx', zh_content)


def main():
    """Main entry point."""
    config = Config()
    generator = LicenseListGenerator(config)
    generator.generate()


if __name__ == "__main__":
    main()