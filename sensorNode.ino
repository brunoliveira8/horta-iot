// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"

#define DHTPIN 4     // what digital pin we're connected to
#define RELAY 13

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.

#include <SoftwareSerial.h>

DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial XBee(2, 3); // RX, TX

unsigned long int time_interval = 10000; //time between measures
unsigned long int last_time = 0;
float h_floor = 20.0; //lowest value to turn on irrigation
float h_ceil = 70.0; //highest value to turn off irrigation
boolean relay = false;

//sensors
int soil_data;
float h_soil; //% of soil humidity
//air humidity and temperature data
float h_air; //% of air humidity
float t;// Read temperature as Celsius (the default)

void setup() {
  Serial.begin(9600);
  XBee.begin(9600);
  XBee.setTimeout(500);
  //Serial.println("DHTxx test!");
  dht.begin();
  pinMode(RELAY, OUTPUT);
  digitalWrite(RELAY, HIGH);
}

void loop() {
  // Wait a few miliseconds between measurements.
  delay(50);

  readSensors();
  measure_timing();
  statusRelay();
  getConfig();

}


void getConfig() {
  if (XBee.available())
  { // If data comes in from XBee
    String data = XBee.readString(); // read the incoming String:
    int len = data.length() + 1;
    char sz[15];
    //char *sz = malloc(len);
    data.toCharArray(sz, len);
    char *p = sz;
    char *str;
    String vec[3];
    int i = 0;
    Serial.begin(9600);
    while ((str = strtok_r(p, ";", &p)) != NULL) { // delimiter is the semicolon
      vec[i] = str;
      i++;
      //Serial.println(str);
    }//while
    h_ceil = vec[0].toFloat();
    h_floor = vec[1].toFloat();
    time_interval = vec[2].toInt();
    time_interval = time_interval * 1000 * 60;

    Serial.print("New floor:");
    Serial.println(h_floor);
    Serial.print("New ceiling:");
    Serial.println(h_ceil);
    Serial.print("New interval:");
    Serial.println(time_interval);

  }//xbee.available

}

void statusRelay() {
  //turn relay on and off comparing humidity values with floor and ceiling
  if (h_soil <  h_floor && relay == false) {
    relay = true;
    digitalWrite(RELAY, LOW);
    //send notification
    XBee.print("atuador,");
    XBee.println(relay);

    //testing
    Serial.print("atuador,");
    Serial.println(relay);
  }
  if (h_soil > h_ceil && relay == true) {
    relay = false;
    digitalWrite(RELAY, HIGH);
    //send notification
    XBee.print("atuador,");
    XBee.println(relay);

    //testing
    Serial.print("atuador,");
    Serial.println(relay);
  }
}

void measure_timing() {
  //interval of time for sending data
  if ((millis() - last_time) > time_interval || (millis() - last_time) < 0) {
    sendSensorData();
    serialDisplay();
    last_time = millis();
  }

}

void readSensors() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)

  //soil humidity data
  soil_data = analogRead(A0);
  h_soil = map(soil_data, 1023, 0, 0, 100); //% of soil humidity

  //air humidity and temperature data
  h_air = dht.readHumidity(); //% of air humidity
  t = dht.readTemperature();// Read temperature as Celsius (the default)

  // Check if any reads failed and exit early (to try again).
  if (isnan(h_air) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

}


void sendSensorData() {
  //xbee transmission
  XBee.print("sensor,"); //identification
  XBee.print(h_soil); //soil humidity
  XBee.print(",");
  XBee.print(h_air); //air humidity
  XBee.print(",");
  XBee.println(t); //temperature
  //XBee.println(relay);
}

void serialDisplay() {
  //serial printing for debug
  Serial.print(h_soil); //soil humidity
  Serial.print(",");
  Serial.print(h_air); //air humidity
  Serial.print(",");
  Serial.println(t); //temperature

}
