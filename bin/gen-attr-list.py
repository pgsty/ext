#!/usr/bin/env python3

"""
Generate attribute-based PostgreSQL extension list pages.
Generates content/docs/list/attr.mdx and content/docs/list/attr.zh.mdx
"""

import os
import sys
from collections import defaultdict
from typing import Dict, List

# Add the bin directory to Python path so we can import common_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_utils import (
    Config, DataLoader, TableGenerator,
    write_content, build_leading_map
)


class AttributeListGenerator:
    """Generate attribute-based extension list."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.extensions = []
        self.table_gen = None
    
    def generate(self):
        """Generate attribute list pages."""
        print("Generating attribute list...")
        
        # Load data
        self.extensions = self.data_loader.load_extensions()
        
        # Build leading extension map
        leading_map = build_leading_map(self.extensions)
        self.table_gen = TableGenerator(leading_map)
        
        # Generate English version
        self._generate_english_version()
        
        # Generate Chinese version
        self._generate_chinese_version()
        
        print("Attribute list generation complete!")
    
    def _generate_english_version(self):
        """Generate English version of attribute list."""
        # Generate sections
        need_loading_section = self._generate_need_loading_section()
        without_ddl_section = self._generate_without_ddl_section()
        has_dependency_section = self._generate_has_dependency_section()
        multiple_extension_section = self._generate_multiple_extension_section()
        
        content = f'''---
title: By Attribute
description: PostgreSQL extensions organized by Attribute
icon: Shapes
full: true
---

import {{ Badge }} from '@/components/ui/badge';

------

{need_loading_section}

------

{without_ddl_section}

------

{has_dependency_section}

------

{multiple_extension_section}
'''
        
        write_content(self.config, 'attr.mdx', content)
    
    def _generate_chinese_version(self):
        """Generate Chinese version of attribute list."""
        print("Generating Chinese attribute list...")
        
        # Generate sections
        need_loading_section = self._generate_need_loading_section_zh()
        without_ddl_section = self._generate_without_ddl_section_zh()
        has_dependency_section = self._generate_has_dependency_section_zh()
        multiple_extension_section = self._generate_multiple_extension_section_zh()
        
        zh_content = f'''---
title: 按属性分类
description: 按属性分类的 PostgreSQL 扩展列表
icon: Shapes
full: true
---

import {{ Badge }} from '@/components/ui/badge';

------

{need_loading_section}

------

{without_ddl_section}

------

{has_dependency_section}

------

{multiple_extension_section}
'''
        
        write_content(self.config, 'attr.zh.mdx', zh_content)
    
    def _generate_need_loading_section(self) -> str:
        """Generate Need Loading section."""
        need_loading_extensions = [ext for ext in self.extensions if ext.need_load]
        need_loading_extensions.sort(key=lambda e: e.name)
        
        return f'''## Need Loading

Extensions that require dynamic loading in [`shared_preload_libraries`](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-SHARED-PRELOAD-LIBRARIES) to work properly.

{self.table_gen.generate_simple_table(need_loading_extensions)}'''
    
    def _generate_need_loading_section_zh(self) -> str:
        """Generate Chinese Need Loading section."""
        need_loading_extensions = [ext for ext in self.extensions if ext.need_load]
        need_loading_extensions.sort(key=lambda e: e.name)
        
        return f'''## 需要加载的扩展

需要在 [`shared_preload_libraries`](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-SHARED-PRELOAD-LIBRARIES) 中动态加载才能正常工作的扩展。

{self.table_gen.generate_simple_table_zh(need_loading_extensions)}'''
    
    def _generate_without_ddl_section(self) -> str:
        """Generate Without DDL section."""
        without_ddl_extensions = [ext for ext in self.extensions if not ext.need_ddl]
        without_ddl_extensions.sort(key=lambda e: e.name)
        
        return f'''## Without DDL

These extensions do not have DDL, so you don't need to run `CREATE EXTENSION` to use them.

{self.table_gen.generate_simple_table(without_ddl_extensions)}'''
    
    def _generate_without_ddl_section_zh(self) -> str:
        """Generate Chinese Without DDL section."""
        without_ddl_extensions = [ext for ext in self.extensions if not ext.need_ddl]
        without_ddl_extensions.sort(key=lambda e: e.name)
        
        return f'''## 无需 DDL 的扩展

这些扩展没有 DDL 语句，所以你不需要（也不能）运行 `CREATE EXTENSION` 来创建它们。

{self.table_gen.generate_simple_table_zh(without_ddl_extensions)}'''
    
    def _generate_has_dependency_section(self) -> str:
        """Generate Has Dependency section."""
        has_dependency_extensions = [ext for ext in self.extensions if ext.requires]
        has_dependency_extensions.sort(key=lambda e: e.name)
        
        if not has_dependency_extensions:
            return '''## Has Dependency

Extensions that have dependencies on other extensions.

No extensions with dependencies found.'''
        
        # Generate dependency table
        headers = ['Extension', 'Dependencies']
        rows = [self.table_gen._format_table_header(headers, [':---', ':---'])]
        
        for ext in has_dependency_extensions:
            dependency_links = []
            for dep in ext.requires:
                # Try to find the dependency extension to create proper links
                dep_ext = next((e for e in self.extensions if e.name == dep), None)
                if dep_ext:
                    dependency_links.append(f'[`{dep}`](/e/{dep})')
                else:
                    dependency_links.append(f'`{dep}`')
            
            dependencies_cell = ', '.join(dependency_links)
            row_data = [
                f'[`{ext.name}`](/e/{ext.name})',
                dependencies_cell
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        dependency_table = '\n'.join(rows)
        
        return f'''## Has Dependency

Extensions that have dependencies on other extensions.

{dependency_table}'''
    
    def _generate_has_dependency_section_zh(self) -> str:
        """Generate Chinese Has Dependency section."""
        has_dependency_extensions = [ext for ext in self.extensions if ext.requires]
        has_dependency_extensions.sort(key=lambda e: e.name)
        
        if not has_dependency_extensions:
            return '''## 有依赖的扩展

依赖其他扩展的扩展。
'''
        
        # Generate dependency table
        headers = ['扩展', '依赖']
        rows = [self.table_gen._format_table_header(headers, [':---', ':---'])]
        
        for ext in has_dependency_extensions:
            dependency_links = []
            for dep in ext.requires:
                # Try to find the dependency extension to create proper links
                dep_ext = next((e for e in self.extensions if e.name == dep), None)
                if dep_ext:
                    dependency_links.append(f'[`{dep}`](/zh/e/{dep})')
                else:
                    dependency_links.append(f'`{dep}`')
            
            dependencies_cell = ', '.join(dependency_links)
            row_data = [
                f'[`{ext.name}`](/zh/e/{ext.name})',
                dependencies_cell
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        dependency_table = '\n'.join(rows)
        
        return f'''## 有依赖

依赖其他扩展的扩展。

{dependency_table}'''
    
    def _generate_multiple_extension_section(self) -> str:
        """Generate Multiple Extension section."""
        # Group extensions by package
        package_extensions = defaultdict(list)
        for ext in self.extensions:
            if ext.pkg:
                package_extensions[ext.pkg].append(ext)
        
        # Find packages with multiple extensions
        multi_packages = {pkg: exts for pkg, exts in package_extensions.items() if len(exts) > 1}
        
        if not multi_packages:
            return '''## Multiple Extension

These packages contain multiple extensions simultaneously:

No packages with multiple extensions found.'''
        
        # Generate multiple extension table
        headers = ['Package', 'Extensions']
        rows = [self.table_gen._format_table_header(headers, [':---', ':---'])]
        
        # Sort packages by the leading extension ID
        sorted_packages = []
        for pkg, exts in multi_packages.items():
            # Sort extensions within package: leading extension first, then by ID
            sorted_exts = sorted(exts, key=lambda e: (not e.lead, e.id))
            sorted_packages.append((pkg, sorted_exts))
        
        # Sort packages by the ID of their leading extension
        sorted_packages.sort(key=lambda item: item[1][0].id)
        
        for pkg, exts in sorted_packages:
            extension_links = []
            for ext in exts:
                extension_links.append(f'[`{ext.name}`](/e/{ext.name})')
            
            extensions_cell = ', '.join(extension_links)
            leading_ext = next((e for e in exts if e.lead), exts[0])
            
            row_data = [
                f'[`{pkg}`](/e/{leading_ext.name})',
                extensions_cell
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        multiple_table = '\n'.join(rows)
        
        return f'''## Multiple Extension

These packages contain multiple extensions simultaneously:

{multiple_table}'''
    
    def _generate_multiple_extension_section_zh(self) -> str:
        """Generate Chinese Multiple Extension section."""
        # Group extensions by package
        package_extensions = defaultdict(list)
        for ext in self.extensions:
            if ext.pkg:
                package_extensions[ext.pkg].append(ext)
        
        # Find packages with multiple extensions
        multi_packages = {pkg: exts for pkg, exts in package_extensions.items() if len(exts) > 1}
        
        if not multi_packages:
            return '''## 一包多扩展

一个扩展包同时包含多个扩展的列表：

未找到包含多个扩展的包。'''
        
        # Generate multiple extension table
        headers = ['软件包', '扩展名']
        rows = [self.table_gen._format_table_header(headers, [':---', ':---'])]
        
        # Sort packages by the leading extension ID
        sorted_packages = []
        for pkg, exts in multi_packages.items():
            # Sort extensions within package: leading extension first, then by ID
            sorted_exts = sorted(exts, key=lambda e: (not e.lead, e.id))
            sorted_packages.append((pkg, sorted_exts))
        
        # Sort packages by the ID of their leading extension
        sorted_packages.sort(key=lambda item: item[1][0].id)
        
        for pkg, exts in sorted_packages:
            extension_links = []
            for ext in exts:
                extension_links.append(f'[`{ext.name}`](/zh/e/{ext.name})')
            
            extensions_cell = ', '.join(extension_links)
            leading_ext = next((e for e in exts if e.lead), exts[0])
            
            row_data = [
                f'[`{pkg}`](/zh/e/{leading_ext.name})',
                extensions_cell
            ]
            rows.append('| ' + ' | '.join(row_data) + ' |')
        
        multiple_table = '\n'.join(rows)
        
        return f'''## 多扩展

同时包含多个扩展的包：

{multiple_table}'''


def main():
    """Main entry point."""
    config = Config()
    generator = AttributeListGenerator(config)
    generator.generate()


if __name__ == "__main__":
    main()