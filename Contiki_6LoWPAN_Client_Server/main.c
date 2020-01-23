#include <stdio.h>

#include <contiki.h>
#include <contiki-net.h>

#include <sys/clock.h>

#include <string.h>

#include "letmecreate/core/common.h"
#include "letmecreate/core/spi.h"
#include "letmecreate/core/debug.h"

#include <contiki.h>
#include <contiki-net.h>
#include <sys/clock.h>
#include <string.h>

#include "dev/leds.h"
#include "sys/clock.h"
#include "letmecreate/core/network.h"
#include <math.h>

#define SERVER_IP_ADDR "fe80::19:f5ff:fe89:1d66"
#define SERVER_PORT 3000
#define CLIENT_PORT 3001
#define BUFFER_SIZE 64
#define V_PER_LSB   (0.0032f)   // este valor resulta de 3.3/1024 
                                //(conversor de 10 bits)  

uint8_t data_envio[3];
uint8_t data_recibido[3];
uint16_t res;
float volt, dist;
int i1;
uint16_t  lim=0b0000001111111111;



PROCESS(main_process, "Main process");
AUTOSTART_PROCESSES(&main_process);
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(main_process, ev, data)
{
    PROCESS_BEGIN();
    INIT_NETWORK_DEBUG();
    {
        static struct uip_udp_conn * conn;
        static char buffer[BUFFER_SIZE];
        static int i = 0;

        int flashes = 2;

         while(flashes--) {
            /* Flash every second */
            for(i = 0; i < 20; i++)
              clock_delay_usec(50000);
            leds_toggle(LED1);
        }


        PRINTF("=====Start=====\n");

        

        conn = udp_new_connection(CLIENT_PORT, SERVER_PORT, SERVER_IP_ADDR);
        
        flashes = 4;

        while(flashes--) {
          /* Flash every second */
           for(i = 0; i < 20; i++)
            clock_delay_usec(50000);
          leds_toggle(LED1);
        }

        spi_init();
        spi_set_mode(MIKROBUS_1, SPI_MODE_3);


        while(1)
        {
            
            data_envio[0] = 0x1; 
            data_envio[1] = 144;
            data_envio[2] = 0xff;

            spi_transfer(data_envio, data_recibido,sizeof(data_envio));

            res = data_recibido[1]; 
            res = res << 8; 
            res |= data_recibido[2]; 
            res = res & lim;


            volt = res * V_PER_LSB;
            dist = 13*pow(volt,-1);

            sprintf(buffer, "Voltaje: %f, distancia: %f\n", volt, dist);

            udp_packet_send(conn, buffer, strlen(buffer));
            PROCESS_WAIT_UDP_SENT();


            for(i = 0; i < 100; i++)
                    clock_delay_usec(6500);


        }

        
        spi_release();
    }

    PROCESS_END();
}

/*---------------------------------------------------------------------------*/
