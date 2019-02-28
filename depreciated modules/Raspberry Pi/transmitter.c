// gcc -o transmitter -lpigpio -lpthread -lm transmitter.c

// THIS MODULE IS DEPRECIATED AND WAS NEVER SUCESSFULLY OPERATIONAL
// YOU WILL NEED TO FIX THE PROGRAM TO GET IT TO WORK, IT WILL NOT BE MAINTAINED BY ME

// COPRIGHT / LICENSE
// parts of this code adapted from work by Guillermo A. Amaral B. <g@maral.me>, found on
// https://elinux.org/RPi_GPIO_Code_Samples which is licenced under a CC BY-SA 3.0 license
// (See https://creativecommons.org/licenses/by-sa/3.0/)
// **NOTE - the author has been contactacted and consents to this content
// being used under a BSD licence.**

// The first part of this code  (code from this point foward and before noted otherwise)
// is covered by the license of this repository:
// https://raw.githubusercontent.com/smouldery/shock-collar-control/master/LICENSE


#include <time.h> // nanosleep ()
#include <string.h> // so we can do stuff with strings
#include <stdio.h> // so we can print, for diagnostics
#include <math.h> // so we can round stuff
#include <stdlib.h>  //for strtof

#include <sys/stat.h> // for sysfs GPIO access
#include <sys/types.h> // for sysfs GPIO access
#include <fcntl.h> // for sysfs GPIO access
#include <unistd.h> // for sysfs GPIO access


#define IN   0 // for sysfs interface usage
#define OUT  1 // for sysfs interface usage

#define LOW  0 // for sysfs interface usage
#define HIGH 1 // for sysfs interface usage

#define PIN  24 // P1-18
#define POUT 17  // Pi2b-11 // for sysfs interface usage

// for sysfs interface usage
static int GPIOExport(int pin);
static int GPIOUnexport(int pin);
static int GPIODirection(int pin, int dir);
static int GPIORead(int pin);
static int GPIOWrite(int pin, int value);


int main(int argc, const char **argv) {

    float shocktimesec = strtod(argv[2], NULL);

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
// CONTENT BEYOND THIS POINT IS LICENSED UNDER CC BY-SA 3.0
// adapted from work by Guillermo A. Amaral B. <g@maral.me>
// the code below this notice is NOT covered by the license repository
// and instead uses the CC BY-SA 3.0 License

int
GPIOExport(int pin)
{
#define BUFFER_MAX 3
    char buffer[BUFFER_MAX];
    ssize_t bytes_written;
    int fd;

    fd = open("/sys/class/gpio/export", O_WRONLY);
    if (-1 == fd) {
	fprintf(stderr, "Failed to open export for writing!\n");
	return(-1);
    }

    bytes_written = snprintf(buffer, BUFFER_MAX, "%d", pin);
    write(fd, buffer, bytes_written);
    close(fd);
    return(0);
}

int
GPIOUnexport(int pin)
{
    char buffer[BUFFER_MAX];
    ssize_t bytes_written;
    int fd;

    fd = open("/sys/class/gpio/unexport", O_WRONLY);
    if (-1 == fd) {
	fprintf(stderr, "Failed to open unexport for writing!\n");
	return(-1);
    }

    bytes_written = snprintf(buffer, BUFFER_MAX, "%d", pin);
    write(fd, buffer, bytes_written);
    close(fd);
    return(0);
}

int
GPIODirection(int pin, int dir)
{
    static const char s_directions_str[]  = "in\0out";

#define DIRECTION_MAX 35
    char path[DIRECTION_MAX];
    int fd;

    snprintf(path, DIRECTION_MAX, "/sys/class/gpio/gpio%d/direction", pin);
    fd = open(path, O_WRONLY);
    if (-1 == fd) {
	fprintf(stderr, "Failed to open gpio direction for writing!\n");
	return(-1);
    }

    if (-1 == write(fd, &s_directions_str[IN == dir ? 0 : 3], IN == dir ? 2 : 3)) {
	fprintf(stderr, "Failed to set direction!\n");
	return(-1);
    }

    close(fd);
    return(0);
}

int
GPIORead(int pin)
{
#define VALUE_MAX 30
    char path[VALUE_MAX];
    char value_str[3];
    int fd;

    snprintf(path, VALUE_MAX, "/sys/class/gpio/gpio%d/value", pin);
    fd = open(path, O_RDONLY);
    if (-1 == fd) {
	fprintf(stderr, "Failed to open gpio value for reading!\n");
	return(-1);
    }

    if (-1 == read(fd, value_str, 3)) {
	fprintf(stderr, "Failed to read value!\n");
	return(-1);
    }

    close(fd);

    return(atoi(value_str));
}

int
GPIOWrite(int pin, int value)
{
    static const char s_values_str[] = "01";

    char path[VALUE_MAX];
    int fd;

    snprintf(path, VALUE_MAX, "/sys/class/gpio/gpio%d/value", pin);
    fd = open(path, O_WRONLY);
    if (-1 == fd) {
	fprintf(stderr, "Failed to open gpio value for writing!\n");
	return(-1);
    }

    if (1 != write(fd, &s_values_str[LOW == value ? 0 : 1], 1)) {
	fprintf(stderr, "Failed to write value!\n");
	return(-1);
    }

    close(fd);
    return(0);
}