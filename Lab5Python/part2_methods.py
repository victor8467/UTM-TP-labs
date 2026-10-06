# Laborator: funcții, metode și importuri pe web 

# Student: <Buzdugan Victor> 

  

BASE_URL = "https://cybercor.org" 
UNSECURE_URL = "http://cybercor.org"

ECHO_URL = "https://httpbin.org" 

TIMEOUT = 10  # secunde

import requests as rq

response = rq.get(BASE_URL,timeout=TIMEOUT)


print(response.status_code)
print(response.ok)
print(response.url)
print(response.encoding)
#toate sunt atribute, cum ar fi ok, este un atribut de tip bool, sau url care contine un link



try:
    response2 = rq.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    response2.raise_for_status()
    print(f"statusul la raspuns este: {response2.status_code}")


except rq.HTTPError:
    print("requestul a esuat")

#in cazul la cybercor , no sa dea eroare , deoarece toate paginile care nu exista formeaza o pagina noua pe care iti    scrie ca pagina nu exista , chiar daca ai accesato, deci statusul va fi mereu 200


for header in response.headers.items():
    print(f"Nume: {header}")

print(response.headers.get("Server","lipsește"))
print(response.headers.get("Content-Type", "lipsește"))
print(response.headers.get("content-type", "lipsește"))

#Apelul response.headers.get("content-type") returneaza aceeasi valoare ca response.headers.get("Content-Type")


print(response.text.lower().count("cyber"))
#putem inlantui lower si count deoarece returnul la functia lower este un string , iar pentru acel string intors este   apelata functia .count()


html = response.text
tag_start = "<title>"
tag_end = "</title>"

start_index = html.find(tag_start) + len(tag_start)
end_index = html.find(tag_end)

if start_index != -1 and end_index != -1:
    titlu_raw = html[start_index:end_index]
    titlu_curat = titlu_raw.strip()
    
    print("Titlul extras este:", titlu_curat)

lines = html.splitlines()

totalLinii = len(lines)
print(f"Liniile totale: {totalLinii}")


CeaMaiLungaLinie = max(lines,key=len)
print(f"Lungimea maxima: {len(CeaMaiLungaLinie)}")

if response.url.startswith("https://"):
    print("Conexiune Securizata")
else:
    print("Conexiune nesecurizata")

uResponse = rq.get(UNSECURE_URL, timeout=TIMEOUT)

for resp in uResponse.history:
    print(resp.url)

hResponse = rq.head(BASE_URL,timeout=TIMEOUT)
print(f"Get Response: {len(response.content)}, Head Response: {len(hResponse.content)}, Head Content: {hResponse.content}")

#request.head() primeste mereu de la server doar antetele sau headersurile de pe server, astfel continutul va fi mereu 0 biti si tine bandwidth mic si mai  rapid
#pe cand request.get descarca pana si corpul siteului, astfel lungimea mereu va fi mai mare ca request.head()

AreCookies = False
for cookie in response.cookies:
    AreCookies = True
    print(f"Cookie Name: {cookie.name}, Cookie Secure: {cookie.secure}")
if not AreCookies:
    print("Nici un cookie setat")

session = rq.Session()

session.headers.update({"User-Agent": "WebLab-Victor Buzdugan"})
Ses1Response = session.get(ECHO_URL + "/headers",timeout=TIMEOUT)
print(f"Response text este: {Ses1Response.text}")
Ses1Json = Ses1Response.json()

ses1Confirm = Ses1Json.get("headers",{}).get("User-Agent")
print(ses1Confirm)

#json are paranteze deoarece este o metoda sau o functie care returneaza o valoare de tip json, insa .text este o proprietate , nu este nevoie sa fie apelat


