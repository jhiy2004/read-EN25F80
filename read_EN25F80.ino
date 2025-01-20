#define CS 2
#define DO 3
#define WP 4
#define DI 5
#define CLK 6
#define HOLD 7

int INSTRUCTION = 0x03;
int WE = 0x06;
int PP = 0x02;
int RSR = 0x05;
int SEC_E = 0x20;
int CHIP_E = 0xc7;

int code = 0;

unsigned char ADD[3] = {0x00, 0x00, 0x16};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  
  pinMode(CS, OUTPUT);
  pinMode(DO, INPUT);
  pinMode(WP, OUTPUT);
  pinMode(DI, OUTPUT);
  pinMode(CLK, OUTPUT);
  pinMode(HOLD, OUTPUT);
  pinMode(8, OUTPUT);

  digitalWrite(8, HIGH);
  delay(50);
  digitalWrite(8, LOW);

  digitalWrite(HOLD, HIGH);

  //dump();

  //overwrite_memory();
  //delay(1000);
  //dump_test();

  //write_enable();
  //read_status_register();
}

void pass_byte(unsigned char byte){
  int bit = 0;

  for(int i=7; i >= 0; i--){
    bit = (byte >> i) & 1;
    if(bit == 1){
      digitalWrite(DI, HIGH);
    }else{
      digitalWrite(DI, LOW);
    }
    
    digitalWrite(CLK, HIGH);
    digitalWrite(CLK, LOW);
  }
}

unsigned char read_byte(unsigned char addr[3]){
  unsigned char byte = 0;
  int bit = 0;

  digitalWrite(CS, HIGH);
  digitalWrite(CLK, LOW);
  digitalWrite(CS, LOW);

  for(int i=0; i < 3; i++){
    pass_byte(addr[i]);
  }

  for(int i=0; i < 8; i++){
    bit = digitalRead(DO);
    byte = (byte << 1) + 1;

    digitalWrite(CLK, LOW);
    digitalWrite(CLK, HIGH);
  }

  digitalWrite(CS, HIGH);

  return byte;
}

void dump(){
  unsigned char start[3] = {0x00, 0x00, 0x00};
  unsigned int bit = 0;
  unsigned long base = 0x000000;

  digitalWrite(CS, HIGH);
  digitalWrite(CLK, LOW);

  digitalWrite(CS, LOW);

  pass_byte(INSTRUCTION);
  for(int i=0; i < 3; i++){
    pass_byte(start[i]);
  }

  while(base <= 0x0FFFF0){
    unsigned char byte[16] = {0};

    for(int j=0; j < 16; j++){
      for(int i=0; i < 8; i++){          
          bit = digitalRead(DO);
          byte[j] = (byte[j] << 1) + bit;

          digitalWrite(CLK, HIGH);
          digitalWrite(CLK, LOW);
      }
      Serial.write(byte[j]);
    }
    base += 16;
  }
  digitalWrite(CS, HIGH);
}

void write_enable(){
  digitalWrite(CS, HIGH);
  digitalWrite(CLK, LOW);

  digitalWrite(CS, LOW);

  pass_byte(WE);

  digitalWrite(CS, HIGH);
}

void wait_wip(){
  unsigned char status;
  do{
    status = read_status_register();
  }while((status & 0x01) != 0);
}

void overwrite_memory(unsigned char page[3], unsigned char arr[256]){
  //Write enable
  write_enable();
  
  //Page program
  digitalWrite(CS, HIGH);
  digitalWrite(CLK, LOW);
  
  digitalWrite(CS, LOW);
  
  pass_byte(PP);
  for(int i=0; i < 3; i++){
    pass_byte(page[i]);
  }

  for(int i=0; i < 256; i++){
    pass_byte(arr[i]);
  }

  digitalWrite(CS, HIGH);
  
  //Espere até que wip seja igual a 0
  wait_wip();
}



unsigned char read_status_register(){
  unsigned char byte = 0x00;
  int bit = 0;

  digitalWrite(CS, HIGH);
  digitalWrite(CLK, LOW);

  digitalWrite(CS, LOW);

  pass_byte(RSR);

    for(int i=0; i < 8; i++){          
      bit = digitalRead(DO);
      byte = (byte << 1) + bit;

      digitalWrite(CLK, HIGH);
      digitalWrite(CLK, LOW);
    }
  digitalWrite(CS, HIGH);

  return byte;
}

void dump_page(unsigned char start[3]){
  unsigned int bit = 0;
  unsigned long base = 0;

  for(int i=0; i < 3; i++){
    base = (base << 4) + start;
  }

  digitalWrite(CS, HIGH);
  digitalWrite(CLK, LOW);

  digitalWrite(CS, LOW);

  pass_byte(INSTRUCTION);
  for(int i=0; i < 3; i++){
    pass_byte(start[i]);
  }

  for(int n=0; n < 16; n++){
    unsigned char byte = 0;

    for(int j=0; j < 16; j++){
      for(int i=0; i < 8; i++){          
          bit = digitalRead(DO);
          byte = (byte << 1) + bit;
          
          digitalWrite(CLK, HIGH);
          digitalWrite(CLK, LOW);
      }
      Serial.write(byte);
    }
    base += 16;
  }
  digitalWrite(CS, HIGH);
}

void sector_erase(unsigned char start[3]){
  //Write enable
  write_enable();
  
  //Sector erase
  digitalWrite(CS, HIGH);
  digitalWrite(CLK, LOW);

  digitalWrite(CS, LOW);

  pass_byte(SEC_E);
  for(int i=0; i < 3; i++){
    pass_byte(start[i]);
  }

  digitalWrite(CS, HIGH);

  wait_wip();
}

void read_bytes(unsigned char *vet, int size){
  int count = 0;
  while(count < size){
    if(Serial.available() > 0){
      vet[count] = Serial.read();
      count++;
    }
  }
}

void chip_erase(){
  //Write enable
  write_enable();
  
  //Sector erase
  digitalWrite(CS, HIGH);
  digitalWrite(CLK, LOW);

  digitalWrite(CS, LOW);

  pass_byte(CHIP_E);

  digitalWrite(CS, HIGH);
  wait_wip();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    unsigned char arr[256] = { 0 };
    unsigned char start[3] = {0x00, 0x00, 0x00};

    code = Serial.read();

    switch(code){
      case 0x01:
        digitalWrite(8, HIGH);
        dump();
        digitalWrite(8, LOW);
        break;
      case 0x02:
        digitalWrite(8, HIGH);

        Serial.write(0x20);
        read_bytes(start, 3);
        read_bytes(arr, 256);

        overwrite_memory(start, arr);
        Serial.write(0x21);

        digitalWrite(8, LOW);

        break;
      case 0x03:
        digitalWrite(8, HIGH);
        read_bytes(start, 3);

        dump_page(start);
        digitalWrite(8, LOW);
        break;
      case 0x04:
        digitalWrite(8, HIGH);
        
        Serial.write(0x20);

        read_bytes(start, 3);
        sector_erase(start);

        Serial.write(0x21);

        digitalWrite(8, LOW);
        break;
      case 0x05:
        digitalWrite(8, HIGH);
        
        Serial.write(0x20);
        
        chip_erase();
        
        Serial.write(0x21);

        digitalWrite(8, LOW);
        break;
    }
  }
}
