#!/usr/bin/env python3

"""
Generate individual category index pages with detailed extension information.
Extracts and processes extension data to create category-specific pages
in content/docs/cate/{category}/ directories.
Generates both English and Chinese versions with extension tables and detailed Callouts.
"""

import os
import sys
import json
from collections import defaultdict
from typing import Dict, List

# Add the bin directory to Python path so we can import common_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_utils import (
    Config, DataLoader, TableGenerator, BadgeFormatter,
    write_content, build_leading_map
)


class CategoryIndexGenerator:
    """Generate individual category index pages."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.extensions = []
        self.categories = {}
        self.table_gen = None
        self.badge_formatter = BadgeFormatter()
        
    def generate(self):
        """Generate all category index pages."""
        print("Generating category index pages...")
        
        # Load data
        self.extensions = self.data_loader.load_extensions()
        self.categories = self.data_loader.load_categories()
        
        # Build leading extension map
        leading_map = build_leading_map(self.extensions)
        self.table_gen = TableGenerator(leading_map)
        
        # Group extensions by category
        category_groups = defaultdict(list)
        for ext in self.extensions:
            category_groups[ext.category].append(ext)
        
        # Generate a page for each category
        for category_code, category_obj in self.categories.items():
            if category_code not in category_groups:
                print(f"Warning: No extensions found for category {category_code}")
                continue
            
            cat_extensions = sorted(category_groups[category_code], key=lambda e: e.id)
            self._generate_category_page(category_code, category_obj, cat_extensions)
        
        print("Category index generation complete!")
    
    def _generate_category_page(self, category_code: str, category_obj, extensions: List):
        """Generate both English and Chinese versions of a category page."""
        count = len(extensions)
        
        # Sort extensions by ID
        sorted_extensions = sorted(extensions, key=lambda e: e.id)
        
        # Generate extension table (English)
        extension_table_en = self.table_gen.generate_category_table(sorted_extensions)
        
        # Generate extension table (Chinese)
        extension_table_zh = self.table_gen.generate_category_table_zh(sorted_extensions)
        
        # Generate detailed callouts for each extension
        callouts_en = self._generate_extension_callouts(sorted_extensions, is_chinese=False)
        callouts_zh = self._generate_extension_callouts(sorted_extensions, is_chinese=True)
        
        # Generate meta.json files for navigation
        self._generate_meta_json_files(category_code, sorted_extensions)
        
        # English version
        en_content = f'''---
title: {category_code}
description: "{category_obj.en_desc}"
icon: {category_obj.icon1}
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Callout }} from 'fumadocs-ui/components/callout';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck, Scale, FileCode2 }} from 'lucide-react';

{category_code} category contains **{count}** PostgreSQL extensions.

{extension_table_en}

--------

{callouts_en}
'''
        
        # Chinese version  
        zh_content = f'''---
title: {category_code}
description: "{category_obj.zh_desc}"
icon: {category_obj.icon1}
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Callout }} from 'fumadocs-ui/components/callout';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck, Scale, FileCode2 }} from 'lucide-react';

{category_code} 分类包含 **{count}** 个 PostgreSQL 扩展。

{extension_table_zh}

--------

{callouts_zh}
'''
        
        # Write category pages (go up from list to docs, then to cate)
        content_docs_dir = os.path.dirname(self.config.OUTPUT_DIR)  # Go from list to docs
        category_dir = os.path.join(content_docs_dir, 'cate', category_code.lower())
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
    
    def _generate_extension_callouts(self, extensions: List, is_chinese: bool = False) -> str:
        """Generate detailed callouts for each extension."""
        callouts = []
        
        for ext in extensions:
            # Load extension details from data/ext/{name}.json
            ext_data = self._load_extension_data(ext.name)
            
            # Generate version info
            version = ext_data.get('version', 'Unknown') if ext_data else 'Unknown'
            
            # Generate callout
            if is_chinese:
                callout = self._generate_chinese_callout(ext, ext_data, version)
            else:
                callout = self._generate_english_callout(ext, ext_data, version)
            
            callouts.append(callout)
        
        return '\n\n'.join(callouts)
    
    def _load_extension_data(self, ext_name: str) -> Dict:
        """Load extension data from JSON file."""
        ext_file = os.path.join(self.config.DATA_DIR, 'ext', f'{ext_name}.json')
        if os.path.exists(ext_file):
            try:
                with open(ext_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}
    
    def _generate_english_callout(self, ext, ext_data: Dict, version: str) -> str:
        """Generate English callout for an extension."""
        # Basic info table
        website = ext_data.get('web', '#')
        rpm_pkg = ext_data.get('rpm', f'{ext.pkg}_$v*')
        deb_pkg = ext_data.get('deb', f'postgresql-$v-{ext.pkg.replace("_", "-")}')
        
        # Attributes badges
        attributes = []
        if ext_data.get('need_load'):
            attributes.append('<Badge variant="red-subtle">LOAD</Badge>')
        if ext_data.get('need_ddl'):
            attributes.append('<Badge variant="blue-subtle">DDL</Badge>')
        if ext_data.get('need_lib'):
            attributes.append('<Badge variant="green-subtle">LIB</Badge>')
        if ext_data.get('trusted'):
            attributes.append('<Badge variant="green-subtle">TRUST</Badge>')
        
        attributes_str = ' '.join(attributes) if attributes else ''
        
        # OS availability matrix
        matrix_table = self._generate_availability_matrix(ext_data.get('matrix', []))
        
        return f'''<Callout title="{ext.name} - {version}">
    <p>{ext.description}</p>
    <div className="grid grid-cols-2 gap-4"><div className="space-y-2">
            | [Extension](/e/{ext.name}) | [Website]({website}) | Attributes |
|:----:|:---------:|:---------:|
| Package  | [`{ext.pkg}`](/e/{ext.name}) | {attributes_str} |
| RPM  | `{rpm_pkg}` | |
| DEB  | `{deb_pkg}` | |
| Language | {BadgeFormatter.format_language(ext.lang, is_chinese=False)} | |
| License | {BadgeFormatter.format_license(ext.license, is_chinese=False)} | |
        </div>
        <div className="space-y-2">
{matrix_table}
        </div>
    </div>
</Callout>'''
    
    def _generate_chinese_callout(self, ext, ext_data: Dict, version: str) -> str:
        """Generate Chinese callout for an extension."""
        # Basic info table
        website = ext_data.get('web', '#')
        rpm_pkg = ext_data.get('rpm', f'{ext.pkg}_$v*')
        deb_pkg = ext_data.get('deb', f'postgresql-$v-{ext.pkg.replace("_", "-")}')
        
        # Attributes badges
        attributes = []
        if ext_data.get('need_load'):
            attributes.append('<Badge variant="red-subtle">LOAD</Badge>')
        if ext_data.get('need_ddl'):
            attributes.append('<Badge variant="blue-subtle">DDL</Badge>')
        if ext_data.get('need_lib'):
            attributes.append('<Badge variant="green-subtle">LIB</Badge>')
        if ext_data.get('trusted'):
            attributes.append('<Badge variant="green-subtle">TRUST</Badge>')
        
        attributes_str = ' '.join(attributes) if attributes else ''
        
        # OS availability matrix
        matrix_table = self._generate_availability_matrix(ext_data.get('matrix', []))
        
        return f'''<Callout title="{ext.name} - {version}">
    <p>{ext.description}</p>
    <div className="grid grid-cols-2 gap-4"><div className="space-y-2">
            | [扩展](/zh/e/{ext.name}) | [官网]({website}) | 属性 |
|:----:|:---------:|:---------:|
| 扩展包  | [`{ext.pkg}`](/zh/e/{ext.name}) | {attributes_str} |
| RPM  | `{rpm_pkg}` | |
| DEB  | `{deb_pkg}` | |
| 语言 | {BadgeFormatter.format_language(ext.lang, is_chinese=True)} | |
| 许可证 | {BadgeFormatter.format_license(ext.license, is_chinese=True)} | |
        </div>
        <div className="space-y-2">
{matrix_table}
        </div>
    </div>
</Callout>'''
    
    def _generate_availability_matrix(self, matrix: List[Dict]) -> str:
        """Generate availability matrix table for OS/Arch combinations."""
        if not matrix:
            return "            | OS/Arch | x86_64 | aarch64 |\n|:-----:|:---:|:---:|\n| N/A | N/A | N/A |"
        
        # Group by OS
        os_data = {}
        for entry in matrix:
            os_code = entry.get('os_code', 'unknown')
            arch = entry.get('os_arch', 'unknown')
            
            if os_code not in os_data:
                os_data[os_code] = {}
            
            # Determine availability badges for each PG version
            badges = []
            for pg_ver in ['17', '16', '15', '14', '13']:
                if entry.get('miss', False) or entry.get('hide', False):
                    badges.append(f'<Badge variant="red-subtle">{pg_ver}</Badge>')
                elif entry.get('warn', False):
                    badges.append(f'<Badge variant="amber-subtle">{pg_ver}</Badge>')
                else:
                    badges.append(f'<Badge variant="blue-subtle">{pg_ver}</Badge>')
            
            os_data[os_code][arch] = ''.join(badges)
        
        # Generate table
        table_lines = ["            | OS/Arch | x86_64 | aarch64 |", "|:-----:|:---:|:---:|"]
        
        for os_code in ['el8', 'el9', 'd12', 'u22', 'u24']:
            if os_code in os_data:
                x86_badges = os_data[os_code].get('x86_64', 'N/A')
                arm_badges = os_data[os_code].get('aarch64', 'N/A')
                table_lines.append(f"| {os_code} | {x86_badges} | {arm_badges} |")
        
        return '\n'.join(table_lines)
    
    def _generate_meta_json_files(self, category_code: str, extensions: List):
        """Generate meta.json and meta.zh.json files for a category."""
        
        # Create category directory if it doesn't exist
        content_docs_dir = os.path.dirname(self.config.OUTPUT_DIR)  # Go from list to docs
        category_dir = os.path.join(content_docs_dir, 'cate', category_code.lower())
        os.makedirs(category_dir, exist_ok=True)
        
        # Sort extensions by ID for meta.json files
        sorted_extensions = sorted(extensions, key=lambda e: e.id)
        
        # Generate pages array for English
        en_pages = []
        zh_pages = []
        
        for ext in sorted_extensions:
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
    generator = CategoryIndexGenerator(config)
    generator.generate()


if __name__ == "__main__":
    main()