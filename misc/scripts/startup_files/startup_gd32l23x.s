;/*!
;    \file    startup_gd32l301.s
;    \brief   start up file
;
;    \version 2020-09-17, V1.0.0, firmware for GD32L23x
;*/
;
;/*
;    Copyright (c) 2020, GigaDevice Semiconductor Inc.
;
;    Redistribution and use in source and binary forms, with or without modification, 
;are permitted provided that the following conditions are met:
;
;    1. Redistributions of source code must retain the above copyright notice, this 
;       list of conditions and the following disclaimer.
;    2. Redistributions in binary form must reproduce the above copyright notice, 
;       this list of conditions and the following disclaimer in the documentation 
;       and/or other materials provided with the distribution.
;    3. Neither the name of the copyright holder nor the names of its contributors 
;       may be used to endorse or promote products derived from this software without 
;       specific prior written permission.
;
;    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
;AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
;WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
;IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
;INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
;NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
;PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
;WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
;ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
;OF SUCH DAMAGE.
;*/

; <h> Stack Configuration
;   <o> Stack Size (in Bytes) <0x0-0xFFFFFFFF:8>
; </h>

Stack_Size      EQU     0x00000400

                AREA    STACK, NOINIT, READWRITE, ALIGN=3
Stack_Mem       SPACE   Stack_Size
__initial_sp


; <h> Heap Configuration
;   <o>  Heap Size (in Bytes) <0x0-0xFFFFFFFF:8>
; </h>

Heap_Size       EQU     0x00000400

                AREA    HEAP, NOINIT, READWRITE, ALIGN=3
__heap_base
Heap_Mem        SPACE   Heap_Size
__heap_limit

                PRESERVE8
                THUMB

;               /* reset Vector Mapped to at Address 0 */
                AREA    RESET, DATA, READONLY
                EXPORT  __Vectors
                EXPORT  __Vectors_End
                EXPORT  __Vectors_Size

__Vectors       DCD     __initial_sp                      ; Top of Stack
                DCD     Reset_Handler                     ; Reset Handler
                DCD     NMI_Handler                       ; NMI Handler
                DCD     HardFault_Handler                 ; Hard Fault Handler
                DCD     0                                 ; Reserved
                DCD     0                                 ; Reserved
                DCD     0                                 ; Reserved
                DCD     0                                 ; Reserved
                DCD     0                                 ; Reserved
                DCD     0                                 ; Reserved
                DCD     0                                 ; Reserved
                DCD     SVC_Handler                       ; SVCall Handler
                DCD     0                                 ; Reserved
                DCD     0                                 ; Reserved
                DCD     PendSV_Handler                    ; PendSV Handler
                DCD     SysTick_Handler                   ; SysTick Handler

;               /* external interrupts handler */
                DCD     WWDGT_IRQHandler                             ; 16:Window Watchdog Timer
                DCD     LVD_IRQHandler                               ; 17:LVD through EXTI Line detect
                DCD     TAMPER_STAMP_IRQHandler                      ; 18:RTC Tamper and TimeStamp through EXTI Line detect
                DCD     RTC_WKUP_IRQHandler                          ; 19:RTC Wakeup from EXTI interrupt
                DCD     FMC_IRQHandler                               ; 20:FMC global interrupt
                DCD     RCU_CTC_IRQHandler                           ; 21:RCU or CTC global interrupt
                DCD     EXTI0_IRQHandler                             ; 22:EXTI Line 0
                DCD     EXTI1_IRQHandler                             ; 23:EXTI Line 1
                DCD     EXTI2_IRQHandler                             ; 24:EXTI Line 2
                DCD     EXTI3_IRQHandler                             ; 25:EXTI Line 3
                DCD     EXTI4_IRQHandler                             ; 26:EXTI Line 4
                DCD     DMA_Channel0_IRQHandler                      ; 27:DMA Channel 0 
                DCD     DMA_Channel1_IRQHandler                      ; 28:DMA Channel 1 
                DCD     DMA_Channel2_IRQHandler                      ; 29:DMA Channel 2 
                DCD     DMA_Channel3_IRQHandler                      ; 30:DMA Channel 3 
                DCD     DMA_Channel4_IRQHandler                      ; 31:DMA Channel 4 
                DCD     DMA_Channel5_IRQHandler                      ; 32:DMA Channel 5 
                DCD     DMA_Channel6_IRQHandler                      ; 33:DMA Channel 6 
                DCD     ADC_IRQHandler                               ; 34:ADC interrupt 
                DCD     USBD_HP_IRQHandler                           ; 35:USBD High Priority interrupt
                DCD     USBD_LP_IRQHandler                           ; 36:USBD Low Priority interrupt
                DCD     TIMER1_IRQHandler                            ; 37:TIMER1
                DCD     TIMER2_IRQHandler                            ; 38:TIMER2
                DCD     TIMER8_IRQHandler                            ; 39:TIMER8
                DCD     TIMER11_IRQHandler                           ; 40:TIMER11
                DCD     TIMER5_IRQHandler                            ; 41:TIMER5
                DCD     TIMER6_IRQHandler                            ; 42:TIMER6
                DCD     USART0_IRQHandler                            ; 43:USART0
                DCD     USART1_IRQHandler                            ; 44:USART1
                DCD     UART3_IRQHandler                             ; 45:UART3
                DCD     UART4_IRQHandler                             ; 46:UART4
                DCD     I2C0_EV_IRQHandler                           ; 47:I2C0 Event
                DCD     I2C0_ER_IRQHandler                           ; 48:I2C0 Error
                DCD     I2C1_EV_IRQHandler                           ; 49:I2C1 Event
                DCD     I2C1_ER_IRQHandler                           ; 50:I2C1 Error
                DCD     SPI0_IRQHandler                              ; 51:SPI0
                DCD     SPI1_IRQHandler                              ; 52:SPI1
                DCD     DAC_IRQHandler                               ; 53:DAC
                DCD     0                                            ; 54:Reserved
                DCD     I2C2_EV_IRQHandler                           ; 55:I2C2 Event
                DCD     I2C2_ER_IRQHandler                           ; 56:I2C2 Error
                DCD     RTC_Alarm_IRQHandler                         ; 57:RTC Alarm through EXTI Line detect
                DCD     USBD_WKUP_IRQHandler                         ; 58:USBD wakeup through EXTI Line detect
                DCD     EXTI5_9_IRQHandler                           ; 59:EXTI5 to EXTI9
                DCD     0                                            ; 60:Reserved
                DCD     0                                            ; 61:Reserved
                DCD     0                                            ; 62:Reserved
                DCD     EXTI10_15_IRQHandler                         ; 63:EXTI10 to EXT15
                DCD     0                                            ; 64:Reserved
                DCD     0                                            ; 65:Reserved
                DCD     0                                            ; 66:Reserved
                DCD     0                                            ; 67:Reserved
                DCD     0                                            ; 68:Reserved
                DCD     0                                            ; 69:Reserved
                DCD     0                                            ; 70:Reserved
                DCD     DMAMUX_IRQHandler                            ; 71:Reserved
                DCD     CMP0_IRQHandler                              ; 72:Comparator 0 interrupt through EXTI Line detect
                DCD     CMP1_IRQHandler                              ; 73:Comparator 1 interrupt through EXTI Line detect
                DCD     I2C0_WKUP_IRQHandler                         ; 74:I2C0 Wakeup interrupt through EXTI Line detect
                DCD     I2C2_WKUP_IRQHandler                         ; 75:I2C2 Wakeup interrupt through EXTI Line detect
                DCD     USART0_WKUP_IRQHandler                       ; 76:USART0 Wakeup interrupt through EXTI Line detect
                DCD     LPUART_IRQHandler                            ; 77:LPUART global interrupt
                DCD     CAU_IRQHandler                               ; 78:CAU
                DCD     TRNG_IRQHandler                              ; 79:TRNG
                DCD     SLCD_IRQHandler                              ; 80:SLCD
                DCD     USART1_WKUP_IRQHandler                       ; 81:USART1 Wakeup interrupt through EXTI Line detect
                DCD     I2C1_WKUP_IRQHandler                         ; 82:I2C1 Wakeup interrupt through EXTI Line detect
                DCD     LPUART_WKUP_IRQHandler                       ; 83:LPUART Wakeup interrupt through EXTI Line detect
                DCD     LPTIMER_IRQHandler                           ; 84:LPTIMER interrupt 

__Vectors_End

__Vectors_Size  EQU     __Vectors_End - __Vectors

                AREA    |.text|, CODE, READONLY

;/* reset Handler */
Reset_Handler   PROC
                EXPORT  Reset_Handler                     [WEAK]
                IMPORT  SystemInit
                IMPORT  __main
                LDR     R0, =SystemInit
                BLX     R0
                LDR     R0, =__main
                BX      R0
                ENDP

;/* dummy Exception Handlers */
NMI_Handler\
                PROC
                EXPORT  NMI_Handler                       [WEAK]
                B       .
                ENDP
HardFault_Handler\
                PROC
                EXPORT  HardFault_Handler                 [WEAK]
                B       .
                ENDP
SVC_Handler\
                PROC
                EXPORT  SVC_Handler                       [WEAK]
                B       .
                ENDP
PendSV_Handler\
                PROC
                EXPORT  PendSV_Handler                    [WEAK]
                B       .
                ENDP
SysTick_Handler\
                PROC
                EXPORT  SysTick_Handler                   [WEAK]
                B       .
                ENDP

Default_Handler PROC
;               /* external interrupts handler */
                EXPORT  WWDGT_IRQHandler                             [WEAK]
                EXPORT  LVD_IRQHandler                               [WEAK]
                EXPORT  TAMPER_STAMP_IRQHandler                      [WEAK]
                EXPORT  RTC_WKUP_IRQHandler                          [WEAK]
                EXPORT  FMC_IRQHandler                               [WEAK]
                EXPORT  RCU_CTC_IRQHandler                           [WEAK]
                EXPORT  EXTI0_IRQHandler                             [WEAK]
                EXPORT  EXTI1_IRQHandler                             [WEAK]
                EXPORT  EXTI2_IRQHandler                             [WEAK]
                EXPORT  EXTI3_IRQHandler                             [WEAK]
                EXPORT  EXTI4_IRQHandler                             [WEAK]
                EXPORT  DMA_Channel0_IRQHandler                      [WEAK]
                EXPORT  DMA_Channel1_IRQHandler                      [WEAK]
                EXPORT  DMA_Channel2_IRQHandler                      [WEAK]
                EXPORT  DMA_Channel3_IRQHandler                      [WEAK]
                EXPORT  DMA_Channel4_IRQHandler                      [WEAK]
                EXPORT  DMA_Channel5_IRQHandler                      [WEAK]
                EXPORT  DMA_Channel6_IRQHandler                      [WEAK]
                EXPORT  ADC_IRQHandler                               [WEAK]
                EXPORT  USBD_HP_IRQHandler                           [WEAK]
                EXPORT  USBD_LP_IRQHandler                           [WEAK]
                EXPORT  TIMER1_IRQHandler                            [WEAK]
                EXPORT  TIMER2_IRQHandler                            [WEAK]
                EXPORT  TIMER8_IRQHandler                            [WEAK]
                EXPORT  TIMER11_IRQHandler                           [WEAK]
                EXPORT  TIMER5_IRQHandler                            [WEAK]
                EXPORT  TIMER6_IRQHandler                            [WEAK]
                EXPORT  USART0_IRQHandler                            [WEAK]
                EXPORT  USART1_IRQHandler                            [WEAK]
                EXPORT  UART3_IRQHandler                             [WEAK]
                EXPORT  UART4_IRQHandler                             [WEAK]
                EXPORT  I2C0_EV_IRQHandler                           [WEAK]
                EXPORT  I2C0_ER_IRQHandler                           [WEAK]
                EXPORT  I2C1_EV_IRQHandler                           [WEAK]
                EXPORT  I2C1_ER_IRQHandler                           [WEAK]
                EXPORT  SPI0_IRQHandler                              [WEAK]
                EXPORT  SPI1_IRQHandler                              [WEAK]
                EXPORT  DAC_IRQHandler                               [WEAK]
                EXPORT  I2C2_EV_IRQHandler                           [WEAK]
                EXPORT  I2C2_ER_IRQHandler                           [WEAK]
                EXPORT  RTC_Alarm_IRQHandler                         [WEAK]
                EXPORT  USBD_WKUP_IRQHandler                         [WEAK]
                EXPORT  EXTI5_9_IRQHandler                           [WEAK]
                EXPORT  EXTI10_15_IRQHandler                         [WEAK]
                EXPORT  DMAMUX_IRQHandler                            [WEAK]
                EXPORT  CMP0_IRQHandler                              [WEAK]
                EXPORT  CMP1_IRQHandler                              [WEAK]
                EXPORT  I2C0_WKUP_IRQHandler                         [WEAK]
                EXPORT  I2C2_WKUP_IRQHandler                         [WEAK]
                EXPORT  USART0_WKUP_IRQHandler                       [WEAK]
                EXPORT  LPUART_IRQHandler                            [WEAK]
                EXPORT  CAU_IRQHandler                               [WEAK]
                EXPORT  TRNG_IRQHandler                              [WEAK]
                EXPORT  SLCD_IRQHandler                              [WEAK]
                EXPORT  USART1_WKUP_IRQHandler                       [WEAK]
                EXPORT  I2C1_WKUP_IRQHandler                         [WEAK]
                EXPORT  LPUART_WKUP_IRQHandler                       [WEAK]
                EXPORT  LPTIMER_IRQHandler                           [WEAK]
                        
;/* external interrupts handler */
WWDGT_IRQHandler
LVD_IRQHandler
TAMPER_STAMP_IRQHandler
RTC_WKUP_IRQHandler
FMC_IRQHandler
RCU_CTC_IRQHandler
EXTI0_IRQHandler
EXTI1_IRQHandler
EXTI2_IRQHandler
EXTI3_IRQHandler
EXTI4_IRQHandler
DMA_Channel0_IRQHandler
DMA_Channel1_IRQHandler
DMA_Channel2_IRQHandler
DMA_Channel3_IRQHandler
DMA_Channel4_IRQHandler
DMA_Channel5_IRQHandler
DMA_Channel6_IRQHandler
ADC_IRQHandler
USBD_HP_IRQHandler
USBD_LP_IRQHandler
TIMER1_IRQHandler
TIMER2_IRQHandler
TIMER8_IRQHandler
TIMER11_IRQHandler
TIMER5_IRQHandler
TIMER6_IRQHandler
USART0_IRQHandler
USART1_IRQHandler
UART3_IRQHandler
UART4_IRQHandler
I2C0_EV_IRQHandler
I2C0_ER_IRQHandler
I2C1_EV_IRQHandler
I2C1_ER_IRQHandler
SPI0_IRQHandler
SPI1_IRQHandler
DAC_IRQHandler
I2C2_EV_IRQHandler
I2C2_ER_IRQHandler
RTC_Alarm_IRQHandler
USBD_WKUP_IRQHandler
EXTI5_9_IRQHandler
EXTI10_15_IRQHandler
CMP0_IRQHandler
CMP1_IRQHandler
DMAMUX_IRQHandler
I2C0_WKUP_IRQHandler
I2C2_WKUP_IRQHandler
USART0_WKUP_IRQHandler
LPUART_IRQHandler
CAU_IRQHandler
TRNG_IRQHandler
SLCD_IRQHandler
USART1_WKUP_IRQHandler
I2C1_WKUP_IRQHandler
LPUART_WKUP_IRQHandler
LPTIMER_IRQHandler

                B       .
                ENDP

                ALIGN

; user Initial Stack & Heap

                IF      :DEF:__MICROLIB

                EXPORT  __initial_sp
                EXPORT  __heap_base
                EXPORT  __heap_limit

                ELSE

                IMPORT  __use_two_region_memory
                EXPORT  __user_initial_stackheap

__user_initial_stackheap PROC
                LDR     R0, =  Heap_Mem
                LDR     R1, =(Stack_Mem + Stack_Size)
                LDR     R2, = (Heap_Mem +  Heap_Size)
                LDR     R3, = Stack_Mem
                BX      LR
                ENDP

                ALIGN

                ENDIF

                END
