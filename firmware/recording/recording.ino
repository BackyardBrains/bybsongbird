#include <ArduinoJson.h>
#include <RTClib.h>
// be careful to use 1.2.0 version SD, otherwise the file.seek() won't work
//#include <SD.h>
#include <SPI.h>
#include <Wire.h>
#include <WiFi101.h>
#include <WiFiUdp.h>
// system defines file for macro
#include "sysdef.h"
//  Test routine heavily inspired by wiring_analog.c from GITHUB site
#include "Arduino.h"
#include "wiring_private.h"
#include "DHT.h"
#include <SdFat.h>
//If you get a compiler error saying that util/delay.h does not exist then just
//comment out the #include line for this in TLS2561.cpp from the adafruit library
#include "TSL2561.h"

#ifdef _VARIANT_ARDUINO_ZERO_
volatile uint32_t *setPin = &PORT->Group[g_APinDescription[PIN].ulPort].OUTSET.reg;
volatile uint32_t *clrPin = &PORT->Group[g_APinDescription[PIN].ulPort].OUTCLR.reg;
const uint32_t  PinMASK = (1ul << g_APinDescription[PIN].ulPin);
#endif


//******************************************************************************
// Global Variables
//
//
//******************************************************************************
WiFiUDP Udp;
WiFiClient client;
SdFat SD;
char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
char ssid_config[30] = {'\0'};
char pass_config[30] = {'\0'};
int keyIndex = 0;            // your network key Index number (needed only for WEP)
int status = WL_IDLE_STATUS;
const int chipSelect = 4;
String upload_filename = "BIRD0.WAV";
char server_ip[] = "10.0.0.193";
char back_yard_brain[] = "songbird.backyardbrains.com";

unsigned int localPort = 2390;

//int buf_size = WIFI_UPLOAD_BUFFER_SIZE;
File audio_file;
//byte content1[WIFI_UPLOAD_BUFFER_SIZE];
int time_length = 0;


// variable for sensor and real-time clock
DHT dht(DHTPIN, DHTTYPE);
TSL2561 tsl(TSL2561_ADDR_FLOAT); //sensor object
RTC_DS1307 rtc;// Real time clock

bool isLEDOn = false;

// variable for read write file in SD card
File myFile;
String filename = "BIRD0.WAV";
int fileNum = 0;
bool fileOpen = 0;

// variable for device configuration
File configFile;
char *configString;
float Lat = 999;
float Lon = 999;
String wifi_name;
String wifi_password;

// Buffer for storing sampling data temporarily
byte buffer[BUFFER_SIZE];
byte *anaHead = &buffer[0];
byte *sdHead = &buffer[0];

const long limit = 2 * sampleRate;
long counter = 0;
bool saveToCard = 0;

uint32_t Status = 0x00000000;
uint32_t ulPin = A1;//This is the analog pin to read
bool doRecord = 1;// recording state flag

//Keeps track of whether the stop button has been pressed since the end of the last recording
bool buttonPressed = 0;
int curHeadPos;
int newPos;
bool hasSaved = 1;

//------------------------------------------------------------------------------
//	Functions define
//
//------------------------------------------------------------------------------
inline void dis_wifi_control() {
  digitalWrite(WIFI_CS, HIGH);
}

inline void en_wifi_control() {
  digitalWrite(WIFI_CS, LOW);
}

void sendStartHttp() {
  client.stop();
  if (client.connect(back_yard_brain, 80)) {
    Serial.println("connecting success");
    en_wifi_control();
    client.println("POST /api/device HTTP/1.1");
    client.println("Host: songbird.backyardbrains.com");
    client.println("User-Agent: Arduino/1.0");
    client.println("Connection: close");
    client.println("Content-Type: text/html");
    client.print("Content-Length: ");
    client.println(sizeof(START_MSG));
    client.println();
    client.print(START_MSG);
    dis_wifi_control();
  } else {
    Serial.println("connecting fail");
  }

}

void sendEndHttp() {
  client.stop();
  if (client.connect(back_yard_brain, 80)) {
    Serial.println("connecting success");
    en_wifi_control();
    client.println("POST /api/device HTTP/1.1");
    client.println("Host: songbird.backyardbrains.com");
    client.println("User-Agent: Arduino/1.0");
    client.println("Connection: close");
    client.println("Content-Type: text/html");
    client.print("Content-Length: ");
    client.println(sizeof(END_MSG));
    client.println();
    client.print(END_MSG);
    dis_wifi_control();
  } else {
    Serial.println("connecting fail");
  }

}

void postDataUdp() {
  // Combine yourdatacolumn header (yourdata=) with the data recorded from your arduino
  // (yourarduinodata) and package them into the String yourdata which is what will be
  // sent in your POST request
  Serial.begin(9600);
  Serial.println("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(SD_CS)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  Serial.println("card initialized.");

  char char_array[30] = {'\0'};
  filename.toCharArray(char_array, 30);
  audio_file = SD.open(char_array, FILE_READ);

  Serial.println("data to send :");

  Serial.println("\nStarting connection to server...");

  Serial.println("Connecting successfully");

  int client_count = 10240;
  int filesize = audio_file.size();
  int slice_size = BUFFER_SIZE;
  int num_slices = filesize / slice_size;
  //num_slices = 1;
  //num_slices = 40;
  //content1[64] = '\0';
  int slice_left = filesize % slice_size;
  Serial.println(num_slices);
  Serial.println(slice_left);
  Serial.print("Start Time: ");
  int time = millis();
  Serial.println(time);


  sendStartHttp();


  int count = 0;
  int ret = 0;
  while (num_slices > 0) {

    audio_file.read(buffer, BUFFER_SIZE);
    en_wifi_control();
    Udp.beginPacket(back_yard_brain, 8080);
    ret = Udp.write(buffer, BUFFER_SIZE);
    Udp.endPacket();
    dis_wifi_control();
    num_slices--;

  }
  audio_file.read(buffer, slice_left);
  en_wifi_control();
  Udp.beginPacket(server_ip, 8080);
  Udp.write(buffer, slice_left);
  Udp.endPacket();
  dis_wifi_control();

  sendEndHttp();

  audio_file.flush();
  audio_file.close();
  Serial.println("Data sent finish");
  Serial.print("End time: ");
  time_length = millis() - time;
  time_length = time_length / 1000.0;
  time = millis();
  Serial.println(time);
  Serial.print("Spend ");
  Serial.print(time_length);
  Serial.print(" s to send data");
  Serial.end();
}



void postData() {
  // Combine yourdatacolumn header (yourdata=) with the data recorded from your arduino
  // (yourarduinodata) and package them into the String yourdata which is what will be
  // sent in your POST request
  Serial.begin(9600);
  Serial.println("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(SD_CS)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  Serial.println("card initialized.");

  // Check existance of file
  //  if(!SD.exists(filename)){
  //    Serial.println("No file: " + filename);
  //  }
  char char_array[30] = {'\0'};
  filename.toCharArray(char_array, 30);
  audio_file = SD.open(char_array, FILE_READ);
  //  read_count++;
  //audio_file.read(header, 44);
  //audio_file.seek(44);

  Serial.println("data to send :");

  Serial.println("\nStarting connection to server...");

  if (1) {
    Serial.println("Connecting successfully");

    int client_count = 10240;
    //int filesize = 1024*200;
    int filesize = audio_file.size();
    int slice_size = 1024 * 1024;
    int num_slices = filesize / slice_size;
    //num_slices = 1;
    //num_slices = 40;
    //content1[64] = '\0';
    Serial.println(num_slices);
    int slice_left = filesize % slice_size;
    Serial.println(slice_left);
    Serial.print("Start Time: ");
    int time = millis();
    Serial.println(time);


    int count = 0;
    int ret = 0;
    //    while(num_slices>0){
    //        //Serial.println(num_slices);
    //        audio_file.read(buffer, BUFFER_SIZE);
    //        en_wifi_control();
    //        Udp.beginPacket(server_ip, 8080);
    //        ret = Udp.write(buffer, BUFFER_SIZE);
    //        Udp.endPacket();
    //        dis_wifi_control();
    //        num_slices--;
    //        //Serial.println(num_slices);
    //        //Serial.println(ret);
    //    }
    //    audio_file.read(buffer,slice_left);
    //    en_wifi_control();
    //    Udp.beginPacket(server_ip, 8080);
    //    Udp.write(buffer, slice_left);
    //    Udp.endPacket();
    //    dis_wifi_control();
    client.stop();
    if (client.connect(back_yard_brain, 80)) {
      Serial.println("connecting success");

      while (num_slices > 0) {
        client.stop();
        client.connect(back_yard_brain, 80);
        //Serial.println(num_slices);
        //audio_file.read(buffer, slice_size);
        en_wifi_control();
        client.println("POST /api/device HTTP/1.1");
        client.println("Host: songbird.backyardbrains.com");
        client.println("User-Agent: Arduino/1.0");
        client.println("Connection: keep-alive");
        client.println("Content-Type: text/html");
        client.print("Content-Length: ");
        client.println(slice_size);
        client.println();
        int ret1 = 0;
        int chunk_size = 1400;
        int chunk_number = slice_size / chunk_size;
        int chunk_left = slice_size % 1400;
        int m = 0;
        for (m = 0; m < chunk_number; m++) {
          dis_wifi_control();
          audio_file.read(buffer, chunk_size);
          en_wifi_control();
          ret1 = client.write((uint8_t*)buffer, chunk_size);
          //Serial.println(ret1);
        }
        dis_wifi_control();
        audio_file.read(buffer, chunk_left);
        en_wifi_control();
        client.write((uint8_t*)buffer, chunk_left);

        //Serial.println(ret1);
        //        for(int c=0;c<slice_size;c++){
        //        client.print((char)buffer[c]);
        //        }        //client.println();
        dis_wifi_control();
        num_slices--;
        Serial.println(num_slices);
        //Serial.println(ret);
      }
      client.stop();
      client.connect(back_yard_brain, 80);
      //audio_file.read(buffer, slice_left);
      en_wifi_control();
      client.println("POST /api/device HTTP/1.1");
      client.println("Host: songbird.backyardbrains.com");
      client.println("User-Agent: Arduino/1.0");
      client.println("Connection: close");
      client.println("Content-Type: text/html");
      client.print("Content-Length: ");
      client.println(slice_left);
      client.println();
      int ret1 = 0;
      int chunk_size = 1400;
      int chunk_number = slice_left / chunk_size;
      int chunk_left = slice_left % 1400;
      int m = 0;
      for (m = 0; m < chunk_number; m++) {
        dis_wifi_control();
        audio_file.read(buffer, chunk_size);
        en_wifi_control();
        ret1 = client.write((uint8_t*)buffer, chunk_size);
        //Serial.println(ret1);
      }
      dis_wifi_control();
      audio_file.read(buffer, chunk_left);
      en_wifi_control();
      client.write((uint8_t*)buffer, chunk_left);
      //      int ret1=0;
      //      ret1 = client.write((uint8_t*)buffer, slice_left);
      //      Serial.println(ret1);
      //      //for(int c=0;c<slice_left;c++){
      //      //  client.print((char)buffer[c]);
      //      //}        //client.println();
      dis_wifi_control();
    } else {

      Serial.println("connection fail");
    }

    audio_file.flush();
    audio_file.close();
    Serial.println("Data sent finish");
    Serial.print("End time: ");
    time_length = millis() - time;
    time_length = time_length / 1000.0;
    time = millis();
    Serial.println(time);
    Serial.print("Spend ");
    Serial.print(time_length);
    Serial.print(" s to send data");


  }
  else {
    // If you couldn't make a connection:
    Serial.println("Connection failed");
    Serial.println("Disconnecting.");

  }
  Serial.end();
}

void printWiFiStatus() {
  // print the SSID of the network you're attached to:
  Serial.begin(9600);
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
  Serial.end();
}


uint8_t wifi_init() {

  //Initialize serial and wait for port to open:
  //digitalWrite(WIFI_CS,LOW);
  Serial.begin(9600);
  status = WL_IDLE_STATUS;
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    return WL_NO_SHIELD;
  }
  // attempt to connect to WiFi network in 3 times

  for(int i=0;i<3;i++){
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);
    delay(10000);
    if(status == WL_CONNECTED){
      break;
    } 
  }

  if(status != WL_CONNECTED){
    Serial.print("fail to connect to SSID: ");
    Serial.println(ssid);
    Serial.end();
    return status; 
  }

  // while ( status != WL_CONNECTED) {
  //   Serial.print("Attempting to connect to SSID: ");
  //   Serial.println(ssid);
  //   // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
  //   status = WiFi.begin(ssid, pass);

  //   // wait 10 seconds for connection:
  //   delay(10000);
  // }
  Serial.println("Connected to wifi");
  printWiFiStatus();

  Serial.println("\nStarting connection to server...");
  Udp.begin(localPort);

  Serial.end();
  return status;
}

void wifi_deinit() {
  Serial.begin(9600);
  if (WiFi.status() == WL_CONNECTED) {
    WiFi.disconnect();
    WiFi.end();
    Serial.println("disable the wifi module");
  }
  Serial.println("disable the wifi module");
  Serial.end();
}


//This sets the sample rate for analog sampling
void setTimerFrequency(int frequencyHz) {
  int compareValue = (CPU_HZ / (TIMER_PRESCALER_DIV * frequencyHz)) - 1;
  TcCount16* TC = (TcCount16*) TC3;
  // Make sure the count is in a proportional position to where it was
  // to prevent any jitter or disconnect when changing the compare value.
  TC->COUNT.reg = map(TC->COUNT.reg, 0, TC->CC[0].reg, 0, compareValue);
  TC->CC[0].reg = compareValue;
  while (TC->STATUS.bit.SYNCBUSY == 1);
}

//Initializs the Real-time Clock
//Gets the current timestamp in a format that can be used later by the SD library
void dateTime(uint16_t* date, uint16_t* time) {
  DateTime now = rtc.now();
  *date = FAT_DATE(now.year(), now.month(), now.day());
  // return time using FAT_TIME macro to format fields
  *time = FAT_TIME(now.hour(), now.minute(), now.second());
}

//Opens a new file on the sd-card for writing
void sdInit() {
  Serial.begin(9600);
  //Loop ensures that files won't be overwritten on the card in the device is reset
  //while(SD.exists(filename)){
  //  ++fileNum;
  //  filename = "BIRD" + (String)fileNum + ".WAV";
  //}
  //fileNum = 0;
  //filename = "BIRD" + (String)fileNum + ".WAV";
  char char_array[30] = {'\0'};

  //Set file creation date and open for writing
  SdFile::dateTimeCallback(dateTime);
  filename.toCharArray(char_array, sizeof(char_array));
  if (!SD.exists(char_array)) {
    SdFile temp_file;
    temp_file.open(char_array, O_CREAT | O_WRITE);
    temp_file.close();

  }
  myFile = SD.open(char_array, FILE_WRITE);

  if (!myFile) {
    Serial.println("Open file fail - sdINIT");
    while (1);
  }
  else {
    //The 1st 44 bytes of a wav file are the header, this will be written later
    myFile.seek(myFile.size());
    fileOpen = 1;
    //Turn of the led connected to pin 13 to indicate that it is unsafe to remove the card
    digitalWrite(sdPin, !fileOpen);
  }

  Serial.end();
}

void readConfig(void) {
  StaticJsonBuffer<256> jsonBuffer;
  Serial.begin(9600);
  if (!SD.exists("config")) {
    Serial.println("No config file: using defaults!");
  }
  else {
    configFile = SD.open("config", FILE_READ);
    configString = (char *) malloc(configFile.size());
    configFile.read(configString, configFile.size());
    configFile.close();
    JsonObject& configObject = jsonBuffer.parseObject(configString);
    //    Lat = configObject["Lat"];
    //    Lon = configObject["Lon"];
    /*
      {
      "wifi_name": "Jun'siPhone",
      "wifi_password": "12345678a"
      }
    */
    wifi_name = configObject["wifi_name"].asString();
    wifi_password = configObject["wifi_password"].asString();
    wifi_name.toCharArray(ssid_config, sizeof(ssid_config));
    wifi_password.toCharArray(pass_config, sizeof(pass_config));

  }
  Serial.end();
}


//This function creates a header for the wav file and writes it to the 1st 44 bytes of the currently open file
void makeHeader(int totalAudioLen) {

  float tem = dht.readTemperature();
  float hum = dht.readHumidity();
  uint16_t lum = tsl.getLuminosity(TSL2561_VISIBLE);

  String temperature = (String)tem;
  String humidity = (String)hum;
  String latitude = (String)Lat;
  String longitude = (String)Lon;
  String light = (String)lum;

  byte metaData[metaDataSize];
  metaData[0] = 'L';
  metaData[1] = 'I';
  metaData[2] = 'S';
  metaData[3] = 'T';
  metaData[4] = metaDataSize;
  metaData[5] = 0;
  metaData[6] = 0;
  metaData[7] = 0;
  metaData[8] = 'I';
  metaData[9] = 'N';
  metaData[10] = 'F';
  metaData[11] = 'O';
  metaData[12] = 'T';
  metaData[13] = 'E';
  metaData[14] = 'M';
  metaData[15] = 'P';
  metaData[16] = 8;
  metaData[17] = 0;
  metaData[18] = 0;
  metaData[19] = 0;
  metaData[20] = 0;
  metaData[21] = 0;
  metaData[22] = 0;
  metaData[23] = 0;
  metaData[24] = 0;
  metaData[25] = 0;
  metaData[26] = 0;
  metaData[27] = 0;

  int j = 20;
  for (int i = 0; i < temperature.length(); ++i) {
    metaData[j] = temperature[i];
    ++j;
  }

  metaData[28] = 'H';
  metaData[29] = 'U';
  metaData[30] = 'M';
  metaData[31] = 'I';
  metaData[32] = 8;
  metaData[33] = 0;
  metaData[34] = 0;
  metaData[35] = 0;
  metaData[36] = 0;
  metaData[37] = 0;
  metaData[38] = 0;
  metaData[39] = 0;
  metaData[40] = 0;
  metaData[41] = 0;
  metaData[42] = 0;
  metaData[43] = 0;

  int k = 36;
  for (int l = 0; l < humidity.length(); ++l) {
    metaData[k] = humidity[l];
    ++k;
  }

  metaData[44] = 'L';
  metaData[45] = 'A';
  metaData[46] = 'T';
  metaData[47] = 'I';
  metaData[48] = 8;
  metaData[49] = 0;
  metaData[50] = 0;
  metaData[51] = 0;
  metaData[52] = 0;
  metaData[53] = 0;
  metaData[54] = 0;
  metaData[55] = 0;
  metaData[56] = 0;
  metaData[57] = 0;
  metaData[58] = 0;
  metaData[59] = 0;

  int m = 52;
  for (int n = 0; n < latitude.length(); ++n) {
    metaData[m] = latitude[n];
    ++m;
  }

  metaData[60] = 'L';
  metaData[61] = 'O';
  metaData[62] = 'N';
  metaData[63] = 'G';
  metaData[64] = 8;
  metaData[65] = 0;
  metaData[66] = 0;
  metaData[67] = 0;
  metaData[68] = 0;
  metaData[69] = 0;
  metaData[70] = 0;
  metaData[71] = 0;
  metaData[72] = 0;
  metaData[73] = 0;
  metaData[74] = 0;
  metaData[75] = 0;

  int o = 68;
  for (int p = 0; p < longitude.length(); ++p) {
    metaData[o] = longitude[p];
    ++o;
  }

  metaData[76] = 'L';
  metaData[77] = 'I';
  metaData[78] = 'T';
  metaData[79] = 'E';
  metaData[80] = 8;
  metaData[81] = 0;
  metaData[82] = 0;
  metaData[83] = 0;
  metaData[84] = 0;
  metaData[85] = 0;
  metaData[86] = 0;
  metaData[87] = 0;
  metaData[88] = 0;
  metaData[89] = 0;
  metaData[90] = 0;
  metaData[91] = 0;

  int q = 84;
  for (int r = 0; r < light.length(); ++r) {
    metaData[q] = light[r];
    ++q;
  }

  //myFile.write(metaData, metaDataSize);

  const int compressionType = 1;
  const int numOfChannels = 1;
  const int byteRate = (sampleRate * numOfChannels * 16) / 8;
  const int totalDataLen = myFile.size();

  byte header[44];
  header[0] = 'R';  // RIFF/WAVE header
  header[1] = 'I';
  header[2] = 'F';
  header[3] = 'F';
  header[4] = (byte) (totalDataLen & 0xff);
  header[5] = (byte) ((totalDataLen >> 8) & 0xff);
  header[6] = (byte) ((totalDataLen >> 16) & 0xff);
  header[7] = (byte) ((totalDataLen >> 24) & 0xff);
  header[8] = 'W';
  header[9] = 'A';
  header[10] = 'V';
  header[11] = 'E';
  header[12] = 'f';  // 'fmt ' chunk
  header[13] = 'm';
  header[14] = 't';
  header[15] = ' ';
  header[16] = 16;  // 4 bytes: size of 'fmt ' chunk
  header[17] = 0;
  header[18] = 0;
  header[19] = 0;
  header[20] = (byte)  compressionType;  // format = 1
  header[21] = 0;
  header[22] = (byte)  numOfChannels;
  header[23] = 0;
  header[24] = (byte) (sampleRate & 0xff);
  header[25] = (byte) ((sampleRate >> 8) & 0xff);
  header[26] = (byte) ((sampleRate >> 16) & 0xff);
  header[27] = (byte) ((sampleRate >> 24) & 0xff);
  header[28] = (byte) (byteRate & 0xff);
  header[29] = (byte) ((byteRate >> 8) & 0xff);
  header[30] = (byte) ((byteRate >> 16) & 0xff);
  header[31] = (byte) ((byteRate >> 24) & 0xff);
  header[32] = (byte) (numOfChannels * 2);  // block align
  header[33] = 0;
  header[34] = 16;  // bits per sample (32 for float)
  header[35] = 0;
  header[36] = 'd';
  header[37] = 'a';
  header[38] = 't';
  header[39] = 'a';
  header[40] = (byte) (totalAudioLen & 0xff);
  header[41] = (byte) ((totalAudioLen >> 8) & 0xff);
  header[42] = (byte) ((totalAudioLen >> 16) & 0xff);
  header[43] = (byte) ((totalAudioLen >> 24) & 0xff);

  Serial.begin(9600);


  if (myFile) {
    // move the write pointer to the head of file and write the header
    myFile.seek(0);
    myFile.write(header, 44);
  }
  else {
    Serial.println("file open fail - header");
    while (1);
  }

  Serial.end();
}


/*
  This is a slightly modified version of the timer setup found at:
  https://github.com/maxbader/arduino_tools
*/
//Function starts the timer which will trigger an interrupt at the set sample rate to sample from the analog pin
void startTimer(int frequencyHz) {
  REG_GCLK_CLKCTRL = (uint16_t) (GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK0
                                 | GCLK_CLKCTRL_ID (GCM_TCC2_TC3)) ;
  while ( GCLK->STATUS.bit.SYNCBUSY == 1 );

  TcCount16* TC = (TcCount16*) TC3;

  TC->CTRLA.reg &= ~TC_CTRLA_ENABLE;

  // Use the 16-bit timer
  TC->CTRLA.reg |= TC_CTRLA_MODE_COUNT16;
  while (TC->STATUS.bit.SYNCBUSY == 1);

  // Use match mode so that the timer counter resets when the count matches the compare register
  TC->CTRLA.reg |= TC_CTRLA_WAVEGEN_MFRQ;
  while (TC->STATUS.bit.SYNCBUSY == 1);

  // Set prescaler to 1024
  TC->CTRLA.reg |= TC_CTRLA_PRESCALER_DIV64;
  while (TC->STATUS.bit.SYNCBUSY == 1);

  setTimerFrequency(frequencyHz);

  // Enable the compare interrupt
  TC->INTENSET.reg = 0;
  TC->INTENSET.bit.MC0 = 1;

  NVIC_EnableIRQ(TC3_IRQn);

  TC->CTRLA.reg |= TC_CTRLA_ENABLE;
  while (TC->STATUS.bit.SYNCBUSY == 1);
}

void stopTimer() {
  TcCount16* TC = (TcCount16*) TC3;
  TC->INTENSET.reg = 0;              // disable all interrupts
  TC->INTENSET.bit.MC0 = 1;          // enable compare match to CC0

  // Enable InterruptVector
  NVIC_DisableIRQ(TC3_IRQn);

  // Enable TC
  TC->CTRLA.reg &= ~TC_CTRLA_ENABLE;
  while (TC->STATUS.bit.SYNCBUSY == 1); // wait for sync

}
//##############################################################################
// Stripped-down fast analogue read anaRead()
// ulPin is the analog input pin number to be read.
////##############################################################################
uint16_t anaRead() {

  ADCsync();
  ADC->INPUTCTRL.bit.MUXPOS = g_APinDescription[ulPin].ulADCChannelNumber; // Selection for the positive ADC input

  ADCsync();
  ADC->CTRLA.bit.ENABLE = 0x01;             // Enable ADC

  ADC->INTFLAG.bit.RESRDY = 1;              // Data ready flag cleared

  ADCsync();
  ADC->SWTRIG.bit.START = 1;                // Start ADC conversion

  while ( ADC->INTFLAG.bit.RESRDY == 0 );   // Wait till conversion done
  ADCsync();
  uint16_t valueRead = ADC->RESULT.reg;

  ADCsync();
  ADC->CTRLA.bit.ENABLE = 0x00;             // Disable the ADC
  ADCsync();
  ADC->SWTRIG.reg = 0x01;                    //  and flush for good measure
  return valueRead;
}
//##############################################################################

//Interrupt triggered by the timer at the set sample rate; Takes one analog sample and adds it to the buffer
void TC3_Handler() {
  static uint16_t anaVal;
  TcCount16* TC = (TcCount16*) TC3;
  // If this interrupt is due to the compare register matching the timer count
  // we toggle the LED.
  if (TC->INTFLAG.bit.MC0 == 1) {
    TC->INTFLAG.bit.MC0 = 1;
    //digitalWrite(2, HIGH);

    //Does a single read from the analog pin and adds it to the buffer
    anaVal = anaRead();
    anaVal = anaVal - 2048; //Center the always positve 12 bit analog sample at 0
    anaVal = anaVal * -16; //Invert the sample to accomodate for the inverted op-amp and multiply by 2^4 to amplifiy (12 bits to 16 bits)

    *anaHead = anaVal & 0xFF;
    ++anaHead;
    *anaHead = (anaVal >> 8) & 0xFF;
    ++anaHead;
    if (anaHead >= &buffer[BUFFER_SIZE - 1]) {
      anaHead = &buffer[0];
    }

    //digitalWrite(2, LOW);
    //reads from the activity detector (sound threshold) on pin 7
    //Increments a counter that will reach it's maximum value after 2 seconds of inactivity
    //This will be used later to trigger the end of the recording
    if (counter < 22 * 1800 * limit) {
      ++counter;
    }
    else {
      //counter = 0;
    }
  }
}

// This is an C/C++ code to insert repetitive code sections in-line pre-compilation
// Wait for synchronization of registers between the clock domains
// ADC
static __inline__ void ADCsync() __attribute__((always_inline, unused));
static void   ADCsync() {
  while (ADC->STATUS.bit.SYNCBUSY == 1); //Just wait till the ADC is free
}

// DAC
static __inline__ void DACsync() __attribute__((always_inline, unused));
static void DACsync() {
  while (DAC->STATUS.bit.SYNCBUSY == 1);
}

//Interrupt function to set the variable that determines whether we should continue recording after the current file
void recordToggle() {
  if (!buttonPressed) {
    doRecord = !doRecord;
    buttonPressed = 1;
  }
}

// Function to delete all saved file in SD card
void delete_all_file() {
  String target_name = "BIRD0.WAV";
  char target_name_c[] =  "BIRD0.WAV";
  int target_filenum = 1;
  digitalWrite(recordPin, HIGH);
  while (SD.exists(target_name_c)) {
    SD.remove(target_name_c);
    //target_name = "BIRD" + (String)target_filenum + ".WAV";
    //++target_filenum;
  }
  digitalWrite(recordPin, LOW);
}

void setup()
{
  dht.begin();
  tsl.begin();
  digitalWrite(recordPin, LOW);
  //Sets the rtc if it's not running
  if (!rtc.begin()) {
    Serial.begin(9600);
    Serial.println("RTC cannot start");
    Serial.end();
  }
  if (!rtc.isrunning()) {
    // following line sets the RTC to the date & time this sketch was compiled
    //This will occur if the external rtc loses power, eg. the coincell dies or is removed
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));

  //Initialize the sd card and the sd-activity led on pin 13
  pinMode(sdPin, OUTPUT);
  pinMode(recordPin, OUTPUT);
  pinMode(WIFI_CS, OUTPUT);
  digitalWrite(sdPin, LOW);
  digitalWrite(recordPin, LOW);
  dis_wifi_control();
  WiFi.setPins(WIFI_CS, 7, 5);
  //wifi_init();

  if (!SD.begin(SD_CS)) {
    Serial.begin(9600);
    Serial.println("Cannot connect to SD Card");
    Serial.end();
    digitalWrite(sdPin, HIGH);
    while (1);
  }
  readConfig(); //Grab Data from config file if it exists
  //delete_all_file();
  fileNum = 0;
  char char_array[30] = {'\0'};
  filename = "BIRD" + (String)fileNum + ".WAV";
  filename.toCharArray(char_array, sizeof(char_array));
  while (SD.exists(char_array)) {
    ++fileNum;
    filename = "BIRD" + (String)fileNum + ".WAV";
    filename.toCharArray(char_array, sizeof(char_array));
  }
  sdInit();
  //pinMode(PIN, OUTPUT);        // setup timing marker

  //###################################################################################
  // ADC setup stuff
  //###################################################################################
  ADCsync();
  ADC->INPUTCTRL.bit.GAIN = ADC_INPUTCTRL_GAIN_1X_Val;      // Gain select as 1X
  ADC->REFCTRL.bit.REFSEL = ADC_REFCTRL_REFSEL_INTVCC0_Val; //  2.2297 V Supply VDDANA

  // Set sample length and averaging
  ADCsync();
  ADC->AVGCTRL.reg = 0x00 ;       //Single conversion no averaging
  ADCsync();
  ADC->SAMPCTRL.reg = 0x0A;  ; //sample length in 1/2 CLK_ADC cycles Default is 3F

  //Control B register
  int16_t ctrlb = 0x400;       // Control register B hibyte = prescale, lobyte is resolution and mode
  ADCsync();
  ADC->CTRLB.reg =  ctrlb     ;
  anaRead();  //Discard first conversion after setup as ref changed

  //Start reading from the activity detection pin and start sampling from the analog pin
  //pinMode(7, INPUT);
  startTimer(sampleRate);
  //Attaches an interrupt to the button on pin 12 to flip a variable that will tell the device not to open a new file after the current
  //one finishes, so the sd-card can be safely removed
  attachInterrupt(digitalPinToInterrupt(12), recordToggle, RISING);
}

void loop()
{
  if (fileOpen) {

    // When press the button or recording last moret than 22 hours, it will recalculate the file header
    if ((counter >= 22 * 1800 * limit) || (!doRecord)) {
      if (!hasSaved || !doRecord) {
        makeHeader(myFile.size() - 44);
        myFile.flush();
        myFile.close();
        stopTimer();
        // Code here for uploading

        en_wifi_control();
        if(wifi_init() == WL_CONNECTED)
        {
        //postData();
        postDataUdp();
        delay(1000);
        wifi_deinit();
        }
        dis_wifi_control();


        startTimer(sampleRate);

        if (counter >= 22 * 1800 * limit) {
          fileNum++;
          filename = "BIRD" + (String)fileNum + ".WAV";
        }
        digitalWrite(recordPin, LOW);
        fileOpen = 0;
        digitalWrite(sdPin, !fileOpen);
        if (doRecord) {
          SD.begin(SD_CS);
          sdInit();
        }
        hasSaved = 1;
        buttonPressed = 0;
        counter = 0;
      }
      counter = 0;
    }

    // Continuously writing data in buffer into file.
    else {
      digitalWrite(recordPin, HIGH);
      hasSaved = 0;
      int numBytes = anaHead - sdHead;
      if (numBytes > 0) {
        //digitalWrite(5, HIGH);
        myFile.write(sdHead, numBytes);
        //digitalWrite(5,LOW);
        sdHead += numBytes;
      }
      else
      {
        if (numBytes != 0)
        {
          numBytes += BUFFER_SIZE;
          curHeadPos = sdHead - &buffer[0];
          newPos = numBytes - (BUFFER_SIZE - curHeadPos);
          //digitalWrite(5, HIGH);
          myFile.write(&buffer[curHeadPos], BUFFER_SIZE - curHeadPos);
          myFile.write(&buffer[0], newPos);
          //digitalWrite(5, LOW);
          sdHead = &buffer[newPos];
        }
      }
    }
  }

  //This should restart recording if the button on d12 is pressed again after recording has stopped
  else if (doRecord) {

    // Code for wifi uploading

    /*
      stopTimer();
      en_wifi_control();
      wifi_init();
      //postData();
      postDataUdp();
      delay(1000);
      wifi_deinit();
      dis_wifi_control();
      startTimer(sampleRate);
    */


    // Remain the begin here for hot swapping of SD card
    SD.begin(SD_CS);
    sdInit();
    digitalWrite(recordPin, HIGH);
    //startTimer(sampleRate);
    buttonPressed = 0;
    //doRecord = 0;
  }
}



