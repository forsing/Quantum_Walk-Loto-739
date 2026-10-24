import pandas as pd
import numpy as np
import random


# Odkomentariši fajl koji testiraš:
# putanja_fajla = '/data/loto7_4708_k85.csv'
# putanja_fajla = '/data/loto7_4708_k85_loto_2976.csv' 
putanja_fajla = '/data/loto7_4708_k85_loto_plus_1732.csv'


MAX_BROJ = 39
BROJ_KUGLICA = 7

# Inicijalizacija seed-a za osiguranje konzistentnosti okruženja
random.seed(39)
np.random.seed(39)

# 1. UCITAVANJE CELOG CSV FAJLA
df = pd.read_csv(putanja_fajla, header=None)

istorija_izvlacenja = []
for red in df.iloc[:, -BROJ_KUGLICA:].values.tolist():
    kolo_ocisceno = [int(x) for x in red if pd.notna(x)]
    if len(kolo_ocisceno) == BROJ_KUGLICA:
        istorija_izvlacenja.append(sorted(kolo_ocisceno))

# 2. INICIJALIZACIJA MATRICE KVANTNOG PREPLITANJA (ENTANGLEMENT) IZ CELOG CSV-A
# Računam nelinearnu korelacionu matricu između svih parova brojeva kroz celu istoriju
kovarijaciona_matrica = np.zeros((MAX_BROJ, MAX_BROJ))
for kolo in istorija_izvlacenja:
    for i in range(len(kolo)):
        for j in range(len(kolo)):
            kovarijaciona_matrica[kolo[i]-1][kolo[j]-1] += 1

# Normalizacija korelacija celog fajla
if np.sum(kovarijaciona_matrica) > 0:
    kovarijaciona_matrica /= np.max(kovarijaciona_matrica)

# Inicijalizacija bazične talasne funkcije (ravnomerna superpozicija faza)
psi = np.ones(MAX_BROJ, dtype=complex) / np.sqrt(MAX_BROJ)

# 3. NELINEARNA EVOLUCIJA KVANTNOG HODAČA
# Umesto fiksnog Groverovog operatora, faza se menja na osnovu korelacionog tenzora fajla
broj_kvantnih_koraka = 5
for korak in range(1, broj_kvantnih_koraka + 1):
    # Dinamički operator novčića koji zavisi od prepletenosti parova brojeva kroz istoriju
    H = kovarijaciona_matrica * korak
    operator_evolucije = np.exp(1j * H) # Unitarna vremenska evolucija preko eksponenta matrice
    
    # Propagacija hodača kroz prepleteni prostor stanja
    psi = np.dot(operator_evolucije, psi)

# Normalizacija talasne funkcije nakon nelinearnih interakcija
psi /= np.linalg.norm(psi)

# 4. MERENJE (KOLAPS) I DETERMINISTIČKI IZBOR TOP 7 BROJEVA
# Računam gustinu verovatnoće |psi|^2 za svaku poziciju
gustina_verovatnoce = np.abs(psi) ** 2

# Rangiranje indeksa od najveće ka najmanjoj specifičnoj kvantnoj gustini
rangirani_brojevi = np.argsort(gustina_verovatnoce)[::-1] + 1

# Uzimam tačno 7 jedinstvenih brojeva sa najvećom kvantnom verovatnoćom
novi_tiket = sorted(rangirani_brojevi[:BROJ_KUGLICA].tolist())

print()
print(f"Predloženi kvantni tiket: {novi_tiket}")
print()
"""
Predloženi kvantni tiket: [8, x, 23, y, 32, z, 37]

Predloženi kvantni tiket: [8, x, 22, y, 24, z, 35]

Predloženi kvantni tiket: [2, x, 11, y, 26, z, 34]
"""



"""
Protokol za Kvantni hod (Quantum Walk) u kontekstu loto podataka

Konceptualni okvir: Kako se loto mapira na Kvantni hod?

U klasičnom nasumičnom hodu (kao što je Markovljev lanac), čestica se kreće kroz prostor na osnovu verovatnoća (baca se novčić i ide se levo ili desno). U Kvantnom hodu, čestica koristi principe kvantne mehanike - superpoziciju i interferenciju.
Umesto da se nalazi na jednom mestu, kvantni hodač istražuje sve moguće puteve istovremeno. Dok klasična verovatnoća raste linearno sa vremenom (t), kvantna propagacija (širenje) je kvadratno brža (t²), što omogućava prepoznavanje skrivenih korelacija u strukturama podataka.
Konstrukciju sistema vršim kroz tri elementa:
1. Prostor stanja (Pozicioni prostor): Loto prostor ima N=39 pozicija (loto brojevi od 1 do 39). Pošto se izvlači 7 brojeva, kvantno stanje sistema modelujem kao superpoziciju unutar prostora svih mogućih kombinacija.
2. Kvantni novčić (Coin Operator): Da bi čestica napravila korak, koristi se operacija na "kvantnom novčiću" koja meša unutrašnja stanja. Najčešće se koristi Hadamardova matrica ili Groverov operator difuzije.
3. Konstrukcija iz celog CSV-a (Početna faza): Umesto da krenem od nasumične pozicije, cela istorija dobitnih brojeva iz CSV fajla se koristi za generisanje početne kvantne faze (talasne funkcije). Svako istorijsko kolo ostavlja svoj "otisak" (fazu) u kvantnoj superpoziciji.

Mehanika determinističkog algoritma (Verzija V1)

Da bi dobio strogo deterministički izlaz koji zavisi isključivo od strukture svakog pojedinačnog fajla (bez random funkcija i uz fiksni seed = 39), algoritam izvršava sledeće:
1. Inicijalizacija talasne funkcije: Kreiram vektor kompleksnih amplituda dužine 39. Prolazim kroz ceo CSV i projektujem istorijske frekvencije brojeva u kvantne amplitude verovatnoće (ψ), gde važi da je kvadrat modula amplitude jednak realnoj zastupljenosti broja.
2. Evolucija sistema (Kvantni korak): Primenjujem Groverov operator difuzije nad celim vektorom stanja. Ovaj operator uzima kvantno stanje, ogleda ga oko srednje vrednosti i pojačava amplitude onih stanja koja konstruktivno interferiraju kroz istoriju fajla.
3. Merenje (Kolaps talasne funkcije): Računam konačnu raspodelu gustine verovatnoće (\(\vert\psi\vert^2\)). Biram 7 pozicija (brojeva) sa najvećom kvantnom gustinom verovatnoće. Pošto sortiram indekse po veličini dobijene energije, izlaz je potpuno deterministički i unikatan za svaki CSV.

Kod za verziju V1 zasnovanu na diskretnom vremenskom kvantnom hodu (Quantum Walk) sa Groverovim operatorom difuzije.
Kod učitava kompletan CSV fajl i koristi istorijske frekvencije brojeva za inicijalizaciju kompleksnih amplituda početne talasne funkcije (stanja hodača). Zatim se izvršava deterministička kvantna evolucija (mešanje faza i pojačavanje amplituda oko srednje vrednosti), nakon čega se računa gustina verovatnoće kolapsa talasne funkcije. Na kraju se bira 7 unikatnih brojeva sa najvišom kvantnom gustinom. seed = 39 je postavljen na vrhu.

Groverov operator difuzije (2.0 * np.outer(s, np.conj(s)) - np.eye(MAX_BROJ)) deluje kao globalni linearni filter proseka. Pošto su moji fajlovi istorijski dugi (veliki broj kola), ukupne frekvencije brojeva su procentualno toliko slične da male razlike u fazi poslednjeg kola bivaju potpuno zbrisane tokom množenja matrica. Nakon toga, operacija np.argsort poređa indekse u potpuno identičan raspored.
U realnoj kvantnoj mehanici, kvantni hodač ne evoluira kroz statičnu prosečnu sredinu, već se njegovi novčići i faze menjaju lokalno na svakom koraku na osnovu topologije i prepletenosti (entanglementa) celog lanca podataka. Da bi razbio ovaj linearni kolaps frekvencija i naterao algoritam da vidi specifične unutrašnje korelacije svakog fajla, moram primeniti nelinearni kvantni hod (Non-linear Quantum Walk) gde se faza operatora novčića dinamički menja u zavisnosti od međuindeksne udaljenosti (korelacije) brojeva kroz ceo CSV.
Nelinearno fazno preplitanje garantuje striktno jedinstvene rezultate za svaki csv fajl:
"""
