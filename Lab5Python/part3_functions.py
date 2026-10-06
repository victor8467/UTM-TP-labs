# Laborator: functii, metode si importuri pe web
# Student: Buzdugan Victor

import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

def fetch(url, timeout=TIMEOUT):
    """Returneaza obiectul raspuns pentru un URL dat."""
    return requests.get(url, timeout=timeout)

res21 = fetch(BASE_URL)
print("Status:", res21.status_code)

def get_status(url):
    """Returneaza doar codul de stare HTTP pentru un URL."""
    res = requests.get(url, timeout=TIMEOUT)
    return res.status_code

for path in ["/", "/robots.txt", "/sitemap.xml"]:
    print(f"Status {path}:", get_status(BASE_URL + path))
    time.sleep(1)

fetch(BASE_URL)
fetch(BASE_URL, timeout=3)

def get_title(html):
    """Extrage si curata titlul dintr-un text HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return None

help(get_title)

def get_status_typed(url: str) -> int:
    """Returneaza codul de stare cu adnotari de tip."""
    res = requests.get(url, timeout=TIMEOUT)
    return res.status_code

# Adnotarile de tip sunt doar informative si nu opresc executia codului daca trimiti alt tip.
# Ele ajuta editorul sa detecteze greseli, dar Python le ignora complet la rulare.
get_status_typed(BASE_URL)

def page_exists(url):
    """Verifica daca o pagina exista fara a opri programul cu eroare."""
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return res.ok
    except requests.RequestException:
        return False

print("Exista domain invalid:", page_exists("https://this-domain-does-not-exist.invalid"))

def check_paths(base, paths):
    """Verifica o lista de cai si returneaza un dictionar cu statusurile lor."""
    results = {}
    for path in paths:
        full_url = base + path
        try:
            res = requests.get(full_url, timeout=TIMEOUT)
            results[path] = res.status_code
        except requests.RequestException:
            results[path] = None
        time.sleep(1)
    return results

print("Verificare cai:", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

def get_header(url, name, default="lipseste"):
    """Returneaza valoarea unui antet specific de la un URL."""
    res = requests.get(url, timeout=TIMEOUT)
    return res.headers.get(name, default)

print("Server:", get_header(BASE_URL, name="Server"))

def security_headers(url):
    """Verifica prezenta antetelor de securitate principale."""
    res = requests.get(url, timeout=TIMEOUT)
    headers = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]
    return {h: h in res.headers for h in headers}

sec_res = security_headers(BASE_URL)
print("Antete securitate:", sec_res)

def score_headers(results):
    """Calculeaza scorul antetelor de securitate prezente."""
    present = sum(1 for val in results.values() if val)
    return f"{present}/{len(results)}"

print("Scor antete:", score_headers(sec_res))

def fetch_robots(base):
    """Descarca fisierul robots.txt."""
    try:
        res = requests.get(base + "/robots.txt", timeout=TIMEOUT)
        return res.text if res.ok else None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text):
    """Extrage caile interzise din robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.strip().lower().startswith("disallow:"):
            parts = line.split(":")
            if len(parts) > 1 and parts[1].strip():
                paths.append(parts[1].strip())
    return paths

robots = fetch_robots(BASE_URL)
print("Cai interzise:", disallowed_paths(robots))

def response_times(*urls):
    """Masoara timpul de raspuns pentru mai multe URL-uri."""
    times = {}
    for u in urls:
        start = time.perf_counter()
        try:
            requests.get(u, timeout=TIMEOUT)
            times[u] = round(time.perf_counter() - start, 3)
        except requests.RequestException:
            times[u] = None
        time.sleep(1)
    return times

print("Timpi de raspuns:", response_times(BASE_URL, ECHO_URL))

def log(message, **details):
    """Afiseaza un mesaj urmat de detaliile primite."""
    details_str = " | ".join([f"{k}={v}" for k, v in details.items()])
    print(f"{message} | {details_str}" if details_str else message)

log("verificat", url=BASE_URL, status=200)

# print() doar afiseaza valoarea pe ecran pentru utilizator.
# return trimite valoarea inapoi in program pentru a fi folosita mai departe.
