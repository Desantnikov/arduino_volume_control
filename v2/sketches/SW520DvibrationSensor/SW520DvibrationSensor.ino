/*
  SW-520D-Tilt-Switch-Sensor
  made on 07 Nov 2020
  by Amir Mohammad Shojaee @ Electropeak
  Home
*/

const int Pin=5;

void setup() {
    pinMode(Pin, INPUT);
    Serial.begin(9600);
}
 
void loop() {
    int sensorValue = digitalRead(Pin);
    if(sensorValue==HIGH){ 
        Serial.println("ON-State");
        delay(500);
    }
    else{
        Serial.println("OFF-State");
        delay(500);
    }
}