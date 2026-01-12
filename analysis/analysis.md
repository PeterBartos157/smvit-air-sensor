# Analýza projektu KNIFE – Stolové zariadenie na monitorovanie kvality vzduchu

## 1. Analýza problému a potrieb

### Identifikovaný problém
V pracovných a obytných priestoroch často chýba lokálne, okamžité a zrozumiteľné monitorovanie kvality vzduchu, najmä hladiny kyslíka (O₂). Používatelia sa spoliehajú na subjektívne pocity (únava, bolesť hlavy), ktoré sa objavujú až pri zhoršených podmienkach.

### Potreby používateľa
- okamžitá vizuálna spätná väzba bez nutnosti aplikácie  
- dlhodobý záznam a analytika dát  
- automatické upozornenia pri prekročení prahov  
- jednoduchá inštalácia a prevádzka  
- spoľahlivá funkcia aj pri výpadku siete  

### Záver
Projekt KNIFE reaguje na reálnu potrebu zlepšenia pracovného komfortu a bezpečnosti pomocou kombinácie lokálneho IoT zariadenia a centrálnej analytickej infraštruktúry.

---

## 2. Analýza navrhnutého riešenia

### Architektúra systému
Riešenie je navrhnuté ako viacvrstvová architektúra:

- **Edge vrstva** – zariadenie s ESP32 a senzormi  
- **Komunikačná vrstva** – zabezpečený prenos dát cez HTTPS (REST API)  
- **Serverová vrstva** – databáza, analytické pravidlá, notifikácie  
- **Prezentačná vrstva** – webový dashboard  

### Hodnotenie architektúry
| Vrstva | Hodnotenie |
|------|-----------|
| Edge zariadenie | nízka latencia, lokálna signalizácia |
| Komunikácia | jednoduchá, rozšíriteľná |
| Server | vhodný pre časové rady |
| UX | okamžitá aj historická spätná väzba |

### Silné stránky návrhu
- fungovanie lokálnej signalizácie bez internetu  
- modulárnosť a možnosť rozšírenia  
- jasne definované rozhrania (API)  

---

## 3. Analýza hardvéru (KNIFE #1)

### Použité komponenty
- mikrokontrolér ESP32 s integrovaným Wi-Fi  
- O₂ senzor (elektrochemický alebo optický)  
- senzor teploty a vlhkosti (napr. SHT31)  
- LED indikátory a napájacie obvody  

### Riziká a obmedzenia
| Riziko | Dopad | Riešenie |
|------|------|---------|
| Drift O₂ senzora | znížená presnosť | pravidelná kalibrácia |
| Šum ADC | falošné alarmy | RC filter + softvérové filtre |
| Tepelné rušenie | skreslené merania | oddelenie senzorovej časti |

### Záver
Hardvérový návrh je realistický, ekonomický a vhodný pre prototyp aj malú sériu zariadení.

---

## 4. Analýza firmvéru (KNIFE #2)

### Spracovanie nameraných dát
Firmware:
- periodicky číta hodnoty senzorov  
- aplikuje low-pass filter  
- vypočítava moving average  
- validuje extrémne alebo chybné hodnoty  

### Rozhodovanie a signalizácia
- **OK stav** – zelená LED  
- **Varovanie** – žltá LED  
- **Kritický stav** – červená LED + bzučiak  

Prahový model je jednoduchý, deterministický a ľahko vysvetliteľný používateľovi.

### Odolnosť systému
- lokálne alarmy pri výpadku siete  
- bufferovanie dát pri strate pripojenia  
- oddelenie modulov (senzory, Wi-Fi, logika)  

---

## 5. Analýza serverovej časti a dát

### Dátový model
- **devices** – evidencia zariadení  
- **readings** – časové rady meraní  
- **alerts** – zaznamenané upozornenia  

Model je vhodný pre časové databázy a analytické spracovanie.

### Analytické funkcie
- porovnávanie s prahovými hodnotami  
- výpočet kĺzavých priemerov  
- generovanie upozornení (email, dashboard)  

### Bezpečnosť
- HTTPS (TLS) komunikácia  
- API kľúče alebo JWT  
- validácia a rate-limiting požiadaviek  

---

## 6. Analýza obalu a mechanického dizajnu (KNIFE #4)

### Funkčné požiadavky
- dostatočné prúdenie vzduchu  
- oddelenie senzorov od tepelného zdroja  
- viditeľnosť LED indikácie  
- jednoduchá montáž a servis  

### Materiály a konštrukcia
- PLA pre prototypy  
- PETG alebo drevo pre finálnu verziu  
- ventilačné štrbiny a perforácia  

### Riziká
- akumulácia tepla  
- zhoršené prúdenie vzduchu  
- vplyv obalu na presnosť merania  

Tieto riziká sú riešiteľné iteratívnym prototypovaním.

---

## 7. SWOT analýza

### Strengths (Silné stránky)
- jasne definovaný problém  
- kompletné end-to-end riešenie  
- okamžitá lokálna spätná väzba  
- nízke hardvérové náklady  

### Weaknesses (Slabé stránky)
- nutnosť pravidelnej kalibrácie  
- obmedzená životnosť O₂ senzora  
- závislosť presnosti od mechanického dizajnu  

### Opportunities (Príležitosti)
- rozšírenie o ďalšie senzory (CO₂, VOC)  
- integrácia do smart office systémov  
- open-source alebo komunitný rozvoj  

### Threats (Hrozby)
- lacné komerčné riešenia  
- legislatívne a certifikačné požiadavky  
- degradácia senzorov v čase  

---

## 8. Celkové zhodnotenie

Projekt KNIFE predstavuje technicky realistické a prakticky využiteľné IoT riešenie, ktoré kombinuje lokálne meranie kvality vzduchu s centrálnou analytikou. Architektúra je modulárna, škálovateľná a vhodná ako základ pre študentský projekt, MVP produktu alebo ďalší výskum v oblasti IoT a monitorovania prostredia.
