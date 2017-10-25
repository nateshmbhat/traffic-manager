char mystr[6] = "Hello"; //String data

void setup() {
  // Begin the Serial at 9600 Baud
  Serial.begin(115200);
}

void loop() {
  Serial.write(mystr,6); //Write the serial data
  Serial.println();
  delay(2000);
}














