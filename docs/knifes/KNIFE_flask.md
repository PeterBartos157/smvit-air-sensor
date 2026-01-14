---
id: "KNIFE-20260114-003"
guid: "7b3f9a0f-4d9c-4b7a-9b0a-1c6d3e2f8c55"
dao: "knife"
title: "Knowledge Contribution"
author: "Peter Bartoš"
category: "deliverable"
type: "knowledge-contribution"
priority: "high"
tags: ["python", "flask", "api", "backend", "rest", "tutorial"]
slug: "python-flask-api-tutorial"
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
Python Flask API Tutorial: základný server, GET a POST endpointy

## 🎯 Čo rieši (účel, cieľ)
Rýchly návod, ako vytvoriť minimalistické REST API vo Flaske – od inštalácie, cez štruktúru projektu, spustenie servera, až po implementáciu GET/POST endpointov s JSON odpoveďami a jednoduchou validáciou.

## 🧩 Ako to rieši (princíp)
Využijeme ľahký mikroframework **Flask**, ktorý umožňuje definovať routy pomocou dekorátorov, parsovať JSON zo žiadosti a vracať štruktúrované odpovede s HTTP kódmi. Pre lokálny vývoj použijeme `venv` a pre nasadenie tipy na `gunicorn` + reverzný proxy.

## 🧪 Ako to použiť (aplikácia)
- Vytvor virtuálne prostredie, nainštaluj Flask a spusti server.
- Definuj GET/POST endpointy (napr. `/health`, `/api/items`).
- Pridaj validáciu vstupu a ošetrenie chýb.
- (Voliteľne) Povoľ CORS pre volania z frontendu.

---

## ⚡ Rýchly návod (Top)

Vytvorenie virtuálneho prostredia pre python, nainštalovanie knižnice Flask a spustenie servera.
```bash
# 1) Projekt a venv
mkdir flask-api && cd flask-api
python3 -m venv .venv && source .venv/bin/activate

# 2) Inštalácia
pip install Flask
```

Súbor aplikácie obsahujúci server API rozhranie:
```python
echo 'from flask import Flask, request, jsonify
app = Flask(__name__)

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/api/items")
def list_items(): return jsonify([{"id":1,"name":"foo"}])

@app.post("/api/items")
def create_item():
    data = request.get_json(force=True, silent=True) or {}
    if "name" not in data: return {"error":"name is required"}, 400
    return {"id":2, "name":data["name"]}, 201

if __name__ == "__main__":
    app.run(debug=True)' > app.py

# Spustenie servera
python app.py
```

## 📜 Detailný článok

#### 1. Štruktúra projektu  
flask-api/  
├─ .venv/  
├─ app.py  
├─ requirements.txt  
└─ README.md  

(voliteľne rozšíriteľné o src/, blueprints/, tests/ atď.)

#### 2. Základný server (app.py)
```python

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok", "service": "flask-api"}, 200

@app.get("/api/items")
def list_items():
    items = [
        {"id": 1, "name": "foo"},
        {"id": 2, "name": "bar"},
    ]
    return jsonify(items), 200

@app.post("/api/items")
def create_item():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    if not name or not isinstance(name, str):
        return {"error": "Field 'name' is required (string)."}, 400
    # v reále by tu bol zápis do DB; teraz vrátime mock
    new_item = {"id": 3, "name": name}
    return new_item, 201

@app.errorhandler(404)
def not_found(e):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def server_error(e):
    return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

#### 3. Testovanie cez curl

```bash
# Healthcheck
curl -s http://localhost:5000/health | jq

# GET zoznamu
curl -s http://localhost:5000/api/items | jq

# POST vytvorenia
curl -s -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"sensor-a"}' | jq

# Chybný POST (validácia)
curl -s -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{}' | jq
```

#### 4. CORS (ak voláš z frontendu)

```bash
pip install flask-cors
```

```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})  # pre dev; v prod zúž na konkrétne domény
```

#### 5. Konfigurácia a premenné prostredia

```python
import os
app.config["ENVIRONMENT"] = os.getenv("ENV", "development")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
```
Spúšťaj s:
```bash
ENV=production SECRET_KEY="change-me" python app.py
```

#### 6. Requirements a zamrazenie verzií

```bash
pip freeze > requirements.txt
```

#### 7. Nasadenie (stručne)

- **Gunicorn:** pip install gunicorn → gunicorn -w 2 -b 0.0.0.0:8000 app:app
- Pred Gunicorn daj reverznú proxy (napr. Nginx) a zapni logovanie/monitoring.
- Pre kontajner: priprav Dockerfile s gunicorn (voliteľne pridám na požiadanie).


## 💡 Tipy a poznámky

- Vždy vracaj správne HTTP kódy (200, 201, 400, 404, 500).
- Pre väčšie API rozdeľ kód do Blueprints.
- Schema validácia: pip install pydantic alebo marshmallow pre robustnejšiu validáciu.
- Bezpečnosť: sanitizácia vstupov, rate limiting, autentifikácia (napr. JWT).
- Testing: pytest + Flask test client pre unit/integration testy.

## ✅ Hodnota / Zhrnutie
Minimálny, ale produkčne smerovateľný základ pre Flask API: jasná štruktúra, GET/POST, error handling, CORS, a návod na lokálny beh aj nasadenie.

## 📚 Knowledge Contribution
### 🔖 Názov a stručný popis

Návod na vytvorenie jednoduchého REST API vo Flaske (GET/POST), s tipmi na validáciu, CORS a nasadenie.

### 🗂️ Taxonómia KNIFE
- Kategória: Backend, Web Development
- Typ: Návod
- Tagy: Flask, Python, REST, API, CORS, Gunicorn

## 📜 Obsah
Krok-za-krokom postup od inštalácie po spustenie a testovanie API, vrátane kódu.

## 🌍 Referencie

- [Dokumentácia Flask](https://flask.palletsprojects.com/)  
- [Flask-CORS](https://flask-cors.readthedocs.io/)

---

[🏠 Domov](../index.md) · [⬅️ Nahor](./index.md)