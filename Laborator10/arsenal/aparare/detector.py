import argparse, json
from collections import Counter
from arsenal.aparare.parse_auth import citeste_esecuri

def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    
    rezultat = []

    for ip, n in counts.most_common():
        if n >= prag:
            rezultat.append((ip,n))
    return rezultat

def main():
    c = Counter({"203.0.113.9": 13, "198.51.100.7": 2})
    print(suspecti(c))
    print(suspecti(c, prag=2))

    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    esecuri = citeste_esecuri(a.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, a.prag)

    if a.json:
        print(json.dumps({
            "esecuri": esecuri,
            "pe_ip": dict(counts),
            "suspecti": sus
        }, indent=2))
    else:
        print(f"Esecuri de autentificare: {len(esecuri)}")
        for ip, n in counts.most_common():
            print(f"  {ip}: {n}")
        print(f"Suspecti (prag {a.prag}):")
        for ip, n in sus:
            print(f"  {ip}  ({n} incercari)  BRUTE FORCE")



if __name__ == "__main__":
    main()

