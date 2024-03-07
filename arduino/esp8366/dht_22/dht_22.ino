/*********
  Rui Santos
  Complete project details at https://randomnerdtutorials.com/esp8266-dht11dht22-temperature-and-humidity-web-server-with-arduino-ide/
*********/

// Import required libraries
#include "arduino_secrets.h"
#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <WiFiClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

// Replace with your network credentials
const char* ssid = SECRET_SSID;
const char* password = SECRET_PASS;

const char* host = "192.168.31.226"; // Server IP address
const int httpPort = 8000; // Server port number
const char* endpoint = "/sensors/api/sensors/"; // Specific endpoint for the POST request

const char* sensor_humidity = "7";
const char* sensor_temperature = "11";

int pin_blink = 2;

#define DHTPIN 5     // Digital pin connected to the DHT sensor

// Uncomment the type of sensor in use:
#define DHTTYPE    DHT22     // DHT 22 (AM2302)

DHT dht(DHTPIN, DHTTYPE);

// current temperature & humidity, updated in loop()
float t = 0.0;
float h = 0.0;


// Generally, you should use "unsigned long" for variables that hold time
// The value will quickly become too large for an int to store
unsigned long previousMillis = 0;    // will store last time DHT was updated

// Updates DHT readings every 10 seconds
const long interval = 300000;


void setup(){
  // Serial port for debugging purposes
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");

  // Example reading
  float reading = 123.45;

  // Call the function to send a POST request with the reading
  sendPostRequest(reading, "6");
}

void loop(){
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    digitalWrite(pin_blink, HIGH);
    // save the last time you updated the DHT values
    previousMillis = currentMillis;
    // Read temperature as Celsius (the default)
    float newT = dht.readTemperature();
    // if temperature read failed, don't change t value
    if (isnan(newT)) {
      Serial.println("Failed to read from DHT sensor!");
    }
    else {
      t = newT;
      sendPostRequest(t, sensor_temperature);
      Serial.println(t);
    }
    // Read Humidity
    float newH = dht.readHumidity();
    // if humidity read failed, don't change h value
    if (isnan(newH)) {
      Serial.println("Failed to read from DHT sensor!");
    }
    else {
      h = newH;
      sendPostRequest(h, sensor_humidity);
      Serial.println(h);
    }
    digitalWrite(pin_blink, LOW);
  }
}


// Function to send a POST request
// Accepts a float value as input and sends it as a JSON object
void sendPostRequest(float reading, String sensor) {
  Serial.print("Connecting to ");
  Serial.println(host);

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  if (!client.connect(host, httpPort)) {
    Serial.println("Connection failed");
    return;
  }

  // Create the JSON object
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["value"] = reading;
  String postData;
  serializeJson(jsonDoc, postData);

  // Send the HTTP POST request
  client.print(String("POST ") + endpoint + sensor + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Content-Type: application/json\r\n" +
               "Content-Length: " + postData.length() + "\r\n" +
               "Connection: close\r\n\r\n" +
               postData + "\r\n");

  Serial.println("Request sent");boolean isHeader = true; // Flag to track when we're done reading headers

  while(client.connected() || client.available()) {
    if (client.available()) {
      String line = client.readStringUntil('\n');
      if (line.startsWith("HTTP/1.1")) {
        Serial.print("Response code: ");
        Serial.println(line);
        break; // Assuming the first line is the status line
      }
    }
  }
}
