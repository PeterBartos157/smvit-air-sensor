KNIFE #1 — Výber senzorov a hardware architektúry

🎯 Čo rieši (účel, cieľ)
Určiť optimálnu kombináciu senzorov a mikrokontroléra pre meranie O₂, teploty a vlhkosti tak, aby boli spoľahlivé, energeticky efektívne a kompatibilné s Wi-Fi komunikáciou. Cieľom je vytvoriť stabilný hardvérový základ celého systému.

🧩 Ako to rieši (princíp)
Hardvérová architektúra používa ESP32 ako hlavný mikrokontrolér, ktorý poskytuje:

Wi-Fi pripojenie

dostatok ADC/I2C rozhraní

dobrú energetickú efektivitu
Pre meranie:

O₂ senzor (elektrochemický alebo optický, najčastejšie I2C alebo analóg)

Teplota/vlhkosť (SHT31, DHT22 alebo podobné)

Napäťová stabilizácia + ochranné obvody
Senzory sú integrované do PCB alebo perforovaného modulu s vhodným umiestnením kvôli prúdeniu vzduchu.

🧪 Ako to použiť (aplikácia)

Vybrať konkrétny model O₂ senzora podľa presnosti a dlhodobej stability.

Navrhnúť pin-maping v Eagle/KiCad.

Otestovať čítanie hodnôt cez jednoduchý Arduino sketch.

Zmerať drift a reakčný čas senzorov.

Overiť kompatibilitu s napájaním a Wi-Fi modulom.

⚡ Rýchly návod (Top)

ESP32 DevKitC

O₂ senzor: MiCS-6814 alebo ZE03-O2

Temp/Hum: SHT31 (I2C)

Testovať hodnoty v sériovom monitore

Skontrolovať šum a stabilitu

📜 Detailný článok
Pinová architektúra:

I2C bus pre SHT31

ADC vstup pre O₂ analóg

LED indikátory priamo z GPIO (cez rezistory)

Micro-USB pre napájanie a programovanie

Prečo ESP32?

Má integrované Wi-Fi

Nižšia cena než kombinácia Arduino + Wi-Fi shield

Podpora OTA firmware

Testovací firmware:

meranie každých 200 ms

výpis na sériovú linku

porovnanie s externým meracím zariadením

💡 Tipy a poznámky

Elektrochemické O₂ senzory môžu mať životnosť ~24 mesiacov.

I2C senzory potrebujú správne pull-up rezistory.

ESP32 má citlivé ADC – vhodné je pridať RC filter.

✅ Hodnota / Zhrnutie
Táto KNIFE definuje celý HW základ. Umožní vám budovať firmware a server s istotou, že vstupné dáta sú stabilné a presné.