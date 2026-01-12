KNIFE #3 — REST API a serverová časť

🎯 Čo rieši (účel, cieľ)
Príjem, ukladanie a spracovanie senzorových dát zo zariadenia cez bezpečné REST API.

🧩 Ako to rieši (princíp)
Server poskytuje endpoint:
POST /api/v1/readings
JSON payload obsahuje O₂, teplotu, vlhkosť, timestamp a ID zariadenia.
Backend vykoná validáciu, uloží dáta do databázy a vyhodnotí, či majú byť spustené alerty.

🧪 Ako to použiť (aplikácia)

Spustiť server (Flask/FastAPI).

Zariadenie odosiela dáta každých X sekúnd.

Analytická služba monitoruje prahy.

Dashboard zobrazuje grafy.

⚡ Rýchly návod (Top)

POST /api/v1/readings
{
 "device_id": "A12",
 "o2": 20.5,
 "temp": 23.1,
 "humidity": 40.1,
 "ts": "2025-12-01T10:22:00Z"
}


📜 Detailný článok
Validácia:

device exists?

ranges: O₂ (0–25%), temp (-20–60°C), humidity (0–100%)

Databáza:

readings(device_id, ts, o2, temp, hum)

alerts(device_id, ts, type, value)

Analytické pravidlá:
Pri každom prijatí:

if o2 < threshold_warn → alert.warn
if o2 < threshold_crit → alert.crit


Bezpečnosť:

API key v hlavičke

HTTPS

Rate limiting

Logging

💡 Tipy a poznámky

Pre mnoho zariadení použiť queue (RabbitMQ).

Pre analytiku sa hodí TimescaleDB.

Pre dashboard odporúčam Grafana / vlastné UI.

✅ Hodnota / Zhrnutie
Tento KNIFE dokumentuje kompletný backend: API, databázu, ukladanie aj analytiku – základ pre serverovú časť.