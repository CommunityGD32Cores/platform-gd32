#include <Arduino.h>

#ifdef LED_BUILTIN
#define LED LED_BUILTIN
#else 
#define LED PC13
//#define LED PB13
#endif 

static int i=0;
void setup(){
    Serial.begin(115200);
    pinMode(LED, OUTPUT);
}

void loop(){
    digitalWrite(LED, LOW);
    delay(500);
    digitalWrite(LED, HIGH);
    delay(500);
    Serial.println("Blinky nr. " + String(i++));
}