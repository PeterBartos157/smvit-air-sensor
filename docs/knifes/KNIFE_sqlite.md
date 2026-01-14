---
id: "KNIFE-20260114-SQLITE"
guid: "GENEROVANÝ-GUID"
dao: "knife"
title: "Knowledge Contribution"
author: "Peter Bartoš"
category: "deliverable"
type: "knowledge-contribution"
priority: "high"
tags: ["Python", "SQLite", "Database", "CRUD", "SQL"]
slug: "python-sqlite-tutorial"
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
Python + SQLite: Kompletný tutoriál na prácu s databázou

## 🎯 Čo rieši (účel, cieľ)
Ako efektívne pracovať s SQLite databázou priamo z Pythonu – od vytvorenia databázy, cez CRUD operácie, až po uzatvorenie spojenia.

## 🧩 Ako to rieši (princíp)
SQLite je ľahká embedded databáza, ktorá nevyžaduje server. Python poskytuje vstavaný modul `sqlite3` na komunikáciu s databázou pomocou SQL príkazov.

## 🧪 Ako to použiť (aplikácia)
- Vytvor súbor databázy (.db)
- Pripoj sa cez `sqlite3.connect()`
- Vytvor tabuľku pomocou SQL
- Vykonaj INSERT, SELECT, UPDATE, DELETE
- Uzavri spojenie

---

## ⚡ Rýchly návod (Top)
```python
import sqlite3
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
cursor.execute('INSERT INTO users (name) VALUES (?)', ('Peter',))
conn.commit()
for row in cursor.execute('SELECT * FROM users'):
    print(row)
conn.close()
```

## 📜 Detailný článok

#### 1. Vytvorenie databázy a pripojenie

```python
import sqlite3
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
```

#### 2. Vytvorenie tabuľky

```python

cursor.execute('''CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL
)''')
```

#### 3. Vkladanie dát

```python
cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)', ('Laptop', 999.99))
conn.commit()
```

#### 4. Čítanie dát

```python
cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)', ('Laptop', 999.99))
conn.commit()
```

#### 5. Aktualizácia a mazanie

```python
cursor.execute('UPDATE products SET price = ? WHERE id = ?', (899.99, 1))
cursor.execute('DELETE FROM products WHERE id = ?', (1,))
conn.commit()
```

#### 6. Uzatvorenie spojenia

```python
conn.close()
```
## 💡 Tipy a poznámky

- Používaj ? placeholdery na prevenciu SQL injection.
- Pre komplexnejšie projekty použi ORM (napr. SQLAlchemy).
- SQLite je ideálne pre malé až stredné aplikácie.

## ✅ Hodnota / Zhrnutie
Jednoduchý spôsob, ako spravovať dáta v aplikáciách bez potreby externého DB servera.

## 📚 Knowledge Contribution
### 🔖 Názov a stručný popis
Ako pracovať so SQLite databázou v Pythone pomocou modulu sqlite3.

### 🗂️ Taxonómia KNIFE
- Kategória: Backend, Databázy
- Typ: Návod
- Tagy: Python, SQLite, SQL, CRUD

## 📜 Obsah

- Vytvorenie databázy 
- CRUD operácie
- Uzatvorenie spojenia

## 🌍 Referencie

- [SQLite Python Tutorial](https://www.sqlitetutorial.net/sqlite-python/creating-database/)
- [SQLite Python CRUD Tutorial](https://www.sqlitetutorial.net/sqlite-python/crud/)

---

[🏠 Domov](../index.md) · [⬅️ Nahor](./index.md)