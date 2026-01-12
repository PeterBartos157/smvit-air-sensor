KNIFE #9 — Dashboard a vizualizácia

🎯 Čo rieši (účel, cieľ)
Pohodlný prehľad o stave vzduchu v reálnom čase aj historicky.

🧩 Ako to rieši (princíp)
Dashboard poskytuje grafy, prehľady, tabuľky a alerty.
Používa WebSockets alebo pravidelný polling.

🧪 Ako to použiť (aplikácia)

Grafy O₂/teplota/vlhkosť (line chart)

Filtre: dátum, zariadenie, prahy

Alert panel

⚡ Rýchly návod (Top)
Tech stack:

React / Vue

Chart.js / ECharts

TailwindCSS

📜 Detailný článok
Realtime:

WebSocket: /ws/live
Historické grafy:

API: GET /api/v1/readings?device_id=X&from=&to=
Alerts panel:

highlight posledných 24h

💡 Tipy a poznámky

Dajte dark mode

Export CSV pre technikov

✅ Hodnota / Zhrnutie
Dashboard predstavuje používateľskú časť celého projektu – prehľadné grafy a upozornenia sú kľúčové pre reálne použitie.