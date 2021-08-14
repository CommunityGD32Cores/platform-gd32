#if defined(GD32F10x)
#include "gd32f10x.h"
#elif defined(GD32F1x0)
#include "gd32f1x0.h"
#elif defined(GD32F3x0)
#include "gd32f3x0.h"
#elif defined(GD32F30x)
#include "gd32f30x.h"
#elif defined(GD32F40x)
#include "gd32f4xx.h"
#elif defined(GD32E10X)
#include "gd32e10x.h"
#endif

/* define blinky LED pin here, board specific, otherwise default PC13 */
#ifdef GD32350G_START
/* correct LED for GD32350G-START board. PA1 */
#define LEDPORT     GPIOA
#define LEDPIN      GPIO_PIN_1
#define LED_CLOCK   RCU_GPIOA
#else
#define LEDPORT     GPIOC
#define LEDPIN      GPIO_PIN_13
#define LED_CLOCK   RCU_GPIOC
#endif

void systick_config(void);
void delay_1ms(uint32_t count);

int main(void)
{
    systick_config();

    rcu_periph_clock_enable(LED_CLOCK);

    /* set output as output */
#if defined(GD32F3x0) || defined(GD32F1x0) || defined(GD32F40x)
    gpio_mode_set(LEDPORT, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, LEDPIN);
    gpio_output_options_set(LEDPORT, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, LEDPIN);
#else /* valid for GD32F10x, GD32F30x, GD32E10X */
    gpio_init(LEDPORT, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, LEDPIN);
#endif
    while (1)
    {
        gpio_bit_set(LEDPORT, LEDPIN);
        delay_1ms(500);
        gpio_bit_reset(LEDPORT, LEDPIN);
        delay_1ms(500);
    }
}

volatile static uint32_t delay;

void systick_config(void)
{
    /* setup systick timer for 1000Hz interrupts */
    if (SysTick_Config(SystemCoreClock / 1000U))
    {
        /* capture error */
        while (1)
        {
        }
    }
    /* configure the systick handler priority */
    NVIC_SetPriority(SysTick_IRQn, 0x00U);
}

void delay_1ms(uint32_t count)
{
    delay = count;

    while (0U != delay)
    {
    }
}

void delay_decrement(void)
{
    if (0U != delay)
    {
        delay--;
    }
}

void NMI_Handler(void) {}

void HardFault_Handler(void)
{
    while (1)
        ;
}

void MemManage_Handler(void)
{
    while (1)
        ;
}

void BusFault_Handler(void)
{
    while (1)
        ;
}

void UsageFault_Handler(void)
{
    while (1)
        ;
}

void SVC_Handler(void)
{
}

void DebugMon_Handler(void)
{
}

void PendSV_Handler(void)
{
}

void SysTick_Handler(void)
{
    delay_decrement();
}
