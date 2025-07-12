#!/usr/bin/env python3

import psycopg
import sqlite3
import json
import re
import io

PGURL = "postgres:///vonng"

def reload_pkg(pgurl=PGURL):
    """
    Parse repository data from pgext.repo_data and populate pgext.apt and pgext.yum tables
    """
    print("Starting package data reload...")
    
    conn = psycopg.connect(pgurl)
    cursor = conn.cursor()
    
    # Clear existing package data
    cursor.execute("TRUNCATE TABLE pgext.yum;")
    cursor.execute("TRUNCATE TABLE pgext.apt;")
    print("Cleared existing package data")
    
    # Get all repositories with binary data from pgext.repo_data
    cursor.execute("""
        SELECT rd.id, r.type, rd.data 
        FROM pgext.repo_data rd
        JOIN pgext.repository r ON rd.id = r.id
        WHERE rd.data IS NOT NULL
        ORDER BY rd.id
    """)
    repos = cursor.fetchall()
    
    yum_data = []
    apt_data = []
    
    for repo_id, repo_type, binary_data in repos:
        print(f"Processing {repo_id} ({repo_type})...")
        
        try:
            if repo_type == 'rpm':
                # Parse YUM repository data (SQLite)
                packages = parse_yum_data(binary_data)
                for package in packages:
                    yum_data.append([repo_id] + list(package))
                    
            elif repo_type == 'deb':
                # Parse APT repository data (Packages file)
                packages = parse_apt_data(binary_data.decode('utf-8'))
                for package in packages:
                    apt_data.append([repo_id] + list(package))
                    
        except Exception as e:
            print(f"Error parsing {repo_id}: {e}")
    
    # Insert YUM data
    if yum_data:
        print(f"Inserting {len(yum_data)} YUM packages...")
        cursor.executemany("""
            INSERT INTO pgext.yum VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
        """, yum_data)
    
    # Insert APT data  
    if apt_data:
        print(f"Inserting {len(apt_data)} APT packages...")
        cursor.executemany("""
            INSERT INTO pgext.apt VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, apt_data)
    
    conn.commit()
    
    # Call stored procedures to update matrix and package tables
    print("Reloading matrix and package tables...")
    cursor.execute("SELECT pgext.reload_matrix();")
    matrix_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT pgext.reload_package();")
    package_count = cursor.fetchone()[0]
    
    conn.commit()
    
    # Update matrix table with new columns: count, pkg_repo, pkg_ver
    print("Updating matrix table with package statistics...")
    cursor.execute("SELECT pgext.update_matrix();")
    matrix_stats_count = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    print(f"Package reload completed: {matrix_count} matrix entries, {package_count} packages, {matrix_stats_count} matrix stats updated")


# Note: update_matrix_stats function replaced with pgext.update_matrix() stored procedure



def parse_yum_data(binary_data):
    """Parse YUM SQLite data from binary data"""
    # Create an in-memory SQLite database
    temp_db = io.BytesIO(binary_data)
    
    # Save to temporary file since sqlite3 doesn't support BytesIO directly
    import tempfile
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(binary_data)
        temp_file.flush()
        
        conn = sqlite3.connect(temp_file.name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM packages")
        rows = cursor.fetchall()
        conn.close()
        
    return rows


def parse_apt_data(packages_content):
    """Parse APT Packages file content"""
    fixed_fields = [
        'Package', 'Version', 'Architecture', 'Size', 'Installed-Size', 'Priority', 'Section', 'Filename', 
        'SHA256', 'SHA1', 'MD5sum', 'Maintainer', 'Homepage', 'Depends', 'Source', 'Provides', 
        'Recommends', 'Suggests', 'Conflicts', 'Breaks', 'Replaces', "Enhances", "Pre-Depends", 
        'Build-Ids', 'Package-Type', 'Auto-Built-Package', 'Multi-Arch', 'Description'
    ]
    
    def parse_package_record(record):
        package_info = {}
        current_key = None
        
        for line in record.split('\n'):
            if not line.strip():
                continue
            if line[0] != ' ':
                match = re.match(r'^(.*?):\s*(.*)', line.strip())
                if match:
                    key, value = match.groups()
                    key = key.strip()
                    value = value.strip()
                    current_key = key
                    
                    if key == 'Installed-Size':
                        if not value or value == '':
                            value = 0
                        else:
                            try:
                                value = int(value) * 1024  # Convert KB to bytes
                            except ValueError:
                                value = 0
                    elif key in ['Size']:
                        try:
                            value = int(value)
                        except ValueError:
                            value = 0
                    
                    if key == 'Description':
                        package_info[key] = [value]
                    else:
                        package_info[key] = value
            elif current_key == 'Description':
                package_info[current_key].append(line.strip())
        
        if 'Description' in package_info:
            description = "\n".join(package_info['Description'])
            package_info['Description'] = description
        
        fixed_values = tuple(package_info.get(field, '') for field in fixed_fields)
        other_fields = {key: value for key, value in package_info.items()
                       if key not in fixed_fields}
        other_fields_json = json.dumps(other_fields)
        return fixed_values + (other_fields_json,)
    
    records = packages_content.split('\n\n')
    parsed_packages = []
    
    for record in records:
        if record.strip():
            package = parse_package_record(record)
            # Fix empty size values
            package = list(package)
            if package[4] == '':  # Installed-Size
                package[4] = 0
            parsed_packages.append(tuple(package))
    
    return parsed_packages


def main():
    reload_pkg()


if __name__ == "__main__":
    main()