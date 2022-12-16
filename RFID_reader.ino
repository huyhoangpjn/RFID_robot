#include <SPI.h>
#include <MFRC522.h>
#include <SoftwareSerial.h>


#define SS_PIN 10
#define RST_PIN 9

SoftwareSerial BT( 6 , 7 );
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class

MFRC522::MIFARE_Key key; 

// Init array that will store new NUID 
byte nuidPICC[4];
int block=2;

String nom = "Arduino";
String msg;

void setup() {
  BT.begin(9600);
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522 
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;// key
  }
//  while(true){
//    if (BT.available() > 0){
//      if (BT.read() == '1'){
//        BT.println("Bluetooth connected!");
//        delay(1000);
//        break;
//      }
//    }
//  }
  while(!BT);
  BT.println("OK");
}
byte readbackblock[18];//lire le block, le tableau doit être inférieur à 6 bytes

void loop() {

  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;

  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);

  // Check is the PICC of Classic MIFARE type
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&  
    piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    return;
  }

  if (rfid.uid.uidByte[0] != nuidPICC[0] || 
    rfid.uid.uidByte[1] != nuidPICC[1] || 
    rfid.uid.uidByte[2] != nuidPICC[2] || 
    rfid.uid.uidByte[3] != nuidPICC[3] ) {

    // Store NUID and information into arrays
    for (byte i = 0; i < 4; i++) {nuidPICC[i] = rfid.uid.uidByte[i];} // reading of tag id
    readBlock(block, readbackblock);//read the block back, the informations

    //Serial.print("id: ");
    for (byte i = 0; i < rfid.uid.size; i++) {
      //Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
      BT.print(rfid.uid.uidByte[i], HEX);
     }
    BT.print("_");
    for (int j=0 ; j<16 ; j++)
     { BT.write (readbackblock[j]);//Serial.write() transmits the ASCII numbers as human readable characters to serial monitor
      Serial.print (readbackblock[j]);
      }
    BT.println("");
    
  }


  // Halt PICC
  rfid.PICC_HaltA();

  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
}





int readBlock(int blockNumber, byte arrayAddress[]) 
{
  int largestModulo4Number=blockNumber/4*4;
  int trailerBlock=largestModulo4Number+3;//determine trailer block for the sector

  /*****************************************authentication of the desired block for access***********************************************************/
  byte status = rfid.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(rfid.uid));
  if (status != MFRC522::STATUS_OK) {
         //Serial.print("PCD_Authenticate() failed (read): ");
         //Serial.println(rfid.GetStatusCodeName((MFRC522::StatusCode)status));//---------------------
         return 3;//return "3" as error message
  }
  //it appears the authentication needs to be made before every block read/write within a specific sector.
  //If a different sector is being authenticated access to the previous one is lost.


  /*****************************************reading a block***********************************************************/
        
  byte buffersize = 18;//we need to define a variable with the read buffer size, since the MIFARE_Read method below needs a pointer to the variable that contains the size... 
  status = rfid.MIFARE_Read(blockNumber, arrayAddress, &buffersize);//&buffersize is a pointer to the buffersize variable; MIFARE_Read requires a pointer instead of just a number
  if (status != MFRC522::STATUS_OK) {
          //Serial.print("MIFARE_read() failed: ");
          //Serial.println(rfid.GetStatusCodeName((MFRC522::StatusCode)status));
          return 4;//return "4" as error message
  }
}
