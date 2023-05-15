

#ifdef _WIN32
#include "C:\Users\user\Desktop\current_tasks\seco_imx\cmbs_v1\cmbs\lib\serial.h"
#else
#include "cmbs_v1\cmbs\lib\serial.h"
#endif


#include <math.h>

#define ARRSIZE 5


int main() {

    serial_t ser;

    if ( serial_open(&ser, "COM3", FACCESS_WRITE) < 0 ) {
        perror("error open COM3\n");
        exit(-1);
    }

    for(float i = 0; ; i+=0.1) {
        short arr[ARRSIZE] = {
            0x5555,
            sin(i),
            cos(i),
            tan(i)
        };

        if ( serial_write(ser, (char *)arr, sizeof(arr)) < 0 ) {
            serial_close(ser);
            perror("error write\n");
            exit(-1);
        }

        Sleep(1000);
    }


    return 0;
}