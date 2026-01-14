# 05-Design

## Návrh púzdra
Projekt počíta s kompaktným púzdrom, ktoré:
- chráni elektroniku pred mechanickým poškodením,
- umožňuje optimálny prietok vzduchu pre presné merania,
- poskytuje otvory pre napájanie a prípadné uchytenie senzora.

### Skica púzdra
<figure>
  <img src="../../images/skica.png" alt="skica" width="700" />
  <figcaption>Obr.:  Počiatočný náčrt drevenej krabičky, ktorá zakrýva hardvér. Návrh obsahuje otvory pre prúdenie vzduchu a prístup k napájaniu.</figcaption>
</figure>


### 3D Model púzdra

Pre lepšiu vizualizáciu bol vytvorený 3D model krabičky, ktorý:
- definuje presné rozmery pre ESP32 a senzory,
- obsahuje drážky na uchytenie komponentov,
- zohľadňuje ventilačné otvory pre minimalizáciu skreslenia meraní.

<figure>
  <img src="../../images/3d_dizajn.png" alt="3d dizajn" width="700" />
  <figcaption>Obr.:  3D model drevenej krabičky s otvormi pre prúdenie vzduchu a presnými drážkami na uchytenie ESP32 a senzorov.</figcaption>
</figure>


## Návrh kabeláže

Prepojenie medzi ESP32 a senzormi je realizované cez I²C zbernicu:
- SDA (GPIO21) a SCL (GPIO22) sú spoločné pre oba senzory a OLED displej.
- Napájanie senzorov je riešené cez VIN a GND.
- Kabeláž je navrhnutá tak, aby bola prehľadná, minimalizovala rušenie a umožnila jednoduchú údržbu.


<figure>
  <img src="../../images/wiring.png" alt="kabeláž" width="700" />
  <figcaption>Obr.:  Schéma zapojenia medzi ESP32, senzormi AHTX0 a ENS160 a voliteľným OLED displejom.</figcaption>
</figure>


## Server API
Server poskytuje REST API pre komunikáciu s ESP32 a webovým rozhraním:

- **GET /health** – stav servera (uptime, verzia)  
- **POST /send-data** – prijme najnovšie merania zo senzora (JSON payload)  
- **GET /read-data** – vráti dáta pre používateľa a dátum/interval, query parametre: user_id, date (napr. 2026-01-13)

## Databázová schéma

Databáza SQLite obsahuje dve hlavné tabuľky:

**users** (väzba používateľ ↔ zariadenie)
| Stĺpec        | Typ     | Popis                         |
|---------------|---------|-------------------------------|
| id            | INTEGER | Primárny kľúč                 |
| serial_number | TEXT    | Jedinečný identifikátor zariadenia |


**sensor_realtime** (posledné merania na používateľa/zariadenie)
| Stĺpec      | Typ     | Popis                          |
|-------------|---------|--------------------------------|
| id          | INTEGER | Primárny kľúč                  |
| user_id     | INTEGER | FK na users.id                 |
| temperature | REAL    | Teplota v °C                   |
| humidity    | REAL    | Relatívna vlhkosť v %          |
| aqi         | INTEGER | Index kvality vzduchu          |
| co2         | REAL    | eCO₂ v ppm                     |
| tvoc        | REAL    | TVOC                           |
| timestamp   | INTEGER | Unix čas merania               |


## Dizajnové princípy

Modularita: jednoduchá výmena senzorov alebo ESP32.

Ergonómia: kompaktné rozmery, estetický vzhľad vhodný do interiéru.

Presnosť: ventilačné otvory pre správny prietok vzduchu.

Bezpečnosť: izolácia elektroniky od vlhkosti a prachu.

<!-- - [Prototypy / dizajn](./prototype.md) -->

**Navigation:** [⬆️ SDLC](../index.md) · [⬅️ Projekt](../../index.md)
