#include <Servo.h>
const int buttonPin1 = 2;
const int buttonPin2 = 4;// the number of the pushbutton pin

Servo arm;
Servo gripper;

// variables will change:
int buttonState1 = 0;
int buttonState2 = 0;
int iIncomingData;   //INCOMING SERIAL DATA
int iSpeedF = 49;
int iSpeedT = 143;
int iAdj = 255;
int iLeftBrake = 9;
int iRightBrake = 8;
int iLeftMotorSpeed = 3;
int iRightMotorSpeed = 11;
int iLeftMotorDir = 12;
int iRightMotorDir = 13;// variable for reading the pushbutton status
int apos =40 ;    // variable to store the servo position
int aup = apos;
int adown = 150;
int gpos = 0;
int gopen = gpos;
int gdown = 120;
//int rmotor = 7;
//int rsensor = 10;
////////////////////////////////////////////////////////////////////////////////////////////////////


void setup() {
  arm.attach(5 );  // attaches the servo on pin 9 to the servo object
  gripper.attach(6);
  //digitalWrite(rmotor,HIGH);
  //digitalWrite(rsensor,HIGH);
  //pinMode(rmotor,OUTPUT);
  //pinMode(rsensor,OUTPUT);


  // initialize the pushbutton pin as an input:
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);


  //BEGIN SERIAL CONNECTION WITH BAUD RATE SPECIFIED
  Serial.begin(9600);
  pinMode(iLeftMotorSpeed, OUTPUT);
  pinMode(iRightMotorSpeed, OUTPUT);
  pinMode(iLeftMotorDir, OUTPUT);
  pinMode(iRightMotorDir, OUTPUT);
  pinMode(iLeftBrake, OUTPUT);
  pinMode(iRightBrake, OUTPUT);
  pinMode(A0,INPUT);//INPUT FROM MAINBRAIN
  ArmUp();
  GripperOpen();
  while (buttonState1==0){

    buttonState1 = digitalRead(buttonPin1);


    if (buttonState1 == HIGH) {
      Serial.println('a');




    }
  }
  void(* resetFunc) (void) = 0;

  ///////////////////////////////////////////////////////////////////////////////////////////////////    
}

void loop() {


  // Serial.println(1);
  // delay(2000);
  if(Serial.available()){

    int iByte = Serial.read();

    switch (iByte){
    case 'a':
      RightTurn();

      break;
    case 'b':
      LeftTurn();

      break;
    case 'c':
      RightWall();

      break;
    case 'd':
      LeftWall();

      break;
    case 'e':
      FrontAdj();

      break;
    case 'f':
      Forward();

      break;
    case 'g':
      RightAdj();

      break;  
    case 'h':
      LeftAdj();

      break;
    case 'i':
      Stop();

      break;
    case 'j':
      Neutral();

      break;
    case 'k':
      ArmUp();
      //delay(500);
      //Serial.println('a');
      break;

    case 'l':
      ArmDown();
      //delay(500);
      //Serial.println('a');
      break;

    case 'm':
      GripperOpen();

      //Serial.println('a');
      break;

    case 'n':
      GripperClose();
      //delay(500);
      //Serial.println('a');
      break;
    case 'o':
      gripper.write(40);
      //delay(500);
      //Serial.println('a');
      break;

    case 'p':
      Backwards();

      break;

    case 'q':
      TurfFrontAdj();
      //delay(500);
      //Serial.println('a');
      break;
    case 'r':
      TurfLeftAdj();
      //delay(500);
      //Serial.println('a');
      break;

    case 's':
      TurfRightAdj();

      break;
    case 'u':
      TRightTurn();
      //delay(500);
      //Serial.println('a');
      break;

    case 't':
      TLeftTurn();

      break;
    case 'v':
      TForwards();

      break;


 //   case 'Z':
   //   digitalWrite(rmotor,LOW);
     // digitalWrite(rsensor,LOW);

    }




  }










}



/////////////////////////////////////////////////////////////////FUNCTIONS///////////////////////////////////////////////////////
void LeftAdj ()
{
  digitalWrite(iLeftMotorDir,HIGH);
  digitalWrite(iRightMotorDir,LOW);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iAdj);
  analogWrite(iRightMotorSpeed, iAdj);
  delay(25);
  analogWrite(iLeftMotorSpeed, 0);
  analogWrite(iRightMotorSpeed, 0);
  return;
}
void RightAdj ()
{
  digitalWrite(iLeftMotorDir,LOW);
  digitalWrite(iRightMotorDir,HIGH);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iAdj);
  analogWrite(iRightMotorSpeed, iAdj);
  delay(25);
  analogWrite(iLeftMotorSpeed, 0);
  analogWrite(iRightMotorSpeed, 0);
  return;
}
void FrontAdj ()
{
  digitalWrite(iLeftMotorDir,LOW);
  digitalWrite(iRightMotorDir,LOW);  
  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iSpeedT);
  analogWrite(iRightMotorSpeed, iSpeedT);
  delay(40);
  analogWrite(iLeftMotorSpeed, 0);
  analogWrite(iRightMotorSpeed, 0);
  return;
}
void TurfLeftAdj ()
{
  digitalWrite(iLeftMotorDir,HIGH);
  digitalWrite(iRightMotorDir,LOW);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iAdj);
  analogWrite(iRightMotorSpeed, iAdj);
  delay(33);
  analogWrite(iLeftMotorSpeed, 0);
  analogWrite(iRightMotorSpeed, 0);
  return;
}
void TurfRightAdj ()
{
  digitalWrite(iLeftMotorDir,LOW);
  digitalWrite(iRightMotorDir,HIGH);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iAdj);
  analogWrite(iRightMotorSpeed, iAdj);
  delay(33);
  analogWrite(iLeftMotorSpeed, 0);
  analogWrite(iRightMotorSpeed, 0);
  return;
}
void TurfFrontAdj ()
{
  digitalWrite(iLeftMotorDir,LOW);
  digitalWrite(iRightMotorDir,LOW);  
  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iSpeedT);
  analogWrite(iRightMotorSpeed, iSpeedT);
  delay(90);
  analogWrite(iLeftMotorSpeed, 0);
  analogWrite(iRightMotorSpeed, 0);
  return;
}


void ArmUp(void)
{ // goes from 180 degrees to 0 degrees
  arm.write(aup);
  //if (apos < aup+1){
  // delay(150);
  //GripperOpen();   // tell servo to go to position in variable 'pos'
  //}
  //delay(10);                       // waits 15ms for the servo to reach the position
}
void ArmDown(void){
  // goes from 0 degrees to 180 degrees
  // in steps of 1 degree
  arm.write(adown);              // tell servo to go to position in variable 'pos'
  //delay(10);                       // waits 15ms for the servo to reach the position
}
void GripperClose(void){
  // goes from 0 degrees to 180 degrees
  // in steps of 1 degree
  gripper.write(gopen);              // tell servo to go to position in variable 'pos'
  //delay(10);                       // waits 15ms for the servo to reach the position
}
void GripperOpen(void){
  // goes from 180 degrees to 0 degrees
  gripper.write(gdown);              // tell servo to go to position in variable 'pos'
  //delay(10);                       // waits 15ms for the servo to reach the position

}
void Forward ()
{
  digitalWrite(iLeftMotorDir,LOW);
  digitalWrite(iRightMotorDir,LOW);

  // read the incoming byte:
  //analogWrite(iLeftMotorSpeed, iSpeedF+10);
  //analogWrite(iRightMotorSpeed, iSpeedF+2);
  //4/10/2016 -- Collin
  analogWrite(iLeftMotorSpeed, iSpeedF+15);
  analogWrite(iRightMotorSpeed, iSpeedF+7);
  //4/10/2016 -- Collin
  
  
  return;
}
void TForwards ()
{
  digitalWrite(iLeftMotorDir,LOW);
  digitalWrite(iRightMotorDir,LOW);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iSpeedF+50);
  analogWrite(iRightMotorSpeed, iSpeedF-8+50);
  return;
}
void Backwards ()
{
  digitalWrite(iLeftMotorDir,HIGH);
  digitalWrite(iRightMotorDir,HIGH);

  // read the incoming byte:
  //4/10/2016 -- Collin
  //analogWrite(iLeftMotorSpeed, iSpeedF);
  //analogWrite(iRightMotorSpeed, iSpeedF);
  analogWrite(iLeftMotorSpeed, iSpeedF+5);
  analogWrite(iRightMotorSpeed, iSpeedF+5);
  //4/10/2016 -- Collin
  return;
}

void Stop ()
{   
  analogWrite(iLeftMotorSpeed, 255);
  analogWrite(iRightMotorSpeed, 255);
  digitalWrite(iLeftBrake,HIGH);
  digitalWrite(iRightBrake,HIGH);

  // read the incoming byte:
  //analogWrite(iLeftMotorSpeed, 150);
  //analogWrite(iRightMotorSpeed, 150);
  return;
}

void Neutral ()
{   
  analogWrite(iLeftMotorSpeed, 0);
  analogWrite(iRightMotorSpeed, 0);

  digitalWrite(iLeftBrake,LOW);
  digitalWrite(iRightBrake,LOW);
}

void TLeftTurn ()
{
  digitalWrite(iLeftMotorDir,HIGH);
  digitalWrite(iRightMotorDir,LOW);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iSpeedT+50);
  analogWrite(iRightMotorSpeed, iSpeedT+50);
  return;
}

void TRightTurn ()
{
  digitalWrite(iLeftMotorDir,LOW);
  digitalWrite(iRightMotorDir,HIGH);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iSpeedT+25);
  analogWrite(iRightMotorSpeed, iSpeedT+25);
  return;
}
void LeftTurn ()
{
  digitalWrite(iLeftMotorDir,HIGH);
  digitalWrite(iRightMotorDir,LOW);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iSpeedT);
  analogWrite(iRightMotorSpeed, iSpeedT);
  return;
}

void RightTurn ()
{
  digitalWrite(iLeftMotorDir,LOW);
  digitalWrite(iRightMotorDir,HIGH);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iSpeedT);
  analogWrite(iRightMotorSpeed, iSpeedT);
}
void RightWall()
{  
  digitalWrite(iLeftMotorDir,LOW);
  digitalWrite(iRightMotorDir,LOW);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, 255);
  analogWrite(iRightMotorSpeed, iSpeedF-20);
  delay(38);
  analogWrite(iLeftMotorSpeed, iSpeedF);
  analogWrite(iRightMotorSpeed, iSpeedF);
  return;
}


void LeftWall()
{  
  digitalWrite(iLeftMotorDir,LOW);
  digitalWrite(iRightMotorDir,LOW);

  // read the incoming byte:
  analogWrite(iLeftMotorSpeed, iSpeedF-20);
  analogWrite(iRightMotorSpeed, 255);
  delay(38);
  analogWrite(iLeftMotorSpeed, iSpeedF);
  analogWrite(iRightMotorSpeed, iSpeedF);
  return;
}









