#include <Stepper.h>

const int stepsPerRevolution = 200;

// Button pin
const int buttonPin = 10;

// Create Stepper object
Stepper myStepper(stepsPerRevolution, 6, 8, 7, 9);
Stepper myStepperT(stepsPerRevolution, 2, 4, 3, 5);

bool startup = true;
int lloop = 0;
bool buttonCon = true;

void setup() {
  myStepper.setSpeed(200);  // Set RPM
  myStepperT.setSpeed(20);  // Set RPM
  pinMode(buttonPin, INPUT_PULLUP);
  while (startup){
    myStepper.step(-200);
    if (digitalRead(buttonPin) == LOW) {
      // Button pressed → STOP motor
      Serial.println("Motor stopped.");
      delay(100);  // Simple debounce
      while (lloop <= 230){
        myStepper.step(200);
        lloop++;
        Serial.println(lloop);
        }
      lloop = 0;
      while (buttonCon){
        if (digitalRead(buttonPin) == LOW){
          buttonCon = false;
          delay(5000);
        }
      }
      buttonCon = true;
      startup = false;
    }
  }
  Serial.begin(9600);
}

void loop() {
  // Button logic: LOW when pressed, HIGH when released
  if (digitalRead(buttonPin) == HIGH) {
    // Button released → run motor FORWARD
    myStepper.step(-200);  // Always step forward
    myStepperT.step(15);
    delay(1000);
    Serial.println("Image Captured");
    delay(15000);
  } else {
    // Button pressed → STOP motor
    Serial.println("Motor stopped.");
    delay(100);  // Simple debounce
    while (lloop <= 230){
      myStepper.step(200);
      lloop++;
      Serial.println(lloop);
      }
    lloop = 0;
    while (buttonCon){
        if (digitalRead(buttonPin) == LOW){
          buttonCon = false;
          delay(5000);
        }
    }
    buttonCon = true;
  }
}
