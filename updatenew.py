import requests
import os
import json
import subprocess


loc = 0.0
urls = []
z = requests.get(
    "https://api.github.com/users/mendelsshop/repos?per_page=1000",
)
l = z.json()
# print(l)
for i in l:
    urls.append(i["full_name"])
os.mkdir("temp")
os.chdir("temp")
for i in urls:
    subprocess.run(["git", "clone", f"https://github.com/{i}", "-q"], stdout=subprocess.PIPE)
result = subprocess.run(['tokei', '.', '--output', 'json'], stdout=subprocess.PIPE)
t = result.stdout.decode('utf-8')
pj = json.loads(t)
loc += float(pj['Total']['code'])
loc += float(pj['Total']['comments'])
loc += float(pj['Total']['blanks'])

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
