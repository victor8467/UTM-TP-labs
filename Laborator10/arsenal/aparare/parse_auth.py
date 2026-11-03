import re
import sys
from collections import Counter

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")
 
def esec(linie):
    m = TIPAR.search(linie)
    if not m:
        return None
    return m.group(1), m.group(2)

def citeste_esecuri(cale):
    esecuri = []
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri
    with f:
        for linie in f:
            r = esec(linie)
            if not r:
                continue
            register = {"user" : r[0], "ip" : r[1]}
            esecuri.append(register)

            
    return esecuri

def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)
 


def main():
    
    cale = sys.argv[1] if len(sys.argv) > 1 else "start/auth.log"
    esecuri = citeste_esecuri(cale)
    print("Esecuri de autentificare:", len(esecuri))

    counts = pe_ip(esecuri)
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")

if __name__ == "__main__":
    main()



