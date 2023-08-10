#include <SoftwareSerial.h>;

// ultrasonic distance detector
const int US100_TX = 5;
const int US100_RX = 6;

// bluetooth module
const int ZS040_TX = 9;
const int ZS040_RX = 8;

// SW-520D-Tilt-Switch-Sensor
const int SW_520D = 2;

SoftwareSerial detectorUS100(US100_RX, US100_TX);
SoftwareSerial bluetoothZS040(ZS040_RX, ZS040_TX);

unsigned int distanceRawFirstByte = 0;
unsigned int distanceRawSecondByte = 0;

unsigned int distanceMillimeters = 0, previousDistanceMillimeters = 0;
int vibroSensorValue;

// function sends string via BT module byte by byte
void sendStringBluetooth(String stringToSend) {
  Serial.print("Sending data via BT: " + stringToSend + "\r\n");

  for (int i = 0; i < stringToSend.length(); i++) {
    bluetoothZS040.write(stringToSend[i]);
  }
  delay(30);
}

unsigned long previousMillis = 0;  
const long interruptionInterval = 250; 


void vibro_handler() {
  // this function is called > 20 times after one hit near the vibration sensor, so 
  // since I don't need 20 events per one hit - I pay attention only to one vibration
  // event in 0.1 second
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interruptionInterval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;
    sendStringBluetooth("Vibro: true\r\n");
  }
  
}

void setup() {
  Serial.begin(9600);
  bluetoothZS040.begin(9600);  // BT module
  detectorUS100.begin(9600);  // distance
  pinMode(SW_520D, INPUT);  // vibration-and-tilt
  attachInterrupt(digitalPinToInterrupt(SW_520D), vibro_handler, FALLING);  // handle vibration with interruptions
}

void loop()
{
  detectorUS100.flush(); 
  delay(30);

  detectorUS100.write(0x55);  // send command to measure distance
  delay(50);  // setting below this value cause shit

  if(detectorUS100.available() >= 2)
  {
    Serial.write("DISTANCE AVAILABLE\r\n");
    previousDistanceMillimeters = distanceMillimeters;

    distanceRawFirstByte = detectorUS100.read();  
    distanceRawSecondByte  = detectorUS100.read();

    distanceMillimeters = distanceRawFirstByte * 256 + distanceRawSecondByte;

    if ((distanceMillimeters - previousDistanceMillimeters) < 5)
    { 
      // Serial.println("Difference less than 5 millimeters, ignore");
      return;
    }

    if((distanceMillimeters > 1) && (distanceMillimeters < 500))  // limits should align with limits from constants.py
    {
      Serial.write("Sending distance millimiters\r\n");
      sendStringBluetooth("Distance: " + String(distanceMillimeters) + "\r\n");
    }
  }
}


