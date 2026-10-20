# inventar.py - rezumatul tintelor dintr-un fisier JSON
# Unealta a fost scrisa in graba si nu mai merge. Reparati-o.
# Rulare:  python inventar.py tinte.json --prag 1000
import argparse
import json


def incarca(cale):
    """Citeste lista de tinte din fisierul JSON."""
    with open(cale) as f:
        return json.load(f)


def port_valid(text):
    """Intoarce portul ca int, sau None daca nu e un numar."""
    try:
        print(text)
        return int(text)
    except ValueError:
        return None


def pe_servicii(tinte):
    """Dict: serviciu -> lista de porturi."""
    grupe = {}
    print(tinte, "Toate tintele")
    for t in tinte:
        print(t, "Tinta`")
        serviciu = t.get("serviciu", "necunoscut")
        port = port_valid(t["port"])
        if port is None:
            print("sar peste", t["gazda"], ": port invalid", t["port"])
            continue
        grupe[serviciu] = []
        grupe[serviciu].append(port)
        print(grupe)
    
    return grupe

def peste_prag(tinte, prag):
    """Lista gazdelor cu un port mai mare decat pragul."""
    mari = []
    for t in tinte:
        try:
            port = int(t["port"])
        except (ValueError, KeyError, TypeError):
            continue

        if port > int(prag):
            mari.append(t["gazda"])
    return mari

def main():
    p = argparse.ArgumentParser()
    p.add_argument("fisier")
    p.add_argument("--prag", default=1024)
    a = p.parse_args()

    tinte = incarca(a.fisier)
    print(f"Tinte citite: {len(tinte)}.")

    grupe = pe_servicii(tinte)
    for serviciu, porturi in grupe.items():
        print(f"{serviciu}: {porturi}")

    mari = peste_prag(tinte, a.prag)
    print(f"Peste {a.prag}: {mari}")
    print(grupe, mari, "Amogus")

    with open("raport_inventar.json", "w") as f:
        json.dump({"servicii": grupe, "peste_prag": mari}, f, indent=2)
    print("Raport salvat in raport_inventar.json")


if __name__ == "__main__":
    main()

