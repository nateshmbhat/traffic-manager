#include <ESP8266WiFi.h>
#include <WiFiClient.h>

// Hardcode WiFi parameters as this isn't going to be moving around.
const char* ssid = "SJBIT3";
const char* password = "sjbit@1912";

const char* ip  = "192.168.68.223"  ;
int port = 34569 ;

// Start a TCP Server on port 5045
WiFiClient client ;

char msg[60]; 
int flag=0,flag1=1;
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid,password);
  Serial.println("");
  //Wait for connection
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("Connected to "); Serial.println(ssid);
  Serial.print("IP Address: "); Serial.println(WiFi.localIP());

  Serial.println("Connecting to : intel ") ;
  
  while(!client.connect( ip, port))
  {
    Serial.print(".") ; 
    delay(250) ;
  }
  if(client.connected()) Serial.println("\nCOnnected to Server ! \n\n") ;
  pinMode(D8,INPUT);
}


void loop() 
{
  
  char msg[60]; 
  int i=0 ;
  char c ;
  
  while(client.available())
  {
    c = client.read();
    Serial.print(c) ;
    if(!client.available())
      {
        //Serial.println(" ");
       // Serial.print("Messagg is : " );
        //Serial.println(msg) ;
      }

      msg[i++]=c;
  }
  Serial.write(msg,i); //Write the serial data
  Serial.println();
  if(digitalRead(D8)==LOW)
    flag=1;
  else
    {
      flag=0;
      if(flag1)
        flag1=0;
    }
  if(flag==1 && flag1==0 && msg[0]=='A')
    {
      char msg[60]; 
      msg[0]='F';
      Serial.write(msg,1); //Write the serial data
      Serial.println();
      client.print("bypassed\n"); 
      flag1=1; 
    }
  delay(500);
  


  
 /*
  *  while(Serial.available())
  {
    c = Serial.read() ; 
    client.print(c) ;
  }*/

}


