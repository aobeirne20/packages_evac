import os
import requests

SPACE_TOKEN = os.getenv('SPACE_TOKEN')
HEADERS = {'Authorization': f'Bearer {SPACE_TOKEN}'}

# 🔧 Replace with your actual org/project name
BASE_URL = 'https://alpenglow.jetbrains.space/p/alpenglow/packages/pypi/alpenglow'

def list_packages():
    response = requests.get(BASE_URL, headers=HEADERS)
    print(f"STATUS: {response.status_code}")
    print("RESPONSE TEXT:")
    print(response.text[:500])  # Show first 500 characters of response body
    response.raise_for_status()  # This will show 401, 403, or 404 if it's a permissions or URL problem
    return response.json()

def list_versions(package):
    url = f"{BASE_URL}/{package}/versions"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def download_file(url, dest):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    with open(dest, 'wb') as f:
        f.write(response.content)

os.makedirs("packages", exist_ok=True)

print("Fetching package list...")
for package in list_packages():
    name = package['name']
    for version in list_versions(name):
        v = version['version']
        for f in version['files']:
            url = f['downloadUrl']
            filename = f"{name}-{v}-{os.path.basename(url)}"
            print(f"Downloading {filename}")
            download_file(url, os.path.join("packages", filename))
