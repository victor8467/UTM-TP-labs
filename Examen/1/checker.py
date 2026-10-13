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
    except rq.ConnectionError or rq.ConnectTimeout:
        return {"status": None, "error": "Nu sa putut de conectat la server"} 

    serv = "unknown"
    for key, r in res.headers.items():
        if key == "Server":
            serv = res.headers[key]

    return {"status": res.status_code, "content-type" : res.headers["Content-Type"], "length" : len(res._content), "server": serv}
        


    
    pass


def scan_sites():
    """Verifică toate site-urile din SITES, afișează cele cu status 200 sortate după lungime și un rezumat."""
    results = []
    success_count = 0
    fail_count = 0
    
    for site in SITES:
        res = check_site(site)
        results.append((site, res))
        if res.get("status") == 200:
            success_count += 1
        else:
            fail_count += 1
            
    valid_sites = []
    for item in results:
        site_url = item[0]
        site_res = item[1]
        if site_res.get("status") == 200:
            valid_sites.append(item)
            

    n = len(valid_sites)
    for i in range(n):
        for j in range(0, n - i - 1):
            len_current = valid_sites[j][1].get("length", 0)
            len_next = valid_sites[j + 1][1].get("length", 0)
            if len_current < len_next:
                temp = valid_sites[j]
                valid_sites[j] = valid_sites[j + 1]
                valid_sites[j + 1] = temp
                
    
    for item in valid_sites:
        site_url = item[0]
        site_res = item[1]
        print(f"{site_url} : status 200, {site_res.get('length')}")
        
    print(f"Reusite: {success_count} Esuate: {fail_count}")


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

    print(check_site('https://httpbin.org/json'))
    print(check_site("https://example.com"))

    scan_sites()




if __name__ == "__main__":
    main()