#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "dynamics";
const char* password = "nodriver@dynamics";
const char* serverName = "http://158.180.55.164:5000/add";

#define DO_PIN 12

void setup() {
  //Serial.begin(115200);
  connectToWiFi();
  pinMode(DO_PIN, INPUT);
}

void loop() {
  int lightState = digitalRead(DO_PIN);

  Serial.print("Light State: ");
  Serial.println(lightState);

  int lightDetected;

  if (lightState == HIGH){
    Serial.println("It is dark");
    lightDetected = 1;
  } else{
    Serial.println("It is bright");
    lightDetected = 0;
  }
  sendPostRequest(lightDetected);
  delay(1000);
}

void connectToWiFi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
}

void sendPostRequest(int lightDetected) {
  HTTPClient http;

  http.begin(serverName);
  http.addHeader("Content-Type", "application/json");

  String httpRequestData = "{\"light_detected\":" + String(lightDetected) + "}";

  int httpResponseCode = http.POST(httpRequestData);

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    Serial.println(response);
  } else {
    Serial.print("Error on sending POST: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}