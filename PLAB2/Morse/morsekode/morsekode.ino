const int buttonPin = 2;
const int ledPinRed = 13;
const int ledPinGreen = 10;

//variables will change
int buttonState = 0;
int lastButtonState = 0;
int startPress = 0;
int endPress = 0;
int pause = 0;
int timePressed = 0;
int message = 0;
int T = 500;

void setup() {
  Serial.begin(9600);
  pinMode(ledPinRed,OUTPUT);
  pinMode(ledPinGreen, OUTPUT);
  pinMode(buttonPin,INPUT);
  
}

void updateState() {
  if(buttonState == HIGH) {
    startPress = millis();
    pause = startPress - endPress;

    if(pause <= T) {
      message = 2;
    }

    else if(pause < 4*T) {
      message = 3;
    }

    else if(pause > 7*T) {
      message = 4;
    }
  }
  else {
    
    endPress = millis();
    timePressed = endPress - startPress;

    //dot
    if(timePressed < T) {
      digitalWrite(ledPinRed, HIGH);
      delay(50);
      digitalWrite(ledPinRed, LOW);
      message = 0;
    }
    //dash
    else if(timePressed >= T) {
      digitalWrite(ledPinGreen, HIGH);
      delay(50);
      digitalWrite(ledPinGreen, LOW);
      message = 1;
    }
    
  }
  Serial.print(message);
}

void loop() {
  buttonState = digitalRead(buttonPin);

  if(buttonState != lastButtonState) {
    updateState();
    
  }

  delay(20);

  digitalWrite(ledPinRed, LOW);
  digitalWrite(ledPinGreen, LOW);
  
  lastButtonState = buttonState;
  


}
