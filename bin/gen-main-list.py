#!/usr/bin/env python3

"""
Generate main extension index pages.
Generates content/docs/list/index.mdx and content/docs/list/index.zh.mdx
"""

import os
import sys
from collections import defaultdict
from typing import Dict, List

# Add the bin directory to Python path so we can import common_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_utils import (
    Config, DataLoader, TableGenerator, BadgeFormatter,
    write_content, build_leading_map
)


class MainIndexGenerator:
    """Generate main extension index."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.categories = {}
        self.extensions = []
        self.table_gen = None
    
    def generate(self):
        """Generate main index pages."""
        print("Generating main extension index...")
        
        # Load data
        self.categories = self.data_loader.load_categories()
        self.extensions = self.data_loader.load_extensions()
        
        # Build leading extension map
        leading_map = build_leading_map(self.extensions)
        self.table_gen = TableGenerator(leading_map)
        
        # Generate English version
        self._generate_english_version()
        
        # Generate Chinese version
        self._generate_chinese_version()
        
        print("Main extension index generation complete!")
    
    def _generate_english_version(self):
        """Generate English version of main index."""
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
        for category_name in self.categories.keys():
            cat_extensions = [ext for ext in self.extensions if ext.category == category_name]
            if not cat_extensions:
                continue
                
            cat_extensions.sort(key=lambda e: e.name)
            extension_badges = [f'[`{ext.name}`](/e/{ext.name})' for ext in cat_extensions]
            category_badge = BadgeFormatter.format_category(category_name, self.categories)
            extensions_row = f'''| {category_badge} | {' '.join(extension_badges)} |'''
            extensions_content.append(extensions_row)
        
        extensions_table = f'''| Category | Extensions |
|:--------:|:-----------|
{chr(10).join(extensions_content)}'''
        
        content = f'''---
title: Extension
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
        
        write_content(self.config, 'index.mdx', content)
    
    def _generate_chinese_version(self):
        """Generate Chinese version of main index."""
        print("Generating Chinese main extension index...")
        
        catalog_summary = f'''扩展目录中共有 **{len(self.extensions)}** 个 PostgreSQL 扩展'''

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
        statistics_table = f'''| 发行版 | 总计 | PGDG | PIGSTY | CONTRIB | OTHER | MISS | {pg_cols} |
| -------------- |:----:|:----:|:----:|:----:|:----:|:----:|{':----:|' * len(self.config.PG_VERSIONS)}
| EL | {el_stats['all']} | {el_stats['PGDG']} | {el_stats['PIGSTY']} | {el_stats['CONTRIB']} | {el_stats['OTHER']} | {el_stats['MISS']} | {' | '.join([str(el_pg_stats[f'PG{pg}']) for pg in self.config.PG_VERSIONS])} |
| Debian | {debian_stats['all']} | {debian_stats['PGDG']} | {debian_stats['PIGSTY']} | {debian_stats['CONTRIB']} | {debian_stats['OTHER']} | {debian_stats['MISS']} | {' | '.join([str(debian_pg_stats[f'PG{pg}']) for pg in self.config.PG_VERSIONS])} |'''

        # Generate extensions by category
        extensions_content = []
        for category_name in self.categories.keys():
            cat_extensions = [ext for ext in self.extensions if ext.category == category_name]
            if not cat_extensions:
                continue
                
            cat_extensions.sort(key=lambda e: e.name)
            extension_badges = [f'[`{ext.name}`](/zh/e/{ext.name})' for ext in cat_extensions]
            category_badge = BadgeFormatter.format_category(category_name, self.categories, is_chinese=True)
            extensions_row = f'''| {category_badge} | {' '.join(extension_badges)} |'''
            extensions_content.append(extensions_row)
        
        extensions_table = f'''| 分类 | 扩展 |
|:--------:|:-----------|
{chr(10).join(extensions_content)}'''
        
        zh_content = f'''---
title: 扩展列表
description: 可用的 PostgreSQL 扩展列表
icon: BookText
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck }} from 'lucide-react';

{catalog_summary}

## 统计

{statistics_table}

-------

## 分类

{extensions_table}

------

## 源码

此目录在 [Apache License 2.0](https://github.com/pgsty/ext/blob/main/LICENSE) 许可下开源，由 [PGSTY](https://github.com/pgsty) 团队维护。

您可以在 [github.com/pgsty/extension/data/extension.csv](https://github.com/pgsty/ext/blob/main/data/extension.csv) 找到原始 CSV 数据文件

扩展目录的源代码仓库地址：https://github.com/pgsty/extension



'''
        
        write_content(self.config, 'index.zh.mdx', zh_content)
    
    def _update_platform_stats(self, ext, stats: Dict, pg_stats: Dict, platform: str):
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


def main():
    """Main entry point."""
    config = Config()
    generator = MainIndexGenerator(config)
    generator.generate()


if __name__ == "__main__":
    main()