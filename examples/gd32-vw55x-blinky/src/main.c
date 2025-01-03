#include "gd32vw55x.h"
#include "systick.h"
#include <stdio.h>

#define LEDPORT     GPIOB
#define LEDPIN      GPIO_PIN_11
#define LED_CLOCK   RCU_GPIOB

int main(void)
{
    systick_config();
    eclic_priority_group_set(ECLIC_PRIGROUP_LEVEL3_PRIO1);
    rcu_periph_clock_enable(LED_CLOCK);
    gpio_mode_set(LEDPORT, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, LEDPIN);
    gpio_output_options_set(LEDPORT, GPIO_OTYPE_PP, GPIO_OSPEED_2MHZ, LEDPIN);

    while (1)
    {
        gpio_bit_set(LEDPORT, LEDPIN);
        delay_1ms(100);
        gpio_bit_reset(LEDPORT, LEDPIN);
        delay_1ms(100);
    }
}

void eclic_mtip_handler(void)
{
    ECLIC_ClearPendingIRQ(CLIC_INT_TMR);
    delay_decrement();
}
