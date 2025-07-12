#!/usr/bin/env python3

"""
Generate category-based PostgreSQL extension list pages.
Generates content/docs/list/cate.mdx and content/docs/list/cate.zh.mdx
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


class CategoryListGenerator:
    """Generate category-based extension list."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.categories = {}
        self.extensions = []
        self.table_gen = None
    
    def generate(self):
        """Generate category list pages."""
        print("Generating category list...")
        
        # Load data
        self.categories = self.data_loader.load_categories()
        self.extensions = self.data_loader.load_extensions()
        
        # Build leading extension map
        leading_map = build_leading_map(self.extensions)
        self.table_gen = TableGenerator(leading_map)
        
        # Group extensions by category
        category_groups = defaultdict(list)
        for ext in self.extensions:
            category_groups[ext.category].append(ext)
        
        # Generate English version
        self._generate_english_version(category_groups)
        
        # Generate Chinese version
        self._generate_chinese_version(category_groups)
        
        print("Category list generation complete!")
    
    def _generate_english_version(self, category_groups: Dict):
        """Generate English version of category list."""
        # Generate category overview table
        category_table_rows = []
        for category_name in self.categories.keys():
            count = len(category_groups[category_name])
            category = self.categories[category_name]
            category_badge = BadgeFormatter.format_category(category_name, self.categories)
            category_table_rows.append(f'| {category_badge} | {count} | {category.en_desc} |')
        
        category_overview_table = f'''| Category | Count | Description |
|:---------|:-----:|:------------|
{chr(10).join(category_table_rows)}'''
        
        # Generate category sections
        category_sections = []
        for category_name in self.categories.keys():
            if category_name not in category_groups:
                continue
            
            cat_extensions = sorted(category_groups[category_name], key=lambda e: e.name)
            count = len(cat_extensions)
            category = self.categories[category_name]
            
            section = f'''
## {category_name}

{category.en_desc}

{BadgeFormatter.format_category(category_name, self.categories)} <Badge variant="gray-subtle">{count} Extensions</Badge>

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
        
        write_content(self.config, 'cate.mdx', content)
    
    def _generate_chinese_version(self, category_groups: Dict):
        """Generate Chinese version of category list."""
        print("Generating Chinese category list...")
        
        # Generate Chinese category overview table
        zh_category_table_rows = []
        for category_name in self.categories.keys():
            count = len(category_groups[category_name])
            category = self.categories[category_name]
            category_badge = BadgeFormatter.format_category(category_name, self.categories)
            zh_category_table_rows.append(f'| {category_badge} | {count} | {category.zh_desc} |')
        
        zh_category_overview_table = f'''| 分类 | 数量 | 描述 |
|:---------|:-----:|:------------|
{chr(10).join(zh_category_table_rows)}'''
        
        # Generate Chinese category sections
        zh_category_sections = []
        for category_name in self.categories.keys():
            if category_name not in category_groups:
                continue
            
            cat_extensions = sorted(category_groups[category_name], key=lambda e: e.name)
            count = len(cat_extensions)
            category = self.categories[category_name]
            
            section = f'''
## {category_name}

{category.zh_desc}

{BadgeFormatter.format_category(category_name, self.categories)} <Badge variant="gray-subtle">{count} 个扩展</Badge>

{self.table_gen.generate_category_table_zh(cat_extensions)}
'''
            zh_category_sections.append(section)
        
        zh_content = f'''---
title: 按功能分类
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
        
        write_content(self.config, 'cate.zh.mdx', zh_content)


def main():
    """Main entry point."""
    config = Config()
    generator = CategoryListGenerator(config)
    generator.generate()


if __name__ == "__main__":
    main()