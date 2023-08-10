#include <SoftwareSerial.h>;

// ultrasonic distance detector
const int US100_TX = 2;
const int US100_RX = 3;

// bluetooth module
const int ZS040_TX = 9;
const int ZS040_RX = 8;

//  SW-520D-Tilt-Switch-Sensor
const int SW_520D = 5;

SoftwareSerial detectorUS100(US100_RX, US100_TX);
SoftwareSerial bluetoothZS040(ZS040_RX, ZS040_TX);

unsigned int distanceRawFirstByte = 0;
unsigned int distanceRawSecondByte = 0;

unsigned int distanceMillimeters = 0;

String distanceString, tiltOrVibrationString;


void setup() {
  Serial.begin(9600);
  bluetoothZS040.begin(9600);  // BT module
  detectorUS100.begin(9600);  // distance
  pinMode(SW_520D, INPUT);  // vibration-and-tilt
}
 
void loop() {
  detectorUS100.flush(); 
  detectorUS100.write(0x55);  // send command to measure distance

  delay(30);  // setting below this value cause shit

  if(detectorUS100.available() >= 2) 
  {
    distanceRawFirstByte = detectorUS100.read();  
    distanceRawSecondByte  = detectorUS100.read();

    distanceMillimeters  = distanceRawFirstByte * 256 + distanceRawSecondByte; 

    if((distanceMillimeters > 1) && (distanceMillimeters < 10000)) 
    {
      distanceString = "Distance: " + String(distanceMillimeters) + "\r\n";
      Serial.print(distanceString);

      for (int i = 0; i < distanceString.length(); i++)
      {
        bluetoothZS040.write(distanceString[i]);
      }
    }
  }

  int sensorValue = digitalRead(SW_520D);

  if(sensorValue==HIGH){ 
    Serial.println("Vibro: false");

    tiltOrVibrationString = "Vibro: false\r\n";
  }
  else
  {
    Serial.println("Vibro: true");

    tiltOrVibrationString = "Vibro: true\r\n";
    for (int i = 0; i < tiltOrVibrationString.length(); i++)
    {
      bluetoothZS040.write(tiltOrVibrationString[i]);
    }
  }

}