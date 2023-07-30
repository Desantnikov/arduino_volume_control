#include <SoftwareSerial.h>;
 
const int US100_TX = 2;
const int US100_RX = 3;
 
// Instancia nuevo canal serie
SoftwareSerial detectorUS100(US100_RX, US100_TX);
 
unsigned int MSByteDist = 0;
unsigned int LSByteDist = 0;
unsigned int mmDist = 0;
int temp = 0;
 
void setup() {
    Serial.begin(9600);
    detectorUS100.begin(9600);
}
 
void loop() {
 
    detectorUS100.flush(); // limpia el buffer del puerto serie
    detectorUS100.write(0x55); // orden de medición de distancia
 
    delay(500);
 
    if(detectorUS100.available() >= 2) // comprueba la recepción de 2 bytes
    {
        MSByteDist = detectorUS100.read(); // lectura de ambos bytes
        LSByteDist  = detectorUS100.read();
        mmDist  = MSByteDist * 256 + LSByteDist; // distancia
        if((mmDist > 1) && (mmDist < 10000)) // comprobación de la distancia dentro de rango
        {
            Serial.print("Distancia: ");
            Serial.print(mmDist, DEC);
            Serial.println(" mm");
        }
    }
 
}