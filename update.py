import requests
import xml.etree.ElementTree as ET
import sys
import os
import time

loc = 0.0
urls = []
z = requests.get(
    "https://api.github.com/users/mendelsshop/repos?per_page=1000",
)
l = z.json()
# print(l)
for i in l:
    urls.append(i["full_name"])

for i in urls:
    print(i)
    q = 0
    while True:
        r = requests.get(f"https://tokei.rs/b1/github/{i}")
        if (r.status_code < 200 or r.status_code >= 400) and q != 3: # if the https reponse code is not 200 and we havent tried 3 times
            time.sleep(60 * 3) # wait s minutes to not overwhelm the server
            print(r.status_code)
            q += 1 # bump the amount of tries
            continue # try again
        else:
            break
    try:
        root = ET.fromstring(r.content)
    except:
        continue
    for child in root:
        for subchild in enumerate(child.itertext()):
            if subchild[1].startswith("total lines"):
                # get the the i
                if child[subchild[0]].text == "total lines":
                    text = child[subchild[0] + 1].text
                    print(text)
                    if text.isdigit():
                        loc += float(text)
                    else:
                        # get the last digit
                        if text[-1] == "K":
                            loc += float(text[:-1]) * 1000
                        elif text[-1] == "M":
                            loc += float(text[:-1]) * 1000000
                        elif text[-1] == "B":
                            loc += float(text[:-1]) * 1000000000
                        elif text[-1] == "T":
                            loc += float(text[:-1]) * 1000000000000
                        else:
                            loc += 0


if loc / 1000 < 1:
    print(f"{loc:.2f}")
elif loc / 1000000 < 1:
    print(f"{loc/1000:.2f}K")
elif loc / 1000000000 < 1:
    print(f"{loc/1000000:.2f}M")
elif loc / 1000000000000 < 1:
    print(f"{loc/1000000000:.2f}B")
else:
    print(f"{loc/1000000000000:.2f}T")
