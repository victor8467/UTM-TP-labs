import os
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash","less", "awk", "python3", "perl"}

def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        linii_curate = []
        for ln in f:
            linie = ln.strip()
            if linie != "" and not linie.startswith("#"):
                linii_curate.append(linie)
        return linii_curate

def cai(fisier):
    return set(citeste_linii(fisier))

if __name__ == "__main__":
    folder_start = "start" if os.path.exists("start") else "arsenal/privesc/start"
    
    baza = cai(os.path.join(folder_start, "baza_suid.txt"))
    acum = cai(os.path.join(folder_start, "suid.txt"))
    print("baza:", len(baza), " acum:", len(acum))
    noi = acum - baza
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)

    periculoase = []
    for c in sorted(noi):
        nume_binar = c.rsplit("/", 1)[-1]
        if nume_binar in GTFO:
            periculoase.append(c)

    print("periculoase noi:", periculoase)

