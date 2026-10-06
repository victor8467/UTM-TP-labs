# Laborator: funcții, metode și importuri pe web 

# Student: <Buzdugan Victor> 
import requests
import urllib.request
from requests import get
import requests as rq
import time

BASE_URL = "https://cybercor.org" 

ECHO_URL = "https://httpbin.org" 

TIMEOUT = 10  # secunde 

print(requests.__version__)

#urllib nu are nevoie de pip install deoarece este din Python standard library , adica este distibuita odata cu python
#aceasta fiind disponibila prin import dar a necesita sa fie instalat prin pip, pe cand requests
#este o biblioteca third-party dezvoltata de comunitate si are nevoie sa fie instalata cu pip.

print(requests.get(BASE_URL,timeout=TIMEOUT))
print(get(BASE_URL,timeout=TIMEOUT))

# Avantaj la requests: Claritate si lizibilitate. Folosind prefixul "requests.", este evident din ce modul provine 
#functia get(), prevenind suprapunerea accidentala de nume (name shadowing) daca in script exista o alta functie numita get.

# Avantaj la from requests: Concizie si scriere mai scurta. Codul devine mai curat cand apelezi functia de mai multe ori, iar spatiul de nume local primeste direct functia fara a fi nevoie sa repeti numele modulului tata.

print(rq.get(BASE_URL, timeout=TIMEOUT))
# Cand face codul mai usor de citit:
# Cand modulul are un nume foarte lung sau complex (ex: "import matplotlib.pyplot as plt" sau "import numpy as np").
# Cand face codul mai greu de citit:
# Cand aliasul este prea scurt, ambiguu sau nestandardizat (ex: "import requests as rq"), fortand pe cineva care citeste codul sa verifice mereu unde a fost definit "rq".

headers = {'User-Agent': 'brother'}

req = urllib.request.Request(BASE_URL,headers=headers)


with urllib.request.urlopen(req,timeout=TIMEOUT) as serverResponse:
    htmlContent = serverResponse.read()
    print(serverResponse.status)
    htmlContent = htmlContent.decode("utf-8")
    print(htmlContent[:200])

print(dir(requests))

# Analiza a 3 elemente din dir(requests):

# 1. Response -> Clasa (reprezinta raspunsul returnat de un request HTTP)
# 2. get      -> Functie (efectueaza un cerere HTTP de tip GET)
# 3. auth     -> Modul / Subpachet (contine logica si clasele pentru autentificare)


#help(requests.get)
print(requests.get(BASE_URL, timeout=TIMEOUT))
FirstCounter = time.perf_counter()
response = requests.get(BASE_URL,timeout=TIMEOUT)
SecondCounter = time.perf_counter()
ElapsedTime = SecondCounter - FirstCounter
print(response.elapsed,ElapsedTime)


try:
    import bs4
except ImportError:
    print("bs4 nu exista in sistem")




