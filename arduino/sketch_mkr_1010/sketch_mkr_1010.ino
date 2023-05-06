#include  <WiFiNINA.h>
#include "arduino_secrets.h"
#include <Arduino_MKRIoTCarrier.h>

MKRIoTCarrier carrier;

char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)

int status = WL_IDLE_STATUS;     // the Wifi radio's stat

float temperature;
float humidity;
float pressure;

int    HTTP_PORT   = 8000;
String HTTP_METHOD = "GET";
char   HOST_NAME[] = "192.168.31.22";
String PATH_NAME   = "/sensors/save_sensor_data/";

WiFiClient client;

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial);

  //Initialize carrier
  delay(1500);
  CARRIER_CASE = true;
  carrier.begin();

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to network: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

  // you're connected now, so print out the data:
  Serial.println("You're connected to the network");

  Serial.println("----------------------------------------");
  printData();
  Serial.println("----------------------------------------");

}


void loop() {
  // check the network connection once every 10 seconds:
  delay(10000);

  Serial.println("Sending temperature value as GET Request");
  temperature = carrier.Env.readTemperature(); //reads temperature
  saveData(1, temperature);
  Serial.print("Temperature: ");
  Serial.println(temperature);


  printData();
  /*
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

  if(client.connect(HOST_NAME, HTTP_PORT))
  {
    client.println(HTTP_METHOD + " " + PATH_NAME + "?sensor=" + sensor_id + "&value=" + value+ " HTTP/1.1");
    client.println("Host: " + String(HOST_NAME));
    client.println("Connection: close");
    client.println(); // end HTTP header

    Serial.println(HTTP_METHOD + " " + PATH_NAME + "?sensor=" + sensor_id + "&value=" + value+ " HTTP/1.1");
    Serial.println("Host: " + String(HOST_NAME));
    Serial.println("Connection: close");
    Serial.println(); // end HTTP header

    while(client.connected()) {
      if(client.available()){
        // read an incoming byte from the server and print it to serial monitor:
        char c = client.read();
        Serial.print(c);
      }
    }
    client.stop();
    Serial.println();
    Serial.println("disconnected");
  }

  else {// if not connected:
    Serial.println("connection failed");
  }

}
