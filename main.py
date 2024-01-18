import datetime
import requests, json, os, time

os.chdir(os.path.basename(os.path.abspath(__file__)))

version_manifest = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

manifest = json.loads(requests.get(version_manifest).text)
# baseTime = datetime.datetime(int("2019"), int("07"), int("19"))
if not os.path.exists("release"): os.mkdir("release")
if not os.path.exists("snapshot"): os.mkdir("snapshot")
for x in manifest["versions"]:
    # print(x["id"], x["type"])
    t = x["releaseTime"].split(":")[0].split("T")[0].split("-")
    releaseTime = datetime.datetime(int(t[0]), int(t[1]), int(t[2]))
    if not os.path.exists(x["type"]+"/"+x["id"]+".txt"):
        vManifest = json.loads(requests.get(x["url"]).text)
        try:
            print()
            print(x["type"], x["id"], t[0]+"-"+t[1]+"-"+t[2], "->", vManifest["downloads"]["client_mappings"]["url"])
            f = open(x["type"]+"/"+x["id"]+".txt", "w")
            f.write(requests.get(vManifest["downloads"]["client_mappings"]["url"]).text)
            f.close()
        except: 1

for root, dirs, files in os.walk("."):
    for x in files:
        f = open(os.path.join(root, x), "r")
        if (f.read().strip() == ""):
            f.close()
            os.remove(os.path.join(root, x))