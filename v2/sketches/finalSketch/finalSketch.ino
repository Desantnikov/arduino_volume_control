#include <SoftwareSerial.h>;

// ultrasonic distance detector
const int US100_TX = 4;
const int US100_RX = 3;

// bluetooth module
const int ZS040_TX = 6;
const int ZS040_RX = 5;

//SW_520D vibration Sensor
//const int SW_520D_ANALOG_INPUT = A7;
const int SW_520D_DIGITAL_INPUT = 2;

int vibroSensorValue = 0;

SoftwareSerial detectorUS100(US100_RX, US100_TX);
SoftwareSerial bluetoothZS040(ZS040_RX, ZS040_TX);

unsigned int distanceRawFirstByte = 0;
unsigned int distanceRawSecondByte = 0;

unsigned int distanceMillimeters = 0, previousDistanceMillimeters = 0;

// function sends string via BT module byte by byte
void sendStringBluetooth(String stringToSend) {
  Serial.print("Sending data via BT: " + stringToSend + "\r\n");

  for (int i = 0; i < stringToSend.length(); i++) {
    bluetoothZS040.write(stringToSend[i]);
  }
  // delay(30);
}

int getDistance() {  // to measure distance in UART mode it's needed to:
    detectorUS100.flush();  // clear buffer
    detectorUS100.write(0x55);  // send command to measure distance

    delay(50);  // setting lower than 100 cause shitty measurements

    distanceRawFirstByte = detectorUS100.read();
    distanceRawSecondByte  = detectorUS100.read();

    distanceMillimeters = distanceRawFirstByte * 256 + distanceRawSecondByte;

    return distanceMillimeters;
}

void processDistance(int distanceMillimeters, int previousDistanceMillimeters) {
    // Serial.print("Distance: ");
    // Serial.print(distanceMillimeters);
    if (distanceMillimeters == previousDistanceMillimeters)
    {
// //
      // Serial.print("; Difference is less than 5 millimeters, ignore \r\n");
      return;
    }

    if((distanceMillimeters > 45) && (distanceMillimeters < 350))  // limits should align with limits from constants.py
    {
      sendStringBluetooth("Distance: " + String(distanceMillimeters) + "\r\n");
    }

}

void setup() {
 Serial.begin(9600);
 Serial.write("STARTED");

  bluetoothZS040.begin(9600);  // BT module
  detectorUS100.begin(9600);  // distance
  
  // pinMode(SW_18010P_ANALOG, INPUT);  // vibro
 pinMode(SW_520D_DIGITAL_INPUT, INPUT);  // vibro
}

void loop()
{

  vibroSensorValue = digitalRead(SW_520D_DIGITAL_INPUT);
// averageVibroSensorValue

   if (vibroSensorValue == LOW) {
    // if (vibroSensorValue == 0) {
      Serial.println("Vibro sensor triggered");
       sendStringBluetooth("Vibro: " + String(vibroSensorValue) + "\r\n");
     }
   delay(50);
  // }
  
  
 previousDistanceMillimeters = distanceMillimeters;
 distanceMillimeters = getDistance();
//
  processDistance(distanceMillimeters, previousDistanceMillimeters);

}


