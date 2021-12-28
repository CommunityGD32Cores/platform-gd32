  .syntax unified
  .cpu cortex-m23
  .fpu softvfp
  .thumb
  
.global  __gVectors
.global  Default_Handler

/* start address for the initialization values of the .data section.
defined in linker script */
.word _sidata
/* start address for the .data section. defined in linker script */
.word _sdata
/* end address for the .data section. defined in linker script */
.word _edata
/* start address for the .bss section. defined in linker script */
.word _sbss
/* end address for the .bss section. defined in linker script */
.word _ebss

.section  .text.Reset_Handler
  .weak  Reset_Handler
  .type  Reset_Handler, %function
Reset_Handler:  

/* Copy the data segment initializers from flash to SRAM */  
  movs  r1, #0
  b  LoopCopyDataInit

CopyDataInit:
  ldr  r3, =_sidata
  ldr  r3, [r3, r1]
  str  r3, [r0, r1]
  adds  r1, r1, #4
    
LoopCopyDataInit:
  ldr  r0, =_sdata
  ldr  r3, =_edata
  adds  r2, r0, r1
  cmp  r2, r3
  bcc  CopyDataInit
  ldr  r2, =_sbss
  b  LoopFillZerobss
/* Zero fill the bss segment. */  
FillZerobss:
  movs  r3, #0
  str  r3, [r2]
  adds r2, r2, #4
    
LoopFillZerobss:
  ldr  r3, = _ebss
  cmp  r2, r3
  bcc  FillZerobss

/* call into Arduino core's low-level first-init function */
  bl first_system_init
/* Call the clock system initialization function.*/
  bl  SystemInit   
/* Call into static constructors (C++) */
  bl __libc_init_array
/* Call the application's entry point.*/
  bl  main
  bx  lr    
.size  Reset_Handler, .-Reset_Handler

/**
 * @brief  This is the code that gets called when the processor receives an 
 *         unexpected interrupt.  This simply enters an infinite loop, preserving
 *         the system state for examination by a debugger.
 * @param  None     
 * @retval None       
*/
    .section  .text.Default_Handler,"ax",%progbits
Default_Handler:
Infinite_Loop:
  b  Infinite_Loop
  .size  Default_Handler, .-Default_Handler
/******************************************************************************
*
* The minimal vector table for a Cortex M4. Note that the proper constructs
* must be placed on this to ensure that it ends up at physical address
* 0x0000.0000.
* 
*******************************************************************************/
   .section  .vectors,"a",%progbits
  .type  __gVectors, %object
  .size  __gVectors, .-__gVectors

__gVectors:
                .word     _sp                            /* Top of Stack */
                .word     Reset_Handler		/* Reset Handler */
                .word     NMI_Handler		/* NMI Handler */
                .word     HardFault_Handler		/* Hard Fault Handler */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     SVC_Handler		/* SVCall Handler */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     PendSV_Handler		/* PendSV Handler */
                .word     SysTick_Handler		/* SysTick Handler */
                .word     WWDGT_IRQHandler		/* 16:Window Watchdog Timer */
                .word     LVD_IRQHandler		/* 17:LVD through EXTI Line detect */
                .word     TAMPER_STAMP_IRQHandler		/* 18:RTC Tamper and TimeStamp through EXTI Line detect */
                .word     RTC_WKUP_IRQHandler		/* 19:RTC Wakeup from EXTI interrupt */
                .word     FMC_IRQHandler		/* 20:FMC global interrupt */
                .word     RCU_CTC_IRQHandler		/* 21:RCU or CTC global interrupt */
                .word     EXTI0_IRQHandler		/* 22:EXTI Line 0 */
                .word     EXTI1_IRQHandler		/* 23:EXTI Line 1 */
                .word     EXTI2_IRQHandler		/* 24:EXTI Line 2 */
                .word     EXTI3_IRQHandler		/* 25:EXTI Line 3 */
                .word     EXTI4_IRQHandler		/* 26:EXTI Line 4 */
                .word     DMA_Channel0_IRQHandler		/* 27:DMA Channel 0  */
                .word     DMA_Channel1_IRQHandler		/* 28:DMA Channel 1  */
                .word     DMA_Channel2_IRQHandler		/* 29:DMA Channel 2  */
                .word     DMA_Channel3_IRQHandler		/* 30:DMA Channel 3  */
                .word     DMA_Channel4_IRQHandler		/* 31:DMA Channel 4  */
                .word     DMA_Channel5_IRQHandler		/* 32:DMA Channel 5  */
                .word     DMA_Channel6_IRQHandler		/* 33:DMA Channel 6  */
                .word     ADC_IRQHandler		/* 34:ADC interrupt  */
                .word     USBD_HP_IRQHandler		/* 35:USBD High Priority interrupt */
                .word     USBD_LP_IRQHandler		/* 36:USBD Low Priority interrupt */
                .word     TIMER1_IRQHandler		/* 37:TIMER1 */
                .word     TIMER2_IRQHandler		/* 38:TIMER2 */
                .word     TIMER8_IRQHandler		/* 39:TIMER8 */
                .word     TIMER11_IRQHandler		/* 40:TIMER11 */
                .word     TIMER5_IRQHandler		/* 41:TIMER5 */
                .word     TIMER6_IRQHandler		/* 42:TIMER6 */
                .word     USART0_IRQHandler		/* 43:USART0 */
                .word     USART1_IRQHandler		/* 44:USART1 */
                .word     UART3_IRQHandler		/* 45:UART3 */
                .word     UART4_IRQHandler		/* 46:UART4 */
                .word     I2C0_EV_IRQHandler		/* 47:I2C0 Event */
                .word     I2C0_ER_IRQHandler		/* 48:I2C0 Error */
                .word     I2C1_EV_IRQHandler		/* 49:I2C1 Event */
                .word     I2C1_ER_IRQHandler		/* 50:I2C1 Error */
                .word     SPI0_IRQHandler		/* 51:SPI0 */
                .word     SPI1_IRQHandler		/* 52:SPI1 */
                .word     DAC_IRQHandler		/* 53:DAC */
                .word     0		/* 54:Reserved */
                .word     I2C2_EV_IRQHandler		/* 55:I2C2 Event */
                .word     I2C2_ER_IRQHandler		/* 56:I2C2 Error */
                .word     RTC_Alarm_IRQHandler		/* 57:RTC Alarm through EXTI Line detect */
                .word     USBD_WKUP_IRQHandler		/* 58:USBD wakeup through EXTI Line detect */
                .word     EXTI5_9_IRQHandler		/* 59:EXTI5 to EXTI9 */
                .word     0		/* 60:Reserved */
                .word     0		/* 61:Reserved */
                .word     0		/* 62:Reserved */
                .word     EXTI10_15_IRQHandler		/* 63:EXTI10 to EXT15 */
                .word     0		/* 64:Reserved */
                .word     0		/* 65:Reserved */
                .word     0		/* 66:Reserved */
                .word     0		/* 67:Reserved */
                .word     0		/* 68:Reserved */
                .word     0		/* 69:Reserved */
                .word     0		/* 70:Reserved */
                .word     DMAMUX_IRQHandler		/* 71:Reserved */
                .word     CMP0_IRQHandler		/* 72:Comparator 0 interrupt through EXTI Line detect */
                .word     CMP1_IRQHandler		/* 73:Comparator 1 interrupt through EXTI Line detect */
                .word     I2C0_WKUP_IRQHandler		/* 74:I2C0 Wakeup interrupt through EXTI Line detect */
                .word     I2C2_WKUP_IRQHandler		/* 75:I2C2 Wakeup interrupt through EXTI Line detect */
                .word     USART0_WKUP_IRQHandler		/* 76:USART0 Wakeup interrupt through EXTI Line detect */
                .word     LPUART_IRQHandler		/* 77:LPUART global interrupt */
                .word     CAU_IRQHandler		/* 78:CAU */
                .word     TRNG_IRQHandler		/* 79:TRNG */
                .word     SLCD_IRQHandler		/* 80:SLCD */
                .word     USART1_WKUP_IRQHandler		/* 81:USART1 Wakeup interrupt through EXTI Line detect */
                .word     I2C1_WKUP_IRQHandler		/* 82:I2C1 Wakeup interrupt through EXTI Line detect */
                .word     LPUART_WKUP_IRQHandler		/* 83:LPUART Wakeup interrupt through EXTI Line detect */
                .word     LPTIMER_IRQHandler		/* 84:LPTIMER interrupt  */

/*******************************************************************************
*
* Provide weak aliases for each Exception handler to the Default_Handler. 
* As they are weak aliases, any function with the same name will override 
* this definition.
*
*******************************************************************************/
.weak NMI_Handler
.thumb_set NMI_Handler,Default_Handler

.weak HardFault_Handler
.thumb_set HardFault_Handler,Default_Handler

.weak SVC_Handler
.thumb_set SVC_Handler,Default_Handler

.weak PendSV_Handler
.thumb_set PendSV_Handler,Default_Handler

.weak SysTick_Handler
.thumb_set SysTick_Handler,Default_Handler

.weak WWDGT_IRQHandler
.thumb_set WWDGT_IRQHandler,Default_Handler

.weak LVD_IRQHandler
.thumb_set LVD_IRQHandler,Default_Handler

.weak TAMPER_STAMP_IRQHandler
.thumb_set TAMPER_STAMP_IRQHandler,Default_Handler

.weak RTC_WKUP_IRQHandler
.thumb_set RTC_WKUP_IRQHandler,Default_Handler

.weak FMC_IRQHandler
.thumb_set FMC_IRQHandler,Default_Handler

.weak RCU_CTC_IRQHandler
.thumb_set RCU_CTC_IRQHandler,Default_Handler

.weak EXTI0_IRQHandler
.thumb_set EXTI0_IRQHandler,Default_Handler

.weak EXTI1_IRQHandler
.thumb_set EXTI1_IRQHandler,Default_Handler

.weak EXTI2_IRQHandler
.thumb_set EXTI2_IRQHandler,Default_Handler

.weak EXTI3_IRQHandler
.thumb_set EXTI3_IRQHandler,Default_Handler

.weak EXTI4_IRQHandler
.thumb_set EXTI4_IRQHandler,Default_Handler

.weak DMA_Channel0_IRQHandler
.thumb_set DMA_Channel0_IRQHandler,Default_Handler

.weak DMA_Channel1_IRQHandler
.thumb_set DMA_Channel1_IRQHandler,Default_Handler

.weak DMA_Channel2_IRQHandler
.thumb_set DMA_Channel2_IRQHandler,Default_Handler

.weak DMA_Channel3_IRQHandler
.thumb_set DMA_Channel3_IRQHandler,Default_Handler

.weak DMA_Channel4_IRQHandler
.thumb_set DMA_Channel4_IRQHandler,Default_Handler

.weak DMA_Channel5_IRQHandler
.thumb_set DMA_Channel5_IRQHandler,Default_Handler

.weak DMA_Channel6_IRQHandler
.thumb_set DMA_Channel6_IRQHandler,Default_Handler

.weak ADC_IRQHandler
.thumb_set ADC_IRQHandler,Default_Handler

.weak USBD_HP_IRQHandler
.thumb_set USBD_HP_IRQHandler,Default_Handler

.weak USBD_LP_IRQHandler
.thumb_set USBD_LP_IRQHandler,Default_Handler

.weak TIMER1_IRQHandler
.thumb_set TIMER1_IRQHandler,Default_Handler

.weak TIMER2_IRQHandler
.thumb_set TIMER2_IRQHandler,Default_Handler

.weak TIMER8_IRQHandler
.thumb_set TIMER8_IRQHandler,Default_Handler

.weak TIMER11_IRQHandler
.thumb_set TIMER11_IRQHandler,Default_Handler

.weak TIMER5_IRQHandler
.thumb_set TIMER5_IRQHandler,Default_Handler

.weak TIMER6_IRQHandler
.thumb_set TIMER6_IRQHandler,Default_Handler

.weak USART0_IRQHandler
.thumb_set USART0_IRQHandler,Default_Handler

.weak USART1_IRQHandler
.thumb_set USART1_IRQHandler,Default_Handler

.weak UART3_IRQHandler
.thumb_set UART3_IRQHandler,Default_Handler

.weak UART4_IRQHandler
.thumb_set UART4_IRQHandler,Default_Handler

.weak I2C0_EV_IRQHandler
.thumb_set I2C0_EV_IRQHandler,Default_Handler

.weak I2C0_ER_IRQHandler
.thumb_set I2C0_ER_IRQHandler,Default_Handler

.weak I2C1_EV_IRQHandler
.thumb_set I2C1_EV_IRQHandler,Default_Handler

.weak I2C1_ER_IRQHandler
.thumb_set I2C1_ER_IRQHandler,Default_Handler

.weak SPI0_IRQHandler
.thumb_set SPI0_IRQHandler,Default_Handler

.weak SPI1_IRQHandler
.thumb_set SPI1_IRQHandler,Default_Handler

.weak DAC_IRQHandler
.thumb_set DAC_IRQHandler,Default_Handler

.weak I2C2_EV_IRQHandler
.thumb_set I2C2_EV_IRQHandler,Default_Handler

.weak I2C2_ER_IRQHandler
.thumb_set I2C2_ER_IRQHandler,Default_Handler

.weak RTC_Alarm_IRQHandler
.thumb_set RTC_Alarm_IRQHandler,Default_Handler

.weak USBD_WKUP_IRQHandler
.thumb_set USBD_WKUP_IRQHandler,Default_Handler

.weak EXTI5_9_IRQHandler
.thumb_set EXTI5_9_IRQHandler,Default_Handler

.weak EXTI10_15_IRQHandler
.thumb_set EXTI10_15_IRQHandler,Default_Handler

.weak DMAMUX_IRQHandler
.thumb_set DMAMUX_IRQHandler,Default_Handler

.weak CMP0_IRQHandler
.thumb_set CMP0_IRQHandler,Default_Handler

.weak CMP1_IRQHandler
.thumb_set CMP1_IRQHandler,Default_Handler

.weak I2C0_WKUP_IRQHandler
.thumb_set I2C0_WKUP_IRQHandler,Default_Handler

.weak I2C2_WKUP_IRQHandler
.thumb_set I2C2_WKUP_IRQHandler,Default_Handler

.weak USART0_WKUP_IRQHandler
.thumb_set USART0_WKUP_IRQHandler,Default_Handler

.weak LPUART_IRQHandler
.thumb_set LPUART_IRQHandler,Default_Handler

.weak CAU_IRQHandler
.thumb_set CAU_IRQHandler,Default_Handler

.weak TRNG_IRQHandler
.thumb_set TRNG_IRQHandler,Default_Handler

.weak SLCD_IRQHandler
.thumb_set SLCD_IRQHandler,Default_Handler

.weak USART1_WKUP_IRQHandler
.thumb_set USART1_WKUP_IRQHandler,Default_Handler

.weak I2C1_WKUP_IRQHandler
.thumb_set I2C1_WKUP_IRQHandler,Default_Handler

.weak LPUART_WKUP_IRQHandler
.thumb_set LPUART_WKUP_IRQHandler,Default_Handler

.weak LPTIMER_IRQHandler
.thumb_set LPTIMER_IRQHandler,Default_Handler

