#include <Wire.h>
#include <MPU6050.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ESP8266WiFi.h>

MPU6050 mpu;

const int averageOverSeconds = 1;
const int sampleCount = 100;
const int measurementDelayMilliseconds = 1000*averageOverSeconds/sampleCount;
double sleepSeconds = 5;

const char* ssid = "wifi-ssid";
const char* password = "wifi-password";
const String endpoint = "http://backend-ip/tilty/measurements";

double pitchSum = 0;
double temperatureSum = 0;

int iteration = 0;

void setup() 
{
  Serial.begin(9600);
  initializeSensor();
}

void sleep() {
  if (sleepSeconds <= 10) {
    Serial.println("Simple delay");
    delay(sleepSeconds*1000);
  }
  else {
    Serial.println("Going to deep sleep");
    mpu.setSleepEnabled(true);
    ESP.deepSleep(sleepSeconds*1000000);
  }
}

void initializeSensor() {
  Serial.println("Initializing MPU6050");
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  Serial.println("Initialized MPU6050");
}

void initializeWifi() {
  Serial.print("Connecting to ");
  Serial.print(ssid);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  
  Serial.print("Connected to ");
  Serial.println(ssid);
}

void loop()
{
  delay(measurementDelayMilliseconds);
  collectMeasurements();
  iteration++;

  if (iteration == sampleCount) {
    exportMeasurements();
    sleep();
  }
}

void exportMeasurements() {
    if (WiFi.status() != WL_CONNECTED) {
      initializeWifi();
    }
    double pitch = pitchSum/iteration;
    double temperature = temperatureSum/iteration;

    iteration = 0;
    pitchSum = 0;
    temperatureSum = 0;
    
    Serial.print("Pitch = ");
    Serial.print(pitch);
    Serial.print("; Temp = ");
    Serial.println(temperature);

    WiFiClient client;
    HTTPClient http;

    String path = endpoint + "?angle=" + String(pitch) + "&temperature=" + String(temperature);
    http.begin(client, path.c_str());
    
    int httpResponseCode = http.GET();
    
    if (httpResponseCode == 200) {
      Serial.println("HTTP 200 with body: ");
      Serial.println(http.getString());
      sleepSeconds = http.getString().toDouble();
    }
    else {
      Serial.print("HTTP Error: ");
      Serial.println(httpResponseCode);
      sleepSeconds = 60;
    }
    http.end();
}

void collectMeasurements() {
  Vector normalizedAcceleration = mpu.readNormalizeAccel();
  
  pitchSum += getPitch(normalizedAcceleration);
  temperatureSum += getTemperature();
}

double getPitch(Vector normalizedAcceleration) {
  return -(atan2(normalizedAcceleration.XAxis, sqrt(normalizedAcceleration.YAxis*normalizedAcceleration.YAxis + normalizedAcceleration.ZAxis*normalizedAcceleration.ZAxis))*180.0)/M_PI;
}

double getTemperature() {
  return mpu.readTemperature();
}
