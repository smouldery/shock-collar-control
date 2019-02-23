// gcc -o transmitter -lpigpio -lpthread -lm -lpigpiod_if2 -lrt transmitter.c

/* tell the compiler to use pigpio daemon interface */
#include <pigpiod_if2.h>
/* tell the compiler to use the module that has nanosleep */
#include <time.h> 
// so we can do stuff with strings
#include<string.h> 
// so we can print, for diagnosticsS
#include <stdio.h>
// so we can round stuff
#include <math.h>
#include <stdlib.h>     /* strtof */

int set_mode(int, unsigned, unsigned); 
int pigpio_start();
int gpio_write(int, unsigned, unsigned);
void pigpio_stop();


int main(int argc, const char **argv) {
    
    //char sequencet;strcpy(sequencet, argv[1]);
    //float shocktimesec = strof (argv[2]);
    
    printf(argv[1]);
    printf(argv[2]);
    //printf(strof(shocktimesec));
    printf("\n test\n");

    /*loads pgpio module*/
    int pinumber;
    pinumber = pigpio_start(NULL, NULL);

    float shocktimesec = strtod(argv[2], NULL);
    // printf('%f', shocktimesec);
    // number of ticks in this time
    // clock_t shocktimeticks = rint(shocktimesecs * CLOCKS_PER_SEC);

    


    set_mode(pinumber,17, 1); // Set GPIO27 as output.

    gpio_write(pinumber,17, 0); // set gpio to zero, as a formality / just in case it was high. 

    // function to transmit a 'zero' bit
    void zero() {

        gpio_write(pinumber,17,1); // set pin to one to START transmitting the bit

    // wait 0 sec and 150000 nanosec
        nanosleep((const struct timespec[]){{0, 180000L}}, NULL);
        
        gpio_write(pinumber,17,0); // set pin to zero to STOP transmitting the bit. 

    //  wait 0 sec and 650000 nanosec */
        nanosleep((const struct timespec[]){{0, 600000L}}, NULL);

    }

    // function to transmit a 'one' bit
    void one() {
        gpio_write(pinumber,17,1); // set pin to one to START transmitting the bit

        /* wait 0 sec and 730000 nanosec */
        nanosleep((const struct timespec[]){{0, 730000L}}, NULL);
        
        gpio_write(pinumber,17,0); // set pin to zero to STOP transmitting the bit.
        
        // wait 0 sec and 70000 nanosec
        nanosleep((const struct timespec[]){{0, 140000L}}, NULL);
    }
    /////////////////////////////////////////////////////////////////

    struct timespec end_time;
    struct timespec current_time;
    
    double shocktimesec_s = floor(shocktimesec);
    double shocktimesec_ns = (shocktimesec - floor(shocktimesec)) * 1e9;

    clock_gettime(CLOCK_MONOTONIC, &end_time);

    if ((end_time.tv_nsec + shocktimesec_ns ) < 1000000000) {
        end_time.tv_sec = end_time.tv_sec + shocktimesec_s;
        end_time.tv_nsec = end_time.tv_nsec + shocktimesec_ns;
    } else { 
        end_time.tv_sec = end_time.tv_sec + shocktimesec_s + 1;
        end_time.tv_nsec = (end_time.tv_nsec + shocktimesec_ns) - 1000000000;
    } 

    long double end_time_value = end_time.tv_sec + (end_time.tv_nsec / 1e9);

    long double current_time_value = 0;

    do {
        // transmit the START bit. same each time. 
        gpio_write(pinumber,17,1); // set pin to one to START transmitting the bit
        /* wait 0 sec and 1300000 nanosec */
        nanosleep((const struct timespec[]){{0, 1500000L}}, NULL);
        gpio_write(pinumber,17,0); // set pin to zero to STOP transmitting the bit.
        // wait 0 sec and 70000 nanosec
        nanosleep((const struct timespec[]){{0, 730000L}}, NULL);

        printf("%s \n", argv[1]);
        printf("transmitting...(c) \n");

        for (int x = 0; x <= 40 ; x++)
        {
           
            if ((argv[1])[x] == '1') {
                one();
                printf("%d-1 \n", x);
            } else {
                zero();
                printf("%d-0 \n", x);
            }
        }

        // give it a sec so we put an appropriate gap between the sequences
        nanosleep((const struct timespec[]){{0, 4500000L}}, NULL);   
        printf("\n");

        clock_gettime(CLOCK_MONOTONIC, &current_time);

        current_time_value = current_time.tv_sec + (current_time.tv_nsec / 1e9);
        printf("current time: %f", current_time_value);
        printf("end time: %f", end_time_value);
        



        } while (current_time_value < end_time_value);
    // set gpio 27 to zero to be safe
    gpio_write(pinumber,27, 0);


    //ends pigpio module
    pigpio_stop(pinumber);

}