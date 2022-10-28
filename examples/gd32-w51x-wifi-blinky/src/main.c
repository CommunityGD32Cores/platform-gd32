#include "gd32w51x.h"
#include "wrapper_os.h"
#include "wifi_netlink.h"
#include "app_type.h"
#include "wifi_management.h"
#include "arm_math.h"
#include "wifi_version.h"
#include "nspe_region.h"
#include "mbl_uart.h"

#define LEDPORT     GPIOB
#define LEDPIN      GPIO_PIN_11
#define LED_CLOCK   RCU_GPIOB

void led_task(void *p_arg) {
    sys_reset_flag_check();
    sys_os_misc_init();
    systick_delay_init();
    //wifi_management_init();

    rcu_periph_clock_enable(LED_CLOCK);
    gpio_mode_set(LEDPORT, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, LEDPIN);
    gpio_output_options_set(LEDPORT, GPIO_OTYPE_PP, GPIO_OSPEED_2MHZ, LEDPIN);
    while(1) {
        gpio_bit_set(LEDPORT, LEDPIN);
        sys_ms_sleep(1000);
        gpio_bit_reset(LEDPORT, LEDPIN);
        sys_ms_sleep(1000);
        printf("Blinky!\r\n");
    }
}

int main(void)
{
    platform_init();

    DEBUGPRINT("SDK git revision: "WIFI_GIT_REVISION" \r\n");
    DEBUGPRINT("SDK version: V%d.%d.%d\r\n", (RE_NSPE_VERSION >> 24), ((RE_NSPE_VERSION & 0xFF0000) >> 16), (RE_NSPE_VERSION & 0xFFFF));
    DEBUGPRINT("SDK build date: " __DATE__ " " __TIME__" \r\n");

    sys_os_init();
    if (NULL == sys_task_create(NULL, (const uint8_t *)"led_task", NULL, START_TASK_STK_SIZE, 0,
            START_TASK_PRIO, led_task, NULL)) {
        DEBUGPRINT("ERROR: create start task failed\r\n");
    }
    sys_os_start();
    while(1);
    return 0;
}