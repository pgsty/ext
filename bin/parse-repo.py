#!/usr/bin/env python3
import requests
import re
import os
import json
from pathlib import Path
import psycopg
import sqlite3

PGURL = "postgres:///vonng"
RawDataDir = Path(__file__).parent.parent / "data" / "raw"
RawDataDir.mkdir(parents=True, exist_ok=True)


APT_REPOS = [
    ('u24.amd.pgdg' , "https://mirrors.tuna.tsinghua.edu.cn/postgresql/repos/apt/dists/noble-pgdg/main/binary-amd64/Packages"    ),
    ('u24.arm.pgdg' , "https://mirrors.tuna.tsinghua.edu.cn/postgresql/repos/apt/dists/noble-pgdg/main/binary-arm64/Packages"    ),
    ('u22.amd.pgdg' , "https://mirrors.tuna.tsinghua.edu.cn/postgresql/repos/apt/dists/jammy-pgdg/main/binary-amd64/Packages"    ),
    ('u22.arm.pgdg' , "https://mirrors.tuna.tsinghua.edu.cn/postgresql/repos/apt/dists/jammy-pgdg/main/binary-arm64/Packages"    ),
    ('d12.amd.pgdg' , "https://mirrors.tuna.tsinghua.edu.cn/postgresql/repos/apt/dists/bookworm-pgdg/main/binary-amd64/Packages" ),
    ('d12.arm.pgdg' , "https://mirrors.tuna.tsinghua.edu.cn/postgresql/repos/apt/dists/bookworm-pgdg/main/binary-arm64/Packages" ),
    ('u24.amd.pigsty' , "https://repo.pigsty.cc/apt/pgsql/noble/dists/noble/main/binary-amd64/Packages"    ),
    ('u24.arm.pigsty' , "https://repo.pigsty.cc/apt/pgsql/noble/dists/noble/main/binary-arm64/Packages"    ),
    ('u22.amd.pigsty' , "https://repo.pigsty.cc/apt/pgsql/jammy/dists/jammy/main/binary-amd64/Packages"    ),
    ('u22.arm.pigsty' , "https://repo.pigsty.cc/apt/pgsql/jammy/dists/jammy/main/binary-arm64/Packages"    ),
    ('d12.amd.pigsty' , "https://repo.pigsty.cc/apt/pgsql/bookworm/dists/bookworm/main/binary-amd64/Packages" ),
    ('d12.arm.pigsty' , "https://repo.pigsty.cc/apt/pgsql/bookworm/dists/bookworm/main/binary-arm64/Packages" ),
]


YUM_REPOS = [
    ('el8.amd.pigsty' , "https://repo.pigsty.cc/yum/pgsql/el8.x86_64/repodata/repomd.xml"  ),
    ('el8.amd.pgdg17' , 'https://download.postgresql.org/pub/repos/yum/17/redhat/rhel-8-x86_64/repodata/repomd.xml'  ),
    ('el8.amd.pgdg16' , 'https://download.postgresql.org/pub/repos/yum/16/redhat/rhel-8-x86_64/repodata/repomd.xml'  ),
    ('el8.amd.pgdg15' , 'https://download.postgresql.org/pub/repos/yum/15/redhat/rhel-8-x86_64/repodata/repomd.xml'  ),
    ('el8.amd.pgdg14' , 'https://download.postgresql.org/pub/repos/yum/14/redhat/rhel-8-x86_64/repodata/repomd.xml'  ),
    ('el8.amd.pgdg13' , 'https://download.postgresql.org/pub/repos/yum/13/redhat/rhel-8-x86_64/repodata/repomd.xml'  ),
    ('el8.amd.pgnf17' , 'https://download.postgresql.org/pub/repos/yum/non-free/17/redhat/rhel-8-x86_64/repodata/repomd.xml'  ),
    ('el8.amd.pgnf16' , 'https://download.postgresql.org/pub/repos/yum/non-free/16/redhat/rhel-8-x86_64/repodata/repomd.xml'  ),
    ('el8.amd.pgnf15' , 'https://download.postgresql.org/pub/repos/yum/non-free/15/redhat/rhel-8-x86_64/repodata/repomd.xml'  ),
    ('el8.amd.pgnf14' , 'https://download.postgresql.org/pub/repos/yum/non-free/14/redhat/rhel-8-x86_64/repodata/repomd.xml'  ),
    ('el8.amd.pgnf13' , 'https://download.postgresql.org/pub/repos/yum/non-free/13/redhat/rhel-8-x86_64/repodata/repomd.xml'  ),

    ('el8.arm.pigsty' , "https://repo.pigsty.cc/yum/pgsql/el8.aarch64/repodata/repomd.xml" ),
    ('el8.arm.pgdg17' , 'https://download.postgresql.org/pub/repos/yum/17/redhat/rhel-8-aarch64/repodata/repomd.xml' ),
    ('el8.arm.pgdg16' , 'https://download.postgresql.org/pub/repos/yum/16/redhat/rhel-8-aarch64/repodata/repomd.xml' ),
    ('el8.arm.pgdg15' , 'https://download.postgresql.org/pub/repos/yum/15/redhat/rhel-8-aarch64/repodata/repomd.xml' ),
    ('el8.arm.pgdg14' , 'https://download.postgresql.org/pub/repos/yum/14/redhat/rhel-8-aarch64/repodata/repomd.xml' ),
    ('el8.arm.pgdg13' , 'https://download.postgresql.org/pub/repos/yum/13/redhat/rhel-8-aarch64/repodata/repomd.xml' ),

    ('el9.amd.pigsty' , "https://repo.pigsty.cc/yum/pgsql/el9.x86_64/repodata/repomd.xml"  ),
    ('el9.amd.pgdg17' , 'https://download.postgresql.org/pub/repos/yum/17/redhat/rhel-9-x86_64/repodata/repomd.xml'  ),
    ('el9.amd.pgdg16' , 'https://download.postgresql.org/pub/repos/yum/16/redhat/rhel-9-x86_64/repodata/repomd.xml'  ),
    ('el9.amd.pgdg15' , 'https://download.postgresql.org/pub/repos/yum/15/redhat/rhel-9-x86_64/repodata/repomd.xml'  ),
    ('el9.amd.pgdg14' , 'https://download.postgresql.org/pub/repos/yum/14/redhat/rhel-9-x86_64/repodata/repomd.xml'  ),
    ('el9.amd.pgdg13' , 'https://download.postgresql.org/pub/repos/yum/13/redhat/rhel-9-x86_64/repodata/repomd.xml'  ),
    ('el9.amd.pgnf17' , 'https://download.postgresql.org/pub/repos/yum/non-free/17/redhat/rhel-9-x86_64/repodata/repomd.xml'  ),
    ('el9.amd.pgnf16' , 'https://download.postgresql.org/pub/repos/yum/non-free/16/redhat/rhel-9-x86_64/repodata/repomd.xml'  ),
    ('el9.amd.pgnf15' , 'https://download.postgresql.org/pub/repos/yum/non-free/15/redhat/rhel-9-x86_64/repodata/repomd.xml'  ),
    ('el9.amd.pgnf14' , 'https://download.postgresql.org/pub/repos/yum/non-free/14/redhat/rhel-9-x86_64/repodata/repomd.xml'  ),
    ('el9.amd.pgnf13' , 'https://download.postgresql.org/pub/repos/yum/non-free/13/redhat/rhel-9-x86_64/repodata/repomd.xml'  ),

    ('el9.arm.pigsty' , "https://repo.pigsty.cc/yum/pgsql/el9.aarch64/repodata/repomd.xml" ),
    ('el9.arm.pgdg17' , 'https://download.postgresql.org/pub/repos/yum/17/redhat/rhel-9-aarch64/repodata/repomd.xml' ),
    ('el9.arm.pgdg16' , 'https://download.postgresql.org/pub/repos/yum/16/redhat/rhel-9-aarch64/repodata/repomd.xml' ),
    ('el9.arm.pgdg15' , 'https://download.postgresql.org/pub/repos/yum/15/redhat/rhel-9-aarch64/repodata/repomd.xml' ),
    ('el9.arm.pgdg14' , 'https://download.postgresql.org/pub/repos/yum/14/redhat/rhel-9-aarch64/repodata/repomd.xml' ),
    ('el9.arm.pgdg13' , 'https://download.postgresql.org/pub/repos/yum/13/redhat/rhel-9-aarch64/repodata/repomd.xml' ),

]

def parse_yum_repo(name):
    sqlite_file = RawDataDir / f"{name}"
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM packages")
    rows = cursor.fetchall()
    conn.close()
    return rows

def merge_yum_repo():
    results = []
    for name, url in YUM_REPOS:
        rows = parse_yum_repo(name)
        rows = [ [name] + list(row) for row in rows]
        results.extend(rows)
    return results

# insert merged result to postgres

def insert_yum_data(data):
    conn = psycopg.connect(PGURL)
    cursor = conn.cursor()
    print("truncate ext.yum")
    cursor.execute("TRUNCATE TABLE ext.yum;")
    print("load %d rows into ext.yum" % len(data))
    cursor.executemany("""INSERT INTO ext.yum VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s,%s)""", data)
    conn.commit()
    print("load complete")

def process_yum_data():
    data = merge_yum_repo()
    insert_yum_data(data)



def parse_package_record(record):
    fixed_fields = [
        'Package', 'Version', 'Architecture', 'Size',  'Installed-Size', 'Priority', 'Section', 'Filename', 'SHA256', 'SHA1', 'MD5sum', 'Maintainer', 
        'Homepage', 'Depends', 'Source', 'Provides', 'Recommends', 'Suggests','Conflicts', 'Breaks', 'Replaces', "Enhances", "Pre-Depends", 
        'Build-Ids', 'Package-Type', 'Auto-Built-Package', 'Multi-Arch', 'Description'
    ]
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

def parse_apt_repo(name):
    pkg_file = RawDataDir / f"{name}"
    records = open(pkg_file).read().split('\n\n')

    parsed_packages = []
    for record in records:
        if record.strip():
            package = parse_package_record(record)
            parsed_packages.append(package)

    return parsed_packages

def merge_apt_repo():
    results = []
    for name, url in APT_REPOS:
        rows = parse_apt_repo(name)
        rows = [[name] + list(row) for row in rows]
        for row in rows:
            if row[5] == '':
                row[5] = 0
            results.append(row)
    return results

def insert_apt_data(data):
    conn = psycopg.connect(PGURL)
    cursor = conn.cursor()
    print("truncate ext.apt")
    cursor.execute("TRUNCATE TABLE ext.apt;")
    print("load %d rows into ext.apt" % len(data))
    cursor.executemany("""
        INSERT INTO ext.apt VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, data)
    conn.commit()
    print("load complete")

def process_apt_data():
    data = merge_apt_repo()
    insert_apt_data(data)

# Replace the test call with the actual processing function
process_yum_data()
process_apt_data()  # Add this line
