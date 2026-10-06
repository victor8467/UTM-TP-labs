# Laborator: functii, metode si importuri pe web
# Student: Buzdugan Victor

import requests
import urllib.parse
import re
import socket
import ssl
from datetime import datetime

DEFAULT_HEADERS = {"User-Agent": "WebLab-Buzdugan Victor"}
TIMEOUT = 10

def fetch(url, timeout=TIMEOUT):
    """Trimite o cerere GET cu antetele implicite."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

def get_status(url):
    """Returneaza codul de stare HTTP."""
    res = fetch(url)
    return res.status_code

def get_title(html):
    """Extrage titlul paginii HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return "Fara titlu"

def security_headers(url):
    """Verifica antetele de securitate."""
    res = fetch(url)
    headers = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]
    return {h: h in res.headers for h in headers}

def score_headers(results):
    """Calculeaza scorul antetelor."""
    present = sum(1 for val in results.values() if val)
    return f"{present}/{len(results)}"

def resolve(hostname):
    """Afla adresa IP."""
    try:
        return socket.gethostbyname(hostname)
    except socket.error:
        return "N/A"

def cert_days_left(hostname):
    """Calculeaza zilele ramase pentru SSL."""
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                exp_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                return (exp_date - datetime.utcnow()).days
    except Exception:
        return 0

def fetch_robots(base):
    """Descarca robots.txt."""
    try:
        res = fetch(base + "/robots.txt")
        return res.text if res.ok else None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text):
    """Extrage caile interzise."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.strip().lower().startswith("disallow:"):
            parts = line.split(":")
            if len(parts) > 1 and parts[1].strip():
                paths.append(parts[1].strip())
    return paths

def site_report(url):
    """Genereaza raportul complet al site-ului."""
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.netloc or parsed.path

    res = fetch(url)
    history_str = " -> ".join([f"{r.status_code}" for r in res.history]) if res.history else "Fara redirectionari"
    
    links = list(set(re.findall(r'href="([^"]+)"', res.text)))
    int_links = [l for l in links if hostname in urllib.parse.urljoin(url, l)]
    ext_links = [l for l in links if hostname not in urllib.parse.urljoin(url, l)]

    sec_res = security_headers(url)
    robots = fetch_robots(url)

    report_data = {
        "url": res.url,
        "status_code": res.status_code,
        "title": get_title(res.text),
        "ip": resolve(hostname),
        "redirects": history_str,
        "security_score": score_headers(sec_res),
        "cert_days_left": cert_days_left(hostname),
        "internal_links": len(int_links),
        "external_links": len(ext_links),
        "disallowed_paths": disallowed_paths(robots)
    }
    return report_data

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
