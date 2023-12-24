#include "DHTesp.h"
#include <Arduino.h>
#include <WiFi.h>
#include <Firebase_ESP_Client.h>
//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

#define API_KEY "AIzaSyC2CFfJ6JPILTawiXko91IUTSfZKvU2080"

#define DATABASE_URL "https://btl-iot-27a9c-default-rtdb.asia-southeast1.firebasedatabase.app/" 

#define WIFI_SSID "abc"
#define WIFI_PASSWORD "123456789"

FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

const int RELAY_PIN = 18;
bool signupOK = false;

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  
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
  if (Firebase.ready() && signupOK){
    //sendDataPrevMillis = millis();
    // humidity
    if(Firebase.RTDB.getBool(&fbdo, "btl-iot/face-detect")){
      if (fbdo.dataAvailable()){
        int dataD = fbdo.to<bool>();
        Serial.println("PASSED");
        Serial.println("PATH: " + fbdo.dataPath());
        Serial.println("TYPE: " + fbdo.dataType());
        Serial.println("DataD: " + String(dataD));
        if(dataD == 0) digitalWrite(RELAY_PIN, HIGH);
        else digitalWrite(RELAY_PIN, LOW);
        }
      else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
      }
    }
  }
  delay(1000);
}
