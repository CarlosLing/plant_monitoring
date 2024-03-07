#include "arduino_secrets.h"
#include <Arduino_MKRIoTCarrier.h>
#include <SPI.h>
#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>

MKRIoTCarrier carrier;

char ssid[] = SECRET_SSID;    // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)

int status = WL_IDLE_STATUS;     // the Wifi radio's stat

float temperature;
float humidity;
float pressure;
int moisture = A5;
int moist;

int    HTTP_PORT   = 8000;
char   HOST_NAME[] = "192.168.1.2";
String endpoint   = "/sensors/api/sensors";


int temperature_sensor_id = 6;
int humidity_sensor_id = 7;
int pressure_sensor_id = 8;
int moisture_sensor_id = 9;
int battery_sensor_id = 10;

WiFiClient client;
HttpClient hclient = HttpClient(client, HOST_NAME, 8000);

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial);

  //Initialize carrier
  delay(15000);
  CARRIER_CASE = true;
  carrier.begin();
  carrier.Buzzer.beep(800, 100);
  delay(1000);

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    carrier.Buzzer.beep(800, 20);
    Serial.print("Attempting to connect to network: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

  // you're connected now, so print out the data:

  carrier.Buzzer.beep(800, 20);
  delay(10);
  carrier.Buzzer.beep(800, 20);
  Serial.println("You're connected to the network");
  Serial.println("----------------------------------------");
  printData();
  Serial.println("----------------------------------------");
  // saveData(1, 0.0);
  delay(10000);
}


void loop() {
  // check the network connection once every 15 mins:
  delay(9000);

  float temperature = carrier.Env.readTemperature(); //reads temperature
  Serial.print("temperature: ");
  Serial.println(temperature);
  // saveData(temperature_sensor_id, temperature);

  float humidity = carrier.Env.readHumidity(); //reads humidiy
  Serial.print("humidity: ");
  Serial.println(humidity);
  // saveData(humidity_sensor_id, humidity);

  float pressure = carrier.Pressure.readPressure();  //reads preassure
  Serial.print("pressure: ");
  Serial.println(pressure);
  // saveData(pressure_sensor_id, pressure);

  int moist = analogRead(moisture);
  Serial.print("moist: ");
  Serial.println(moist);


  float sensorValue = analogRead(ADC_BATTERY);
  float battery = sensorValue * (4.3 / 1023.0);

  Serial.print("Battery: ");
  Serial.println(battery);
  saveData(1, battery);
  // saveData(battery_sensor_id, battery);
  /*
  printData();
  temperature = carrier.Env.readTemperature(); //reads temperature
  humidity = carrier.Env.readHumidity(); //reads humidity
  pressure = carrier.Pressure.readPressure(); //reads pressure
  Serial.print("Temperature: ");
  Serial.println(temperature);
  Serial.print("Humidity: ");
  Serial.println(humidity);
  Serial.print("Pressure: ");
  Serial.println(pressure);
  */

  Serial.println("----------------------------------------");
}


void printData() {
  Serial.println("Board Information:");
  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  Serial.println();
  Serial.println("Network Information:");
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.println(rssi);

}

void saveData(int sensor_id, float value) {
  /**
   * Saves data:
   * Sends Request to HOST_NAME
   * Adds query arguments sensor and value from the inputs sensor_id and value respectivey
  */


  String sensor_endpoint = endpoint + "/" + sensor_id;
  String postData = "{\"value\":" + String(value)+"}";
  Serial.println(postData);
  // Set the HTTP method, headers, and data
  hclient.beginRequest();
  hclient.post(sensor_endpoint);
  hclient.sendHeader("Content-Type", "application/json");
  hclient.sendHeader("Content-Length", postData.length());
  hclient.sendHeader("Connection", "close");
  hclient.beginBody();
  hclient.print(postData);

  int statusCode = hclient.responseStatusCode();

  if (statusCode > 0) {
    String response = hclient.responseBody();
    Serial.print("HTTP Response Code: ");
    Serial.println(statusCode);
    Serial.print("Response Data: ");
    Serial.println(response);
  } else {
    Serial.print("Error on HTTP request: ");
    Serial.println(statusCode);
  }

  hclient.stop();

}
