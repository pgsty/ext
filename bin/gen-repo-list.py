#!/usr/bin/env python3

"""
Generate repository-based PostgreSQL extension list pages.
Generates content/docs/list/repo.mdx and content/docs/list/repo.zh.mdx
"""

import os
import sys
from typing import Dict, List

# Add the bin directory to Python path so we can import common_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_utils import (
    Config, DataLoader, TableGenerator, BadgeFormatter,
    write_content, build_leading_map
)


class RepoListGenerator:
    """Generate repository-based extension list."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.categories = {}
        self.extensions = []
        self.table_gen = None
    
    def generate(self):
        """Generate repository list pages."""
        print("Generating repository list...")
        
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
        
        print("Repository list generation complete!")
    
    def _categorize_extensions(self):
        """Categorize extensions by availability."""
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
        
        return contrib_extensions, both_extensions, el_only_extensions, debian_only_extensions
    
    def _generate_english_version(self):
        """Generate English version of repository list."""
        contrib_extensions, both_extensions, el_only_extensions, debian_only_extensions = self._categorize_extensions()
        
        # Generate content sections
        contrib_table = self.table_gen.generate_simple_table(contrib_extensions)
        both_table = self.table_gen.generate_repo_table(both_extensions, self.categories)
        el_only_table = self.table_gen.generate_repo_table(el_only_extensions, self.categories)
        debian_only_table = self.table_gen.generate_repo_table(debian_only_extensions, self.categories)
        
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
        
        write_content(self.config, 'repo.mdx', content)
    
    def _generate_chinese_version(self):
        """Generate Chinese version of repository list."""
        print("Generating Chinese repository list...")
        
        contrib_extensions, both_extensions, el_only_extensions, debian_only_extensions = self._categorize_extensions()
        
        # Generate content sections (using Chinese table generators)
        contrib_table = self.table_gen.generate_simple_table_zh(contrib_extensions)
        
        # For repo tables, we need to create a Chinese version
        both_table = self._generate_repo_table_zh(both_extensions)
        el_only_table = self._generate_repo_table_zh(el_only_extensions)
        debian_only_table = self._generate_repo_table_zh(debian_only_extensions)
        
        # Generate summary
        total_extensions = len(self.extensions)
        summary_text = f'''总共有 **{total_extensions}** 个 PostgreSQL 扩展：**{len(contrib_extensions)}** 个 CONTRIB 扩展，**{len(both_extensions)}** 个在 EL 和 Debian 平台上都可用，**{len(el_only_extensions)}** 个仅在 EL 平台上可用，**{len(debian_only_extensions)}** 个仅在 Debian 平台上可用。'''
        
        # Generate summary table
        summary_table = f'''| 条目 | 总计 | [CONTRIB](#contrib) | [都支持](#both) | [仅 EL](#el) | [仅 Debian](#debian) |
|:-----:|:---:|:-------------------:|:-------------:|:--------------:|:----------------------:|
| 数量 | {total_extensions} | {len(contrib_extensions)} | {len(both_extensions)} | {len(el_only_extensions)} | {len(debian_only_extensions)} |'''
        
        zh_content = f'''---
title: 按来源仓库分类
description: 按仓库来源组织的 PostgreSQL 扩展
icon: Warehouse
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck }} from 'lucide-react';

{summary_text}

{summary_table}

## CONTRIB

PostgreSQL 核心发行版自带的扩展。共有 **{len(contrib_extensions)}** 个 contrib 扩展。

{contrib_table}

## BOTH

**{len(both_extensions)}** 个非 contrib 扩展在 EL 和 Debian 平台上都可用。

{both_table}

## EL

**{len(el_only_extensions)}** 个非 contrib 扩展仅在 EL 平台上可用。

{el_only_table}

## Debian

**{len(debian_only_extensions)}** 个非 contrib 扩展仅在 Debian 平台上可用。

{debian_only_table}
'''
        
        write_content(self.config, 'repo.zh.mdx', zh_content)
    
    def _generate_repo_table_zh(self, extensions: List) -> str:
        """Generate Chinese version of repo table."""
        if not extensions:
            return "未找到扩展。"
        
        headers = ['ID', '名称', '分类', 'RPM', 'DEB', '描述']
        rows = [self.table_gen._format_table_header(headers, [':---:',':---',':---',':---:',':---:',':---'])]
        
        for ext in extensions:
            rpm_badge = BadgeFormatter.format_repo(ext.rpm_repo) if ext.rpm_repo else '-'
            deb_badge = BadgeFormatter.format_repo(ext.deb_repo) if ext.deb_repo else '-'
            category_badge = BadgeFormatter.format_category(ext.category, self.categories) if ext.category else '-'
            
            row_data = [
                str(ext.id),
                f'[`{ext.name}`](/zh/e/{ext.name})',
                category_badge,
                rpm_badge,
                deb_badge,
                ext.zh_desc or ext.en_desc or '暂无描述'
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        return '\n'.join(rows)


def main():
    """Main entry point."""
    config = Config()
    generator = RepoListGenerator(config)
    generator.generate()


if __name__ == "__main__":
    main()