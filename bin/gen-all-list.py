#!/usr/bin/env python3

"""
Generate all extension list pages.
Master script that calls all individual list generators.
"""

import os
import sys
import time

# Add the bin directory to Python path so we can import other generators
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all list generators using importlib to handle hyphenated module names
import importlib

def import_generator(module_file, class_name):
    """Import generator class from module file."""
    # Import using the actual file name  
    import importlib.util
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    module_path = os.path.join(script_dir, f"{module_file}.py")
    
    spec = importlib.util.spec_from_file_location(module_file, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return getattr(module, class_name)

from common_utils import Config


def main():
    """Generate all extension list pages."""
    print("=" * 70)
    print("PostgreSQL Extension List Generator")
    print("=" * 70)
    
    start_time = time.time()
    config = Config()
    
    # List of all generators with their descriptions  
    generators = [
        ("gen-main-list", "MainIndexGenerator", "Main Extension Index"),
        ("gen-cate-list", "CategoryListGenerator", "Category-based Lists"),
        ("gen-cate-index", "CategoryIndexGenerator", "Individual Category Pages"),
        ("gen-lang-list", "LanguageListGenerator", "Language-based Lists"),
        ("gen-repo-list", "RepoListGenerator", "Repository-based Lists"), 
        ("gen-linux-list", "LinuxListGenerator", "Linux Distribution Lists"),
        ("gen-pgsql-list", "PGMajorListGenerator", "PostgreSQL Version Lists"),
        ("gen-attr-list", "AttributeListGenerator", "Attribute-based Lists"),
        ("gen-lic-list", "LicenseListGenerator", "License-based Lists"),
    ]
    
    # Generate all lists
    total_generators = len(generators)
    for i, (module_name, class_name, description) in enumerate(generators, 1):
        print(f"\n[{i}/{total_generators}] {description}")
        print("-" * 50)
        
        try:
            generator_class = import_generator(module_name, class_name)
            generator = generator_class(config)
            generator.generate()
            print(f"✓ {description} generated successfully")
        except Exception as e:
            print(f"✗ Error generating {description}: {e}")
            sys.exit(1)
    
    # Summary
    end_time = time.time()
    elapsed = end_time - start_time
    
    print("\n" + "=" * 70)
    print("Generation Summary")
    print("=" * 70)
    print(f"Total generators: {total_generators}")
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print("All extension list pages generated successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()