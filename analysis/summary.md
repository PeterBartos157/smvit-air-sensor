
# Summary

## Cieľ 

Vytvoriť kompaktné stolové zariadenie, ktoré meria hladinu kyslíka (O₂), teplotu a ďalšie ukazovatele kvality vzduchu. Údaje odosiela cez Wi-Fi na centrálny REST server, ktorý zabezpečuje analýzu a upozornenia. 

 
 

## Čo bude dodané 

Zabudované senzorické zariadenie 

Hardvér založený na Arduino/ESP platforme. 

Integrovaný senzor O₂ a teplotný senzor. 

Spracovanie dát v reálnom čase. 

Kompaktný drevený alebo 3D-tlačený obal optimalizovaný pre prúdenie vzduchu. 

LED indikátory pre okamžitú vizuálnu spätnú väzbu (farebné zobrazenie úrovne kvality vzduchu). 

Konektivita a firmvér 

Wi-Fi komunikácia pomocou ESP32 alebo podobného modulu. 

Firmvér pokrývajúci odčítanie a kalibráciu senzorov, spracovanie dát a bezpečný prenos. 

Lokálne LED upozornenia pri prekročení prahových hodnôt. 

Server a analytika 

REST API na príjem dát. 

Databáza na ukladanie záznamov. 

Dashboard/API poskytujúci prehľady, trendy a upozornenia. 

Dokumentácia a nasadenie 

Schéma zapojenia, zoznam komponentov. 

Zdrojový kód firmvéru. 

CAD súbory puzdra. 

Inštalačný návod (Wi-Fi pairing, serverové napojenie). 

 
 

## Prečo je tento projekt dôležitý 

Lokálne monitorovanie priamo na úrovni pracovného stola. 

Zlepšuje zdravie, komfort a sústredenie pomocou včasných upozornení. 

Pomáha odhaliť nedostatočné vetranie. 

Umožňuje analytiku v čase a optimalizáciu pracovného prostredia. 

 
 

## Ako to má fungovať 

Senzory merajú v pravidelných intervaloch. 

Lokálna spätná väzba cez LED indikáciu (zelená/žltá/červená). 

Údaje sa bezpečne odosielajú cez REST na centrálny server. 

Server tieto údaje ukladá, spracúva a poskytuje prehľady. 

Dashboard poskytuje historické grafy a upozornenia. 

 
 

## Kedy (časový plán – 14 týždňov) 

1.–3. týždeň: Špecifikácia, výber senzorov, prototyp obalu. 

4.–5. týždeň: Hardvérová montáž, testovanie senzorov. 

6.–7. týždeň: Vývoj firmvéru (komunikácia, spracovanie dát, kalibrácia). 

8.–10. týždeň: Implementácia REST API, serverová infraštruktúra, databáza. 

11.–12. týždeň: Dashboard, vizualizácie, analytické funkcie. 

13. týždeň: Testovanie, ladenie, kalibrácia. 

14. týždeň: Finálny obal, dokumentácia, nasadenie.