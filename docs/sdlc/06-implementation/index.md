# 06-Implementation

### Príprava hardvéru

Pred samotnou implementáciou bolo potrebné zabezpečiť všetky komponenty projektu. Hardvér bol doručený v samostatných balíkoch, čo umožnilo jednoduchú kontrolu a prípravu na montáž.

<figure>
  <img src="../../images/package.png" alt="balík" width="700" />
  <figcaption>Obr.:  Kompletný balík s hardvérom obsahujúci ESP32, senzory, káble a doplnky potrebné na realizáciu projektu.</figcaption>
</figure>

<figure>
  <img src="../../images/esp32.png" alt="balík mikrokontroléra" width="700" />
  <figcaption>Obr.:  Balík s mikrokontrolérom ESP32 DevKit – hlavný riadiaci prvok projektu, ktorý zabezpečuje komunikáciu so senzormi, spracovanie dát a pripojenie na Wi-Fi.</figcaption>
</figure>

<figure>
  <img src="../../images/sensor.png" alt="balík senzora" width="700" />
  <figcaption>Obr.:  Balík obsahujúci senzor ENS160 (TVOC, eCO₂, AQI) a AHT21 (teplota, vlhkosť). Tieto senzory sú základom pre meranie kvality ovzdušia.</figcaption>
</figure>

---

### Kód senzora

Ďalej si prejdeme úsek kódu, ktorý je zodpovedný za hlavnú funkcionalitu riešenia:

- čítanie dát zo senzorov AHT21 (teplota, vlhkosť) a ENS160 (TVOC, eCO₂, AQI),
- zobrazenie nameraných hodnôt na OLED displeji,
- odosielanie dát na server každých 5 minút vo formáte JSON.

#### Úryvok kódu
```ino
// Reading the sensor data
void readSensorData(unsigned long currentMillis) {
  // --- Read AHT21 ---
  sensors_event_t hmd, temp;
  aht.getEvent(&hmd, &temp);
  float temperature = temp.temperature;
  float humidity = hmd.relative_humidity;
  // --- Print AHT21 results ---
  Serial.print("Temp: "); Serial.print(temperature); Serial.print(" °C, ");
  Serial.print("Humidity: "); Serial.print(humidity); Serial.println(" %");
  // --- Read ENS160 ---
  int aqi; // air quality index (1-5)
  int co2; // estimated CO2 (ppm)
  int tvoc; // total VOC [Volatile Organic Compounds] (ppb)
  if( ens.checkDataStatus() ) {
    aqi = ens.getAQI();
    co2 = ens.getECO2();
    tvoc = ens.getTVOC();
    // --- Print ENS160 results ---
    Serial.print("Air Quality Index (1-5): "); Serial.print(aqi); Serial.print(", ");
    Serial.print("eCO2: "); Serial.print(co2); Serial.print(" ppm, ");
    Serial.print("TVOC: "); Serial.print(tvoc); Serial.println(" ppb");
  }
  else {
    Serial.print("Failed to read air quality data!");
  }
  // Displaying message to display
  displayMessage(
    "Temperature: " + String(temperature) + "C\nHumidity:    " + String(humidity) +
    "%\nAQI:         " + String(aqi) + "index\nCO2:         " + String(co2) + 
    "ppm\nTVOC:        " + String(tvoc) + "mg/m3"
  );
  // Every 5 minutes also send to server
  if (currentMillis - lastSendTime >= SEND_INTERVAL) {
    Serial.println("Sending sensor data to server...");
    lastSendTime = currentMillis;
    sendDataToServer(temperature, humidity, aqi, co2, tvoc);
  }
}
```

#### Detailný popis kódu

- Čítanie AHT21
  - Funkcia aht.getEvent() získava teplotu a vlhkosť.
  - Hodnoty sa ukladajú do premenných temperature a humidity.


- Čítanie ENS160
  - Funkcia ens.checkDataStatus() overí dostupnosť dát.
  - Získava sa AQI (index kvality vzduchu), eCO₂ (ppm) a TVOC (ppb).

- Výpis do Serial Monitoru
  - Pre debugovanie sa hodnoty vypisujú cez Serial.print().

- Zobrazenie na OLED displeji
  - Funkcia displayMessage() vykreslí hodnoty v prehľadnom formáte.


- Odosielanie dát na server
  - Každých 5 minút sa volá sendDataToServer() s nameranými hodnotami.


---

### Kód servera

Server je hostovaný na platforme **Azure**.

Serverová časť prijíma dáta od ESP32 cez HTTP POST a:
- kontroluje, či bol odoslaný validný JSON,
- overuje schému dát (musí obsahovať všetky požadované kľúče),
- ukladá dáta do SQLite databázy,
- vracia odpoveď vo formáte JSON s informáciou o stave operácie (success, bad request, server error).

#### Úryvok kódu
```python
@app.route('/send-data/', methods=['POST'])
def receive_data():
    """Receive data endpoint."""
    try:
        # If no JSON is provided
        request_json = request.json
        if not request_json:
            return fill_json_response(status=STATUS_OK, error="No JSON provided")
        # Convert JSON to dictionary
        request_dict = dict(request_json)
        # Validate JSON schema
        valid, missing_key = validate_received_data_schema(data=request_dict)
        if not valid:
            return fill_json_response(status=STATUS_BAD, error=f"Missing key: {missing_key}")
        # Save to database
        write_data(data=request_dict)
        # Return success
        return fill_json_response(status=STATUS_ADD, error=None)
    # Handle errors
    except (ValueError, RuntimeError) as error:
        print("Error:", error)
        return fill_json_response(status=STATUS_ERROR, error="Internal server error")
```

#### Detailný popis kódu

- Overenie JSON
  - Ak JSON chýba, vráti sa chyba.


- Validácia dát
  - Funkcia validate_received_data_schema() kontroluje povinné kľúče.

- Uloženie do DB
  - Funkcia write_data() zapisuje dáta do tabuľky sensor_realtime.

- Ošetrenie chýb
  - V prípade chyby sa vráti status STATUS_ERROR.


---

### Zapojenie hardvéru a prototypovanie

Po rozbalení komponentov nasledovalo zapojenie ESP32 a senzorov na testovacom stole. Prepojenie bolo realizované cez I²C zbernicu, pričom sa použili Dupont káble. Tento krok bol dôležitý na overenie funkčnosti senzorov a komunikácie s mikrokontrolérom.

<figure>
  <img src="../../images/esp32_wired.jpg" alt="zapojený mikrokontrolér" width="700" />
  <figcaption>Obr.:  Zapojený ESP32 DevKit s napájaním cez USB. Mikrokontrolér je pripravený na komunikáciu so senzormi a odosielanie dát na server.</figcaption>
</figure>

<figure>
  <img src="../../images/sensor_wired.jpg" alt="zapojený senzor" width="700" />
  <figcaption>Obr.:  Zapojený senzor ENS160+AHT21 cez I²C zbernicu. Testovanie prebiehalo na otvorenom stole pred vložením do púzdra.</figcaption>
</figure>

---

### Vloženie hardvéru do krabičky z dreva

Po úspešnom testovaní bol hardvér vložený do drevenej krabičky, ktorá bola navrhnutá tak, aby:

- chránila elektroniku,
- umožnila prúdenie vzduchu pre presné merania,
- poskytla otvory pre displej a napájanie.

<figure>
  <img src="../../images/final_1.jpg" alt="box 1" width="700" />
  <figcaption>Obr.:  Otvor na vzduch – zabezpečuje správny prietok vzduchu cez senzory, čím sa minimalizuje skreslenie meraní.</figcaption>
</figure>

<figure>
  <img src="../../images/final_2.jpg" alt="box 2" width="700" />
  <figcaption>Obr.:  Otvor na displej – umožňuje používateľovi sledovať aktuálne hodnoty priamo na OLED displeji.</figcaption>
</figure>

<figure>
  <img src="../../images/final_3.jpg" alt="box 3" width="700" />
  <figcaption>Obr.:  Otvor na napájanie – prístup k USB konektoru pre napájanie ESP32.</figcaption>
</figure>

- [Odkazy na kód / repozitáre](./code-links.md)

**Navigation:** [⬆️ SDLC](../index.md) · [⬅️ Projekt](../../index.md)
