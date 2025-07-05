#!/usr/bin/env python3

import requests
import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import re
from xml.etree import ElementTree as ET
import hashlib
import bz2


RawDataDir = Path(__file__).parent.parent / "data" / "raw"
RawDataDir.mkdir(parents=True, exist_ok=True)


APT_REPOS = [
    ('u24.amd.pgdg' , "https://download.postgresql.org/pub/repos/apt/dists/noble-pgdg/main/binary-amd64/Packages"    ),
    ('u24.arm.pgdg' , "https://download.postgresql.org/pub/repos/apt/dists/noble-pgdg/main/binary-arm64/Packages"    ),
    ('u22.amd.pgdg' , "https://download.postgresql.org/pub/repos/apt/dists/jammy-pgdg/main/binary-amd64/Packages"    ),
    ('u22.arm.pgdg' , "https://download.postgresql.org/pub/repos/apt/dists/jammy-pgdg/main/binary-arm64/Packages"    ),
    ('d12.amd.pgdg' , "https://download.postgresql.org/pub/repos/apt/dists/bookworm-pgdg/main/binary-arm64/Packages" ),
    ('d12.arm.pgdg' , "https://download.postgresql.org/pub/repos/apt/dists/bookworm-pgdg/main/binary-amd64/Packages" ),
    ('u24.amd.pigsty' , "https://repo.pigsty.io/apt/pgsql/noble/dists/noble/main/binary-amd64/Packages"    ),
    ('u24.arm.pigsty' , "https://repo.pigsty.io/apt/pgsql/noble/dists/noble/main/binary-arm64/Packages"    ),
    ('u22.amd.pigsty' , "https://repo.pigsty.io/apt/pgsql/jammy/dists/jammy/main/binary-amd64/Packages"    ),
    ('u22.arm.pigsty' , "https://repo.pigsty.io/apt/pgsql/jammy/dists/jammy/main/binary-arm64/Packages"    ),
    ('d12.amd.pigsty' , "https://repo.pigsty.io/apt/pgsql/bookworm/dists/bookworm/main/binary-amd64/Packages" ),
    ('d12.arm.pigsty' , "https://repo.pigsty.io/apt/pgsql/bookworm/dists/bookworm/main/binary-arm64/Packages" ),
]


YUM_REPOS = [
    ('el8.amd.pigsty' , "https://repo.pigsty.io/yum/pgsql/el8.x86_64/repodata/repomd.xml"  ),
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

    ('el8.arm.pigsty' , "https://repo.pigsty.io/yum/pgsql/el8.aarch64/repodata/repomd.xml" ),
    ('el8.arm.pgdg17' , 'https://download.postgresql.org/pub/repos/yum/17/redhat/rhel-8-aarch64/repodata/repomd.xml' ),
    ('el8.arm.pgdg16' , 'https://download.postgresql.org/pub/repos/yum/16/redhat/rhel-8-aarch64/repodata/repomd.xml' ),
    ('el8.arm.pgdg15' , 'https://download.postgresql.org/pub/repos/yum/15/redhat/rhel-8-aarch64/repodata/repomd.xml' ),
    ('el8.arm.pgdg14' , 'https://download.postgresql.org/pub/repos/yum/14/redhat/rhel-8-aarch64/repodata/repomd.xml' ),
    ('el8.arm.pgdg13' , 'https://download.postgresql.org/pub/repos/yum/13/redhat/rhel-8-aarch64/repodata/repomd.xml' ),

    ('el9.amd.pigsty' , "https://repo.pigsty.io/yum/pgsql/el9.x86_64/repodata/repomd.xml"  ),
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

    ('el9.arm.pigsty' , "https://repo.pigsty.io/yum/pgsql/el9.aarch64/repodata/repomd.xml" ),
    ('el9.arm.pgdg17' , 'https://download.postgresql.org/pub/repos/yum/17/redhat/rhel-9-aarch64/repodata/repomd.xml' ),
    ('el9.arm.pgdg16' , 'https://download.postgresql.org/pub/repos/yum/16/redhat/rhel-9-aarch64/repodata/repomd.xml' ),
    ('el9.arm.pgdg15' , 'https://download.postgresql.org/pub/repos/yum/15/redhat/rhel-9-aarch64/repodata/repomd.xml' ),
    ('el9.arm.pgdg14' , 'https://download.postgresql.org/pub/repos/yum/14/redhat/rhel-9-aarch64/repodata/repomd.xml' ),
    ('el9.arm.pgdg13' , 'https://download.postgresql.org/pub/repos/yum/13/redhat/rhel-9-aarch64/repodata/repomd.xml' ),

]

def get_apt_repo(name, url, dir=RawDataDir):
    packages_url = url
    target_file = dir / name
    
    # 检查本地文件是否存在
    if target_file.exists():
        # 获取本地文件大小
        local_size = target_file.stat().st_size
        
        # 获取远程文件信息
        try:
            response = requests.head(packages_url)
            response.raise_for_status()
            remote_size = int(response.headers.get('Content-Length', 0))
            
            # 如果文件大小相同，跳过下载
            if local_size == remote_size:
                print(f"{name} 已是最新，跳过下载")
                return
        except requests.RequestException as e:
            print(f"无法获取 {name} 的远程信息: {e}")
            return

    # 下载文件
    try:
        print(f"正在下载 {name}...")
        response = requests.get(packages_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        with open(target_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    # 打印下载进度
                    print(f"\r{name}: {downloaded_size}/{total_size} bytes ({downloaded_size/total_size:.1%})", end="")
        print(f"\n{name} 下载完成")
    except requests.RequestException as e:
        print(f"\n下载 {name} 失败: {e}")

def download_all_apt_repos(max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(get_apt_repo, name, url)
            for name, url in APT_REPOS
        ]
        for future in futures:
            future.result()



def get_yum_repo(name, url, dir=RawDataDir):
    # 第一步：下载并解析 repomd.xml
    try:
        print(f"正在获取 {name} 的 repomd.xml...")
        response = requests.get(url)
        response.raise_for_status()
        
        # 直接在内存中解析 XML
        root = ET.fromstring(response.content)
        
        # 查找 primary.sqlite.bz2 的 location 和 checksum
        namespace = {'repo': 'http://linux.duke.edu/metadata/repo'}
        primary_data = root.find(".//repo:data[@type='primary_db']", namespace)
        primary_location = primary_data.find('repo:location', namespace).attrib['href']
        primary_checksum = primary_data.find('repo:open-checksum[@type="sha256"]', namespace).text
        
        base_url = url.rsplit('/', 2)[0]  # 去掉 repodata/repomd.xml
        primary_url = f"{base_url}/{primary_location}"
    except Exception as e:
        print(f"处理 {name} 的 repomd.xml 失败: {e}")
        return

    # 目标文件路径（去掉.bz2后缀）
    target_file = dir / name
    
    # 检查本地文件是否存在且校验和匹配
    if target_file.exists():
        try:
            # 计算本地文件的sha256
            sha256_hash = hashlib.sha256()
            with open(target_file, 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            local_checksum = sha256_hash.hexdigest()
            
            if local_checksum == primary_checksum:
                print(f"{name} 已是最新，跳过下载")
                return
        except Exception as e:
            print(f"无法验证 {name} 的校验和: {e}")

    # 下载并解压 primary.sqlite.bz2
    try:
        print(f"正在下载 {name}...")
        response = requests.get(primary_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        # 使用内存中的临时文件进行解压
        with bz2.BZ2File(response.raw) as bz2_file:
            with open(target_file, 'wb') as f:
                while True:
                    chunk = bz2_file.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    # 打印下载进度
                    print(f"\r{name}: {downloaded_size}/{total_size} bytes ({downloaded_size/total_size:.1%})", end="")
        
        print(f"\n{name} 下载并解压完成")
        
        # 验证解压后的文件校验和
        sha256_hash = hashlib.sha256()
        with open(target_file, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        local_checksum = sha256_hash.hexdigest()
        
        if local_checksum != primary_checksum:
            print(f"警告：{name} 的校验和不匹配，可能下载损坏")
            target_file.unlink()  # 删除损坏的文件
            return False
        return True
        
    except requests.RequestException as e:
        print(f"\n下载 {name} 失败: {e}")
        return False
    except Exception as e:
        print(f"\n处理 {name} 失败: {e}")
        if target_file.exists():
            target_file.unlink()  # 删除可能损坏的文件
        return False

def download_all_yum_repos(max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(get_yum_repo, name, url)
            for name, url in YUM_REPOS
        ]
        for future in futures:
            future.result()


download_all_apt_repos(8)
download_all_yum_repos(8)

# get_yum_repo('pigsty.el9.arm64' , "https://repo.pigsty.cc/yum/pgsql/el9.aarch64/repodata/repomd.xml")