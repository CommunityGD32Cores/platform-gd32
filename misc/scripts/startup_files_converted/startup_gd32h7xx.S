  .syntax unified
  .cpu cortex-m7
  .fpu softvfp
  .thumb
  
.global  g_pfnVectors
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
   .section  .isr_vector,"a",%progbits
  .type  g_pfnVectors, %object
  .size  g_pfnVectors, .-g_pfnVectors

g_pfnVectors:
                .word     _estack                            /* Top of Stack */
                .word     Reset_Handler		/* Reset Handler */
                .word     NMI_Handler		/* NMI Handler */
                .word     HardFault_Handler		/* Hard Fault Handler */
                .word     MemManage_Handler		/* MPU Fault Handler */
                .word     BusFault_Handler		/* Bus Fault Handler */
                .word     UsageFault_Handler		/* Usage Fault Handler */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     SVC_Handler		/* SVCall Handler */
                .word     DebugMon_Handler		/* Debug Monitor Handler */
                .word     0		/* Reserved */
                .word     PendSV_Handler		/* PendSV Handler */
                .word     SysTick_Handler		/* SysTick Handler */
                .word     WWDGT_IRQHandler		/* 16:Window Watchdog Timer */
                .word     AVD_LVD_OVD_IRQHandler		/* 17:AVD */
                .word     TAMPER_STAMP_LXTAL_IRQHandler		/* 18:RTC Tamper and TimeStamp through EXTI Line detect */
                .word     RTC_WKUP_IRQHandler		/* 19:RTC Wakeup from EXTI interrupt */
                .word     FMC_IRQHandler		/* 20:FMC global interrupt */
                .word     RCU_IRQHandler		/* 21:RCU global interrupt */
                .word     EXTI0_IRQHandler		/* 22:EXTI Line 0 */
                .word     EXTI1_IRQHandler		/* 23:EXTI Line 1 */
                .word     EXTI2_IRQHandler		/* 24:EXTI Line 2 */
                .word     EXTI3_IRQHandler		/* 25:EXTI Line 3 */
                .word     EXTI4_IRQHandler		/* 26:EXTI Line 4 */
                .word     DMA0_Channel0_IRQHandler		/* 27:DMA0 Channel 0  */
                .word     DMA0_Channel1_IRQHandler		/* 28:DMA0 Channel 1  */
                .word     DMA0_Channel2_IRQHandler		/* 29:DMA0 Channel 2  */
                .word     DMA0_Channel3_IRQHandler		/* 30:DMA0 Channel 3  */
                .word     DMA0_Channel4_IRQHandler		/* 31:DMA0 Channel 4  */
                .word     DMA0_Channel5_IRQHandler		/* 32:DMA0 Channel 5  */
                .word     DMA0_Channel6_IRQHandler		/* 33:DMA0 Channel 6  */
                .word     ADC0_1_IRQHandler		/* 34:ADC0 and ADC1 interrupt */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     EXTI5_9_IRQHandler		/* 39:EXTI5 to EXTI9 */
                .word     TIMER0_BRK_IRQHandler		/* 40:TIMER0 Break */
                .word     TIMER0_UP_IRQHandler		/* 41:TIMER0 Update */
                .word     TIMER0_TRG_CMT_IRQHandler		/* 42:TIMER0 Trigger and Commutation */
                .word     TIMER0_Channel_IRQHandler		/* 43:TIMER0 Capture Compare */
                .word     TIMER1_IRQHandler		/* 44:TIMER1 */
                .word     TIMER2_IRQHandler		/* 45:TIMER2 */
                .word     TIMER3_IRQHandler		/* 46:TIMER3 */
                .word     I2C0_EV_IRQHandler		/* 47:I2C0 Event */
                .word     I2C0_ER_IRQHandler		/* 48:I2C0 Error */
                .word     I2C1_EV_IRQHandler		/* 49:I2C1 Event */
                .word     I2C1_ER_IRQHandler		/* 50:I2C1 Error */
                .word     SPI0_IRQHandler		/* 51:SPI0 */
                .word     SPI1_IRQHandler		/* 52:SPI1 */
                .word     USART0_IRQHandler		/* 53:USART0 global and wakeup */
                .word     USART1_IRQHandler		/* 54:USART1 global and wakeup */
                .word     USART2_IRQHandler		/* 55:USART2 global and wakeup */
                .word     EXTI10_15_IRQHandler		/* 56:EXTI10 to EXTI15 */
                .word     RTC_Alarm_IRQHandler		/* 57:RTC Alarm */
                .word     0		/* Reserved */
                .word     TIMER7_BRK_IRQHandler		/* 59:TIMER7 Break */
                .word     TIMER7_UP_IRQHandler		/* 60:TIMER7 Update */
                .word     TIMER7_TRG_CMT_IRQHandler		/* 61:TIMER7 Trigger and Commutation */
                .word     TIMER7_Channel_IRQHandler		/* 62:TIMER7 Channel Capture Compare */
                .word     DMA0_Channel7_IRQHandler		/* 63:DMA0 Channel 7 */
                .word     EXMC_IRQHandler		/* 64:EXMC */
                .word     SDIO0_IRQHandler		/* 65:SDIO0 */
                .word     TIMER4_IRQHandler		/* 66:TIMER4 */
                .word     SPI2_IRQHandler		/* 67:SPI2 */
                .word     UART3_IRQHandler		/* 68:UART3 */
                .word     UART4_IRQHandler		/* 69:UART4 */
                .word     TIMER5_DAC_UDR_IRQHandler		/* 70:TIMER5 global interrupt and DAC1 */
                .word     TIMER6_IRQHandler		/* 71:TIMER6 */
                .word     DMA1_Channel0_IRQHandler		/* 72:DMA1 Channel0 */
                .word     DMA1_Channel1_IRQHandler		/* 73:DMA1 Channel1 */
                .word     DMA1_Channel2_IRQHandler		/* 74:DMA1 Channel2 */
                .word     DMA1_Channel3_IRQHandler		/* 75:DMA1 Channel3 */
                .word     DMA1_Channel4_IRQHandler		/* 76:DMA1 Channel4 */
                .word     ENET0_IRQHandler		/* 77:Ethernet0 */
                .word     ENET0_WKUP_IRQHandler		/* 78:Ethernet0 Wakeup through EXTI Line */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     DMA1_Channel5_IRQHandler		/* 84:DMA1 Channel5 */
                .word     DMA1_Channel6_IRQHandler		/* 85:DMA1 Channel6 */
                .word     DMA1_Channel7_IRQHandler		/* 86:DMA1 Channel7 */
                .word     USART5_IRQHandler		/* 87:USART5 global and wakeup */
                .word     I2C2_EV_IRQHandler		/* 88:I2C2 Event */
                .word     I2C2_ER_IRQHandler		/* 89:I2C2 Error */
                .word     USBHS0_EP1_OUT_IRQHandler		/* 90:USBHS0 Endpoint 1 Out  */
                .word     USBHS0_EP1_IN_IRQHandler		/* 91:USBHS0 Endpoint 1 in */
                .word     USBHS0_WKUP_IRQHandler		/* 92:USBHS0 Wakeup through EXTI Line */
                .word     USBHS0_IRQHandler		/* 93:USBHS0 */
                .word     DCI_IRQHandler		/* 94:DCI */
                .word     CAU_IRQHandler		/* 95:CAU */
                .word     HAU_TRNG_IRQHandler		/* 96:HAU and TRNG */
                .word     FPU_IRQHandler		/* 97:FPU */
                .word     UART6_IRQHandler		/* 98:UART6 */
                .word     UART7_IRQHandler		/* 99:UART7 */
                .word     SPI3_IRQHandler		/* 100:SPI3 */
                .word     SPI4_IRQHandler		/* 101:SPI4 */
                .word     SPI5_IRQHandler		/* 102:SPI5 */
                .word     SAI0_IRQHandler		/* 103:SAI0 */
                .word     TLI_IRQHandler		/* 104:TLI */
                .word     TLI_ER_IRQHandler		/* 105:TLI Error */
                .word     IPA_IRQHandler		/* 106:IPA */
                .word     SAI1_IRQHandler		/* 107:SAI1 */
                .word     OSPI0_IRQHandler		/* 108:OSPI0 */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     I2C3_EV_IRQHandler		/* 111:I2C3 Event */
                .word     I2C3_ER_IRQHandler		/* 112:I2C3 Error */
                .word     RSPDIF_IRQHandler		/* 113:RSPDIF */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     DMAMUX_OVR_IRQHandler		/* 118:DMAMUX Overrun interrupt */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     HPDF_INT0_IRQHandler		/* 126:HPDF global interrupt 0 */
                .word     HPDF_INT1_IRQHandler		/* 127:HPDF global interrupt 1 */
                .word     HPDF_INT2_IRQHandler		/* 128:HPDF global interrupt 2 */
                .word     HPDF_INT3_IRQHandler		/* 129:HPDF global interrupt 3 */
                .word     SAI2_IRQHandler		/* 130:SAI2 global interrupt */
                .word     0		/* Reserved */
                .word     TIMER14_IRQHandler		/* 132:TIMER14 */
                .word     TIMER15_IRQHandler		/* 133:TIMER15 */
                .word     TIMER16_IRQHandler		/* 134:TIMER16 */
                .word     0		/* Reserved */
                .word     MDIO_IRQHandler		/* 136:MDIO */
                .word     0		/* Reserved */
                .word     MDMA_IRQHandler		/* 138:MDMA */
                .word     0		/* Reserved */
                .word     SDIO1_IRQHandler		/* 140:SDIO1 */
                .word     HWSEM_IRQHandler		/* 141:HWSEM */
                .word     0		/* Reserved */
                .word     ADC2_IRQHandler		/* 143:ADC2 */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     CMP0_1_IRQHandler		/* 153:CMP0 and CMP1 */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     CTC_IRQHandler		/* 160:Clock Recovery System */
                .word     RAMECCMU_IRQHandler		/* 161:RAMECCMU */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     OSPI1_IRQHandler		/* 166:OSPI1 */
                .word     RTDEC0_IRQHandler		/* 167:RTDEC0 */
                .word     RTDEC1_IRQHandler		/* 168:RTDEC1 */
                .word     FAC_IRQHandler		/* 169:FAC */
                .word     TMU_IRQHandler		/* 170:TMU */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     0		/* Reserved */
                .word     TIMER22_IRQHandler		/* 177:TIMER22 */
                .word     TIMER23_IRQHandler		/* 178:TIMER23 */
                .word     TIMER30_IRQHandler		/* 179:TIMER30 */
                .word     TIMER31_IRQHandler		/* 180:TIMER31 */
                .word     TIMER40_IRQHandler		/* 181:TIMER40 */
                .word     TIMER41_IRQHandler		/* 182:TIMER41 */
                .word     TIMER42_IRQHandler		/* 183:TIMER42 */
                .word     TIMER43_IRQHandler		/* 184:TIMER43 */
                .word     TIMER44_IRQHandler		/* 185:TIMER44 */
                .word     TIMER50_IRQHandler		/* 186:TIMER50 */
                .word     TIMER51_IRQHandler		/* 187:TIMER51 */
                .word     USBHS1_EP1_OUT_IRQHandler		/* 188:USBHS1 endpoint 1 out */
                .word     USBHS1_EP1_IN_IRQHandler		/* 189:USBHS1 endpoint 1 in */
                .word     USBHS1_WKUP_IRQHandler		/* 190:USBHS1 wakeup */
                .word     USBHS1_IRQHandler		/* 191:USBHS1 */
                .word     ENET1_IRQHandler		/* 192:Ethernet1 */
                .word     ENET1_WKUP_IRQHandler		/* 193:Ethernet1 wakeup */
                .word     0		/* Reserved */
                .word     CAN0_WKUP_IRQHandler		/* 195:CAN0 wakeup */
                .word     CAN0_Message_IRQHandler		/* 196:CAN0 interrupt for message buffer */
                .word     CAN0_Busoff_IRQHandler		/* 197:CAN0 interrupt for Bus off  */
                .word     CAN0_Error_IRQHandler		/* 198:CAN0 interrupt for Error */
                .word     CAN0_FastError_IRQHandler		/* 199:CAN0 interrupt for Error in fast transmission */
                .word     CAN0_TEC_IRQHandler		/* 200:CAN0 interrupt for Transmit warning */
                .word     CAN0_REC_IRQHandler		/* 201:CAN0 interrupt for Receive warning */
                .word     CAN1_WKUP_IRQHandler		/* 202:CAN1 wakeup */
                .word     CAN1_Message_IRQHandler		/* 203:CAN1 interrupt for message buffer */
                .word     CAN1_Busoff_IRQHandler		/* 204:CAN1 interrupt for Bus off  */
                .word     CAN1_Error_IRQHandler		/* 205:CAN1 interrupt for Error */
                .word     CAN1_FastError_IRQHandler		/* 206:CAN1 interrupt for Error in fast transmission */
                .word     CAN1_TEC_IRQHandler		/* 207:CAN1 interrupt for Transmit warning */
                .word     CAN1_REC_IRQHandler		/* 208:CAN1 interrupt for Receive warning */
                .word     CAN2_WKUP_IRQHandler		/* 209:CAN2 wakeup */
                .word     CAN2_Message_IRQHandler		/* 210:CAN2 interrupt for message buffer */
                .word     CAN2_Busoff_IRQHandler		/* 211:CAN2 interrupt for Bus off  */
                .word     CAN2_Error_IRQHandler		/* 212:CAN2 interrupt for Error */
                .word     CAN2_FastError_IRQHandler		/* 213:CAN2 interrupt for Error in fast transmission */
                .word     CAN2_TEC_IRQHandler		/* 214:CAN2 interrupt for Transmit warning */
                .word     CAN2_REC_IRQHandler		/* 215:CAN2 interrupt for Receive warning */
                .word     EFUSE_IRQHandler		/* 216:EFUSE */
                .word     I2C0_WKUP_IRQHandler		/* 217:I2C0 wakeup */
                .word     I2C1_WKUP_IRQHandler		/* 218:I2C1 wakeup */
                .word     I2C2_WKUP_IRQHandler		/* 219:I2C2 wakeup */
                .word     I2C3_WKUP_IRQHandler		/* 220:I2C3 wakeup */
                .word     LPDTS_IRQHandler		/* 221:LPDTS */
                .word     LPDTS_WKUP_IRQHandler		/* 222:LPDTS wakeup */
                .word     TIMER0_DEC_IRQHandler		/* 223:TIMER0 DEC */
                .word     TIMER7_DEC_IRQHandler		/* 224:TIMER7 DEC */
                .word     TIMER1_DEC_IRQHandler		/* 225:TIMER1 DEC */
                .word     TIMER2_DEC_IRQHandler		/* 226:TIMER2 DEC */
                .word     TIMER3_DEC_IRQHandler		/* 227:TIMER3 DEC */
                .word     TIMER4_DEC_IRQHandler		/* 228:TIMER4 DEC */
                .word     TIMER22_DEC_IRQHandler		/* 229:TIMER22 DEC */
                .word     TIMER23_DEC_IRQHandler		/* 230:TIMER23 DEC */
                .word     TIMER30_DEC_IRQHandler		/* 231:TIMER30 DEC */
                .word     TIMER31_DEC_IRQHandler		/* 232:TIMER31 DEC */

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

.weak MemManage_Handler
.thumb_set MemManage_Handler,Default_Handler

.weak BusFault_Handler
.thumb_set BusFault_Handler,Default_Handler

.weak UsageFault_Handler
.thumb_set UsageFault_Handler,Default_Handler

.weak SVC_Handler
.thumb_set SVC_Handler,Default_Handler

.weak DebugMon_Handler
.thumb_set DebugMon_Handler,Default_Handler

.weak PendSV_Handler
.thumb_set PendSV_Handler,Default_Handler

.weak SysTick_Handler
.thumb_set SysTick_Handler,Default_Handler

.weak WWDGT_IRQHandler
.thumb_set WWDGT_IRQHandler,Default_Handler

.weak AVD_LVD_OVD_IRQHandler
.thumb_set AVD_LVD_OVD_IRQHandler,Default_Handler

.weak TAMPER_STAMP_LXTAL_IRQHandler
.thumb_set TAMPER_STAMP_LXTAL_IRQHandler,Default_Handler

.weak RTC_WKUP_IRQHandler
.thumb_set RTC_WKUP_IRQHandler,Default_Handler

.weak FMC_IRQHandler
.thumb_set FMC_IRQHandler,Default_Handler

.weak RCU_IRQHandler
.thumb_set RCU_IRQHandler,Default_Handler

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

.weak DMA0_Channel0_IRQHandler
.thumb_set DMA0_Channel0_IRQHandler,Default_Handler

.weak DMA0_Channel1_IRQHandler
.thumb_set DMA0_Channel1_IRQHandler,Default_Handler

.weak DMA0_Channel2_IRQHandler
.thumb_set DMA0_Channel2_IRQHandler,Default_Handler

.weak DMA0_Channel3_IRQHandler
.thumb_set DMA0_Channel3_IRQHandler,Default_Handler

.weak DMA0_Channel4_IRQHandler
.thumb_set DMA0_Channel4_IRQHandler,Default_Handler

.weak DMA0_Channel5_IRQHandler
.thumb_set DMA0_Channel5_IRQHandler,Default_Handler

.weak DMA0_Channel6_IRQHandler
.thumb_set DMA0_Channel6_IRQHandler,Default_Handler

.weak ADC0_1_IRQHandler
.thumb_set ADC0_1_IRQHandler,Default_Handler

.weak EXTI5_9_IRQHandler
.thumb_set EXTI5_9_IRQHandler,Default_Handler

.weak TIMER0_BRK_IRQHandler
.thumb_set TIMER0_BRK_IRQHandler,Default_Handler

.weak TIMER0_UP_IRQHandler
.thumb_set TIMER0_UP_IRQHandler,Default_Handler

.weak TIMER0_TRG_CMT_IRQHandler
.thumb_set TIMER0_TRG_CMT_IRQHandler,Default_Handler

.weak TIMER0_Channel_IRQHandler
.thumb_set TIMER0_Channel_IRQHandler,Default_Handler

.weak TIMER1_IRQHandler
.thumb_set TIMER1_IRQHandler,Default_Handler

.weak TIMER2_IRQHandler
.thumb_set TIMER2_IRQHandler,Default_Handler

.weak TIMER3_IRQHandler
.thumb_set TIMER3_IRQHandler,Default_Handler

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

.weak USART0_IRQHandler
.thumb_set USART0_IRQHandler,Default_Handler

.weak USART1_IRQHandler
.thumb_set USART1_IRQHandler,Default_Handler

.weak USART2_IRQHandler
.thumb_set USART2_IRQHandler,Default_Handler

.weak EXTI10_15_IRQHandler
.thumb_set EXTI10_15_IRQHandler,Default_Handler

.weak RTC_Alarm_IRQHandler
.thumb_set RTC_Alarm_IRQHandler,Default_Handler

.weak TIMER7_BRK_IRQHandler
.thumb_set TIMER7_BRK_IRQHandler,Default_Handler

.weak TIMER7_UP_IRQHandler
.thumb_set TIMER7_UP_IRQHandler,Default_Handler

.weak TIMER7_TRG_CMT_IRQHandler
.thumb_set TIMER7_TRG_CMT_IRQHandler,Default_Handler

.weak TIMER7_Channel_IRQHandler
.thumb_set TIMER7_Channel_IRQHandler,Default_Handler

.weak DMA0_Channel7_IRQHandler
.thumb_set DMA0_Channel7_IRQHandler,Default_Handler

.weak EXMC_IRQHandler
.thumb_set EXMC_IRQHandler,Default_Handler

.weak SDIO0_IRQHandler
.thumb_set SDIO0_IRQHandler,Default_Handler

.weak TIMER4_IRQHandler
.thumb_set TIMER4_IRQHandler,Default_Handler

.weak SPI2_IRQHandler
.thumb_set SPI2_IRQHandler,Default_Handler

.weak UART3_IRQHandler
.thumb_set UART3_IRQHandler,Default_Handler

.weak UART4_IRQHandler
.thumb_set UART4_IRQHandler,Default_Handler

.weak TIMER5_DAC_UDR_IRQHandler
.thumb_set TIMER5_DAC_UDR_IRQHandler,Default_Handler

.weak TIMER6_IRQHandler
.thumb_set TIMER6_IRQHandler,Default_Handler

.weak DMA1_Channel0_IRQHandler
.thumb_set DMA1_Channel0_IRQHandler,Default_Handler

.weak DMA1_Channel1_IRQHandler
.thumb_set DMA1_Channel1_IRQHandler,Default_Handler

.weak DMA1_Channel2_IRQHandler
.thumb_set DMA1_Channel2_IRQHandler,Default_Handler

.weak DMA1_Channel3_IRQHandler
.thumb_set DMA1_Channel3_IRQHandler,Default_Handler

.weak DMA1_Channel4_IRQHandler
.thumb_set DMA1_Channel4_IRQHandler,Default_Handler

.weak ENET0_IRQHandler
.thumb_set ENET0_IRQHandler,Default_Handler

.weak ENET0_WKUP_IRQHandler
.thumb_set ENET0_WKUP_IRQHandler,Default_Handler

.weak DMA1_Channel5_IRQHandler
.thumb_set DMA1_Channel5_IRQHandler,Default_Handler

.weak DMA1_Channel6_IRQHandler
.thumb_set DMA1_Channel6_IRQHandler,Default_Handler

.weak DMA1_Channel7_IRQHandler
.thumb_set DMA1_Channel7_IRQHandler,Default_Handler

.weak USART5_IRQHandler
.thumb_set USART5_IRQHandler,Default_Handler

.weak I2C2_EV_IRQHandler
.thumb_set I2C2_EV_IRQHandler,Default_Handler

.weak I2C2_ER_IRQHandler
.thumb_set I2C2_ER_IRQHandler,Default_Handler

.weak USBHS0_EP1_OUT_IRQHandler
.thumb_set USBHS0_EP1_OUT_IRQHandler,Default_Handler

.weak USBHS0_EP1_IN_IRQHandler
.thumb_set USBHS0_EP1_IN_IRQHandler,Default_Handler

.weak USBHS0_WKUP_IRQHandler
.thumb_set USBHS0_WKUP_IRQHandler,Default_Handler

.weak USBHS0_IRQHandler
.thumb_set USBHS0_IRQHandler,Default_Handler

.weak DCI_IRQHandler
.thumb_set DCI_IRQHandler,Default_Handler

.weak CAU_IRQHandler
.thumb_set CAU_IRQHandler,Default_Handler

.weak HAU_TRNG_IRQHandler
.thumb_set HAU_TRNG_IRQHandler,Default_Handler

.weak FPU_IRQHandler
.thumb_set FPU_IRQHandler,Default_Handler

.weak UART6_IRQHandler
.thumb_set UART6_IRQHandler,Default_Handler

.weak UART7_IRQHandler
.thumb_set UART7_IRQHandler,Default_Handler

.weak SPI3_IRQHandler
.thumb_set SPI3_IRQHandler,Default_Handler

.weak SPI4_IRQHandler
.thumb_set SPI4_IRQHandler,Default_Handler

.weak SPI5_IRQHandler
.thumb_set SPI5_IRQHandler,Default_Handler

.weak SAI0_IRQHandler
.thumb_set SAI0_IRQHandler,Default_Handler

.weak TLI_IRQHandler
.thumb_set TLI_IRQHandler,Default_Handler

.weak TLI_ER_IRQHandler
.thumb_set TLI_ER_IRQHandler,Default_Handler

.weak IPA_IRQHandler
.thumb_set IPA_IRQHandler,Default_Handler

.weak SAI1_IRQHandler
.thumb_set SAI1_IRQHandler,Default_Handler

.weak OSPI0_IRQHandler
.thumb_set OSPI0_IRQHandler,Default_Handler

.weak I2C3_EV_IRQHandler
.thumb_set I2C3_EV_IRQHandler,Default_Handler

.weak I2C3_ER_IRQHandler
.thumb_set I2C3_ER_IRQHandler,Default_Handler

.weak RSPDIF_IRQHandler
.thumb_set RSPDIF_IRQHandler,Default_Handler

.weak DMAMUX_OVR_IRQHandler
.thumb_set DMAMUX_OVR_IRQHandler,Default_Handler

.weak HPDF_INT0_IRQHandler
.thumb_set HPDF_INT0_IRQHandler,Default_Handler

.weak HPDF_INT1_IRQHandler
.thumb_set HPDF_INT1_IRQHandler,Default_Handler

.weak HPDF_INT2_IRQHandler
.thumb_set HPDF_INT2_IRQHandler,Default_Handler

.weak HPDF_INT3_IRQHandler
.thumb_set HPDF_INT3_IRQHandler,Default_Handler

.weak SAI2_IRQHandler
.thumb_set SAI2_IRQHandler,Default_Handler

.weak TIMER14_IRQHandler
.thumb_set TIMER14_IRQHandler,Default_Handler

.weak TIMER15_IRQHandler
.thumb_set TIMER15_IRQHandler,Default_Handler

.weak TIMER16_IRQHandler
.thumb_set TIMER16_IRQHandler,Default_Handler

.weak MDIO_IRQHandler
.thumb_set MDIO_IRQHandler,Default_Handler

.weak MDMA_IRQHandler
.thumb_set MDMA_IRQHandler,Default_Handler

.weak SDIO1_IRQHandler
.thumb_set SDIO1_IRQHandler,Default_Handler

.weak HWSEM_IRQHandler
.thumb_set HWSEM_IRQHandler,Default_Handler

.weak ADC2_IRQHandler
.thumb_set ADC2_IRQHandler,Default_Handler

.weak CMP0_1_IRQHandler
.thumb_set CMP0_1_IRQHandler,Default_Handler

.weak CTC_IRQHandler
.thumb_set CTC_IRQHandler,Default_Handler

.weak RAMECCMU_IRQHandler
.thumb_set RAMECCMU_IRQHandler,Default_Handler

.weak OSPI1_IRQHandler
.thumb_set OSPI1_IRQHandler,Default_Handler

.weak RTDEC0_IRQHandler
.thumb_set RTDEC0_IRQHandler,Default_Handler

.weak RTDEC1_IRQHandler
.thumb_set RTDEC1_IRQHandler,Default_Handler

.weak FAC_IRQHandler
.thumb_set FAC_IRQHandler,Default_Handler

.weak TMU_IRQHandler
.thumb_set TMU_IRQHandler,Default_Handler

.weak TIMER22_IRQHandler
.thumb_set TIMER22_IRQHandler,Default_Handler

.weak TIMER23_IRQHandler
.thumb_set TIMER23_IRQHandler,Default_Handler

.weak TIMER30_IRQHandler
.thumb_set TIMER30_IRQHandler,Default_Handler

.weak TIMER31_IRQHandler
.thumb_set TIMER31_IRQHandler,Default_Handler

.weak TIMER40_IRQHandler
.thumb_set TIMER40_IRQHandler,Default_Handler

.weak TIMER41_IRQHandler
.thumb_set TIMER41_IRQHandler,Default_Handler

.weak TIMER42_IRQHandler
.thumb_set TIMER42_IRQHandler,Default_Handler

.weak TIMER43_IRQHandler
.thumb_set TIMER43_IRQHandler,Default_Handler

.weak TIMER44_IRQHandler
.thumb_set TIMER44_IRQHandler,Default_Handler

.weak TIMER50_IRQHandler
.thumb_set TIMER50_IRQHandler,Default_Handler

.weak TIMER51_IRQHandler
.thumb_set TIMER51_IRQHandler,Default_Handler

.weak USBHS1_EP1_OUT_IRQHandler
.thumb_set USBHS1_EP1_OUT_IRQHandler,Default_Handler

.weak USBHS1_EP1_IN_IRQHandler
.thumb_set USBHS1_EP1_IN_IRQHandler,Default_Handler

.weak USBHS1_WKUP_IRQHandler
.thumb_set USBHS1_WKUP_IRQHandler,Default_Handler

.weak USBHS1_IRQHandler
.thumb_set USBHS1_IRQHandler,Default_Handler

.weak ENET1_IRQHandler
.thumb_set ENET1_IRQHandler,Default_Handler

.weak ENET1_WKUP_IRQHandler
.thumb_set ENET1_WKUP_IRQHandler,Default_Handler

.weak CAN0_WKUP_IRQHandler
.thumb_set CAN0_WKUP_IRQHandler,Default_Handler

.weak CAN0_Message_IRQHandler
.thumb_set CAN0_Message_IRQHandler,Default_Handler

.weak CAN0_Busoff_IRQHandler
.thumb_set CAN0_Busoff_IRQHandler,Default_Handler

.weak CAN0_Error_IRQHandler
.thumb_set CAN0_Error_IRQHandler,Default_Handler

.weak CAN0_FastError_IRQHandler
.thumb_set CAN0_FastError_IRQHandler,Default_Handler

.weak CAN0_TEC_IRQHandler
.thumb_set CAN0_TEC_IRQHandler,Default_Handler

.weak CAN0_REC_IRQHandler
.thumb_set CAN0_REC_IRQHandler,Default_Handler

.weak CAN1_WKUP_IRQHandler
.thumb_set CAN1_WKUP_IRQHandler,Default_Handler

.weak CAN1_Message_IRQHandler
.thumb_set CAN1_Message_IRQHandler,Default_Handler

.weak CAN1_Busoff_IRQHandler
.thumb_set CAN1_Busoff_IRQHandler,Default_Handler

.weak CAN1_Error_IRQHandler
.thumb_set CAN1_Error_IRQHandler,Default_Handler

.weak CAN1_FastError_IRQHandler
.thumb_set CAN1_FastError_IRQHandler,Default_Handler

.weak CAN1_TEC_IRQHandler
.thumb_set CAN1_TEC_IRQHandler,Default_Handler

.weak CAN1_REC_IRQHandler
.thumb_set CAN1_REC_IRQHandler,Default_Handler

.weak CAN2_WKUP_IRQHandler
.thumb_set CAN2_WKUP_IRQHandler,Default_Handler

.weak CAN2_Message_IRQHandler
.thumb_set CAN2_Message_IRQHandler,Default_Handler

.weak CAN2_Busoff_IRQHandler
.thumb_set CAN2_Busoff_IRQHandler,Default_Handler

.weak CAN2_Error_IRQHandler
.thumb_set CAN2_Error_IRQHandler,Default_Handler

.weak CAN2_FastError_IRQHandler
.thumb_set CAN2_FastError_IRQHandler,Default_Handler

.weak CAN2_TEC_IRQHandler
.thumb_set CAN2_TEC_IRQHandler,Default_Handler

.weak CAN2_REC_IRQHandler
.thumb_set CAN2_REC_IRQHandler,Default_Handler

.weak EFUSE_IRQHandler
.thumb_set EFUSE_IRQHandler,Default_Handler

.weak I2C0_WKUP_IRQHandler
.thumb_set I2C0_WKUP_IRQHandler,Default_Handler

.weak I2C1_WKUP_IRQHandler
.thumb_set I2C1_WKUP_IRQHandler,Default_Handler

.weak I2C2_WKUP_IRQHandler
.thumb_set I2C2_WKUP_IRQHandler,Default_Handler

.weak I2C3_WKUP_IRQHandler
.thumb_set I2C3_WKUP_IRQHandler,Default_Handler

.weak LPDTS_IRQHandler
.thumb_set LPDTS_IRQHandler,Default_Handler

.weak LPDTS_WKUP_IRQHandler
.thumb_set LPDTS_WKUP_IRQHandler,Default_Handler

.weak TIMER0_DEC_IRQHandler
.thumb_set TIMER0_DEC_IRQHandler,Default_Handler

.weak TIMER7_DEC_IRQHandler
.thumb_set TIMER7_DEC_IRQHandler,Default_Handler

.weak TIMER1_DEC_IRQHandler
.thumb_set TIMER1_DEC_IRQHandler,Default_Handler

.weak TIMER2_DEC_IRQHandler
.thumb_set TIMER2_DEC_IRQHandler,Default_Handler

.weak TIMER3_DEC_IRQHandler
.thumb_set TIMER3_DEC_IRQHandler,Default_Handler

.weak TIMER4_DEC_IRQHandler
.thumb_set TIMER4_DEC_IRQHandler,Default_Handler

.weak TIMER22_DEC_IRQHandler
.thumb_set TIMER22_DEC_IRQHandler,Default_Handler

.weak TIMER23_DEC_IRQHandler
.thumb_set TIMER23_DEC_IRQHandler,Default_Handler

.weak TIMER30_DEC_IRQHandler
.thumb_set TIMER30_DEC_IRQHandler,Default_Handler

.weak TIMER31_DEC_IRQHandler
.thumb_set TIMER31_DEC_IRQHandler,Default_Handler

