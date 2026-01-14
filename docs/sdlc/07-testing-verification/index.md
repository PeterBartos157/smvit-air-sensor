# 07-Testing & Verification

## Metodika testovania

Na overenie presnosti meraní sme vykonali dlhodobý test v reálnych podmienkach:

- Trvanie: 8 dní
- Miesto: internátna izba (stabilné prostredie)
- Rozdelenie testu:
  - 4 dni senzor bez krytu (voľný prístup vzduchu)
  - 4 dni senzor v drevenej krabičke (obmedzený prietok vzduchu)

Cieľom bolo zistiť, ako púzdro ovplyvňuje presnosť meraní teploty, vlhkosti a kvality vzduchu (CO₂, TVOC).

---

### Výsledky bez krytu

<figure>
  <img src="../../images/data_before.png" alt="data before" width="700" />
  <figcaption>Obr.:  Hodnoty teploty a vlhkosti sú pomerne presné a stabilné. Hodnoty oxidu uhličitého (eCO₂) sú primerané, bez výrazných odchýlok.</figcaption>
</figure>
  

#### Pozorovania:

- Teplota: stabilná, zodpovedá reálnym podmienkam.
- Vlhkosť: presná, bez výrazných výkyvov.
- eCO₂: hodnoty primerané, korelujú s počtom osôb v miestnosti.

---

### Výsledky s krytom

<figure>
  <img src="../../images/data_after.png" alt="data after" width="700" />
  <figcaption>Obr.:  Hodnoty teploty sú značne zvýšené (v priemere o +4 °C). Vlhkosť ostáva rovnaká. Hodnoty eCO₂ sú zvýšené (v priemere o +300 ppm).</figcaption>
</figure>


#### Pozorovania:

- Teplota: zvýšená o 4 °C v priemere → dôvodom je nedostatočné odvetranie krabičky.
- Vlhkosť: prakticky nezmenená.
- eCO₂: zvýšené hodnoty o ~300 ppm, čo naznačuje slabú výmenu vzduchu.


## Analýza dopadu

- Krabička nedodáva senzoru dostatočnú výmenu vzduchu.
- Zariadenie sa mierne prehrieva, čo skresľuje merania teploty.
- Nedostatočný prietok vzduchu spôsobuje vyššie koncentrácie CO₂ a TVOC v púzdre.
- Presnosť meraní je ovplyvnená najmä pri dlhodobom uzavretí senzora.


## Odporúčania na zlepšenie

- Pridať ventilačné otvory alebo mriežky na zabezpečenie prúdenia vzduchu.
- Optimalizovať vnútorné usporiadanie komponentov, aby sa minimalizovalo prehrievanie.
- Použiť materiál s lepšou tepelnou vodivosťou alebo implementovať pasívne chladenie.
- Kalibrácia senzorov po vložení do púzdra.

<!-- - [Test report a QA výstupy](./test-report.md) -->

**Navigation:** [⬆️ SDLC](../index.md) · [⬅️ Projekt](../../index.md)
