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
import csv
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
        self.matrix_data = None
        
    def generate(self):
        """Generate all category index pages."""
        print("Generating category index pages...")
        
        # Load data
        self.extensions = self.data_loader.load_extensions()
        self.categories = self.data_loader.load_categories()
        self.matrix_data = self._load_matrix_data()
        
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
        """Generate detailed callouts for each extension, matching the format in content/docs/cate/time/index.mdx."""
        callouts = []
        
        for ext in extensions:
            # Load extension details from data/ext/{name}.json
            ext_data = self._load_extension_data(ext.name)
            
            # Generate version info
            version = ext.version or ext_data.get('version', 'Unknown')
            
            # Generate callout
            if is_chinese:
                callout = self._generate_chinese_callout(ext, ext_data, version)
            else:
                callout = self._generate_english_callout(ext, ext_data, version)
            
            callouts.append(callout)
        
        return '\n\n'.join(callouts)
    
    def _load_matrix_data(self) -> Dict:
        """Load matrix data - no longer needed since we use individual extension data."""
        return {}
    
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
        """Generate English callout for an extension, matching time/index.mdx format."""
        # Get basic info
        website = ext_data.get('web', ext.url or '#')
        rpm_pkg = ext.rpm_pkg or f'{ext.pkg}_$v*'
        deb_pkg = ext.deb_pkg or f'postgresql-$v-{ext.pkg.replace("_", "-")}'
        description = ext.en_desc or ext.description or 'No description'
        
        # Prepare attributes for fixed positions
        load_badge = '<Badge variant="red-subtle">LOAD</Badge>' if ext.need_load else ''
        ddl_badge = '<Badge variant="blue-subtle">DDL</Badge>' if ext.need_ddl else ''
        lib_badge = '<Badge variant="green-subtle">LIB</Badge>' if ext.has_lib else ''
        trust_badge = '<Badge variant="green-subtle">TRUST</Badge>' if ext.trusted else ''
        
        # Generate OS availability matrix using extension data
        matrix_table = self._generate_availability_matrix_from_data(ext.name)
        
        return f'''<Callout title="{ext.name} - {version}">
    <p>{description}</p>
    <div className="grid grid-cols-2 gap-4"><div className="space-y-2">
            | [Extension](/e/{ext.name}) | [Website]({website}) | Attributes |
|:----:|:---------:|:---------:|
| Package  | [`{ext.pkg}`](/e/{ext.name}) | {load_badge} |
| RPM  | `{rpm_pkg}` | {ddl_badge} |
| DEB  | `{deb_pkg}` | {lib_badge} |
| Language | {BadgeFormatter.format_language(ext.lang, is_chinese=False)} | {trust_badge} |
| License | {BadgeFormatter.format_license(ext.license, is_chinese=False)} |  |
        </div>
        <div className="space-y-2">
{matrix_table}
        </div>
    </div>
</Callout>'''
    
    def _generate_chinese_callout(self, ext, ext_data: Dict, version: str) -> str:
        """Generate Chinese callout for an extension, matching time/index.mdx format."""
        # Get basic info
        website = ext_data.get('web', ext.url or '#')
        rpm_pkg = ext.rpm_pkg or f'{ext.pkg}_$v*'
        deb_pkg = ext.deb_pkg or f'postgresql-$v-{ext.pkg.replace("_", "-")}'
        description = ext.zh_desc or ext.en_desc or ext.description or '暂无描述'
        
        # Prepare attributes for fixed positions
        load_badge = '<Badge variant="red-subtle">LOAD</Badge>' if ext.need_load else ''
        ddl_badge = '<Badge variant="blue-subtle">DDL</Badge>' if ext.need_ddl else ''
        lib_badge = '<Badge variant="green-subtle">LIB</Badge>' if ext.has_lib else ''
        trust_badge = '<Badge variant="green-subtle">TRUST</Badge>' if ext.trusted else ''
        
        # Generate OS availability matrix using extension data
        matrix_table = self._generate_availability_matrix_from_data(ext.name)
        
        return f'''<Callout title="{ext.name} - {version}">
    <p>{description}</p>
    <div className="grid grid-cols-2 gap-4"><div className="space-y-2">
            | [扩展](/zh/e/{ext.name}) | [官网]({website}) | 属性 |
|:----:|:---------:|:---------:|
| 扩展包  | [`{ext.pkg}`](/zh/e/{ext.name}) | {load_badge} |
| RPM  | `{rpm_pkg}` | {ddl_badge} |
| DEB  | `{deb_pkg}` | {lib_badge} |
| 语言 | {BadgeFormatter.format_language(ext.lang, is_chinese=True)} | {trust_badge} |
| 许可证 | {BadgeFormatter.format_license(ext.license, is_chinese=True)} |  |
        </div>
        <div className="space-y-2">
{matrix_table}
        </div>
    </div>
</Callout>'''
    
    def _generate_availability_matrix_from_data(self, ext_name: str) -> str:
        """Generate availability matrix table using extension data from data/ext/{name}.json."""
        ext_data = self._load_extension_data(ext_name)
        
        # Check if this is a CONTRIB extension
        is_contrib = ext_data.get('contrib', False) or ext_data.get('repo', '').upper() == 'CONTRIB'
        
        # Generate table header
        table_lines = ["            | OS/Arch | x86_64 | aarch64 |", "|:-----:|:---:|:---:|"]
        
        for os_code in ['el8', 'el9', 'd12', 'u22', 'u24']:
            x86_badges = []
            arm_badges = []
            
            for pg_ver in ['17', '16', '15', '14', '13']:
                if is_contrib:
                    # For CONTRIB extensions, use pg_ver field to determine availability
                    pg_versions = ext_data.get('pg_ver', [])
                    if str(pg_ver) in [str(v) for v in pg_versions]:
                        x86_badges.append(f'<Badge variant="green-subtle">{pg_ver}</Badge>')
                        arm_badges.append(f'<Badge variant="green-subtle">{pg_ver}</Badge>')
                    else:
                        x86_badges.append(f'<Badge variant="red-subtle">{pg_ver}</Badge>')
                        arm_badges.append(f'<Badge variant="red-subtle">{pg_ver}</Badge>')
                else:
                    # For non-CONTRIB extensions, use matrix data
                    matrix_data = ext_data.get('matrix', [])
                    
                    # Find matching entries for this PG version and OS/arch combination
                    x86_info = self._find_matrix_entry(matrix_data, pg_ver, os_code, 'x86_64')
                    arm_info = self._find_matrix_entry(matrix_data, pg_ver, os_code, 'aarch64')
                    
                    x86_badges.append(self._get_availability_badge_from_matrix(x86_info, pg_ver))
                    arm_badges.append(self._get_availability_badge_from_matrix(arm_info, pg_ver))
            
            x86_str = ''.join(x86_badges)
            arm_str = ''.join(arm_badges)
            table_lines.append(f"| {os_code} | {x86_str} | {arm_str} |")
        
        return '\n'.join(table_lines)
    
    def _find_matrix_entry(self, matrix_data: List[Dict], pg_ver: str, os_code: str, os_arch: str) -> Dict:
        """Find matrix entry for specific PG version, OS code and architecture."""
        for entry in matrix_data:
            if (str(entry.get('pg', '')) == str(pg_ver) and 
                entry.get('os_code', '') == os_code and 
                entry.get('os_arch', '') == os_arch):
                return entry
        return {}
    
    def _get_availability_badge_from_matrix(self, matrix_entry: Dict, pg_ver: str) -> str:
        """Generate availability badge from matrix entry with repository-based colors."""
        # If no matrix entry found, treat as missing (red)
        if not matrix_entry:
            return f'<Badge variant="red-subtle">{pg_ver}</Badge>'
            
        # If hide is true, use gray
        if matrix_entry.get('hide', False):
            return f'<Badge variant="gray-subtle">{pg_ver}</Badge>'
            
        # If missing, use red
        if matrix_entry.get('miss', True):
            return f'<Badge variant="red-subtle">{pg_ver}</Badge>'
        
        # Map repository to badge color
        pkg_repo = matrix_entry.get('pkg_repo', '').lower()
        if 'pgdg' in pkg_repo:
            variant = 'blue-subtle'
        elif 'pigsty' in pkg_repo:
            variant = 'amber-subtle'  # Yellow for Pigsty
        elif 'contrib' in pkg_repo:
            variant = 'green-subtle'
        else:
            variant = 'blue-subtle'  # Default to blue for unknown repos
        
        return f'<Badge variant="{variant}">{pg_ver}</Badge>'
    
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