#include <SPI.h>
#include <MFRC522.h>
#define RST_PIN 9
#define SS_PIN 10
#define RED_PIN 2
#define GREEN_PIN 3
MFRC522::MIFARE_Key key;
MFRC522::StatusCode card_status;
MFRC522 mfrc522(SS_PIN, RST_PIN);// Create an instance of the MFRC522 class
byte nuidPICC[4];
int buzzerPin = 5;
void setup() {
  Serial.begin(9600);   // Initialize serial communication
  SPI.begin();   // Initialize SPI bus
  pinMode(buzzerPin, OUTPUT);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);

  mfrc522.PCD_Init();   // Initialize MFRC522 module
  Serial.println("Place your card near the reader...");
}
void loop() {
  // Check if a new card is present
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    //    Serial.println("Card detected!");
    // Get the UID of the card
    String uid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      uid += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
      uid += String(mfrc522.uid.uidByte[i], HEX);
    }
    Serial.println("uid:" + uid);

    if (Serial.available()) {
      String data = Serial.readStringUntil('\n');  // Read the incoming data until newline character
      // Parse the data by splitting it using the delimiter
      int delimiterIndex = data.indexOf('|');
      String balanceStr = data.substring(0, delimiterIndex);
      String pointsStr = data.substring(delimiterIndex + 1);

      // Convert the balance and points values to integers
      int balance = balanceStr.toInt();
      int points = pointsStr.toInt();

      Serial.println("Balance: ");
      Serial.println(balance);

      Serial.println("Points: ");
      Serial.println(points);

      byte balanceBytes[sizeof(balance)];
      byte pointsBytes[sizeof(points)];

      // Copy the balance and points values to the byte arrays
      memcpy(balanceBytes, &balance, sizeof(balance));
      memcpy(pointsBytes, &points, sizeof(points));

      // Write balance to block 4
      writeBytesToBlock(4, balanceBytes);

      // Write points to block 5
      writeBytesToBlock(5, pointsBytes);
      success();

    }

  }
}


void success() {
  digitalWrite(GREEN_PIN, HIGH);
  digitalWrite(buzzerPin, HIGH);
  delay(500);
  digitalWrite(buzzerPin, LOW);
  digitalWrite(GREEN_PIN, LOW);
}

void error() {
  digitalWrite(RED_PIN, HIGH);
  digitalWrite(buzzerPin, HIGH);
  delay(100);
  digitalWrite(buzzerPin, LOW);
  delay(100);
  digitalWrite(buzzerPin, HIGH);
  delay(100);
  digitalWrite(buzzerPin, LOW);
  delay(100);
  digitalWrite(buzzerPin, HIGH);
  delay(100);
  digitalWrite(buzzerPin, LOW);
  delay(100);
  digitalWrite(buzzerPin, HIGH);
  delay(100);
  digitalWrite(buzzerPin, LOW);
  digitalWrite(RED_PIN, LOW);
}

String readBytesFromBlock() {
  byte blockNumber = 4;

  card_status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockNumber, &key, &(mfrc522.uid));
  if (card_status != MFRC522::STATUS_OK) {
    Serial.print(F("Authentication failed: "));
    Serial.println(mfrc522.GetStatusCodeName(card_status));
    return;
  }
  byte arrayAddress[18];
  byte buffersize = sizeof(arrayAddress);
  card_status = mfrc522.MIFARE_Read(blockNumber, arrayAddress, &buffersize);
  if (card_status != MFRC522::STATUS_OK) {
    Serial.print(F("Reading failed: "));
    Serial.println(mfrc522.GetStatusCodeName(card_status));
    return;
  }

  String value = "";
  for (uint8_t i = 0; i < 16; i++) {
    value += (char)arrayAddress[i];
  }
  value.trim();
  return value;
}


void writeBytesToBlock(byte block, byte buff[]) {
  card_status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));

  if (card_status != MFRC522::STATUS_OK) {
    Serial.print(F("PCD_Authenticate() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(card_status));
    return;
  }

  else {
    Serial.println(F("PCD_Authenticate() success: "));
  }
  // Write block
  card_status = mfrc522.MIFARE_Write(block, buff, 16);

  if (card_status != MFRC522::STATUS_OK) {
    Serial.print(F("MIFARE_Write() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(card_status));
    return;
  }
  else {
    Serial.println(F("Data saved."));
  }
}
