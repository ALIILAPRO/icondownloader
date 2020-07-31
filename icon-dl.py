import os
import time
import re
import math
import requests
from enum import Enum

class IconFormat(Enum):
    PNG_512 = 512
    PNG_256 = 256
    PNG_128 = 128
    PNG_96  = 96
    PNG_72  = 72
    PNG_64  = 64
    PNG_48  = 48
    PNG_32  = 32
    PNG_24  = 24
    PNG_16  = 16
    ICO     = -1
    ICNS    = -2
    SVG     = -3

class Pack():
    def __init__(self, pack : str, iconformat : IconFormat):
        self.pages       = []
        self.icons       = []
        if pack.startswith("https://iconarchive.com/show/"):
            self.packid  = pack.replace("https://iconarchive.com/show/", "").split(".")[0]
        else:
            self.packid  = pack.replace(" ", "-").lower()
        self.name        = self.packid.replace("-", " ").title()
        self.iconformat  = iconformat
        self.url         = "https://iconarchive.com/show/" + self.packid + ".html"

    def fetch(self):
        r = requests.get(self.url)
        if (r.status_code != 200) or ("Page not found ..." in r.text.split("\n")[4]):
            raise Exception("Error, check your connection and URL.")
            exit(1)
        iconcount        = int(r.text.split("\n")[4].split(" icons) | ")[0].split("(")[1])
        pagecount        = math.ceil(iconcount / 50)
        for i in range(pagecount):
            page         = Page(f"https://iconarchive.com/show/{self.packid}.{i + 1}.html", self)
            self.pages.append(page)

class Page():
    def __init__(self, url : str, pack : Pack):
        self.url         = url
        self.icons       = []
        self.pack        = pack
        r = requests.get(url)
        if r.status_code == 200:
            for u in self.parse_links(r.text):
                icon = Icon(u, self, self.pack)
                if icon not in self.icons:
                    self.icons.append(icon)
                    self.pack.icons.append(icon)
        else:
            raise Exception("Error, check your connection and URL.")
            exit(1)

    def parse_links(self, text : str):
        links = []
        if self.pack.iconformat.name.startswith("PNG"):
            l = re.findall('http[s]?://icons\.iconarchive\.com/icons/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.png', text)
            links = list(set(link.replace("/128/", f"/{self.pack.iconformat.value}/") for link in l))
        else:
            l = re.findall('/download/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.' + self.pack.iconformat.name.lower(), text)
            for link in l:
                links.append("https://iconarchive.com" + link)
        return links

class Icon():
    def __init__(self, url : str, page : Page, pack : Pack):
        self.url      = url
        ext           = self.url.split(".")[len(self.url.split(".")) - 1]
        self.filename = self.url.split("/")[len(url.split("/")) - 1].replace("-"," ").split(".")[0].title() + "." + ext
        if ext.upper() == "PNG":
            self.iconformat = IconFormat[ext.upper() + "_" + self.url.replace("https://icons.iconarchive.com/icons/", "").split("/")[2]]
        else:
            self.iconformat = IconFormat[ext.upper()]
        self.page = page
        self.pack = pack

script_version = "1.0.0"
script_title   = "Icon Downloader By ALIILAPRO"       
def logostart():
    print (f'''
	 ..: {script_title} :..
 
 [!] ABOUT SCRIPT:
 [-] With this script, you can download any icon pack from IconArchive.com
 [-] Version: {script_version}
 --------
 [!] ABOUT CODER:
 [-] ALIILAPRO, Programmer and developer from IRAN.
 [-] Website  : aliilapro.github.io
 [-] Telegram : aliilapro
 [-] Instagram: mr.aliilapro
 --------
''')
os.system('title ' + script_title if os.name == 'nt' else 'PS1="\[\e]0;' + script_title + '\a\]"; echo $PS1')
os.system('cls' if os.name == 'nt' else 'clear')
logostart()
url       = input("[#] Enter the URL:")
type_file = input('''#---------------
Available formats
1  =  png-512
2  =  png-256
3  =  png-128
4  =  png-96
5  =  png-72
6  =  png-64
7  =  png-48
8  =  png-32
9  =  png-24
10 =  png-16
11 =  ico
12 =  icns
13 =  svg
#---------------
[#] Select the format number:''')
if type_file == "1":
    icon      = IconFormat.PNG_512
if type_file == "2":
    icon      = IconFormat.PNG_256
if type_file == "3":
    icon      = IconFormat.PNG_128
if type_file == "4":
    icon      = IconFormat.PNG_96
if type_file == "5":
    icon      = IconFormat.PNG_72
if type_file == "6":
    icon      = IconFormat.PNG_64
if type_file == "7":
    icon      = IconFormat.PNG_48
if type_file == "8":
    icon      = IconFormat.PNG_32
if type_file == "9":
    icon      = IconFormat.PNG_24
if type_file == "10":
    icon      = IconFormat.PNG_16
if type_file == "11":
    icon      = IconFormat.ICO
if type_file == "12":
    icon      = IconFormat.ICNS
if type_file == "13":
    icon      = IconFormat.SVG   


os.system('cls' if os.name == 'nt' else 'clear')
logostart()                                  
print("[#] Fetching data, this may take a while ...")
iconset = Pack(url, icon)
iconset.fetch()
print(f"[!] About Pack:")
print(f"\n[-] {iconset.name}")
[print(f"[-] page #{iconset.pages.index(page) + 1} -- {len(page.icons)} icons") for page in iconset.pages]
print(f"[-] {len(iconset.pages)} pages, {len(iconset.icons)} icons")
time.sleep(5)
os.system('cls' if os.name=='nt' else 'clear')
folder = iconset.name + " - " + iconset.iconformat.name
os.mkdir(str(folder))
for i, icon in enumerate(iconset.icons):
    os.system('cls' if os.name=='nt' else 'clear')
    logostart()
    print(f"[#] Downloading {iconset.name} ...")
    print("—————————————————————————————————————————")
    percent = round(((i + 1) / len(iconset.icons)) * 100, 3)
    print(f"[%] {percent} completed - {i + 1} / {len(iconset.icons)}")
    r       = requests.get(icon.url, allow_redirects = True)
    open(str(folder) + "/" + icon.filename, 'wb').write(r.content)

print("\n\n[#] Done, all files successfully downloaded.")
time.sleep(5)