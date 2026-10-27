import argparse, json, os
 
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash","less", "awk", "python3", "perl"}

def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce lista liniilor .strip(), fara cele goale si fara cele cu #
        ...
        listaDeLinii = []
        for UnPLine in f:
            linie = UnPLine.strip()
            if linie != "" and not linie.startswith("#"):
                listaDeLinii.append(linie)
        return listaDeLinii
        

def nume(cale):
    return cale.rsplit("/", 1)[-1]


def suid_constatari(cale):
    cai = citeste_linii(cale)
    # TODO: pentru fiecare cale UNICA, in ordine sortata, un dict:
    #   {"cale": c, "nume": nume(c),
    #    "risc": "mare" daca nume(c) in GTFO, altfel "normal"}
    ...
    cai_unice = sorted(set(cai))
    HashMap_Final = []
    #print(GTFO)
    for c in cai_unice:
        riscCalculat = "Normal"
        #print(nume(c),nume(c) in GTFO)
        if nume(c) in GTFO:
            riscCalculat = "Mare"
        
        fisa = {"cale" : c , "nume" : nume(c) , "risk" : riscCalculat}
        HashMap_Final.append(fisa)
    return HashMap_Final

def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)   # despachetare in tuplu

        if "NOPASSWD" in drept:
            risc_calculat = "mare"
        else:
            risc_calculat = "normal"

        fisa = {
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": risc_calculat
        }
        out.append(fisa)
    return out

def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])
        
        fisa = {
            "user": user,
            "comanda": comanda
        }
        out.append(fisa)
    return out

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }

def main():
    cai = citeste_linii("start/suid.txt")
    print(f"linii SUID {len(cai)}")
    nume_unice = {nume(c) for c in cai}    # set comprehension
    print("SUID distincte:", len(nume_unice))

     
    suid = suid_constatari("start/suid.txt")
    mari = [c for c in suid if c["risk"] == "Mare"]
    print(len(suid), "SUID,", len(mari), "cu risc mare")
    print(sorted(c["nume"] for c in mari))

    print(sudo_constatari("start/sudo.txt"))
    print(cron_constatari("start/crontab.txt"))
    

    raport = enumereaza("start")
    print(f"Cron gasite {len(raport["cron"])}")
    print(f"Sudo gasite {len(raport["sudo"])}")

    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False)); return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
    # TODO: utilizatorii implicati = multimea userilor din sudo REUNITA cu cei din cron

    useri_sudo = set()
    for c in raport["sudo"]:
        useri_sudo.add(c["user"])
    useri_cron = set()
    for c in raport["cron"]:
        useri_cron.add(c["user"])
    
    toti_userii = sorted(useri_sudo | useri_cron)
    print("utilizatori implicati:", ", ".join(toti_userii))
    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")




if __name__ == "__main__":
    main()

