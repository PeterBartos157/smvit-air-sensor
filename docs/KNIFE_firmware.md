KNIFE #2 — Firmware: meranie, filtrovanie a prahové hodnoty

🎯 Čo rieši (účel, cieľ)
Návrh firmvéru, ktorý spoľahlivo odčíta hodnoty senzorov, aplikuje filtre a rozhoduje o LED indikácii kvality vzduchu.

🧩 Ako to rieši (princíp)
Firmware v cykle:

prečíta O₂, teplotu a vlhkosť

aplikuje low-pass filter na zníženie šumu

vypočíta moving average

porovná hodnoty s prahmi:

OK → zelená

varovanie → žltá

kritické → červená + bzučiak

🧪 Ako to použiť (aplikácia)

Kalibrácia O₂ senzora po zapnutí (30–60 sekúnd).

Prahy napr. O₂ < 19.5% = VAROVANIE, < 18% = KRITIKA.

Upload firmvéru cez Arduino IDE alebo PlatformIO.

⚡ Rýchly návod (Top)

o2 = read_o2();
filtered = alpha*o2 + (1-alpha)*prev;
if (filtered < WARN) led_yellow();
if (filtered < CRIT) led_red();


📜 Detailný článok
Filtrovanie:
Použitý low-pass filter:

filtered = filtered_prev * 0.8 + new_value * 0.2


Priemerovanie:
Moving average z posledných N hodnôt pre stabiln cieľ.
Zvládanie šumu:

analyzovali sme jitter

pridali sme 50 ms settle time po čítaní senzora
Spracovanie chýb:
Ak senzor vráti NAN alebo extrémnu hodnotu → ignorovať.

💡 Tipy a poznámky

LED prebliknutie každých X sekúnd môže indikovať heartbeat.

Pri testovaní ukladať logy na UART.

Odporúčame oddeliť modul sensors.cpp od wifi.cpp.

✅ Hodnota / Zhrnutie
Tento KNIFE popisuje robustný firmware pipeline, ktorý zaručuje presné dáta a spoľahlivé správanie LED indikácie.