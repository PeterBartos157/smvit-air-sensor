Project Summary KNIFE

🎯 Čo rieši (účel, cieľ)

Vytvorenie kompaktného stolového zariadenia na monitorovanie kvality vzduchu (hladina O₂, teplota, vlhkosť a ďalšie indikátory), ktoré zabezpečí lokálnu vizuálnu spätnú väzbu používateľovi a zároveň odosiela namerané dáta cez Wi-Fi na centrálny REST server pre ukladanie, analýzu a upozornenia. Cieľom je včasná detekcia problémov s vetraním a zlepšenie pohodlia a bezpečnosti pri práci.



🧩 Ako to rieši (princíp)

Zariadenie obsahuje senzory pripojené k mikrokontroléru (ESP32/Arduino) čítajúcemu hodnoty v pravidelných intervaloch. Firmware vykoná kalibráciu, základné spracovanie (napr. filtrovanie a vyhladzovanie), porovnanie s prahovými hodnotami a vizualizáciu cez LED (zelená / žltá / červená). Súčasne je zabezpečený bezpečný prenos dát cez Wi-Fi (HTTP POST) na REST API server, ktorý ukladá záznamy do databázy, spúšťa analytické pravidlá a generuje upozornenia (email/push/dashboard).



🧪 Ako to použiť (aplikácia)

1\. Zapojte zariadenie a umiestnite ho vo výške pracovnej plochy s voľným prúdením vzduchu.  

2\. Pri prvom spustení spustite pairing režim (firmvér vytvorí AP alebo WPS pairing).  

3\. Používateľ nastaví Wi-Fi credentials cez web UI alebo provisioning endpoint.  

4\. Zariadenie začne pravidelné merania (napr. každých 10 s) a posiela JSON s payloadom na /api/v1/readings.  

5\. Server prijme, uloží a vyhodnotí hodnoty; v prípade prekročenia prahov vyšle upozornenie a zobrazí upozornenie v dashboarde.



⚡ Rýchly návod (Top)

1\. Zapnite zariadenie.  

2\. Pripojte ho k Wi-Fi cez provisioning (AP mode/QR/serial).  

3\. Skontrolujte zelenú LED = ok.  

4\. Ak LED žltá alebo červená → pozrite detail v dashboarde.  

5\. Ak chcete manuálny export, použite endpoint GET /api/v1/readings?device\_id=XXX.



📜 Detailný článok

\*\*Architektúra riešenia\*\*  

\- \*Edge\*: ESP32 (firmvér), O₂ senzor (analógový alebo I2C), teplota/vlhkosť (napr. SHT3x), LED indikátory, napájanie a obal.  

\- \*Komunikácia\*: HTTPS POST s JWT/API-key (alebo TLS client certifikát) do REST API (`/api/v1/readings`).  

\- \*Server\*: REST-based microservice, DB (timeseries-friendly: InfluxDB / PostgreSQL+Timescale), analytické pravidlá (thresholding, rolling averages), notifikácie (SMTP, push).  

\- \*Dashboard\*: Grafy (O₂, teplota, vlhkosť), per-device history, alerts list, device management.



\*\*Dátový model (príklad)\*\*

\- `devices` (device\_id PK, name, location, firmware\_version, last\_seen)  

\- `readings` (id, device\_id FK, ts, o2\_ppm, temp\_c, humidity\_pct, raw\_payload)  

\- `alerts` (id, device\_id, ts, alert\_type, value, acknowledged\_by, ack\_ts)



\*\*Firmware logika (pseudokód)\*\*



loop every MEASURE\_INTERVAL:

o2 = read\_o2()

temp, hum = read\_temp\_hum()

o2\_filtered = lowpass\_filter(o2)

if o2\_filtered < O2\_WARN\_THRESHOLD:

set\_led(YELLOW)

if o2\_filtered < O2\_CRITICAL\_THRESHOLD:

set\_led(RED); raise\_local\_alarm()

post\_payload = {

"device\_id": DEVICE\_ID,

"ts": utc\_now(),

"o2": o2\_filtered,

"temp": temp,

"hum": hum

}

try:

http\_post(SERVER\_URL + "/api/v1/readings", json=post\_payload, headers=auth)

except NetworkError:

queue\_payload\_locally()

\*\*Bezpečnosť\*\*

\- Použiť TLS (HTTPS) a API keys or JWT.  

\- Overiť požiadavky na serveri, rate-limit a validáciu payloadu.  

\- Pri párovaní dočasné provisioning tokeny s limitovaným časom platnosti.



\*\*Kalibrácia\*\*

\- Poskytnúť UI pre offset/scale kalibráciu O₂ senzora (manuálne alebo cez two-point calibration).  

\- Pri vývoji vykonať porovnanie so referenčnými prístrojmi.



\*\*Nasadenie\*\*

\- Docker-based REST service + Managed DB recommended.  

\- Device provisioning cez secured endpoint.  

\- CI pipeline pre firmware build a OTA (ak plánované).



💡 Tipy a poznámky

\- Výber senzora: niektoré O₂ senzory sú spotrebné (kyslíkové elektrochemické), iné optické — vyberte podľa presnosti a driftu.  

\- Umiestenie senzora v obale: zabezpečte dobré prúdenie vzduchu a oddialenie od tepelného zdroja (CPU).  

\- Power management: ak používať batériu, nastavte sleep režimy a menej časté odosielanie dát.  

\- Lokálne alarmy sú dôležité (LED + buzzer) ak sieť nie je dostupná.  

\- Pri ladení pridajte verbose logging a endpoint pre ostatné diagnostiky (GET /api/v1/device/{id}/diag).



✅ Hodnota / Zhrnutie

Tento KNIFE zhrňuje kompletný návrh: HW, FW, server, API, DB a UX. Poskytuje jasné požiadavky, postupy pre nasadenie a testovanie a zabezpečenie. Projekt dodáva meranie kvality vzduchu na úrovni pracovného stola, okamžité vizuálne upozornenia a historickú analytiku — zlepšenie zdravia a komfortu.





