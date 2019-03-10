
// STILL A WIP
const int TransPin =  13;// the number of the LED pin
String sequence;
String power;

void one(){
    digitalWrite(TransPin, HIGH);
    delayMicroseconds(730); // wait 730 uS 
    digitalWrite(TransPin, LOW);
    delayMicroseconds(70);// wait 70 uS
}
void zero(){
    digitalWrite(TransPin, HIGH);
    delayMicroseconds(150); // wait 730 uS 
    digitalWrite(TransPin, LOW);
    delayMicroseconds(650);// wait 70 uS
}
void setup() {
    // set the digital pin as output:
    pinMode(TransPin, OUTPUT);

}
void loop() {
  	// set Variables
    String Power = "0000101"; // 7 bit binary number, 0-100 in decimal
    int mode = 3;
    int channel = 1;
    String key = "00101100101001010";
    
    String channelnorm;
    String channelinv;
    String modenorm;
    String modeinv;
    
    if(channel == 1){
    String channelnorm = "111";
    String channelinv = "000";
    } else {
    String channelnorm = "000";
    String channelinv = "111";
    }

    if(mode == 1){
        String modenorm = "1000";
        String modeinv = "1110";
    } else if (mode == 2) {
        String modenorm = "0100";
        String modeinv = "1101";
    } else if (mode == 4) {
        String modenorm = "1000";
        String modeinv = "1110";
    } else {
        String modenorm = "0010";
        String modeinv = "1011";
    }
    String sequence = "1" + channelnorm + modenorm + power + key + modeinv + channelinv + "00";
  	
  	// start bit
    digitalWrite(TransPin, HIGH);
    delayMicroseconds(1500); // wait 730 uS 
    digitalWrite(TransPin, LOW);
    delayMicroseconds(730);// wait 70 uS
  	int n = 0;
    for (n = 0; n < 40 ; n++) {
        if (sequence.charAt(n) == '1'){
            one();
        } else {
            zero();
        }
    }

    delayMicroseconds(4500); // add delay between packets
}