KNIFE #8 — Návrh databázy a modelu dát

🎯 Čo rieši (účel, cieľ)
Organizácia senzorových dát tak, aby boli ľahko dostupné pre analytiku a dashboard.

🧩 Ako to rieši (princíp)
Použije sa PostgreSQL + Timescale (alebo InfluxDB).
Dátový model rozdeľuje dáta na identitu zariadenia, merania, a alerty.

🧪 Ako to použiť (aplikácia)

SQL migrácie

Indexy na ts + device_id

Partitioning podľa času

⚡ Rýchly návod (Top)
Tabuľky:

devices

readings

alerts

📜 Detailný článok
readings:

device_id

timestamp

o2_ppm

temp_c

humidity
alerts:

type (low_o2, high_temp)

threshold
device:

firmware version

location

💡 Tipy a poznámky

Použiť foreign keys

Monitorovať veľkosť DB

✅ Hodnota / Zhrnutie
DB dizajn umožňuje rýchlu analytiku a spoľahlivý historický prehľad.