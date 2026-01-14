---
id: "KNIFE-20260114-006"
guid: "45ed497a-27a2-4e11-b6b5-0d5eeb39b226"
dao: "knife"
title: "Knowledge Contribution"
author: "Peter Bartoš"
category: "deliverable"
type: "knowledge-contribution"
priority: "high"
tags: ["ESP32", "Arduino", "OLED", "SSD1306", "TFT", "ILI9341", "Adafruit GFX", "TFT_eSPI", "I2C", "SPI", "display", "fonts"]
slug: "esp32-display-text-tutorial"
created: "2026-01-14"
modified: "2026-01-14"
status: "draft"
# ⚖️ IP rights
rights_holder_content: "Peter Bartoš"
rights_holder_system: "Roman Kazička (CAA/KNIFE/LetItGrow)"
license: "CC-BY-NC-SA-4.0"
disclaimer: "Use at your own risk. Methods provided as-is; participation is voluntary and context-aware."
locale: "sk"
---

[🏠 Domov](../index.md) · [⬅️ Nahor](./index.md)

# Knowledge Contribution

## Názov
ESP32 (Arduino) – ako vykresľovať text na displej (OLED SSD1306)

## 🎯 Čo rieši (účel, cieľ)
Praktický návod, ako na **ESP32** zobraziť text na bežných displejoch:
- **OLED 0.96'' SSD1306 (I²C)** pomocou **Adafruit GFX + Adafruit SSD1306**

## 🧩 Ako to rieši (princíp)
- Pre **OLED** použijeme I²C zbernicu (SDA/SCL). Knižnica **Adafruit_SSD1306** poskytne framebuffer a kresliace príkazy, **Adafruit_GFX** zasa text, čiaru, bitmapy.

## 🧪 Ako to použiť (aplikácia)
- Vyber typ displeja a zapoj ho (I²C/SPI).
- Nainštaluj príslušnú knižnicu (Library Manager / manuál).
- Inicializuj displej v `setup()`.
- Vykresli text: nastav font, farbu, kurzor a zavolaj `print()`/`drawString()`.
- Pri potrebe pridaj **diakritiku** cez vlastné fonty alebo UTF‑8 mapovanie.

---

## ⚡ Rýchly návod (Top)
### OLED SSD1306 (I²C)
```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup(){
  Wire.begin(21,22);                 // SDA=21, SCL=22 (ESP32 default)
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextSize(2);            // 2x väčší bitmapový font
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Ahoj, svet!");
  display.display();                 // odošle framebuffer na OLED
}
void loop(){}
```

---

## 📜 Detailný článok
#### 1. Hardvér a zapojenie
- **OLED SSD1306 (I²C)**: 3V3, GND, **SDA→GPIO21**, **SCL→GPIO22**, adresa zvyčajne `0x3C`.

#### 2. Inštalácia knižníc
- **Adafruit GFX** + **Adafruit SSD1306** (Library Manager)

#### 3. Základy textu (OLED – Adafruit_GFX)
```cpp
// Zarovnanie a rámovanie
int16_t x1, y1; uint16_t w, h;
String text = "Status: OK";
display.getTextBounds(text, 0, 0, &x1, &y1, &w, &h);
display.setCursor((SCREEN_WIDTH - w)/2, (SCREEN_HEIGHT - h)/2);
display.println(text);
```
- **Diakritika**: vstavaný 5×7 font nepokrýva UTF‑8; použi vlastný bitmapový font (konvertor) alebo vykresli **bitmapové glyphy**. Alternatíva: nahradiť diakritiku ASCII ekvivalentom pri malej OLED obrazovke.

#### 4. Výkon a optimalizácia
- **OLED**: minimalizuj počet volaní `display.display()` – zoskup kreslenie a volaj ho po dávkach.
- **TFT**: používaj **`setTextColor(fg, bg)`** pre rýchle prekreslenie, zvýš **SPI frekvenciu** (napr. 40–80 MHz podľa modulu), pri animáciách kresli len poškodené oblasti.

#### 5. Špeciálne prípady
- **Otočenie displeja**: `setRotation(0..3)`
- **Viacriadkový text**: `println()` alebo manuálne `
` s kontrolou `getTextBounds`.
- **Ikony/emoji**: vykresli bitmapy (XBM, RAW) alebo importuj glyphy ako vlastný font.

#### 6. Obrazová ukážka

<img src="./images/display.jpg" alt="lcd" width="500"/>

## 💡 Tipy a poznámky
- Pre slovenské texty na malom OLED je často lepšie **bez diakritiky** alebo použiť **VLW** fonty na TFT.
- Pri problémoch s OLED adresou spusti I²C skener a over `0x3C/0x3D`.
- Na rozloženie UI si priprav **grid** (konštanty okrajov a riadkov) a helper funkcie (napr. `drawLabel(x,y,text)`).

## ✅ Hodnota / Zhrnutie
Unifikovaný postup, ako na ESP32 rýchlo rozbehnúť text na **OLED** aj **TFT** displejoch, s dôrazom na správne zapojenie, knižnice, fonty a výkon.

---

# 📚 Knowledge Contribution

## 🔖 Názov a stručný popis
ESP32 (Arduino): vykresľovanie textu na OLED (SSD1306) a TFT (ILI9341) – od zapojenia po fonty a optimalizácie.

## 🗂️ Taxonómia KNIFE
- **Kategória:** IoT, Embedded, UI
- **Typ:** Návod
- **Tagy:** ESP32, OLED, TFT, text, fonty, Adafruit_GFX, SSD1306, TFT_eSPI

## 📜 Obsah
- Zapojenie I²C/SPI a inštalácia knižníc
- Základný kód pre OLED
- Fonty, diakritika, zarovnanie
- Výkon a optimalizácia

## 🌍 Referencie
- [Adafruit GFX](https://github.com/adafruit/Adafruit-GFX-Library)
- [Adafruit SSD1306](https://github.com/adafruit/Adafruit_SSD1306)

---

[🏠 Domov](../index.md) · [⬅️ Nahor](./index.md)
