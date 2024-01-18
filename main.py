import datetime
import requests, json, os, time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

version_manifest = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

manifest = requests.get(version_manifest).json()
if not os.path.exists("release"): os.mkdir("release")
if not os.path.exists("snapshot"): os.mkdir("snapshot")
for x in manifest["versions"]:
    if not os.path.exists(x["type"]+"/"+x["id"]+"/client.txt"):
        vManifest = requests.get(x["url"]).json()
        try:
            os.makedirs(x["type"]+"/"+x["id"])
            print(x["type"], x["id"], "->", vManifest["downloads"]["client_mappings"]["url"])
            if "client_mappings" in vManifest["downloads"]:
                f = open(x["type"]+"/"+x["id"]+"/client.txt", "wb")
                f.write(requests.get(vManifest["downloads"]["client_mappings"]["url"]).content)
                f.close()
            print(x["type"], x["id"], "->", vManifest["downloads"]["server_mappings"]["url"])
            if "server_mappings" in vManifest["downloads"]:
                f = open(x["type"]+"/"+x["id"]+"/server.txt", "wb")
                f.write(requests.get(vManifest["downloads"]["server_mappings"]["url"]).content)
                f.close()
        except: 1

for root, dirs, files in os.walk("."):
    for x in files:
        f = open(os.path.join(root, x), "r")
        if (f.read().strip() == ""):
            f.close()
            os.remove(os.path.join(root, x))