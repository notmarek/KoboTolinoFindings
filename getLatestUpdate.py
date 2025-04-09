import requests
import re

URL="https://api.kobobooks.com/1.0/UpgradeCheck/Device/00000000-0000-0000-0000-000000000{code}/kobo/{version}/T0"

def walk(dev_code, version="0.0", prev_version=None, raw=None):
    if version == prev_version:
        return version
    
    res = requests.get(URL.replace("{version}", version).replace("{code}", str(dev_code)), headers={"Accept": "application/json"})
    data = res.json()
    if data["UpgradeURL"] is None:
        return (version, raw["UpgradeURL"])
    next_version = re.search(r"-(\d\..*\d)", data["UpgradeURL"]).group(1)
    return walk(dev_code, next_version, version, data)




MARKDOWN_TEMPLATE = "| {VERSION} | {MONTH} {YEAR}  | [Normal]({URL})                                                                                                                         |"


DEVICES = [
    {
        "name": "Tolino Vision Color",
        "code": 690,
    },
    {
        "name": "Tolino Shine BW",
        "code": 691,
    },
    {
        "name": "Tolino Shine Color",
        "code": 693
    }
]
month_dict = {
    "Jan": "January",
    "Feb": "February", 
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December"
}
for dev in DEVICES:
    (version, url) = walk(dev["code"])
    url = url.replace(".zip", "/update.tar")
    date = re.search(r"\/(.{3})(\d{4})\/", url)
    month = month_dict[date.group(1)]
    year = date.group(2)
    md = MARKDOWN_TEMPLATE.replace("{VERSION}", version).replace("{MONTH}", month).replace("{YEAR}", year).replace("{URL}", url)

    print(dev["name"], version)
    print(md)

# # updates for vision are almost identical to shine but have foxit
# print(, walk(URL, "0.0"))
# # updates for shine bw and c are identical
# print("Tolino Shine BW", walk(URL.replace("690", "691"), "0.0"))
# print("Tolino Shine Color", walk(URL.replace("690", "693"), "0.0"))


