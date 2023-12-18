#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "DESKTOP-078BH87";
const char* password = "123456780";
const char* mqtt_server = "broker.example.com"; // Thay đổi thành địa chỉ IP hoặc tên máy chủ MQTT của bạn
const int mqtt_port = 1883; // Port mặc định của MQTT

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  // Bắt đầu kết nối Wi-Fi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

void reconnect() {
  // Vòng lặp kết nối cho đến khi kết nối thành công
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.publish("esp32/test", "hello from ESP32");
      client.subscribe("laptop/test");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
