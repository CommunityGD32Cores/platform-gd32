#include "gd32e50x.h"

#define LEDPORT     GPIOA
#define LEDPIN      GPIO_PIN_7
#define LED_CLOCK   RCU_GPIOA
void systick_config(void);
void delay_1ms(uint32_t count);

int main(void) {
    systick_config();
    rcu_periph_clock_enable(LED_CLOCK);
    gpio_init(LEDPORT, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, LEDPIN);
    while (1) {
        gpio_bit_set(LEDPORT, LEDPIN);
        delay_1ms(100);
        gpio_bit_reset(LEDPORT, LEDPIN);
        delay_1ms(100);
    }
}
