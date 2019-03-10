// thanks to @mikey_dk for help with large parts of this code + formatting! https://twitter.com/mikey_dk 
// This is free and unencumbered software released into the public domain. 
// see LICENSE file or https://unlicense.org/ for full text of license.

// Tested by @mikey_dk and working on all modes. 

// Constant variables
const int TransPin =  D8;// the number of the LED pin
const String key = "00101100101001010";
const int shock_min = 0;
const int shock_max = 100;
const int pin_led = LED_BUILTIN;

// Variables which do change
int collar_mode = 3; // 
int collar_chan = 0; // 0 = channel 1, 1 = channel 2
int collar_duration = 2000;
int collar_power = 100;

String sequence;
String power;
String channelnorm;
String channelinv;
String modenorm;
String modeinv;

void transmit_command(int c, int m, int d, int p = 0)
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
      modenorm = "0001";
      modeinv = "0111";
      break;
    default: // Vibrate
      modenorm = "0010";
      modeinv = "1011";
      break;
  }

  // Convert power to binary
  p = constrain(p, shock_min, shock_max);
  int zeros = String(p, BIN).length();

  String power;
  for (int i = 0; i < 7 - zeros; i++)
  {
    power = power + "0";
  }
  power = power + String(p, BIN);

  String sequence = "1" + channelnorm + modenorm + power + key + modeinv + channelinv + "00";

  digitalWrite(pin_led, LOW);
  unsigned long cmd_start = millis();
  while (millis() - cmd_start < d)
  {
    // start bit
    digitalWrite(TransPin, HIGH);
    delayMicroseconds(1500); // wait 1500 uS
    digitalWrite(TransPin, LOW);
    delayMicroseconds(741);// wait 730 uS

    for (int n = 0; n < 40 ; n++)
    {
      //Serial.print(sequence.charAt(n));
      if (sequence.charAt(n) == '1') // Transmit a one
      {
        digitalWrite(TransPin, HIGH);
        delayMicroseconds(741); // wait 730 uS
        digitalWrite(TransPin, LOW);
        delayMicroseconds(247);// wait 70 uS
      }
      else // Transmit a zero
      {
        digitalWrite(TransPin, HIGH);
        delayMicroseconds(247); // wait 150 uS
        digitalWrite(TransPin, LOW);
        delayMicroseconds(741);// wait 650 uS
      }
    }
    delayMicroseconds(4500);
    //Serial.println();
  }
  digitalWrite(pin_led, HIGH);
}

void setup()
{
  pinMode(TransPin, OUTPUT); // Set transmitter pin as an output
  pinMode(pin_led, OUTPUT);
  Serial.begin(115200);
}

void loop()
{
  transmit_command(collar_chan, 1, collar_duration, collar_power); // FLASH
  delay(1000);
  transmit_command(collar_chan, 2, collar_duration, collar_power); // BEEP
  delay(1000);
  transmit_command(collar_chan, 3, collar_duration, collar_power); // VIBRATE
  delay(1000);
  // transmit_command(collar_chan, 4, collar_duration, collar_power); // SHOCK! (commented out by default because a 100 shock is nasty)
  // delay(1000);
}