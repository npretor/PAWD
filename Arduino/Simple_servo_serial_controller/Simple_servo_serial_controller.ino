/* 
 * Nathan Pretorius 2023. Parsing taken from: 
 *  This demo expects a string sent over serial: 
 *    <move, int, int>
 *  
 */ 

#include <Servo.h>


// - - - - Hardware pin definitions - - - - //
const int X_SERVO_PIN = 9; 
const int Y_SERVO_PIN = 8; 
const int TRIGGER_PIN = 7; 

// - - - - Parsing values - - - - //
int x_angle = 1500;
int y_angle = 1500;
int triggerValue = 0;

int prevTrigger = 0;


const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables to hold the parsed data
char messageFromPC[numChars] = {0};
int integerFromPC = 0;
int integer2fromPC = 0;

boolean newData = false;
  
Servo x_servo;
Servo y_servo;

//============

void setup() {
    // - - - - Motor settings - - - - //
    x_servo.attach(X_SERVO_PIN, 1000, 2000);
    y_servo.attach(Y_SERVO_PIN, 1000, 2000);
    delay(100);
  
    Serial.begin(115200);
    //This demo expects 4 pieces of data - text, an integer and a floating point value
    Serial.println("Enter data in this style <-100, 100, >  ");
}

//============

void loop() {
  
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        
        //or ACK
        Serial.println("ack");
        
        newData = false;

        // = = = = = = = Move motors = = = = = = = //
        x_servo.writeMicroseconds(x_angle);
        y_servo.writeMicroseconds(y_angle);
        

        // = = = = = = = Trigger logic = = = = = = = //

        // Check to see if trigger values are updated 
        // TODO: Need to set up digitalWrite setup 
        // if (prevTrigger == triggerValue){
        //   // Pass
        // } else {
        //     digitalWrite(TRIGGER_PIN, triggerValue);
        // }

    }

    
}

//============

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }
        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx       = strtok(tempChars, ",");
    x_angle           = atoi(strtokIndx);

    strtokIndx       = strtok(NULL, ",");
    y_angle           = atoi(strtokIndx);
    
    strtokIndx       = strtok(NULL, ",");
    triggerValue           = atoi(strtokIndx);                
    

    //strtokIndx = strtok(tempChars,",");      // get the first part - the string
    //strcpy(messageFromPC, strtokIndx); // copy it to messageFromPC
    //strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    
    //x_speed = atoi(strtokIndx);     // convert this part to an integer
    //strtokIndx = strtok(NULL, ",");
    
    //y_speed = atoi(strtokIndx);
    //floatFromPC = atof(strtokIndx);     // convert this part to a float

}

//============

void showParsedData(int xPulses, int yPulses) {
    //Serial.print("Message ");
    //Serial.println(messageFromPC);
    //Serial.println("Set speed to x: %d   y: %d ", x_speed, y_speed)

    Serial.print("Set speed to x: ");
    Serial.print(xPulses);
    Serial.print("  y: ");
    Serial.println(yPulses);
    
    //Serial.print("Integer ");
    //Serial.print(integerFromPC);
    //Serial.print("Int ");
    //Serial.println(integer2fromPC);
}
