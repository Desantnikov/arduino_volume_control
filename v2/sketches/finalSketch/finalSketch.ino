#include <SoftwareSerial.h>;

// ultrasonic distance detector
const int US100_TX = 5;
const int US100_RX = 6;

// bluetooth module
const int ZS040_TX = 9;
const int ZS040_RX = 8;

//SW_18010P vibration Sensor
const int SW_18010P = 2;

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
  // delay(30);
}

unsigned long previousMicros = 0;  
 // lowering will lead to redudant sensor activity when pressing for some time instead of just two quick clicks
const long interruptionInterval = 175000; 


void vibro_handler() {
  detachInterrupt(digitalPinToInterrupt(SW_18010P));
  // vibroSensorValue = digitalRead(SW_18010P);
  Serial.println("VIBRO HANDLED: " + String(vibroSensorValue));

  // this function is called > 20 times after one hit near the vibration sensor, so 
  // since I don't need 20 events per one hit - I pay attention only to one vibration
  // event in 0.1 second
  unsigned long currentMicros = micros();  // google says micros should be used inside interruptions instead of millis

  if ( currentMicros - previousMicros >= interruptionInterval) {
    previousMicros = currentMicros;
    sendStringBluetooth("Vibro: true\r\n");
  } 
}

void setup() {
  
  Serial.begin(9600);
  bluetoothZS040.begin(9600);  // BT module
  detectorUS100.begin(9600);  // distance
  pinMode(SW_18010P, INPUT);  // vibration
  // attachInterrupt(digitalPinToInterrupt(SW_18010P), vibro_handler, FALLING);  // handle vibration with interruptions
}

void loop()
{
  // looks like a bad idea, but attaching and detaching this interrupt makes
  // sensor accuracy to double tap almost perfect
  attachInterrupt(digitalPinToInterrupt(SW_18010P), vibro_handler, RISING);  


  detectorUS100.flush(); 
  detectorUS100.write(0x55);  // send command to measure distance
  delay(100);  // setting below this value cause shit

  if(detectorUS100.available() >= 2)
  {
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
      sendStringBluetooth("Distance: " + String(distanceMillimeters) + "\r\n");
    }
  }
}


