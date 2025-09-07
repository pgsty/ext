#!/usr/bin/env python3.13

import os
import requests
import concurrent.futures
import pathlib

PG_SEARCH_VERSION = '0.18.1'

# Create target directory if it doesn't exist
target_dir = os.path.expanduser("~/pgsty/paradedb")
pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)

# You can set HTTP_PROXY environment variable if needed
http_proxy = os.getenv("HTTPS_PROXY", None)

# Function to download a single file
def download_file(url):
    local_filename = os.path.join(target_dir, url.split('/')[-1])
    headers = {}
    proxies = {}

    # If HTTP_PROXY is set, configure proxies
    if http_proxy:
        proxies = {
            "http": http_proxy,
            "https": http_proxy
        }
    
    # Check if file already exists and has the same size
    if os.path.exists(local_filename):
        # Get file size from server without downloading
        head_response = requests.head(url, headers=headers, proxies=proxies)
        head_response.raise_for_status()
        remote_size = int(head_response.headers.get('content-length', 0))
        local_size = os.path.getsize(local_filename)
        
        if remote_size == local_size:
            print(f"Skipping {local_filename} (already downloaded with matching size)")
            return local_filename

    with requests.get(url, stream=True, headers=headers, proxies=proxies) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

# Function to get download URLs for PG Search
def get_pg_search_assets(version=PG_SEARCH_VERSION):
    api_url = f"https://api.github.com/repos/paradedb/paradedb/releases/tags/v{version}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    release_data = response.json()
    download_urls = [asset['browser_download_url']
                     for asset in release_data['assets']
                     if not asset['name'].endswith('.sig') and not asset['name'].endswith('.pkg')]

    return download_urls

# Function to download all files concurrently using ThreadPoolExecutor
def download_all_files(download_urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(download_file, url) for url in download_urls]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(f"Downloaded {result}")
            except Exception as e:
                print(f"Error downloading file: {e}")

def main():
    print("Fetching release assets...")
    search = get_pg_search_assets()
    print(f"\nTotal URLs to download: {len(search)}")
    download_all_files(search)

if __name__ == "__main__":
    main()
