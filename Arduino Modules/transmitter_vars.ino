// thanks to @mikey_dk for help with large parts of this code + formatting! https://twitter.com/mikey_dk 


// Constant variables
const int TransPin =  LED_BUILTIN;// the number of the LED pin
const String key = "00101100101001010";
 
// Variables which do change
int collar_mode = 3;
int collar_chan = 1;
int collar_duration = 1000; // time to transmit in us
String Power = "0000101"; // 7 bit binary number, 0-100 in decimal
 
String sequence;
String power;
String channelnorm;
String channelinv;
String modenorm;
String modeinv;
 
void transmit_command(int c, int m, int d)
{
  switch (c) // Check the channel
  {
    case 1: // Channel 1
      channelnorm = "111";
      channelinv = "000";
      break;
    default: // Channel 0
      channelnorm = "000";
      channelinv = "111";
      break;
  }
 
  switch (m) // Check the mode
  {
    case 1: // Light
      modenorm = "1000";
      modeinv = "1110";
      break;
    case 2: // Beep
      modenorm = "0100";
      modeinv = "1101";
      break;
    case 4: // Shock
      modenorm = "1000";
      modeinv = "1110";
      break;
    default: // Vibrate
      modenorm = "0010";
      modeinv = "1011";
      break;
  }
 
  String sequence = "1" + channelnorm + modenorm + power + key + modeinv + channelinv + "00";
 
  unsigned long cmd_start = millis();
  while (millis() - cmd_start < d)
  {
    // start bit
    digitalWrite(TransPin, HIGH);
    delayMicroseconds(1500); // wait 1500 uS
    digitalWrite(TransPin, LOW);
    delayMicroseconds(730);// wait 730 uS
 
    for (int n = 0; n < 40 ; n++)
    {
      if (sequence.charAt(n) == '1') // Transmit a one
      {
        digitalWrite(TransPin, HIGH);
        delayMicroseconds(730); // wait 730 uS
        digitalWrite(TransPin, LOW);
        delayMicroseconds(70);// wait 70 uS
      }
      else // Transmit a zero
      {
        digitalWrite(TransPin, HIGH);
        delayMicroseconds(150); // wait 150 uS
        digitalWrite(TransPin, LOW);
        delayMicroseconds(650);// wait 650 uS
      }
    }
  }
}
 
void setup()
{
  pinMode(TransPin, OUTPUT); // Set transmitter pin as an output
  Serial.begin(115200);
}
 
void loop()
{
  collar_mode = 3;
  transmit_command(collar_chan, collar_mode, collar_duration);
  delay(1000);
}