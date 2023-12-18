#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
const int LED_PIN = 2;
const int PIR_PIN = 4;
const int RELAY_PIN = 18;

const char* ssid = "DESKTOP-078BH87";
const char* password = "123456780";
WiFiServer server(80);
void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  digitalWrite(LED_PIN, LOW);
  delay(1000);

  // Kết nối với Wi-Fi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  // Bắt đầu server trên cổng 80
  server.begin();
  Serial.println("Server started");
}

unsigned long startTime = 0;
bool waitStatus = false;
void loop() {
  int motion = digitalRead(PIR_PIN);
  int doorStatus = digitalRead(RELAY_PIN);
  if (motion == HIGH) {
    digitalWrite(LED_PIN, HIGH);
    if (doorStatus == HIGH && waitStatus == false) {
      Serial.println("MOTION");
      waitStatus = true;
    }
  } else {
    digitalWrite(LED_PIN, LOW);
    if (doorStatus == LOW) {
      if (millis() - startTime > 10000) {
        digitalWrite(RELAY_PIN, HIGH);
        Serial.println("CLOSE_DOOR");
        waitStatus = false;
        delay(3000);
      }
    }
  }
  WiFiClient client = server.available();
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        String command = client.readStringUntil('\n');
        Serial.println("PC: " + command);
        if (command == "OPEN") {
          digitalWrite(RELAY_PIN, LOW);
          startTime = millis();
          waitStatus = false;
          // client.print("OPEN_DOOR");
          Serial.println("OPEN_DOOR");
          delay(3000);
        } else if (command == "CLOSE") {
          digitalWrite(RELAY_PIN, HIGH);
          startTime = millis();
          waitStatus = false;
          // client.print("CLOSE_DOOR");
          Serial.println("CLOSE_DOOR");
          delay(3000);
        }
      }
    }
  }
}
