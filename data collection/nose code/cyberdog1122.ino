
#include <SPI.h>
#include <Wire.h>
#include <AD7173.h>

#include "Adafruit_SGP40.h"
#include "Adafruit_CCS811.h"
#include "SHT85.h"

#define SHT85_ADDRESS   0x44

uint32_t start;
uint32_t stop;
char wk='1';
SHT85 sht;

Adafruit_SGP40 sgp;
Adafruit_CCS811 ccs;

byte data[4];
unsigned long adc_val[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // store readings in array


void setup() {
  SerialUSB.begin(115200);
  Wire.begin();
  sht.begin(SHT85_ADDRESS);
  Wire.setClock(100000);

  uint16_t stat = sht.readStatus();
  
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);  
  pinMode(12, INPUT);
  pinMode(3, OUTPUT);
  AD7173.init();
  
  AD7173.sync();
  
  AD7173.reset();
  
  digitalWrite(11, HIGH); 
  
  if (AD7173.is_valid_id()) SerialUSB.println("AD7173 ID is valid");
  else SerialUSB.println("AD7173 ID is invalid");
  
  AD7173.set_channel_config(CH0, true, SETUP0, AIN0, AIN16);
  AD7173.set_channel_config(CH1, true, SETUP0, AIN1, AIN16);
  AD7173.set_channel_config(CH2, true, SETUP0, AIN2, AIN16);
  AD7173.set_channel_config(CH3, true, SETUP0, AIN3, AIN16);
  AD7173.set_channel_config(CH4, true, SETUP0, AIN4, AIN16);
  AD7173.set_channel_config(CH5, true, SETUP0, AIN5, AIN16);
  AD7173.set_channel_config(CH6, true, SETUP0, AIN6, AIN16);
  AD7173.set_channel_config(CH7, true, SETUP0, AIN7, AIN16);
  AD7173.set_channel_config(CH8, true, SETUP0, AIN8, AIN16);
  AD7173.set_channel_config(CH9, true, SETUP0, AIN9, AIN16);
  AD7173.set_channel_config(CH10, true, SETUP0, AIN10, AIN16);
  AD7173.set_channel_config(CH11, true, SETUP0, AIN11, AIN16);
  AD7173.set_channel_config(CH12, true, SETUP0, AIN12, AIN16);
  AD7173.set_channel_config(CH13, true, SETUP0, AIN13, AIN16);
  AD7173.set_channel_config(CH14, true, SETUP0, AIN14, AIN16);
  AD7173.set_channel_config(CH15, true, SETUP0, AIN15, AIN16);
  
  AD7173.set_setup_config(SETUP0, UNIPOLAR, AIN_BUF_DISABLE, REF_PWR);
  
  AD7173.set_offset_config(OFFSET0, 0);
  
  AD7173.set_filter_config(FILTER0, SPS_1007);
  
  AD7173.set_adc_mode_config(CONTINUOUS_CONVERSION_MODE, INTERNAL_CLOCK, REF_DISABLE);
  
  AD7173.set_interface_mode_config(false, true);
  
  if (! sgp.begin()){
    SerialUSB.println("Sensor not found :(");
    while (1);
  }
  
  if (!ccs.begin()){
    SerialUSB.println("Failed to start sensor! Please check your wiring.");
    while(1);
  }
  while(!ccs.available());
}


void loop() {
  uint16_t raw;
  uint16_t co2;
  uint16_t tvoc;

  if(ccs.available()){
    if(!ccs.readData()){
      co2 = ccs.geteCO2();
      tvoc = ccs.getTVOC();
    }
    else{
      SerialUSB.println("ERROR!");
      while(1);
    }
  }

  raw = sgp.measureRaw();

  int val1 = analogRead(14);
  float v1 = val1 * (5.0 / 1023.0)*0.65;
  int val2 = analogRead(15);
  float v2 = val2 * (5.0 / 1023.0)*0.65;
  int val3 = analogRead(16);
  float v3 = val3 * (5.0 / 1023.0)*0.65;
  int val4 = analogRead(17);
  float v4 = val4 * (5.0 / 1023.0)*0.65;
  int val5 = analogRead(18);
  float v5 = val5 * (5.0 / 1023.0)*0.65;

  int k = 0;
  while(1){
    if (DATA_READY) {
      k++;
      if(k>16) break;
      AD7173.get_data(data);
//      SerialUSB.println(data[3]);
      if(data[3]<16){
        adc_val[data[3]] = data[0];
        adc_val[data[3]] <<= 8; //shift to left
        adc_val[data[3]] |= data[1];
        adc_val[data[3]] <<= 8;
        adc_val[data[3]] |= data[2];
      }
    }
  }
  
  for (int i = 0; i < 16; i++) {
    SerialUSB.print(adc_val[i] * 0.0000003);
    SerialUSB.print(",");
  }
    wk = SerialUSB.read();
//    SerialUSB.print(wk);
    if(wk=='0'){
//      pinMode(3, OUTPUT);
      digitalWrite(3, HIGH);
//      SerialUSB.print("cnm");
}
    else if(wk=='1'){
         digitalWrite(3, LOW);
//      pinMode(3, INPUT);
//      SerialUSB.print("kkk");
}
    else{
//      pinMode(3, INPUT);
        digitalWrite(3, LOW);
//      SerialUSB.print("ooo");
      }
  SerialUSB.print(v1);
  SerialUSB.print(",");
  SerialUSB.print(v2);
  SerialUSB.print(",");
  SerialUSB.print(v3);
  SerialUSB.print(",");
//  SerialUSB.print(v4);
//  SerialUSB.print(",");
//  SerialUSB.print(v5);
//  SerialUSB.print(",");
  SerialUSB.print(raw);
  SerialUSB.print(",");
  SerialUSB.print(co2);
  //place for zmod
  SerialUSB.print(",");
  SerialUSB.print(tvoc);
  SerialUSB.print(",");
//  SerialUSB.print('\n');
//  start = micros();
  sht.read();         // default = true/fast       slow = false
//  stop = micros();
//  SerialUSB.print("\t");
//  SerialUSB.print((stop - start) * 0.001);
//  SerialUSB.print("\t");
  SerialUSB.print(sht.getTemperature(), 1);
  SerialUSB.print(",");
  SerialUSB.println(sht.getHumidity(), 1);
//  SerialUSB.print('\n');

  delay(200);
}
