import requests as rq

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]
TIMEOUT = 5


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    firstSite = f"https://{host}"
    if path[0] == "/":
        return firstSite+path
    else:
        return firstSite+f"/{path}"
    pass


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if url[4] == "s":
        return True
    else:
        return False
    


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    res = rq.get(url,timeout=TIMEOUT)
    print(f"Status: {res.status_code}")
    print(f"Content-Type: {res.headers["Content-Type"]}")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        res = rq.get(url, timeout = TIMEOUT)
    except rq.ConnectionError or rq.ConnectTimeout or rq.exceptions.MissingSchema:
        return {"status": None, "error": "Nu sa putut de conectat la server"} 

    serv = "unknown"
    for key, r in res.headers.items():
        if key == "Server":
            serv = res.headers[key]

    return {"status": res.status_code, "content-type" : res.headers["Content-Type"], "length" : len(res._content), "server": serv}
        


    
    pass


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    pass


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass


def main():

    print(build_url("example.com", "/login"))
    print(build_url("example.com", "login"))


    print(is_https("https://example.com"))
    print(is_https("http://example.com"))

    show_response("https://example.com")
    show_response("https://httpbin.org/html")

    print(check_site('https://httpbin.org/status/404'))
    print(check_site("https://example.com"))
    print(check_site("nope"))





if __name__ == "__main__":
    main()