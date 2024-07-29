/*
This code is used to read and respond to a UDP Python Script
*/
  #include <WiFi.h>
  #include <WiFiUdp.h>
  #include <cstring>
  #define SSID "Embedded"                 // Wi-Fi User Name
  #define PSWD "Embedded54321"            // Wi-Fi Password
  WiFiUDP udp;
/***********************************************************************/
  unsigned int localUdpPort = 4210;       // port to listen on
  char incomingPacket[255];
  String msg = "SystemReady" ;
  String RCV_MSG = "NONE";
/***********************************************************************/
  void Connect_WiFi();
  void UDP_RCV();
  void UDP_Transmit(IPAddress,uint16_t,char *s);
/***********************************************************************/
  void setup() 
  {
    Connect_WiFi();
  }
/***********************************************************************/
  void loop() 
  {
    if(Serial.available())
    {
      char x;
      x=Serial.read();
      if(x=='a')
      {
        msg = "TB";
      }
      else if(x=='b')
      {
        msg = "RTB";
      }
      else if(x=='c')
      {
        msg = "READY";
      }
    }
    UDP_RCV();
    delay(800);
  }
/***********************************************************************/
  void Connect_WiFi()
  {
    Serial.begin(9600);
    WiFi.disconnect();
    delay(1000);
    pinMode(2, OUTPUT);
    Serial.println("Connecting to WiFi");
    WiFi.begin(SSID, PSWD);
    delay(100);
    Serial.println("");
    while (!(WiFi.status() == WL_CONNECTED))
    {
      digitalWrite(2, LOW);
      delay(250);
      digitalWrite(2, HIGH);
      delay(250);
      Serial.print("*");
    }
    Serial.println("Connected to Wi-Fi");
    udp.begin(localUdpPort);
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    Serial.print("PORT: ");
    Serial.println(localUdpPort);
    delay(1000);
  }
/***********************************************************************/
void UDP_RCV()
{
  uint8_t buffer[50] = "";
  char n[10];
  String m;
  memset(buffer, 0, 50);
  int packetSize = udp.parsePacket();
  if (packetSize > 0)
  {
    // Get the remote IP address and port
    IPAddress remoteIP = udp.remoteIP();    
    uint16_t remotePort = udp.remotePort();

    Serial.print("\n\nReceived from\nIP Adress : ");
    Serial.print(remoteIP);
    Serial.print("  PORT  : ");
    Serial.println(remotePort);

    udp.read(buffer, 50);
    RCV_MSG = String((char *)buffer);
    Serial.print("Server to client: ");
    Serial.println(RCV_MSG);
    for(int i=0; RCV_MSG[i] != '\0';i++)
    {
      Serial.print("RCV_MSG[");Serial.print(i);Serial.print("] > =");Serial.println(RCV_MSG[i]);
    }

    UDP_Transmit(remoteIP,remotePort,&msg[0]);
  }
}
/***********************************************************************/
void UDP_Transmit(IPAddress udpAddress,uint16_t udpPort,char *s)
{
  int i;
  uint8_t buffer[50] = "";
  for (i = 0; *s != '\0'; i++, s++)
  {
    buffer[i] = *s;
  }
  buffer[i] = '\0';
  udp.beginPacket(udpAddress, 2020);
  udp.write(buffer, i);
  udp.endPacket();
}
/***********************************************************************/
 
