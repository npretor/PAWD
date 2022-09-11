/* 
 * Nathan Pretorius 2023. Parsing taken from: 
 *  This demo expects a string sent over serial: 
 *    <move, int, int>
 *  
 */ 


 #include <AccelStepper.h>

  // - - - - Hardware definitions - - - - //
const int X_ENABLE_PIN = 0; 
const int X_DIR_PIN = 1; 
const int X_STEP_PIN = 2;   
const int Y_ENABLE_PIN = 3; 
const int Y_DIR_PIN = 4; 
const int Y_STEP_PIN = 5; 

//const int X_ENDSTOP_PIN = 3;
//const int Y_ENDSTOP_PIN = 7;
//const int TRIGGER_PIN = 8;

int xPulses = 0;
int yPulses = 0;
int xPulseDuration = 0;
int yPulseDuration = 0;
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

AccelStepper xStepper(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);           
AccelStepper yStepper(AccelStepper::DRIVER, Y_STEP_PIN, Y_DIR_PIN);       

//============

void setup() {

    // - - - - Pin setup - - - - //
    pinMode(X_ENABLE_PIN, OUTPUT); 
    pinMode(Y_ENABLE_PIN, OUTPUT); 
    delay(100);

    // - - - - Motor settings - - - - //
    xStepper.setMaxSpeed(5000.0);
    xStepper.setAcceleration(35000.0);
    xStepper.moveTo(200);
    
    yStepper.setMaxSpeed(5000.0);
    yStepper.setAcceleration(35000.0);
    yStepper.moveTo(200);
  
  
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
        //showParsedData(xPulses, yPulses); 
        // Relative move
        xStepper.move(xPulses); 
        yStepper.move(yPulses); 
        // Absolute move
        //xStepper.moveTo(xPulses); 
        //yStepper.moveTo(yPulses);  
        // = = = = = = = Trigger logic = = = = = = = //

        // Check to see if trigger values are updated 
        if (prevTrigger == triggerValue){
          // Pass
        } else {
            digitalWrite(TRIGGER_PIN, triggerValue);
        }

    }


    // Variables we can use: 
    // - xPulses 
    // - yPulses
    xStepper.run();
    yStepper.run();
    
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
    xPulses           = atoi(strtokIndx);
    strtokIndx       = strtok(NULL, ",");
    yPulses           = atoi(strtokIndx);
    strtokIndx       = strtok(NULL, ",");    
    xPulseDuration    = atoi(strtokIndx);
    strtokIndx       = strtok(NULL, ",");            
    yPulseDuration    = atoi(strtokIndx);
    
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
