#include <Arduino_MKRIoTCarrier.h>

MKRIoTCarrier carrier;


float temperature;
float humidity;
float pressure;
int moisture = A5;
int moist;

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial);

  //Initialize carrier
  delay(1500);
  CARRIER_CASE = true;
  carrier.begin();

}


void loop() {
  // check the network connection once every 10 seconds:
  delay(1000);

  temperature = carrier.Env.readTemperature(); //reads temperature
  humidity = carrier.Env.readHumidity(); //reads humidity
  pressure = carrier.Pressure.readPressure(); //reads pressure
  Serial.print("Temperature: ");
  Serial.println(temperature);
  Serial.print("Humidity: ");
  Serial.println(humidity);
  Serial.print("Pressure: ");
  Serial.println(pressure);


  moist = analogRead(moisture);
  Serial.print("Moist: ");
  Serial.print(moist);


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
