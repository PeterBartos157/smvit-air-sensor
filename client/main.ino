// ----------------- WHOLE FUNCTIONALITY - SENSOR READING, SENDING DATA TO SERVER ----------------------- //

// Network
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
// Wiring
#include <Wire.h>
// Sensors
#include <Adafruit_AHTX0.h>
#include <SparkFun_ENS160.h>
// Display
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ---- Serial number ----
# define SERIAL_NUMBER "A9F3D72C1B84E65F0C2A7B9E4D81F630"
// ---- Display settings ----
#define OLED_MEM_ADDR 0x3C
#define SCREEN_WIDTH   128
#define SCREEN_HEIGHT   64
#define OLED_RESET      -1 // Reset pin not used
#define TEMP_ADJUSTMENT -5
// ---- Display object ----
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
// ---- Sensor objects ----
Adafruit_AHTX0 aht; // Temperature & humidity
SparkFun_ENS160 ens; // Air quality - co2
// ---- Sensor read & sent timestamps ----
unsigned long lastSensorReadTime = 0;
unsigned long lastSendTime = 0;
// ---- Intervals in milliseconds ----
const unsigned long SENSOR_INTERVAL = 5000;
const unsigned long SEND_INTERVAL = 1 * 60 * 1000;
// ---- Error codes ----
int ERROR_CODE = 0; // 1 - wifi error, 2 - server error
// ---- Blue LED ----
int ESP32_LED = 2;
// ---- WiFi credentials ----
const char* SSID = "Hotspot";
const char* PASSWORD = "smvit12345";
// ---- Server endpoint ----
// const char* HEALTH_CHECK_URL = "http://192.168.137.1:5000/health";
// const char* SEND_DATA_URL = "http://192.168.137.1:5000/send-data";
const char* HEALTH_CHECK_URL = "https://smvit-super-server-hvash7e3dfe6drcb.polandcentral-01.azurewebsites.net/health";
const char* SEND_DATA_URL = "https://smvit-super-server-hvash7e3dfe6drcb.polandcentral-01.azurewebsites.net/send-data";

// Make http request to server for health check
void serverHealthCheck() {
    // Init http request
    HTTPClient http;
    http.begin(HEALTH_CHECK_URL);
    http.addHeader("Content-Type", "application/json");
    // Send the request
    int httpResponseCode = http.GET();
    // Handling response for request
    if (httpResponseCode > 0) {
      ERROR_CODE = 0;
      Serial.print("Server response code: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println("Response: " + response);
    } else {
      ERROR_CODE = 2;
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    // Close http request
    http.end();
}

// Function to write message to display
void displayMessage(const String &text) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("---- Air Sensor ----");
  display.println("--------------------");
  display.println(text);
  display.display();
}

// the setup function runs once when you press reset or power the board
void setup() {
  // Init serial monitor baud
  Serial.begin(115200);
  delay(1000);
  // starting I²C
  Wire.begin(21, 22); // SDA=GPIO21, SCL=GPIO22 (our ESP32 pins)
  // Initialize OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_MEM_ADDR)) {
    Serial.println("SSD1306 allocation failed!");
    while (1);
  }
  delay(500);
  // Write to display
  Serial.println("Booting ESP32...");
  displayMessage("Booting...");
  delay(1000);
  // Connect to WiFi
  displayMessage("Connecting to WiFi...");
  Serial.print("Connecting to WiFi.");
  WiFi.begin(SSID, PASSWORD);
  // Keep trying to connect
  int maxAttempts = 10;
  int attempt = 0;
  while (WiFi.status() != WL_CONNECTED && attempt < maxAttempts) {
    delay(1000);
    Serial.print(".");
  }
  // Logs
  Serial.println("\nConnected to WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  displayMessage("Connected to WiFi!");
  delay(500);
  // Health check of the server
  if (WiFi.status() == WL_CONNECTED) {
    serverHealthCheck();
  // Got disconnected from WiFi for some reason
  } else {
    ERROR_CODE = 1;
    Serial.println("Not connected to WiFi or disconnected!");
    displayMessage("Server health check failed!");
  delay(500);
  }
  // Initialize digital pin LED_BUILTIN
  pinMode(ESP32_LED, OUTPUT);
  // Initialize AHT21 (Temperature & Humidity Sensor)
  if (!aht.begin()) {
    Serial.println("Failed to find AHT21 sensor!");
    displayMessage("Failed to find AHT21 sensor!");
    while (1) delay(10);
  }
  Serial.println("AHT21 initialized.");
  displayMessage("Sensors initialized.");
  delay(500);
  // Initialize ENS160
  if (!ens.begin(0x53)) { // Official ENS160 address
    Serial.println("Failed to initialize ENS160 sensor!");
    displayMessage("Failed to find ENS160 sensor!");
    while (1) delay(10);
  }
  Serial.println("ENS160 initialized.");
  // Reset the indoor air quality sensor's settings.
  ens.setOperatingMode(SFE_ENS160_RESET);
  delay(100);
  // Set to standard operation
  // Others include SFE_ENS160_DEEP_SLEEP and SFE_ENS160_IDLE
  ens.setOperatingMode(SFE_ENS160_STANDARD);
  // There are four values here: 
  // 0 - Operating ok: Standard Operation
  // 1 - Warm-up: occurs for 3 minutes after power-on.
  // 2 - Initial Start-up: Occurs for the first hour of operation.
  //												and only once in sensor's lifetime.
  // 3 - No Valid Output
  delay(500);
}

// Heart beat LED signal
void successSignal() {
  digitalWrite(ESP32_LED, HIGH);
  delay(250);
  digitalWrite(ESP32_LED, LOW);
  delay(150);
  digitalWrite(ESP32_LED, HIGH);
  delay(250);
  digitalWrite(ESP32_LED, LOW);
  delay(1000);
}

// Failure LED signal - medium turn on and off
void errorWifiSignal() {
  digitalWrite(ESP32_LED, HIGH);
  delay(500);
  digitalWrite(ESP32_LED, LOW);
  delay(500);
}

// Failure LED signal - slow turn on and off
void errorHttpSignal() {
  digitalWrite(ESP32_LED, HIGH);
  delay(1000);
  digitalWrite(ESP32_LED, LOW);
  delay(1000);
}

// Send sensor data to server
void sendDataToServer(float temperature, float humidity, int aqi, int co2, int tvoc) {
  // Prepare JSON data
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["user"] = SERIAL_NUMBER; 
  jsonDoc["temperature"] = temperature;
  jsonDoc["humidity"] = humidity;
  jsonDoc["aqi"] = aqi;
  jsonDoc["co2"] = co2;
  jsonDoc["tvoc"] = tvoc;
  // Serialize json to string
  String jsonString;
  serializeJson(jsonDoc, jsonString);
  // Send data to the server
  if (WiFi.status() == WL_CONNECTED) {
    // Init http request
    HTTPClient http;
    http.begin(SEND_DATA_URL);
    http.addHeader("Content-Type", "application/json");
    // Send the request
    int httpResponseCode = http.POST(jsonString);
    // Handling response for request
    if (httpResponseCode > 0) {
      ERROR_CODE = 0;
      Serial.print("Server response code: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println("Response: " + response);
    } else {
      ERROR_CODE = 2;
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    // Close http request
    http.end();
  // Got disconnected from WiFi for some reason
  } else {
    ERROR_CODE = 1;
    Serial.println("Not connected to WiFi or disconnected!");
  }
}

// Reading the sensor data
void readSensorData(unsigned long currentMillis) {
  // --- Read AHT21 ---
  sensors_event_t hmd, temp;
  aht.getEvent(&hmd, &temp);
  float temperature = temp.temperature + TEMP_ADJUSTMENT;
  float humidity = hmd.relative_humidity;
  // --- Print AHT21 results ---
  Serial.print("Temp: "); Serial.print(temperature); Serial.print(" °C, ");
  Serial.print("Humidity: "); Serial.print(humidity); Serial.println(" %");
  // --- Read ENS160 ---
  int aqi = -1000; // air quality index (1-5)
  int co2 = -1000; // estimated CO2 (ppm)
  int tvoc = -1000; // total VOC [Volatile Organic Compounds] (ppb)
  if( ens.checkDataStatus() ) {
    aqi = ens.getAQI();
    co2 = ens.getECO2();
    tvoc = ens.getTVOC();
    // --- Print ENS160 results ---
    Serial.print("Air Quality Index (1-5): "); Serial.print(aqi); Serial.print(", ");
    Serial.print("eCO2: "); Serial.print(co2); Serial.print(" ppm, ");
    Serial.print("TVOC: "); Serial.print(tvoc); Serial.println(" ppb");
  }
  else {
    Serial.print("Failed to read air quality data!");
  }
  displayMessage(
    "Temperature: " + String(temperature) + "C\nHumidity:    " + String(humidity) +
    "%\nAQI:         " + String(aqi) + "index\nCO2:         " + String(co2) + 
    "ppm\nTVOC:        " + String(tvoc) + "mg/m3"
  );
  // Every 5 minutes also send to server
  if (currentMillis - lastSendTime >= SEND_INTERVAL) {
    Serial.println("Sending sensor data to server...");
    lastSendTime = currentMillis;
    sendDataToServer(temperature, humidity, aqi, co2, tvoc);
  }
}

// the loop function runs over and over again forever
void loop() {
  unsigned long currentMillis = millis();
  // Read sensor data every 5 seconds
  if (currentMillis - lastSensorReadTime >= SENSOR_INTERVAL) {
    lastSensorReadTime = currentMillis;
    readSensorData(currentMillis);
  }
  // Signal the status via LED signaling
  if (ERROR_CODE == 0) {
    successSignal();
  }
  else if (ERROR_CODE == 1) {
    errorWifiSignal();
  }
  else if (ERROR_CODE == 2) {
    errorHttpSignal();
  }
}
