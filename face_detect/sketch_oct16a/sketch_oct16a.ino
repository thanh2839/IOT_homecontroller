const int ledPin = 2; // Gắn LED vào chân GPIO 2 của ESP32

void setup() {
  pinMode(ledPin, OUTPUT); // Khai báo chân GPIO là OUTPUT
}

void loop() {
  digitalWrite(ledPin, HIGH); // Bật đèn LED
  delay(1000); // Chờ 1 giây

  digitalWrite(ledPin, LOW); // Tắt đèn LED
  delay(1000); // Chờ 1 giây
}
