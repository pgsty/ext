#!/usr/bin/env python3

import requests
import psycopg
import sqlite3
import json
import re
import bz2
import hashlib
from xml.etree import ElementTree as ET
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import io

PGURL = "postgres:///vonng"

def reload_repo(pgurl=PGURL, max_workers=4):
    """
    Download repository metadata and store binary data to pgext.repo_data
    Uses HTTP caching headers (etag, size, last-modified) to avoid redundant downloads
    """
    print("Starting repository reload...")

    conn = psycopg.connect(pgurl)
    cursor = conn.cursor()

    # Get all repositories with their metadata URLs and existing cache data
    cursor.execute("""
                   SELECT r.id, r.default_meta, r.type, rd.etag, rd.size, rd.last_modified, rd.extra
                   FROM pgext.repository r
                            LEFT JOIN pgext.repo_data rd ON r.id = rd.id
                   WHERE r.default_meta IS NOT NULL
                   ORDER BY r.id
                   """)
    repos = cursor.fetchall()

    def download_repo_data(repo_info):
        repo_id, metadata_url, repo_type, existing_etag, existing_size, existing_last_modified, existing_extra = repo_info
        existing_extra = existing_extra or {}

        print(f"Processing {repo_id} ({repo_type})...")

        try:
            # Prepare headers for conditional requests
            headers = {}
            if existing_etag:
                headers['If-None-Match'] = existing_etag
            if existing_last_modified:
                headers['If-Modified-Since'] = existing_last_modified.strftime('%a, %d %b %Y %H:%M:%S GMT')

            # Make conditional request first
            response = requests.head(metadata_url, headers=headers, timeout=30)

            # Check if content has been modified
            if response.status_code == 304:
                print(f"{repo_id}: Not modified (304), skipping download")
                return
            elif response.status_code != 200:
                print(f"{repo_id}: Error {response.status_code}")
                return

            # Check content-length for additional validation
            remote_size = response.headers.get('Content-Length')
            remote_etag = response.headers.get('ETag')

            if (existing_size and remote_size and int(remote_size) == existing_size and
                    existing_etag and remote_etag and existing_etag == remote_etag):
                print(f"{repo_id}: Same size and etag, skipping download")
                return

            # Download the actual data
            if repo_type == 'deb':
                # APT repository - download Packages file directly
                response = requests.get(metadata_url, timeout=60)
                response.raise_for_status()
                binary_data = response.content

            elif repo_type == 'rpm':
                # YUM repository - download and parse repomd.xml, then get primary.sqlite.bz2
                response = requests.get(metadata_url, timeout=60)
                response.raise_for_status()

                # Parse repomd.xml to find primary.sqlite.bz2
                root = ET.fromstring(response.content)
                namespace = {'repo': 'http://linux.duke.edu/metadata/repo'}
                primary_data = root.find(".//repo:data[@type='primary_db']", namespace)

                if primary_data is None:
                    print(f"{repo_id}: No primary_db found in repomd.xml")
                    return

                primary_location = primary_data.find('repo:location', namespace).attrib['href']
                primary_checksum = primary_data.find('repo:open-checksum[@type="sha256"]', namespace).text

                # Construct URL for primary.sqlite.bz2
                base_url = metadata_url.rsplit('/', 2)[0]  # Remove repodata/repomd.xml
                primary_url = f"{base_url}/{primary_location}"

                # Download and decompress primary.sqlite.bz2
                response = requests.get(primary_url, stream=True, timeout=120)
                response.raise_for_status()

                # Decompress bz2 data in memory
                compressed_data = response.content
                binary_data = bz2.decompress(compressed_data)

                # Verify checksum
                actual_checksum = hashlib.sha256(binary_data).hexdigest()
                if actual_checksum != primary_checksum:
                    print(f"{repo_id}: Checksum mismatch, skipping")
                    return
            else:
                print(f"{repo_id}: Unknown repository type {repo_type}")
                return

            # Extract cache information from response headers
            etag = response.headers.get('ETag')
            last_modified_str = response.headers.get('Last-Modified')
            content_length = response.headers.get('Content-Length')

            # Parse last_modified timestamp
            last_modified = None
            if last_modified_str:
                from datetime import datetime
                try:
                    last_modified = datetime.strptime(last_modified_str, '%a, %d %b %Y %H:%M:%S GMT')
                except ValueError:
                    pass

            size = len(binary_data)

            # Store or update binary data and cache info in pgext.repo_data
            update_cursor = conn.cursor()
            update_cursor.execute("""
                                  INSERT INTO pgext.repo_data (id, etag, size, extra, data, last_modified, update_at)
                                  VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                                  ON CONFLICT (id) DO UPDATE SET
                                                                 etag = EXCLUDED.etag,
                                                                 size = EXCLUDED.size,
                                                                 extra = EXCLUDED.extra,
                                                                 data = EXCLUDED.data,
                                                                 last_modified = EXCLUDED.last_modified,
                                                                 update_at = CURRENT_TIMESTAMP
                                  """, (repo_id, etag, size, json.dumps(existing_extra), binary_data, last_modified))
            conn.commit()

            print(f"{repo_id}: Downloaded {size} bytes")

        except Exception as e:
            print(f"{repo_id}: Error downloading - {e}")

    # Use ThreadPoolExecutor for parallel downloads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_repo_data, repo) for repo in repos]
        for future in futures:
            future.result()

    conn.close()
    print("Repository reload completed")


def main():
    """Main function to run both reload operations"""
    print("=== PostgreSQL Extension Repository Reload ===")

    # Step 1: Download repository metadata
    reload_repo()


if __name__ == "__main__":
    main()