import requests
import re

URL="https://api.kobobooks.com/1.0/UpgradeCheck/Device/00000000-0000-0000-0000-000000000690/kobo/{version}/T0"

def walk(url, version, prev_version=None):
    if version == prev_version:
        return version
    
    res = requests.get(url.replace("{version}", version), headers={"Accept": "application/json"})
    data = res.json()
    if data["UpgradeURL"] is None:
        return version
    next_version = re.search(r"-(\d\..*\d)", data["UpgradeURL"]).group(1)
    return walk(url, next_version, version)

# updates for vision are almost identical to shine but have foxit
print("Tolino Vision Color", walk(URL, "0.0"))
# updates for shine bw and c are identical
print("Tolino Shine BW", walk(URL.replace("690", "691"), "0.0"))
print("Tolino Shine Color", walk(URL.replace("690", "693"), "0.0"))