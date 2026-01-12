
# ESP32 Air Quality Monitor (AHTX0 + ENS160) → Flask + SQLite Web UI

A complete, end‑to‑end project to measure **CO₂ equivalent (eCO₂)**, **Air Quality Index (TVOC/eCO₂ based)**, **temperature**, and **humidity** using an **ESP32** with **AHTX0** and **ENS160** sensors. The device connects to Wi‑Fi, renders live values on an I²C display, and periodically sends readings to a Python **Flask** server. The server stores data in **SQLite** and serves a responsive web UI (desktop & mobile) to view historical and live air quality. User can view its sensor's data anytime.

---

## Table of Contents
- Features
- Hardware
- Wiring
- Firmware (ESP32 Arduino)
- Server (Flask + SQLite)
- Database Schema

---

## Features
- ESP32 reads **AHTX0** (temperature & humidity) and **ENS160** (TVOC, eCO₂, AQI)
- Sends JSON measurements via HTTP to Flask server over Wi‑Fi
- Local I²C display (e.g., SSD1306 128×64 OLED) shows current values
- Historical charts & latest readings in a responsive web UI (PC/mobile)
- Data stored in SQLite; easy export and backup

> **Note:** ENS160 reports **TVOC** and **eCO₂**; AQI is derived from sensor-computed index. AHTX0 provides temperature and relative humidity.

---

## Hardware
- **Microcontroller:** ESP32 DevKit (e.g., DOIT ESP32 DEVKIT V1)
- **Sensors:**
  - **AHTX0** (I²C) — temp & humidity
  - **ENS160** (I²C) — TVOC, eCO₂, AQI
- **Display (optional):** SSD1306 128×64 OLED (I²C)
- **Power:** 5V via USB or regulated supply
- **Cables:** Dupont wires; ensure 3.3V sensor compatibility

---

## Wiring
All devices on **I²C** bus (ESP32 default: `SDA=GPIO21`, `SCL=GPIO22`).

| Component | Pin | ESP32 |
|---|---|---|
| SENSOR | VIN | VIN |
| SENSOR | GND | GND |
| SENSOR | SDA | GPIO21 |
| SENSOR | SCL | GPIO22 |


---

## Firmware (ESP32 Arduino)
### Libraries
Install via **Arduino Library Manager**:
- **Adafruit AHTX0** (for AHTX0)
- **Adafruit Unified Sensor** (dependency)
- **ENS160** (Sparkfun/Arduino-ENS160*)
- **Adafruit SSD1306** and **Adafruit GFX** (for OLED)
- **ArduinoJSON** (requests via json to server)

---

## Server (Flask + SQLite)
The server is built using **Flask** and stores data in **SQLite**. It provides REST endpoints for ingesting sensor data and retrieving it for visualization.

### Key Responsibilities:
- Accept sensor data via HTTP POST requests
- Maintain user and sensor mapping
- Provide endpoints for real-time and historical data queries
- Serve a responsive web UI for monitoring

### Example Endpoints:
- `GET /health` — Check server health
- `POST /send-data` — Sensor sends latest data to server
- `GET /read-data` — Get sensor data of user and date (and additional possible params)
- `GET /visualize-data` - Renders data to user (based on date, and additional possible params) 

---

## Database Schema
The SQLite database consists of two tables:

### 1. `users`
Stores user information and sensor association.
| Column        | Type    | Description                  |
|---------------|---------|-----------------------------|
| id            | INTEGER | Primary key                |
| serial_number | TEXT    | Unique identifier for user |

### 2. `sensor_realtime`
Stores the latest sensor readings for each user.
| Column      | Type    | Description                          |
|-------------|---------|-------------------------------------|
| id          | INTEGER | Primary key                        |
| user_id     | INTEGER | Foreign key referencing `users.id` |
| temperature | REAL    | Temperature in °C                  |
| humidity    | REAL    | Humidity in %                      |
| aqi         | INTEGER | Air Quality Index                  |
| co2         | REAL    | CO₂ concentration (ppm)            |
| tvoc        | REAL    | Total Volatile Organic Compounds   |
| timestamp   | INTEGER | Unix timestamp of the reading      |

---
