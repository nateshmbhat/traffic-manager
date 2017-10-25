char mystr[60]; //Initialized variable to store recieved data
String str;

int signal1[][12]={{0,0,1,1,0,0,1,0,0,1,0,0},{1,0,0,0,0,1,1,0,0,1,0,0},{1,0,0,1,0,0,0,0,1,1,0,0},{1,0,0,1,0,0,1,0,0,0,0,1},{0,1,1,1,0,0,1,0,0,1,0,0}};
int lights[]={2,3,4,5,6,7,8,9,10,11,12,A0,A1,A2,A3,A4};

void setup() {
  // Begin the Serial at 9600 Baud
  Serial.begin(115200);
  for(int i=0;i<16;i++)
    pinMode(lights[i],OUTPUT);
  pinMode(A5,INPUT);
  pinMode(A6,OUTPUT);
  pinMode(13,OUTPUT);
  digitalWrite(13,HIGH);
}
String msg;
void loop() {
  Serial.println(digitalRead(A5));
  digitalWrite(13,digitalRead(A5));
  while(Serial.available())
    {
      char ch=Serial.read();
      msg.concat(ch);

      if(ch=='F')
      {
        Serial.println("flash");
        digitalWrite(A1,HIGH);
        delay(500);
        digitalWrite(A1,LOW);
      }
    
    }
    if(msg.startsWith("A"))
      controlsignals(0);
    if(msg.startsWith("B"))
      controlsignals(1);
    if(msg.startsWith("C"))
      controlsignals(2);
    if(msg.startsWith("D"))
      controlsignals(3);
    if(msg.startsWith("G"))
      controlsignals(4);
    
    delay(100) ; 
    msg="" ;
    
}


void controlsignals(int side)
{
  Serial.println(side);
  for(int i=0;i<12;i++)
      {
        if(side==0)
          digitalWrite(A0,0);
        if(signal1[side][i]==1 && (i+1)%3==0)
        {
          digitalWrite(lights[i-1],HIGH);
          delay(1000);
          digitalWrite(lights[i-1],LOW);
        }
        digitalWrite(lights[i],signal1[side][i]);
        Serial.println("light "+ (String)i +" is "+(String)signal1[side][i]);
      }
    
}





