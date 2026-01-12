// ----------------- CHECKING SENSOR ADDRESSES (HARDWARE VERIFICATION) ----------------------- //

#include <Wire.h>

void setup() {
  Serial.begin(115200);
  Serial.println("DEBUG: ESP32 BOOT OK");

  Serial.println("DEBUG: Starting I2C...");
  Wire.begin(21, 22); // SCL=21, SDA=22
  Serial.println("DEBUG: I2C OK");

  delay(1000);
  Serial.println("DEBUG: Scanning I2C...");
}

void loop() {
  byte error, address;
  int nDevices = 0;

  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("DEBUG: I2C device found at 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      nDevices++;
    }
    else if (error==4) {
      Serial.print("Unknown error at 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
    }
  }
  if (nDevices == 0) Serial.println("DEBUG: No I2C devices found");
  else Serial.println("DEBUG: Done scanning iteration");
  delay(5000);
}
