import requests
import xml.etree.ElementTree as ET
loc = 0.0
urls = []
z = requests.get("https://api.github.com/users/mendelsshop/repos?per_page=1000")
l = z.json()
for i in l:
    urls.append(i["full_name"])

for i in urls:
    r = requests.get(f"https://tokei.rs/b1/github/{i}")
    root = ET.fromstring(r.content)
    for child in root:
        for subchild in enumerate(child.itertext()):
            if subchild[1].startswith("total lines"):
                # get the the i
                if child[subchild[0]].text == "total lines":
                    text = child[subchild[0] + 1].text
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
    print(f"{loc:.2f} lines of code")
elif loc / 1000000 < 1:
    print(f"{loc/1000:.2f}K lines of code")
elif loc / 1000000000 < 1:
    print(f"{loc/1000000:.2f}M lines of code")
elif loc / 1000000000000 < 1:
    print(f"{loc/1000000000:.2f}B lines of code")
else:
    print(f"{loc/1000000000000:.2f}T lines of code")

