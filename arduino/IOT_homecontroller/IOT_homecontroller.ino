#include "DHTesp.h"
#include <Arduino.h>
#include <WiFi.h>
#include <Firebase_ESP_Client.h>
//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

#define LED 13
#define AnalogAS 35

#define WIFI_SSID "Abc"
#define WIFI_PASSWORD "1234567890"

// Insert Firebase project API Key
#define API_KEY "AIzaSyBgBWKb9LdDpMpQdbGe4vKaZn3TZv3euRA"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://cogent-cocoa-378019-default-rtdb.asia-southeast1.firebasedatabase.app/" 

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
int count = 0;
bool signupOK = false;
//fan
int in1 = 32;
int in2 = 33;
int enb = 14;
//cam bien anh sang
int sensorDigital = 27;
//cam bien nhiet do
const int DHT_PIN =26;
DHTesp dhtSensor;
//flame sensor
const int buzzer = 12;
const int flamePin = 34;
int flame = HIGH;
//digital Photoresistor nhan gia tri 0 khi sang 1 thi toi
//analog Photoresistor nhan gia tri lumen

void setup() {
  Serial.begin(115200);
  dhtSensor.setup(DHT_PIN, DHTesp::DHT11);
  pinMode(LED, OUTPUT);
  //delay(1000);
// digital Photoresistor
  pinMode(sensorDigital, INPUT);
  pinMode(AnalogAS, INPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(flamePin, INPUT);
  pinMode (in1, OUTPUT);
  pinMode (in2, OUTPUT);
  pinMode (enb, OUTPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() { 
  int valAnalog = analogRead (AnalogAS);
  int valueDigital = digitalRead(sensorDigital);
  flame = digitalRead(flamePin);
  TempAndHumidity  data = dhtSensor.getTempAndHumidity();

  if (Firebase.ready() && signupOK){
    sendDataPrevMillis = millis();
    // humidity
    if (Firebase.RTDB.setFloat(&fbdo, "btl-iot/humidity", data.humidity)){
      Serial.println("PASSED");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }
    
    // temperature
    if (Firebase.RTDB.setFloat(&fbdo, "btl-iot/tempurater", data.temperature)){
      Serial.println("PASSED");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }
    // cam bien flame
    if (Firebase.RTDB.setInt(&fbdo, "btl-iot/flame", flame)){
      Serial.println("PASSED");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println(flame);
      if(flame == 1) {
        Serial.print("flame: ");
        Serial.println(flame);
        digitalWrite(buzzer, LOW);
      }
      else {
        digitalWrite(buzzer, HIGH);
      }
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
      }

    // cam bien anh sang
    if (Firebase.RTDB.setInt(&fbdo, "btl-iot/sensor", valueDigital)){
      Serial.println("PASSED");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println(valueDigital);
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }
    // crawl data light
    if(Firebase.RTDB.getBool(&fbdo, "btl-iot/light")){
      if (fbdo.dataAvailable()){
        int dataL = fbdo.to<bool>();
        Serial.println("PASSED");
        Serial.println("PATH: " + fbdo.dataPath());
        Serial.println("TYPE: " + fbdo.dataType());
        Serial.println("DataL: " + String(dataL));
        if(dataL == 0) digitalWrite(LED, HIGH);
        else digitalWrite(LED, LOW);
        }
      else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
      }
    }

  //crawl data fan
    if(Firebase.RTDB.getBool(&fbdo, "btl-iot/fan")){
      if (fbdo.dataAvailable()){
        int dataF = fbdo.to<int>();
        Serial.println("PASSED");
        Serial.println("PATH: " + fbdo.dataPath());
        Serial.println("TYPE: " + fbdo.dataType());
        Serial.println("DataF: " + String(dataF));
        if(dataF == 0 ) {
          digitalWrite (in1, LOW);
          digitalWrite (in2, LOW);
        }
        else {
          analogWrite (enb, dataF);
          digitalWrite (in1, HIGH);
          digitalWrite (in2, LOW);
          }
        }
      else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
      }
    }
  }
//Flame sensor
  /*Serial.print("Flame sensor: ");
  Serial.println(flame);
//Analog
  Serial.print("Value Analog: ");
  Serial.println(valAnalog);
// Digital
  Serial.print("Value digital: ");
  Serial.println(valueDigital);*/
// Buzzer
 /* delay(500);
  if(flame == LOW) {
    digitalWrite(buzzer, HIGH);
  }
  else {
    digitalWrite(buzzer, LOW);
  }*/

// LED
  //---digitalWrite(LED, HIGH);
  //delay(500);
  //digitalWrite(LED, LOW);
  //delay(500);
  delay(1000);

  
}


//---------------
/*
int sensor = 27;
int value;

void setup () {
  Serial.begin(115200);
  pinMode(sensor, INPUT);
}

void loop() {
  value = digitalRead(sensor);
  Serial.print("Value: ");
  Serial.println(value);
  delay(1000);
}
*/
//------------------------ FAN
//FAN
/*
int in1 = 33;
int in2 = 32;

void setup() 
{
  pinMode (in1, OUTPUT);
  pinMode (in2, OUTPUT);

}

void loop() 
{
  digitalWrite (in1, HIGH);
  digitalWrite (in2, LOW);

  delay (1000);

  //digitalWrite (in1, LOW);
  //digitalWrite (in2, LOW);

  delay (3000);

}
*/

//--------------------------flame
//Flame sensor
/*
const int buzzer = 12;
const int flamePin = 34;
int flame = HIGH;

void setup() {
  Serial.begin(115200);
  pinMode(buzzer, OUTPUT);
  pinMode(flamePin, INPUT);
  
}

void loop() {
  
  flame = digitalRead(flamePin);
  Serial.print("flame: ");
  if(flame == LOW) {
    Serial.print("flame: ");
    Serial.println(flame);

    Serial.print("buzzer: ");
    Serial.println(buzzer);
    digitalWrite(buzzer, HIGH);
    delay(1000);
  }
  else {
    Serial.print("flame: ");
    Serial.println(flame);

    Serial.print("buzzer: ");
    Serial.println(buzzer);
    digitalWrite(buzzer, LOW);
    delay(1000);
  }
}*/