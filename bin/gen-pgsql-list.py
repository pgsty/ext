#!/usr/bin/env python3

"""
Generate PostgreSQL major version-based extension list pages.
Generates content/docs/list/pgsql.mdx and content/docs/list/pgsql.zh.mdx
"""

import os
import sys
from typing import Dict, List

# Add the bin directory to Python path so we can import common_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_utils import (
    Config, DataLoader, TableGenerator,
    write_content, build_leading_map
)


class PGMajorListGenerator:
    """Generate PG major version extension list."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.extensions = []
        self.table_gen = None
    
    def generate(self):
        """Generate PostgreSQL version list pages."""
        print("Generating PostgreSQL major version list...")
        
        # Load data
        self.extensions = self.data_loader.load_extensions()
        
        # Build leading extension map
        leading_map = build_leading_map(self.extensions)
        self.table_gen = TableGenerator(leading_map)
        
        # Generate English version
        self._generate_english_version()
        
        # Generate Chinese version
        self._generate_chinese_version()
        
        print("PostgreSQL version list generation complete!")
    
    def _generate_english_version(self):
        """Generate English version of PG version list."""
        pg_sections = []
        for pg in self.config.PG_VERSIONS:
            # Find extensions NOT available for this PG version
            unavailable_extensions = [ext for ext in self.extensions if str(pg) not in ext.pg_ver]
            unavailable_extensions.sort(key=lambda e: e.name)
            
            section = f'''
## PostgreSQL {pg}

Extensions **NOT available** for PostgreSQL {pg}

{self.table_gen.generate_simple_table(unavailable_extensions)}
'''
            pg_sections.append(section)
        
        content = f'''---
title: By PostgreSQL
description: PostgreSQL extensions unavailable by major version
icon: Database
full: true
---

import {{ Badge }} from '@/components/ui/badge';

{''.join(pg_sections)}
'''
        
        write_content(self.config, 'pgsql.mdx', content)
    
    def _generate_chinese_version(self):
        """Generate Chinese version of PG version list."""
        print("Generating Chinese PostgreSQL version list...")
        
        pg_sections = []
        for pg in self.config.PG_VERSIONS:
            # Find extensions NOT available for this PG version
            unavailable_extensions = [ext for ext in self.extensions if str(pg) not in ext.pg_ver]
            unavailable_extensions.sort(key=lambda e: e.name)
            
            section = f'''
## PostgreSQL {pg}

在 PostgreSQL {pg} 中 **不可用** 的扩展

{self.table_gen.generate_simple_table_zh(unavailable_extensions)}
'''
            pg_sections.append(section)
        
        zh_content = f'''---
title: 按PG大版本分类
description: 按主要版本分类不可用的 PostgreSQL 扩展
icon: Database
full: true
---

import {{ Badge }} from '@/components/ui/badge';

{''.join(pg_sections)}
'''
        
        write_content(self.config, 'pgsql.zh.mdx', zh_content)


def main():
    """Main entry point."""
    config = Config()
    generator = PGMajorListGenerator(config)
    generator.generate()


if __name__ == "__main__":
    main()