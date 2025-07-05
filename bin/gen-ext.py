#!/usr/bin/env python3

import os
import json
import psycopg2
from typing import Dict, List, Optional, Any
from datetime import datetime

# Database connection
CONN = psycopg2.connect('postgres:///vonng')

# Directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'data', 'ext'))

def parse_array(value: str) -> List[str]:
    """Parse PostgreSQL array string to Python list."""
    if isinstance(value, list):
        return value
    if not value or not value.startswith('{') or not value.endswith('}'):
        return []
    return [item.strip() for item in value[1:-1].split(',') if item.strip()]

def serialize_date(obj):
    """JSON serializer for dates."""
    from datetime import datetime, date
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def get_extension_data(extension_name: str) -> Dict[str, Any]:
    """Get extension data from pgext.extension table."""
    with CONN.cursor() as cur:
        cur.execute("""
            SELECT id, name, pkg, lead_ext, category, state, url, license, tags, version, repo, lang, 
                   contrib, lead, has_bin, has_lib, need_ddl, need_load, trusted, relocatable, schemas, 
                   pg_ver, requires, require_by, see_also, rpm_ver, rpm_repo, rpm_pkg, rpm_pg, rpm_deps, 
                   deb_ver, deb_repo, deb_pkg, deb_deps, deb_pg, source, extra, en_desc, zh_desc, comment, mtime
            FROM pgext.extension WHERE name = %s
        """, (extension_name,))
        row = cur.fetchone()
        
        if not row:
            return None
            
        # Column names matching the query above
        columns = [
            'id', 'name', 'pkg', 'lead_ext', 'category', 'state', 'url', 'license', 'tags', 'version', 'repo', 'lang',
            'contrib', 'lead', 'has_bin', 'has_lib', 'need_ddl', 'need_load', 'trusted', 'relocatable', 'schemas',
            'pg_ver', 'requires', 'require_by', 'see_also', 'rpm_ver', 'rpm_repo', 'rpm_pkg', 'rpm_pg', 'rpm_deps',
            'deb_ver', 'deb_repo', 'deb_pkg', 'deb_deps', 'deb_pg', 'source', 'extra', 'en_desc', 'zh_desc', 'comment', 'mtime'
        ]
        
        ext_data = dict(zip(columns, row))
        
        # Parse array fields
        array_fields = ['tags', 'schemas', 'pg_ver', 'requires', 'require_by', 'see_also', 'rpm_pg', 'rpm_deps', 'deb_pg', 'deb_deps']
        for field in array_fields:
            if ext_data[field]:
                ext_data[field] = parse_array(ext_data[field])
            else:
                ext_data[field] = []
        
        return ext_data

def get_siblings(pkg_name: str) -> List[str]:
    """Get all extensions in the same package (siblings)."""
    with CONN.cursor() as cur:
        cur.execute("SELECT name FROM pgext.extension WHERE pkg = %s ORDER BY name", (pkg_name,))
        return [row[0] for row in cur.fetchall()]

def get_matrix_data(pkg_name: str) -> List[Dict[str, Any]]:
    """Get matrix data for the package."""
    with CONN.cursor() as cur:
        cur.execute("""
            SELECT pg, os, type, os_code, os_arch, pkg, ext, pname, miss, hide, pkg_repo, pkg_ver, count
            FROM pgext.matrix WHERE pkg = %s ORDER BY pg DESC, os, type
        """, (pkg_name,))
        
        columns = ['pg', 'os', 'type', 'os_code', 'os_arch', 'pkg', 'ext', 'pname', 'miss', 'hide', 'pkg_repo', 'pkg_ver', 'count']
        return [dict(zip(columns, row)) for row in cur.fetchall()]

def get_availability_data(pkg_name: str) -> List[Dict[str, Any]]:
    """Get availability data for the package."""
    with CONN.cursor() as cur:
        cur.execute("""
            SELECT pkg, ext, pname, os, pg, name, ver, org, type, os_code, os_arch, repo, 
                   version, release, file, sha256, url, mirror_url, size, size_full
            FROM pgext.availability WHERE pkg = %s ORDER BY pkg, pname, os, pg
        """, (pkg_name,))
        
        columns = ['pkg', 'ext', 'pname', 'os', 'pg', 'name', 'ver', 'org', 'type', 'os_code', 'os_arch', 'repo',
                   'version', 'release', 'file', 'sha256', 'url', 'mirror_url', 'size', 'size_full']
        
        availability_data = []
        for row in cur.fetchall():
            pkg_data = dict(zip(columns, row))
            # Create compact inline JSON object with required parameters
            availability_data.append({
                "os": pkg_data['os'],
                "pg": pkg_data['pg'],
                "name": pkg_data['name'],
                "ver": pkg_data['ver'],
                "file": pkg_data['file'],
                "size": pkg_data['size'],
                "url": pkg_data['url'],
                "sha256": pkg_data['sha256']
            })
        
        return availability_data

def generate_extension_json(extension_name: str) -> None:
    """Generate JSON file for a single extension."""
    print(f"Processing extension: {extension_name}")
    
    # Get extension data
    ext_data = get_extension_data(extension_name)
    if not ext_data:
        print(f"  Warning: Extension {extension_name} not found")
        return
    
    # Get siblings
    siblings = get_siblings(ext_data['pkg'])
    
    # Get matrix data
    matrix_data = get_matrix_data(ext_data['pkg'])
    
    # Get availability data  
    availability_data = get_availability_data(ext_data['pkg'])
    
    # Build final JSON structure
    json_data = {
        **ext_data,  # All extension fields
        "siblings": siblings,
        "matrix": matrix_data,
        "package": availability_data
    }
    
    # Write to file
    output_file = os.path.join(OUTPUT_DIR, f"{extension_name}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False, default=serialize_date)
    
    print(f"  Generated: {output_file}")

def get_all_extensions() -> List[str]:
    """Get all extension names."""
    with CONN.cursor() as cur:
        cur.execute("SELECT name FROM pgext.extension ORDER BY name")
        return [row[0] for row in cur.fetchall()]

def main():
    """Main function to generate all extension JSON files."""
    print("Generating extension JSON files...")
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get all extensions
    extensions = get_all_extensions()
    print(f"Found {len(extensions)} extensions to process")
    
    # Generate JSON for each extension
    for ext_name in extensions:
        try:
            generate_extension_json(ext_name)
        except Exception as e:
            print(f"Error processing {ext_name}: {e}")
    
    print(f"JSON generation complete! Files generated in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()