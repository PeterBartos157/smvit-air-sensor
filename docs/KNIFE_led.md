KNIFE #78 — LED indikácia a UX pre koncového používateľa

🎯 Čo rieši (účel, cieľ)
Vytvoriť jednoduchý, intuitívny spôsob, ako používateľ okamžite pochopí kvalitu vzduchu.

🧩 Ako to rieši (princíp)
Používa sa LED RGB indikátor:

zelená = OK

žltá = pozor

červená = kritické hodnoty
Prechodové animácie zjemňujú UX (fade-in/out).

🧪 Ako to použiť (aplikácia)

LED na GPIO s PWM

Hysteréza prahov, aby svetlo nepreblikávalo

LED must be visible from user angle

⚡ Rýchly návod (Top)

analogWrite(LED_R, 255);
analogWrite(LED_G, 0);
analogWrite(LED_B, 0);


📜 Detailný článok
Prečo PWM?

Jemné prechody medzi farbami

Nižšia spotreba
Hysteréza:

O₂ LOW → žltá, až keď stúpne o +0.5 → späť na zelenú

💡 Tipy a poznámky

Vyrobiť svetlovod/difúzor pre mäkké svetlo

Testovať viditeľnosť na dennom svetle

✅ Hodnota / Zhrnutie
Svetelná indikácia je najdôležitejší prvok UX. KNIFE definuje pravidlá, ktoré ho robia spoľahlivým.