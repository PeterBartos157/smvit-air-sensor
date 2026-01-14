KNIFE #5 — Wi-Fi Provisioning & Secure Pairing

🎯 Čo rieši (účel, cieľ)
Bezpečné pripojenie nového zariadenia k Wi-Fi sieti bez nutnosti flashovania kódu alebo manuálneho zadávania hesla cez UART.

🧩 Ako to rieši (princíp)
ESP32 po zapnutí vstúpi do provisioning režimu:

vytvorí Wi-Fi AP („AirBox-Setup-XXXX“),

používateľ sa pripojí mobilom/notebookom,

jednoduché web UI umožní vložiť SSID + heslo,

firmware skúsi spojenie, uloží konfiguráciu do NVS a reštartuje sa.

🧪 Ako to použiť (aplikácia)

Zapnite zariadenie so stlačeným tlačidlom RESET → provisioning mód.

Pripojte sa k AP a otvorte 192.168.4.1.

Zadajte údaje do formulára.

Po reštarte LED zabliká zelenou = úspech.

⚡ Rýchly návod (Top)

AP: WiFi.softAP("AirBox-Setup")

Mini webserver v ESPAsyncWebServer

Uloženie údajov: preferences.putString("ssid", ssid)

📜 Detailný článok

Použitá knižnica: ESPAsyncWebServer

Bezpečnosť: provisioning AP má časový limit 10 minút

Možnosť doplniť WPA2-Enterprise

Podpora fallback režimu, ak sa zariadenie 5× nepripojí

💡 Tipy a poznámky

Pre produkciu odporúčame QR-kód pre rýchly onboarding.

Do UI pridať test spojenia na server.

Po provisioning režime vypnúť AP pre úsporu energie.

✅ Hodnota / Zhrnutie
Spoľahlivý spôsob, ako rýchlo a bezpečne pripojiť zariadenie do ľubovoľnej Wi-Fi siete bez servisného zásahu.