// mode power time channel key (opt)
// IN PROGRESS!!!!
#include <time.h> // nanosleep ()
#include <string.h> // so we can do stuff with strings
#include <stdio.h> // so we can print, for diagnostics
#include <math.h> // so we can round stuff
#include <stdlib.h>  //for strtof

// give it a name:
int Transmitter = 13;
 
// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(Transmitter, OUTPUT);     
}
 
// the loop routine runs over and over again forever:
void loop() {
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);               // wait for a second
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);               // wait for a second
}


void main(int argc, const char **argv) {

    float shocktimesec = strtod(argv[3], NULL);

    if (-1 == GPIOExport(POUT)) // Enable GPIO pin
	    return(1);

    if (-1 == GPIODirection(POUT, OUT)) // Set GPIO direction
	    return(2);

	if (-1 == GPIOWrite(POUT, 0)) // Write GPIO value
	    return(3);

    // function to transmit a 'zero' bit
    void zero() {

        if (-1 == GPIOWrite(POUT, 1)) // Write GPIO value
	        return(3); // set pin to one to START transmitting the bit

    // wait 0 sec and 150000 nanosec
        nanosleep((const struct timespec[]){{0, 180000L}}, NULL);
        
        if (-1 == GPIOWrite(POUT, 0)) // Write GPIO value
	        return(3); // set pin to zero to STOP transmitting the bit. 

    //  wait 0 sec and 650000 nanosec */
        nanosleep((const struct timespec[]){{0, 600000L}}, NULL);

    }

    // function to transmit a 'one' bit
    void one() {
        if (-1 == GPIOWrite(POUT, 1)) // Write GPIO value
	        return(3); // set pin to one to START transmitting the bit

        /* wait 0 sec and 730000 nanosec */
        nanosleep((const struct timespec[]){{0, 730000L}}, NULL);
        
        if (-1 == GPIOWrite(POUT, 0)) // Write GPIO value
	        return(3); // set pin to zero to STOP transmitting the bit.
        
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
        if (-1 == GPIOWrite(POUT, 1)) // Write GPIO value
	        return(3); // set pin to one to START transmitting the bit
        /* wait 0 sec and 1300000 nanosec */
        nanosleep((const struct timespec[]){{0, 1500000L}}, NULL);
        if (-1 == GPIOWrite(POUT, 0)) // Write GPIO value
	        return(3); // set pin to zero to STOP transmitting the bit.
        // wait 0 sec and 70000 nanosec
        nanosleep((const struct timespec[]){{0, 730000L}}, NULL);

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
    // set gpio 17 to zero to be safe
    if (-1 == GPIOWrite(POUT, 0)) // Write GPIO value
	    return(3);

    if ( -1 == GPIOUnexport(PIN)) // Disable GPIO pin
	    return(4);

    return(0);
}