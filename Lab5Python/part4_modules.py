# Laborator: functii, metode si importuri pe web
# Student: Buzdugan Victor

import requests
import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
from datetime import datetime

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

url_obj = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
print("URL descompus:", url_obj.scheme, url_obj.netloc, url_obj.path, url_obj.query, url_obj.fragment)

for link in ["/about", "contact.html", "../index.html"]:
    print("URL compus:", urllib.parse.urljoin(BASE_URL, link))

def extract_links(html):
    """Extrage toate legaturile din HTML fara duplicate."""
    return list(set(re.findall(r'href="([^"]+)"', html)))

res = requests.get(BASE_URL, timeout=TIMEOUT)
links = extract_links(res.text)
print(f"Gasit {len(links)} link-uri")

def split_links(links, domain):
    """Separa legaturile in interne si externe."""
    internal, external = [], []
    for l in links:
        full = urllib.parse.urljoin(BASE_URL, l)
        parsed = urllib.parse.urlparse(full)
        if domain in parsed.netloc:
            internal.append(full)
        else:
            external.append(full)
    return internal, external

int_links, ext_links = split_links(links, "cybercor.org")
print(f"Interne: {len(int_links)}, Externe: {len(ext_links)}")

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

test_html = """<html><body>
<img src="/logo.png" alt="Logo">
<IMG SRC="poza.jpg">
<img alt="imagine fara src">
<img src="https://cdn.example.com/banner.webp" />
<a href="/despre">Aceasta nu este o imagine</a>
</body></html>"""

finder = ImageFinder()
finder.feed(test_html)
assert finder.images == ["/logo.png", "poza.jpg", "https://cdn.example.com/banner.webp"]
print("Testul pentru imagini a trecut!")

def page_fingerprint(url):
    """Returneaza hash-ul SHA256 al continutului paginii."""
    res = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(res.content).hexdigest()

fp1 = page_fingerprint(BASE_URL)
fp2 = page_fingerprint(BASE_URL)
# Rezultatele sunt diferite daca continutul paginii se schimba intre cereri.
# Acest lucru se intampla cand pagina contine reclame sau timestamp-uri dinamice.
print("Hash identic:", fp1 == fp2)

res = requests.get(BASE_URL, timeout=TIMEOUT)
with open("headers.json", "w") as f:
    json.dump(dict(res.headers), f, indent=2)

with open("headers.json", "r") as f:
    saved_headers = json.load(f)
print("Server din JSON:", saved_headers.get("Server"))

def resolve(hostname):
    """Returneaza adresa IP pentru un hostname."""
    return socket.gethostbyname(hostname)

print("IP:", resolve("cybercor.org"))

def cert_days_left(hostname):
    """Calculeaza zilele ramase pana la expirarea certificatului SSL."""
    ctx = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            exp_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            return (exp_date - datetime.utcnow()).days

print("Zile certificat:", cert_days_left("cybercor.org"))

# Metoda handle_starttag este apelata automat de catre metoda feed() a parser-ului HTML.
