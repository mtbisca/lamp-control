/*lampcontrolserver.ino 
 * to be used with kivy sketch implementing
 * the same functionality of original lampcontrol-progmem.ino
 * and also displaying temperature, humidity and luminosity
 * added measures to deiect/correct connection problems
 * Celio G. MC853 May 27, 2019 
 */
#include <ESP8266WiFi.h>
#include "DHT.h"
#define DHTPIN D2
#define DHTTYPE DHT11

#define Show(string,val)Serial.print(string);Serial.println(val); //macro for common print case
const char* ssid = "aula-ic3";     // WiFi parameters
const char* password = "iotic@2019";

WiFiServer server(50007); // Create an instance of the server
WiFiClient client;        // and one of client to talk to client invoker
int userled=D0;

DHT dht(DHTPIN, DHTTYPE);
//*****************************************************************
void setup() {
  Serial.begin(115200);
  delay(10);
  pinMode(userled, OUTPUT);
  digitalWrite(userled, 1);  //Off 
  Serial.println();
  Show("Lamp Control Server is connecting to: ",ssid);
  WiFi.begin(ssid, password);    //WiFi connect
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  server.begin();        // Start the server
  Serial.println("Server started");
  Show("local IP= ",WiFi.localIP());
}
//**********************************************************
void loop() {
  client = server.available();  // Check if a client has connected
  if (!client) 
    return;                     // no, start loop() again
  Serial.println("new client");
  while (!client.available()){     
     delay(1);               // wait until client sends some data
    }
  while (1){                        //loop will read and echo lines sent by client
    if (!client.connected())break;      // seems not working!   
       while (!client.available()){       //but this works!
       delay(1);
       if (!client.connected())return;    
    }
    client.flush();
    String req = client.readStringUntil('\r'); 
    client.flush();
    Serial.print("***"+req);
    Serial.flush(); 
    if (req.indexOf("on")!= -1){
       digitalWrite(userled, 0);
       client.print(req);
    } else if (req.indexOf("off")!= -1) {
       digitalWrite(userled, 1);
       client.print(req);
    } else if (req.indexOf("state") != -1) {
      int state= digitalRead(userled);
      if (state==0)
         client.print("Led is On");
       else  
          client.print("Led is Off"); 
    } else if (req.indexOf("temp") != -1) {
      client.print(dht.readTemperature());       
    } else if (req.indexOf("hum") != -1) {
      client.print(dht.readHumidity());       
    } else if (req.indexOf("lum") != -1) {
      client.print(analogRead(A0));       
    }
    else ;//Show("Invalid request:",req);
    client.flush();
  }
  Serial.println("Client disconnected!");
}
