
///////////////////////////////////////////////////////////////////////////////
//INITIALIZATION
///////////////////////////////////////////////////////////////////////////////
//SENOSR1 TOPLEFT
int iTrig1 = 2; //TRIG TO PIN 2
int iEcho1 = 3; //ECHO TO PIN 3
//SENSOR2 TOPRIGHT
int iTrig2 = 4; //TRIG TO PIN 4
int iEcho2 = 5; //ECHO TO PIN 5
//SENOR3 BOTTOMLEFT
int iTrig3 = 6; //TRIG TO PIN 6
int iEcho3 = 7; //ECHO TO PIN 7
//SENSOR4 BOTTOMRIGHT
int iTrig4 = 8; //TRIG TO PIN 8
int iEcho4 = 9; //ECHO TO PIN 9
int iTrig5 = 10; //TRIG TO PIN 8
int iEcho5 = 11; //ECHO TO PIN 9
//COMUNICATION AND READY PIN
int pinout = 13;
///////////////////////////////////////////////////////////////////////////////
//SETUP
///////////////////////////////////////////////////////////////////////////////

void setup()
{
    //BEGIN SERIAL CONNECTION WITH BAUD RATE SPECIFIED
    Serial.begin(9600);
    //SETS UP ALL OF THE SENSORS
    
    //SENSOR1
    pinMode(iTrig1, OUTPUT);
    pinMode(iEcho1, INPUT);
    //SENSOR2
    pinMode(iTrig2, OUTPUT);
    pinMode(iEcho2, INPUT);
    //SENSOR3
    pinMode(iTrig3, OUTPUT);
    pinMode(iEcho3, INPUT);
    //SENSOR4
    pinMode(iTrig4, OUTPUT);
    pinMode(iEcho4, INPUT);
    //SENSOR4
    pinMode(iTrig5, OUTPUT);
    pinMode(iEcho5, INPUT);
    //COMUNCATION AND READY PIN SETUP
   
    
    
    
    
    
    



}
///////////////////////////////////////////////////////////////////////////////
//MAIN FUNCTION
///////////////////////////////////////////////////////////////////////////////

void loop()
{   
    
    int y,z = 0;
    //int iTime;       //TIME OF PING
    //int iInches;
    int iAnswer;     //DISTANCE IN INCHES
    int iSensor1[] = {iTrig1 , iEcho1};       //Arrays for all of the sensors
    int iSensor2[] = {iTrig2 , iEcho2};
    int iSensor3[] = {iTrig3 , iEcho3};
    int iSensor4[] = {iTrig4 , iEcho4};
    int iSensor5[] = {iTrig5 , iEcho5};
    

/////////////////////////////////////////////////////////////////////
    if(Serial.available()){
    
    int iByte = Serial.read();//-'0';
    //int iByte='1';
    switch (iByte){
      case '1':{
        y= SensorRead(iSensor1);
        Serial.println(y); 
        break;}
        
        
      case '2':{
       
        y= SensorRead(iSensor2);
        
        Serial.println(y); 
        break;}
        
        
      case '3':{
       
        y= SensorRead(iSensor3);
        Serial.println(y); 
        break;}
      
      
      case '4':{
       y= SensorRead(iSensor4);
        
        Serial.println(y); 
        break;}
      
      
      case '5':{
         y= SensorRead(iSensor5);
       
        
        Serial.println(y); 
        break;}
      
//         
//      case '2': {
//        x=0;
//        y=0;
//        z=0;
//        while (z<3){
//          x= x + SensorRead(iSensor1);
//          z++;
//        }
//        x=x/3;
//        Serial.print(x); 
//        break;} 
//        
//        
//      case '3': {
//        x=0;
//        y=0;
//        z=0;
//        while (z<3){
//          x= x + SensorRead(iSensor1);
//          y= y + SensorRead(iSensor2);
//          z++;
//        }
//        x=x/3;
//        
//        Serial.print(x); 
//        break;} 
//        
//        
//    
//    
//    
    
    
    
   }
    
    
  
}
}
///////////////////////////////////////////////////////////////////////////////
//RETURN DISTANCE OF OBSTACLE IN INCHES
///////////////////////////////////////////////////////////////////////////////


int SensorRead(int iReadArray[])
{   int iTime;          //TIME OF PING
    digitalWrite(iReadArray[0], LOW);
    delayMicroseconds(20);
    
    //TRIGGER
    digitalWrite(iReadArray[0], HIGH);
    delayMicroseconds(2);
    digitalWrite(iReadArray[0], LOW);

    //READ THE ECHO
    iTime = pulseIn(iReadArray[1], HIGH);
    //Serial.print(iTime);
    delay(10);
    
    return iTime;
}

//int Parallel(int iFS[],int iBS[])//INT ARRAY FOR FS=FRONT SENSOR, BS=BACK SENSOR
//{   int x,y,z;
//    y,z=0;
//    while (z<5){
//    x=SensorRead(iFS);
//    x=x-SensorRead(iBS);
//    y=y+x;
//    z++;
//    }
//    return y/5;
//    }


