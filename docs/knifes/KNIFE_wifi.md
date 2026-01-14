---
id: "KNIFE-20260114-005"
guid: "cad7da80-72af-4fdb-9ca3-2decb3b8b840"
dao: "knife"
title: "Knowledge Contribution"
author: "Peter Bartoš"
category: "deliverable"
type: "knowledge-contribution"
priority: "high"
tags: ["ESP32", "WiFi", "Arduino", "Network", "HTTP", "TCP"]
slug: "esp32-wifi-tutorial"
created: "2026-01-14"
modified: "2026-01-14"
status: "draft"
# ⚖️ IP rights
rights_holder_content: "Peter Bartoš"
rights_holder_system: "Roman Kazička (CAA/KNIFE/LetItGrow)"
license: "CC-BY-NC-SA-4.0"
disclaimer: "Use at your own risk. Methods provided as-is; participation is voluntary and context-aware."
locale: "sk"
---

[🏠 Domov](../index.md) · [⬅️ Nahor](./index.md)

# Knowledge Contribution

## Názov
ESP32 Wi‑Fi: pripojenie, klient/server, skenovanie sietí a spoľahlivé znovunapájanie

## 🎯 Čo rieši (účel, cieľ)
Návod ukazuje, ako na ESP32 vytvoriť Wi‑Fi pripojenie v režime **station (STA)**, založiť **HTTP/TCP server**, používať **WiFiClient** na odosielanie požiadaviek, skenovať dostupné siete, riešiť **znovupripojenie** a nastaviť **statickú IP**, **mDNS** a **režimy úspory energie**.

## 🧩 Ako to rieši (princíp)
ESP32 má integrované Wi‑Fi 2.4 GHz (802.11 b/g/n). V Arduino core poskytuje knižnice `WiFi.h`, `WiFiClient`, `WiFiServer` a `WebServer`/`ESPAsyncWebServer`.

## 🧪 Ako to použiť (aplikácia)
- **STA pripojenie**: pripoj sa k AP, čakaj na `WL_CONNECTED` a publikuj IP.
- **HTTP server**: obslúž GET/POST endpointy.
- **Klient**: odošli HTTP požiadavku na REST API.
- **Sken sietí**: vyber najsilnejší SSID.
- **Spoľahlivosť**: watchdog a automatické reconnect.

---

## ⚡ Rýchly návod (Top)
```cpp
#include <WiFi.h>
const char* SSID = "TvojeSSID";
const char* PASS = "TvojeHeslo";

void setup(){
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);
  Serial.print("Pripajam sa");
  while (WiFi.status()!=WL_CONNECTED){ Serial.print('.'); delay(500);} 
  Serial.print("
IP: "); Serial.println(WiFi.localIP());
}
void loop(){ }
```

## 📜 Detailný článok
#### 1) Station mód + robustné pripojenie
```cpp
#include <WiFi.h>
const char* SSID = "TvojeSSID";
const char* PASS = "TvojeHeslo";
unsigned long lastTry = 0; 

void connectWifi(){
  if(WiFi.status()==WL_CONNECTED) return;
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);
  Serial.print("WiFi: ");
  for(int i=0;i<30 && WiFi.status()!=WL_CONNECTED;i++){ Serial.print('.'); delay(500);} 
  if(WiFi.status()==WL_CONNECTED){
    Serial.printf("
Pripojeny, IP: %s
", WiFi.localIP().toString().c_str());
  } else {
    Serial.println("
Nepripojene");
  }
}

void setup(){ Serial.begin(115200); connectWifi(); }
void loop(){
  if(WiFi.status()!=WL_CONNECTED && millis()-lastTry>5000){ lastTry=millis(); connectWifi(); }
}
```

#### 2) Jednoduchý HTTP server (WebServer)
```cpp
#include <WiFi.h>
#include <WebServer.h>
const char* SSID = "TvojeSSID";
const char* PASS = "TvojeHeslo";
WebServer server(80);

void setup(){
  Serial.begin(115200);
  WiFi.mode(WIFI_STA); WiFi.begin(SSID, PASS);
  while(WiFi.status()!=WL_CONNECTED){ delay(300);} 
  server.on("/", [](){ server.send(200, "text/plain", "OK"); });
  server.on("/status", [](){
    String j = String("{"ip":"") + WiFi.localIP().toString() + ""}";
    server.send(200, "application/json", j);
  });
  server.begin();
  Serial.println("HTTP server bezi na "+WiFi.localIP().toString());
}
void loop(){ server.handleClient(); }
```

#### 3) HTTP klient (GET na REST API)
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
const char* SSID = "TvojeSSID"; const char* PASS = "TvojeHeslo";

void setup(){
  Serial.begin(115200);
  WiFi.begin(SSID,PASS); while(WiFi.status()!=WL_CONNECTED) delay(200);
  HTTPClient http; http.begin("http://example.com/api/health");
  int code = http.GET();
  Serial.printf("HTTP %d
", code);
  if(code>0){ Serial.println(http.getString()); }
  http.end();
}
void loop(){}
```

#### 4) Skenovanie sietí a výber najlepšej
```cpp
#include <WiFi.h>
void setup(){
  Serial.begin(115200); WiFi.mode(WIFI_STA);
  int n = WiFi.scanNetworks();
  for(int i=0;i<n;i++){
    Serial.printf("%2d: %s	RSSI:%d	%s
", i, WiFi.SSID(i).c_str(), WiFi.RSSI(i), WiFi.encryptionType(i)==WIFI_AUTH_OPEN?"open":"secured");
  }
}
void loop(){}
```

#### 5) Statická IP + mDNS + úspora energie
```cpp
#include <WiFi.h>
#include <ESPmDNS.h>
IPAddress local(192,168,1,50), gateway(192,168,1,1), mask(255,255,255,0);
void setup(){
  Serial.begin(115200);
  WiFi.config(local, gateway, mask);
  WiFi.begin("SSID","PASS"); while(WiFi.status()!=WL_CONNECTED) delay(200);
  if(MDNS.begin("moje-esp32")) Serial.println("mDNS: http://moje-esp32.local");
  // úspora: modem sleep
  WiFi.setSleep(true); // pre periodické merania
}
void loop(){}
```


## 💡 Tipy a poznámky
- **Stabilita**: Pridaj watchdog a retry backoff (napr. exponenciálne). Pri častom reconnect skontroluj napájanie (aspoň 500 mA špičkovo).
- **Bezpečnosť**: Vyhýbaj sa plain HTTP pre citlivé dáta; pre TLS môžeš použiť `WiFiClientSecure`.
- **OTA**: Pre vzdialené aktualizácie využi `ArduinoOTA`.
- **Výkon**: Obmedzuj blokujúce operácie v `loop()`; WebServer spracuj čo najkratšie alebo použi asynchrónny server.

## ✅ Hodnota / Zhrnutie
Rýchly recept na Wi‑Fi komunikáciu s ESP32: robustné STA pripojenie, jednoduchý HTTP server, klient na volanie API, skenovanie sietí a doplnky (statická IP, mDNS, šetrenie energie).

---

# 📚 Knowledge Contribution

## 🔖 Názov a stručný popis
ESP32 Wi‑Fi: od pripojenia k sieti po HTTP server/klienta s dôrazom na spoľahlivosť.

## 🗂️ Taxonómia KNIFE
- **Kategória:** IoT, Embedded, Networking
- **Typ:** Návod
- **Tagy:** ESP32, WiFi, Arduino, HTTP, TCP, mDNS, OTA

## 📜 Obsah
- STA pripojenie a reconnect
- HTTP server a klient
- Skenovanie sietí
- Statická IP, mDNS, úspora energie

## 🌍 Referencie
- [Arduino-ESP32 Wifi](https://randomnerdtutorials.com/esp32-wifi/)
- [WiFi.h documentation](https://www.arduino.cc/reference/en/libraries/wifi/)

---

[🏠 Domov](../index.md) · [⬅️ Nahor](./index.md)