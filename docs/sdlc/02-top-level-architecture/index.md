# 02-Top Level Architecture


### Fyzické komponenty
Projekt pozostáva z nasledujúcich hardvérových prvkov:

- ESP32 DevKit
  - Hlavný mikrokontrolér s integrovaným Wi-Fi modulom
  - GPIO piny na pripojenie periférií
  - I²C zbernica pre komunikáciu so senzormi a displejom
  - Napájanie cez USB (5V)


- Senzor AHTX0
  - Meranie teploty a vlhkosti
  - Komunikácia cez I²C


- Senzor ENS160
  - Meranie TVOC, eCO₂
  - Výpočet Air Quality Index (AQI)
  - Komunikácia cez I²C


- OLED displej (SSD1306)
  - Zobrazenie aktuálnych hodnôt priamo na zariadení


- Kryt (drevený)
  - Otvory pre prúdenie vzduchu (presné merania)
  - Otvor na napájanie senzora

---

### Hardvérová architektúra
Zariadenie je postavené na I²C zbernici, ktorá spája ESP32 s oboma senzormi a voliteľným OLED displejom.

- ESP32 je centrálny uzol, ktorý:
  - číta dáta zo senzorov,
  - zobrazuje ich na displeji,
  - odosiela ich cez Wi-Fi na server.


- Napájanie je riešené cez USB kábel (5V), ktorý napája ESP32 aj senzory.

<figure>
  <img src="../../images/hardware_architecture.png" alt="hardware architecture" width="700" />
  <figcaption>Obr.:  Diagram zobrazujúci fyzické komponenty</figcaption>
</figure>

---

### Systémová architektúra

Architektúra riešenia zahŕňa:
- ESP32 firmware (Arduino IDE):
  - Zber dát zo senzorov
  - Lokálne zobrazenie na OLED
  - Odosielanie dát cez HTTP POST na server

- Python server:
  - REST API na príjem dát
  - Ukladanie dát do SQLite databázy
  - Webová aplikácia na vizualizáciu (grafy, tabuľky)

- Používateľské rozhranie:
  - Responzívny web (PC & mobil)
  - Možnosť filtrovania dát podľa času a senzora
<figure>
  <img src="../../images/component_architecture.png" alt="component architecture" width="700" />
  <figcaption>Obr.:  Diagram zobrazujúci softvérové a systémové komponenty</figcaption>
</figure>

---

### Tok dát

1. Senzory → ESP32: meranie teploty, vlhkosti, TVOC, eCO₂, AQI
2. ESP32 → Server: odosielanie dát cez HTTP POST (JSON)
3. Server → SQLite: ukladanie dát do databázy
4. Web UI → Používateľ: vizualizácia dát (aktuálne hodnoty + historické grafy)

**Navigation:** [⬆️ SDLC](../index.md) · [⬅️ Projekt](../../index.md)
