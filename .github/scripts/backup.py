import os
import requests

SPACE_TOKEN = os.getenv('SPACE_TOKEN')  # Not used, but leave in case you secure registry later

# Registry root for your Space instance
BASE_URL = "https://pypi.pkg.jetbrains.space/alpenglow/p/alpenglow"

# Add all known package names here
packages = [
    "alpenbar",  # Add more package names if needed
    "alpenglow-cereal",
    "alpenglow-datamodel",
    "alpenglow-nexus"
]

os.makedirs("packages", exist_ok=True)

for pkg in packages:
    index_url = f"{BASE_URL}/{pkg}/json"
    print(f"Fetching {index_url} ...")
    resp = requests.get(index_url)
    if resp.status_code != 200:
        print(f"❌ Failed to get metadata for {pkg}: {resp.status_code}")
        continue

    data = resp.json()
    releases = data.get("releases", {})

    for version, files in releases.items():
        for f in files:
            url = f["url"]
            filename = f["filename"]
            print(f"Downloading {filename} from {url}")
            r = requests.get(url)
            with open(f"packages/{filename}", "wb") as out:
                out.write(r.content)
