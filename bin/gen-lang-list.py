#!/usr/bin/env python3

"""
Generate language-based PostgreSQL extension list pages.
Generates content/docs/list/lang.mdx and content/docs/list/lang.zh.mdx
"""

import os
import sys
from collections import Counter
from typing import Dict, List

# Add the bin directory to Python path so we can import common_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_utils import (
    Config, DataLoader, TableGenerator, BadgeFormatter, 
    LANGUAGE_DESCRIPTIONS, write_content, build_leading_map
)


class LanguageListGenerator:
    """Generate language-based extension list."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.extensions = []
        self.table_gen = None
    
    def generate(self):
        """Generate language list pages."""
        print("Generating language list...")
        
        # Load data
        self.extensions = self.data_loader.load_extensions()
        
        # Build leading extension map
        leading_map = build_leading_map(self.extensions)
        self.table_gen = TableGenerator(leading_map)
        
        # Generate English version
        self._generate_english_version()
        
        # Generate Chinese version
        self._generate_chinese_version()
        
        print("Language list generation complete!")
    
    def _generate_english_version(self):
        """Generate English version of language list."""
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

<a href="#c"><Badge      icon={{<FileCode2 />}} variant="blue-subtle">C</Badge></a>
<a href="#c-1"><Badge    icon={{<FileCode2 />}} variant="purple-subtle">C++</Badge></a>
<a href="#rust"><Badge   icon={{<FileCode2 />}} variant="amber-subtle">Rust</Badge></a>
<a href="#java"><Badge   icon={{<FileCode2 />}} variant="pink-subtle">Java</Badge></a>
<a href="#python"><Badge icon={{<FileCode2 />}} variant="blue-subtle">Python</Badge></a>
<a href="#sql"><Badge    icon={{<FileCode2 />}} variant="green-subtle">SQL</Badge></a>
<a href="#data"><Badge   icon={{<FileCode2 />}} variant="teal-subtle">Data</Badge></a>

## Summary

{summary_table}

{''.join(language_sections)}
'''
        
        write_content(self.config, 'lang.mdx', content)
    
    def _generate_chinese_version(self):
        """Generate Chinese version of language list."""
        print("Generating Chinese language list...")
        
        # Count extensions by language
        language_counts = Counter(ext.lang for ext in self.extensions if ext.lang)
        
        # Generate summary table with Chinese descriptions
        language_descriptions_zh = {
            'C': 'C 语言， PostgreSQL 默认的扩展开发语言',
            'C++': '利用 C++ 特性和库的扩展',
            'Rust': '使用 pgrx 框架的 Rust 语言扩展',
            'Python': 'Python 语言编写的扩展',
            'SQL': '纯 SQL 扩展和函数',
            'Java': '运行在 JVM 上的扩展',
            'Data': '仅数据的扩展',
        }
        
        summary_rows = []
        for lang, count in language_counts.most_common():
            desc = language_descriptions_zh.get(lang, f'使用 {lang} 编写的扩展')
            summary_rows.append(f'| {BadgeFormatter.format_language(lang)} | {count} | {desc} |')
        
        summary_table = f'''| 语言 | 数量 | 描述 |
|:-------:|:-----:|:------------|
{chr(10).join(summary_rows)}'''
        
        # Generate language sections
        language_sections = []
        for lang, count in language_counts.most_common():
            lang_extensions = [ext for ext in self.extensions if ext.lang == lang]
            lang_extensions.sort(key=lambda e: e.name)
            
            desc = language_descriptions_zh.get(lang, f'使用 {lang} 编写的扩展')
            
            section = f'''
## {lang}

{BadgeFormatter.format_language(lang)} <Badge icon={{<Package />}} variant="gray-subtle">{count} 个扩展</Badge>

{desc}

{self.table_gen.generate_simple_table_zh(lang_extensions)}
'''
            language_sections.append(section)
        
        zh_content = f'''---
title: 按语言分类
description: 按开发语言分类的 PostgreSQL 扩展列表
icon: FileCode2
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ FileCode2, Package }} from 'lucide-react';

<a href="#c"><Badge      icon={{<FileCode2 />}} variant="blue-subtle">C</Badge></a>
<a href="#c-1"><Badge    icon={{<FileCode2 />}} variant="purple-subtle">C++</Badge></a>
<a href="#rust"><Badge   icon={{<FileCode2 />}} variant="amber-subtle">Rust</Badge></a>
<a href="#java"><Badge   icon={{<FileCode2 />}} variant="pink-subtle">Java</Badge></a>
<a href="#python"><Badge icon={{<FileCode2 />}} variant="blue-subtle">Python</Badge></a>
<a href="#sql"><Badge    icon={{<FileCode2 />}} variant="green-subtle">SQL</Badge></a>
<a href="#data"><Badge   icon={{<FileCode2 />}} variant="teal-subtle">Data</Badge></a>

## 概览

{summary_table}

{''.join(language_sections)}
'''
        
        write_content(self.config, 'lang.zh.mdx', zh_content)


def main():
    """Main entry point."""
    config = Config()
    generator = LanguageListGenerator(config)
    generator.generate()


if __name__ == "__main__":
    main()