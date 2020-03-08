uint8_t sensores1[]={64,34,9,17,25,48,7,3,10,16,18};
uint8_t sensores2[]={7,24,29,7,5,8,3,2,19,1,8};
uint8_t sensores3[]={4,39,9,17,25,4,7,8,1,16,18};
uint8_t sensores4[]={60,3,9,1,25,8,7,45,10,46,8};
uint8_t i=0;
char buffer[50];

void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);
}
 
// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  //int sensorValue = analogRead(A0);
  // print out the value you read:
  sprintf(buffer, "%d,%d,%d,%d", sensores1[i], sensores2[i], sensores3[i],sensores4[i]);
  Serial.println(buffer);
  delay(10000);        // delay in between reads for stability
  if(i<11){
    i++;  
  }else{
    i=0;
    }
}
