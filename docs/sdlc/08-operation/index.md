# 08-Operation

## Bežná prevádzka
Zariadenie je navrhnuté tak, aby bolo plug & play:
- Používateľ pripojí senzor cez micro-USB kábel.
- Po zapnutí sa ESP32 automaticky inicializuje:
  - vykoná kontrolu senzorov,
  - zobrazí stav na OLED displeji,
  - začne merať teplotu, vlhkosť, TVOC, eCO₂ a AQI.


- Ak je dostupné Wi-Fi pripojenie, zariadenie začne periodicky odosielať dáta na server (napr. každých 5 minút).


## Wi-Fi pripojenie
Pre účely Proof of Concept (PoC) je pripojenie riešené jednoducho:
- SSID siete musí byť „Hotspot“.
- Heslo: „smvit12345“.
- Po pripojení zariadenie začne komunikovať so serverom cez HTTP protokol.

#### Poznámka:
Vo finálnom produkte by bol použitý sofistikovanejší prístup, napríklad:
- konfigurácia cez webový setup alebo mobilnú aplikáciu,
- podpora viacerých sietí.

## Signalizácia stavu (LED indikátor)

Zariadenie využíva modrú LED diódu na indikáciu stavu:
#### ✅ Blikanie v intervale pripomínajúci „tlkot srdca“
- Všetko beží v poriadku.
- Zariadenie meria a úspešne odosiela dáta na server.

#### ⚠️ Blikanie v polsekundovom rovnomernom intervale
- Zariadenie sa nepripojilo na Wi-Fi.
- Meranie pokračuje, ale dáta sa neodosielajú na server.

#### ❌ Blikanie v sekundovom rovnomernom intervale
- Zariadenie je pripojené na Wi-Fi, ale nedokáže komunikovať so serverom.
- Možné príčiny:
  - výpadok servera,
  - problém s lokálnou sieťou.
- Meranie pokračuje, dáta sa neodosielajú na server.


## Odporúčania pre prevádzku

Zariadenie umiestniť na miesto s dobrým prúdením vzduchu.
Vyhnúť sa priamemu slnečnému žiareniu (skreslenie teploty).
Pravidelne kontrolovať stav Wi-Fi a servera.
V prípade dlhodobého výpadku siete použiť lokálne zobrazenie na OLED.

<!-- - [Prevádzka a podpora](./operations.md) -->

**Navigation:** [⬆️ SDLC](../index.md) · [⬅️ Projekt](../../index.md)
