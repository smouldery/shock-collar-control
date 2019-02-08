// gcc -Wall -o transmitter -lpigpio -lpthread transmitter.c

/* tell the compiler to use pigpio */
#include <pigpio.h>
/* tell the compiler to use the module that has nanosleep */
#include <time.h>
// so we can do stuff with strings
#include<string.h>
// so we can print, for diagnosticsS
#include <stdio.h>

int gpioSetMode(unsigned, unsigned); 
int gpioInitialise();
int gpioWrite(unsigned, unsigned);
void gpioTerminate();

int main() {

    /*loads pgpio module*/
    gpioInitialise();

    // for now, we manually set the input string to a test value below, just for testing purposes
    char sequence[] = "10000100001011001010010100000001110111100";
    // 1 000 0100 0010-1100-1010-01010 0000001 1101 111 00
    gpioSetMode(17, 1); // Set GPIO27 as output.

    gpioWrite(17, 0); // set gpio to zero, as a formality / just in case it was high. 

    // function to transmit a 'zero' bit
    void zero() {

        gpioWrite(17,1); // set pin to one to START transmitting the bit

    // wait 0 sec and 150000 nanosec
        nanosleep((const struct timespec[]){{0, 180000L}}, NULL);
        
        gpioWrite(17, 0); // set pin to zero to STOP transmitting the bit. 

    //  wait 0 sec and 650000 nanosec */
        nanosleep((const struct timespec[]){{0, 600000L}}, NULL);

    }

    // function to transmit a 'one' bit
    void one() {
        gpioWrite(17,1); // set pin to one to START transmitting the bit

        /* wait 0 sec and 730000 nanosec */
        nanosleep((const struct timespec[]){{0, 730000L}}, NULL);
        
        gpioWrite(17,0); // set pin to zero to STOP transmitting the bit.
        
        // wait 0 sec and 70000 nanosec
        nanosleep((const struct timespec[]){{0, 140000L}}, NULL);
    }
    /////////////////////////////////////////////////////////////////

    for (int y = 0; y <= 40 ; y++) {
        // transmit the START bit. same each time. 
        gpioWrite(17,1); // set pin to one to START transmitting the bit
        /* wait 0 sec and 1300000 nanosec */
        nanosleep((const struct timespec[]){{0, 1500000L}}, NULL);
        gpioWrite(17,0); // set pin to zero to STOP transmitting the bit.
        // wait 0 sec and 70000 nanosec
        nanosleep((const struct timespec[]){{0, 730000L}}, NULL);

        printf("%s \n", sequence);

        for (int x = 0; x <= 40 ; x++)
        {
           
            if (sequence[x] == '1') {
                one();
                printf("%d-1", x);
            } else {
                zero();
                printf("%d-0", x);
            }
        }

        // give it a sec so we put an appropriate gap between the sequences
        nanosleep((const struct timespec[]){{0, 4500000L}}, NULL);   
        printf("\n");
        }
    // set gpio 27 to zero to be safe
    gpioWrite(27, 0);


    //ends pigpio module
    gpioTerminate(); 

}