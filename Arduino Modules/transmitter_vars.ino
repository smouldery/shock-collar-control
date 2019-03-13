// thanks to @mikey_dk for massive help with large parts of this code + formatting! 
// This is free and unencumbered software released into the public domain. 
// see LICENSE file or https://unlicense.org/ for full text of license.

// Tested by @mikey_dk and working on all modes.
// please log any bugs you encounter in a github issue 

// Constant variables
const String key = "00101100101001010"; // this is a 'static' key - each remote has it's own 
const int shock_min = 0; // minimum value of the shock 
const int shock_max = 10; // maximum value of the shock
const int pin_led = LED_BUILTIN; // Pin for indication LED
const int pin_rtx =  D8; // Pin to transmit over

// Variables which do change
int collar_mode = 3; 
int collar_chan = 0; 
int collar_duration = 500;
int collar_power = 100;

#define COLLAR_LED 1
#define COLLAR_BEEP 2
#define COLLAR_VIB 3
#define COLLAR_ZAP 4

// Strings used for building up the command sequence
String sequence, power, channelnorm, channelinv, modenorm, modeinv;

unsigned long transmit_last = 0;

void transmit_command(int c, int m, int d, int p = 0)
{
  transmit_last = millis();
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
    digitalWrite(pin_rtx, HIGH);
    delayMicroseconds(1500); // wait 1500 uS
    digitalWrite(pin_rtx, LOW);
    delayMicroseconds(741);// wait 741 uS

    for (int n = 0; n < 40 ; n++)
    {
      if (sequence.charAt(n) == '1') // Transmit a one
      {
        digitalWrite(pin_rtx, HIGH);
        delayMicroseconds(741);
        digitalWrite(pin_rtx, LOW);
        delayMicroseconds(247);
      }
      else // Transmit a zero
      {
        digitalWrite(pin_rtx, HIGH);
        delayMicroseconds(247);
        digitalWrite(pin_rtx, LOW);
        delayMicroseconds(741);
      }
    }
    delayMicroseconds(4500);
  }
  digitalWrite(pin_led, HIGH);
}

void setup()
{
  pinMode(pin_rtx, OUTPUT); // Set transmitter pin as an output
  pinMode(pin_led, OUTPUT);
  Serial.begin(115200);
}

void loop()
{
  //transmit_command(collar_chan, COLLAR_VIB, collar_duration, collar_power);

  if (millis() - transmit_last >= 120000) // Send command to the collar at least every 2 minutes to make it stay on
  {
    Serial.println("Keep-alive:\t\tCollar");
    transmit_command(collar_chan, COLLAR_LED, 10);
  }
}