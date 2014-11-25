int Data_pin[8]; //le numéro du pin connecté à D0

/*Distribuer les pins*/
int Busy = 21;   //Busy évoque interrupt 2   pin 11
int Ack = 20;    //Ack évoque interrupt 3    pin 10
//int PaperEmpty = 22; //paper is not empty    pin 12

/*les pins suivant sont pas encore manipulé dans le code principal.*/
int Online =  23;  // Online                  pin 13
int AutoFeed = 24; //Auto Feed                pin 14
int Error = 25;    //ERROR                    pin 15
int Reset = 26;    //Initialize               pin 16
int SelectInput = 27;  //Select Input         pin 17
/////////////////////////////////////////////////

int i;      //Variable sert à parcourir
int num = 0;  //nombre de octats réçu
char DATA[500];    //louer d'espace pour 100 byte des données reçues
int Data_byte[8];  //un octat de donnée

int PrintFlag = 0;
int CapFlag = 0;

void SetPin(){
  digitalWrite(Online,HIGH);
  digitalWrite(Busy,LOW);
  digitalWrite(Ack,HIGH);
}

void setup()
{
  
  /*$$$$$$$$$$$$$$$$$$$$$$$$$$
  D7-D0 sont connectés au pins 53-46 d'arduino
  $$$$$$$$$$$$$$$$$$$$$$$$$$$$*/
  for(i = 0;i < 8;i++){
    Data_pin[i] = i+46;
    pinMode(Data_pin[i],INPUT);
  }
  /*$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  Mettre PaperEmpty Bas pour mentir le PC
  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$*/
  pinMode(Busy,OUTPUT);
  pinMode(Ack,OUTPUT);
  pinMode(Online,OUTPUT);
  pinMode(AutoFeed,INPUT);
  pinMode(Reset,INPUT);
  pinMode(SelectInput,INPUT);
  Serial.begin(9600); //communication avec MacBook
  SetPin();
  attachInterrupt(0, capture_data,FALLING); //interruption provoqué par le front descendant de strobe
  
}

/**$$$$$$$$$$$$$$$$$$$$
initialiser les variable, surtout les flags.
$$$$$$$$$$$$$$$$$$$$$$**/
void initial(){  
  PrintFlag = 0;
  CapFlag = 0;
  AckFlag = 0;
  BusyFlag = 0;
  memset(Data_byte,0,sizeof(Data_byte));
  memset(DATA,'\0',sizeof(DATA[0]) * num);
  num = 0;
}

void loop(){
  
  if(PrintFlag == 0){
    if (CapFlag != 0){
      delay(500);//wait that all the datas have been sent
      
      /*$$$$$$$$$$$$$$$$$$$
      Afficher le résultat 
      $$$$$$$$$$$$$$$$$$$$*/

      for(i = 0;i<num;i++){
        Serial.print(DATA[i]);
        //Serial.println(DATA[i],HEX);
        //if (Serial.read()==
      }
      PrintFlag = 1;//Afficher juste une fois
    }
    initial();
    delay(500);
  }
}

void capture_data(){
 
  /**$$$$$$$$$$$$$$$$$$$$$$$$$$$
  construire un octat
  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$**/
  digitalWrite(Busy,HIGH);
  DATA[num] =char( (digitalRead(Data_pin[7]) << 7) | (digitalRead(Data_pin[6]) << 6) | (digitalRead(Data_pin[5]) << 5) | (digitalRead(Data_pin[4]) << 4) | (digitalRead(Data_pin[3]) << 3) | (digitalRead(Data_pin[2]) << 2) | (digitalRead(Data_pin[1]) << 1) | digitalRead(Data_pin[0]));
  delayMicroseconds(3);
  digitalWrite(Busy,LOW);
  digitalWrite(Ack,LOW);
  delayMicroseconds(3);
  digitalWrite(Ack,HIGH);
  num++;
  if (num>=500)
    num = 0;
  CapFlag ++;
}

