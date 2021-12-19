;/*!
;    \file    startup_gd32w51x.s
;    \brief   start up file
;
;    \version 2021-03-25, V1.0.0, firmware for GD32W51x
;*/
;/*
;    Copyright (c) 2021, GigaDevice Semiconductor Inc.
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
                DCD     MemManage_Handler                 ; MPU Fault Handler
                DCD     BusFault_Handler                  ; Bus Fault Handler
                DCD     UsageFault_Handler                ; Usage Fault Handler
                DCD     SecureFault_Handler               ; Secure Fault Handler
                DCD     0                                 ; Reserved
                DCD     0                                 ; Reserved
                DCD     0                                 ; Reserved
                DCD     SVC_Handler                       ; SVCall Handler
                DCD     DebugMon_Handler                  ; Debug Monitor Handler
                DCD     0                                 ; Reserved
                DCD     PendSV_Handler                    ; PendSV Handler
                DCD     SysTick_Handler                   ; SysTick Handler

;               /* external interrupts handler */
                DCD     WWDGT_IRQHandler                  ; 16:Window Watchdog Timer
                DCD     LVD_IRQHandler                    ; 17:LVD through EXTI Line detect
                DCD     TAMPER_STAMP_IRQHandler           ; 18:Tamper and TimeStamp through EXTI Line detect
                DCD     RTC_WKUP_IRQHandler               ; 19:RTC Wakeup through EXTI Line
                DCD     FMC_IRQHandler                    ; 20:FMC
                DCD     RCU_IRQHandler                    ; 21:RCU
                DCD     EXTI0_IRQHandler                  ; 22:EXTI Line 0
                DCD     EXTI1_IRQHandler                  ; 23:EXTI Line 1
                DCD     EXTI2_IRQHandler                  ; 24:EXTI Line 2
                DCD     EXTI3_IRQHandler                  ; 25:EXTI Line 3
                DCD     EXTI4_IRQHandler                  ; 26:EXTI Line 4
                DCD     DMA0_Channel0_IRQHandler          ; 27:DMA0 Channel0
                DCD     DMA0_Channel1_IRQHandler          ; 28:DMA0 Channel1
                DCD     DMA0_Channel2_IRQHandler          ; 29:DMA0 Channel2
                DCD     DMA0_Channel3_IRQHandler          ; 30:DMA0 Channel3
                DCD     DMA0_Channel4_IRQHandler          ; 31:DMA0 Channel4
                DCD     DMA0_Channel5_IRQHandler          ; 32:DMA0 Channel5
                DCD     DMA0_Channel6_IRQHandler          ; 33:DMA0 Channel6
                DCD     DMA0_Channel7_IRQHandler          ; 34:DMA0 Channel7
                DCD     ADC_IRQHandler                    ; 35:ADC
                DCD     TAMPER_STAMP_S_IRQHandler         ; 36:RTC Tamper and TimeStamp Events Security Interrupt
                DCD     RTC_WKUP_S_IRQHandler             ; 37:RTC Wakeup Security Interrupt
                DCD     RTC_Alarm_S_IRQHandler            ; 38:RTC Alarm Security Interrupt
                DCD     EXTI5_9_IRQHandler                ; 39:EXTI5 to EXTI9
                DCD     TIMER0_BRK_IRQHandler             ; 40:TIMER0 Break
                DCD     TIMER0_UP_IRQHandler              ; 41:TIMER0 Update
                DCD     TIMER0_CMT_IRQHandler             ; 42:TIMER0 Commutation
                DCD     TIMER0_Channel_IRQHandler         ; 43:TIMER0 Channel Capture Compare
                DCD     TIMER1_IRQHandler                 ; 44:TIMER1
                DCD     TIMER2_IRQHandler                 ; 45:TIMER2
                DCD     TIMER3_IRQHandler                 ; 46:TIMER3
                DCD     I2C0_EV_IRQHandler                ; 47:I2C0 Event
                DCD     I2C0_ER_IRQHandler                ; 48:I2C0 Error
                DCD     I2C1_EV_IRQHandler                ; 49:I2C1 Event
                DCD     I2C1_ER_IRQHandler                ; 50:I2C1 Error
                DCD     SPI0_IRQHandler                   ; 51:SPI0
                DCD     SPI1_IRQHandler                   ; 52:SPI1/I2S1
                DCD     USART0_IRQHandler                 ; 53:USART0
                DCD     USART1_IRQHandler                 ; 54:USART1
                DCD     USART2_IRQHandler                 ; 55:USART2
                DCD     EXTI10_15_IRQHandler              ; 56:EXTI10 to EXTI15
                DCD     RTC_Alarm_IRQHandler              ; 57:RTC Alarm
                DCD     VLVDF_IRQHandler                  ; 58:VDDA Low Voltage Detector
                DCD     0                                 ; 59:Reserved
                DCD     TIMER15_IRQHandler                ; 60:TIMER15
                DCD     TIMER16_IRQHandler                ; 61:TIMER16
                DCD     0                                 ; 62:Reserved
                DCD     0                                 ; 63:Reserved
                DCD     0                                 ; 64:Reserved
                DCD     SDIO_IRQHandler                   ; 65:SDIO
                DCD     TIMER4_IRQHandler                 ; 66:TIMER4
                DCD     I2C0_WKUP_IRQHandler              ; 67:I2C0 Wakeup
                DCD     USART0_WKUP_IRQHandler            ; 68:USART0 Wakeup
                DCD     USART2_WKUP_IRQHandler            ; 69:USART2 Wakeup
                DCD     TIMER5_IRQHandler                 ; 70:TIMER5
                DCD     0                                 ; 71:Reserved
                DCD     DMA1_Channel0_IRQHandler          ; 72:DMA1 Channel0
                DCD     DMA1_Channel1_IRQHandler          ; 73:DMA1 Channel1
                DCD     DMA1_Channel2_IRQHandler          ; 74:DMA1 Channel2
                DCD     DMA1_Channel3_IRQHandler          ; 75:DMA1 Channel3
                DCD     DMA1_Channel4_IRQHandler          ; 76:DMA1 Channel4
                DCD     DMA1_Channel5_IRQHandler          ; 77:DMA1 Channel5
                DCD     DMA1_Channel6_IRQHandler          ; 78:DMA1 Channel6
                DCD     DMA1_Channel7_IRQHandler          ; 79:DMA1 Channel7
                DCD     0                                 ; 80:Reserved
                DCD     0                                 ; 81:Reserved
                DCD     WIFI11N_WKUP_IRQHandler           ; 82:WIFI11N wakeup interrupt
                DCD     USBFS_IRQHandler                  ; 83:USBFS global interrupt
                DCD     0                                 ; 84:Reserved
                DCD     0                                 ; 85:Reserved
                DCD     0                                 ; 86:Reserved
                DCD     0                                 ; 87:Reserved
                DCD     0                                 ; 88:Reserved
                DCD     0                                 ; 89:Reserved
                DCD     0                                 ; 90:Reserved
                DCD     0                                 ; 91:Reserved
                DCD     USBFS_WKUP_IRQHandler             ; 92:USBFS_WKUP
                DCD     0                                 ; 93:Reserved
                DCD     DCI_IRQHandler                    ; 94:DCI
                DCD     CAU_IRQHandler                    ; 95:CAU
                DCD     HAU_TRNG_IRQHandler               ; 96:HAU and TRNG
                DCD     FPU_IRQHandler                    ; 97:FPU
                DCD     0                                 ; 98:Reserved
                DCD     0                                 ; 99:Reserved
                DCD     0                                 ; 100:Reserved
                DCD     0                                 ; 101:Reserved
                DCD     0                                 ; 102:Reserved
                DCD     0                                 ; 103:Reserved
                DCD     0                                 ; 104:Reserved
                DCD     HPDF_INT0_IRQHandler              ; 105:HPDF global Interrupt 0
                DCD     HPDF_INT1_IRQHandler              ; 106:HPDF global Interrupt 1
                DCD     WIFI11N_INT0_IRQHandler           ; 107:WIFI11N global interrupt0
                DCD     WIFI11N_INT1_IRQHandler           ; 108:WIFI11N global interrupt1
                DCD     WIFI11N_INT2_IRQHandler           ; 109:WIFI11N global interrupt2
                DCD     EFUSE_IRQHandler                  ; 110:EFUSE
                DCD     QSPI_IRQHandler                   ; 111:QUADSPI
                DCD     PKCAU_IRQHandler                  ; 112:PKCAU
                DCD     TSI_IRQHandler                    ; 113:TSI
                DCD     ICACHE_IRQHandler                 ; 114:ICACHE
                DCD     TZIAC_S_IRQHandler                ; 115:TrustZone interrupt controller secure interrupts
                DCD     FMC_S_IRQHandler                  ; 116:FMC
                DCD     QSPI_S_IRQHandler                 ; 117:QSPI security interrupt

__Vectors_End

__Vectors_Size  EQU     __Vectors_End - __Vectors

                AREA    |.text|, CODE, READONLY

;/* reset Handler */
Reset_Handler   PROC
                EXPORT  Reset_Handler                        [WEAK]
                IMPORT  SystemInit
                IMPORT  __main
                LDR     R0, =SystemInit
                BLX     R0
                LDR     R0, =__main
                BX      R0
                ENDP

;/* dummy Exception Handlers */
NMI_Handler     PROC
                EXPORT  NMI_Handler                          [WEAK]
                B       .
                ENDP
HardFault_Handler\
                PROC
                EXPORT  HardFault_Handler                    [WEAK]
                B       .
                ENDP
MemManage_Handler\
                PROC
                EXPORT  MemManage_Handler                    [WEAK]
                B       .
                ENDP
BusFault_Handler\
                PROC
                EXPORT  BusFault_Handler                     [WEAK]
                B       .
                ENDP
UsageFault_Handler\
                PROC
                EXPORT  UsageFault_Handler                   [WEAK]
                B       .
                ENDP
SecureFault_Handler\
                PROC
                EXPORT  SecureFault_Handler                  [WEAK]
                B       .
                ENDP
SVC_Handler     PROC
                EXPORT  SVC_Handler                          [WEAK]
                B       .
                ENDP
DebugMon_Handler\
                PROC
                EXPORT  DebugMon_Handler                     [WEAK]
                B       .
                ENDP
PendSV_Handler\
                PROC
                EXPORT  PendSV_Handler                       [WEAK]
                B       .
                ENDP
SysTick_Handler\
                PROC
                EXPORT  SysTick_Handler                      [WEAK]
                B       .
                ENDP

Default_Handler PROC
;               /* external interrupts handler */
                EXPORT     WWDGT_IRQHandler                  [WEAK]
                EXPORT     LVD_IRQHandler                    [WEAK]
                EXPORT     TAMPER_STAMP_IRQHandler           [WEAK]
                EXPORT     RTC_WKUP_IRQHandler               [WEAK]
                EXPORT     FMC_IRQHandler                    [WEAK]
                EXPORT     RCU_IRQHandler                    [WEAK]
                EXPORT     EXTI0_IRQHandler                  [WEAK]
                EXPORT     EXTI1_IRQHandler                  [WEAK]
                EXPORT     EXTI2_IRQHandler                  [WEAK]
                EXPORT     EXTI3_IRQHandler                  [WEAK]
                EXPORT     EXTI4_IRQHandler                  [WEAK]
                EXPORT     DMA0_Channel0_IRQHandler          [WEAK]
                EXPORT     DMA0_Channel1_IRQHandler          [WEAK]
                EXPORT     DMA0_Channel2_IRQHandler          [WEAK]
                EXPORT     DMA0_Channel3_IRQHandler          [WEAK]
                EXPORT     DMA0_Channel4_IRQHandler          [WEAK]
                EXPORT     DMA0_Channel5_IRQHandler          [WEAK]
                EXPORT     DMA0_Channel6_IRQHandler          [WEAK]
                EXPORT     DMA0_Channel7_IRQHandler          [WEAK]
                EXPORT     ADC_IRQHandler                    [WEAK]
                EXPORT     TAMPER_STAMP_S_IRQHandler         [WEAK]
                EXPORT     RTC_WKUP_S_IRQHandler             [WEAK]
                EXPORT     RTC_Alarm_S_IRQHandler            [WEAK]
                EXPORT     EXTI5_9_IRQHandler                [WEAK]
                EXPORT     TIMER0_BRK_IRQHandler             [WEAK]
                EXPORT     TIMER0_UP_IRQHandler              [WEAK]
                EXPORT     TIMER0_CMT_IRQHandler             [WEAK]
                EXPORT     TIMER0_Channel_IRQHandler         [WEAK]
                EXPORT     TIMER1_IRQHandler                 [WEAK]
                EXPORT     TIMER2_IRQHandler                 [WEAK]
                EXPORT     TIMER3_IRQHandler                 [WEAK]
                EXPORT     I2C0_EV_IRQHandler                [WEAK]
                EXPORT     I2C0_ER_IRQHandler                [WEAK]
                EXPORT     I2C1_EV_IRQHandler                [WEAK]
                EXPORT     I2C1_ER_IRQHandler                [WEAK]
                EXPORT     SPI0_IRQHandler                   [WEAK]
                EXPORT     SPI1_IRQHandler                   [WEAK]
                EXPORT     USART0_IRQHandler                 [WEAK]
                EXPORT     USART1_IRQHandler                 [WEAK]
                EXPORT     USART2_IRQHandler                 [WEAK]
                EXPORT     EXTI10_15_IRQHandler              [WEAK]
                EXPORT     RTC_Alarm_IRQHandler              [WEAK]
                EXPORT     VLVDF_IRQHandler                  [WEAK]
                EXPORT     TIMER15_IRQHandler                [WEAK]
                EXPORT     TIMER16_IRQHandler                [WEAK]
                EXPORT     SDIO_IRQHandler                   [WEAK]
                EXPORT     TIMER4_IRQHandler                 [WEAK]
                EXPORT     I2C0_WKUP_IRQHandler              [WEAK]
                EXPORT     USART0_WKUP_IRQHandler            [WEAK]
                EXPORT     USART2_WKUP_IRQHandler            [WEAK]
                EXPORT     TIMER5_IRQHandler                 [WEAK]
                EXPORT     DMA1_Channel0_IRQHandler          [WEAK]
                EXPORT     DMA1_Channel1_IRQHandler          [WEAK]
                EXPORT     DMA1_Channel2_IRQHandler          [WEAK]
                EXPORT     DMA1_Channel3_IRQHandler          [WEAK]
                EXPORT     DMA1_Channel4_IRQHandler          [WEAK]
                EXPORT     DMA1_Channel5_IRQHandler          [WEAK]
                EXPORT     DMA1_Channel6_IRQHandler          [WEAK]
                EXPORT     DMA1_Channel7_IRQHandler          [WEAK]
                EXPORT     WIFI11N_WKUP_IRQHandler           [WEAK]
                EXPORT     USBFS_IRQHandler                  [WEAK]
                EXPORT     USBFS_WKUP_IRQHandler             [WEAK]
                EXPORT     DCI_IRQHandler                    [WEAK]
                EXPORT     CAU_IRQHandler                    [WEAK]
                EXPORT     HAU_TRNG_IRQHandler               [WEAK]
                EXPORT     FPU_IRQHandler                    [WEAK]
                EXPORT     HPDF_INT0_IRQHandler              [WEAK]
                EXPORT     HPDF_INT1_IRQHandler              [WEAK]
                EXPORT     WIFI11N_INT0_IRQHandler           [WEAK]
                EXPORT     WIFI11N_INT1_IRQHandler           [WEAK]
                EXPORT     WIFI11N_INT2_IRQHandler           [WEAK]
                EXPORT     EFUSE_IRQHandler                  [WEAK]
                EXPORT     QSPI_IRQHandler                   [WEAK]
                EXPORT     PKCAU_IRQHandler                  [WEAK]
                EXPORT     TSI_IRQHandler                    [WEAK]
                EXPORT     ICACHE_IRQHandler                 [WEAK]
                EXPORT     TZIAC_S_IRQHandler                [WEAK]
                EXPORT     FMC_S_IRQHandler                  [WEAK]
                EXPORT     QSPI_S_IRQHandler                 [WEAK]
  
;/* external interrupts handler */
WWDGT_IRQHandler
LVD_IRQHandler
TAMPER_STAMP_IRQHandler
RTC_WKUP_IRQHandler
FMC_IRQHandler
RCU_IRQHandler
EXTI0_IRQHandler
EXTI1_IRQHandler
EXTI2_IRQHandler
EXTI3_IRQHandler
EXTI4_IRQHandler
DMA0_Channel0_IRQHandler
DMA0_Channel1_IRQHandler
DMA0_Channel2_IRQHandler
DMA0_Channel3_IRQHandler
DMA0_Channel4_IRQHandler
DMA0_Channel5_IRQHandler
DMA0_Channel6_IRQHandler
DMA0_Channel7_IRQHandler
ADC_IRQHandler
TAMPER_STAMP_S_IRQHandler
RTC_WKUP_S_IRQHandler
RTC_Alarm_S_IRQHandler
EXTI5_9_IRQHandler
TIMER0_BRK_IRQHandler
TIMER0_UP_IRQHandler
TIMER0_CMT_IRQHandler
TIMER0_Channel_IRQHandler
TIMER1_IRQHandler
TIMER2_IRQHandler
TIMER3_IRQHandler
I2C0_EV_IRQHandler
I2C0_ER_IRQHandler
I2C1_EV_IRQHandler
I2C1_ER_IRQHandler
SPI0_IRQHandler
SPI1_IRQHandler
USART0_IRQHandler
USART1_IRQHandler
USART2_IRQHandler
EXTI10_15_IRQHandler
RTC_Alarm_IRQHandler
VLVDF_IRQHandler
TIMER15_IRQHandler
TIMER16_IRQHandler
SDIO_IRQHandler
TIMER4_IRQHandler
I2C0_WKUP_IRQHandler
USART0_WKUP_IRQHandler
USART2_WKUP_IRQHandler
TIMER5_IRQHandler
DMA1_Channel0_IRQHandler
DMA1_Channel1_IRQHandler
DMA1_Channel2_IRQHandler
DMA1_Channel3_IRQHandler
DMA1_Channel4_IRQHandler
DMA1_Channel5_IRQHandler
DMA1_Channel6_IRQHandler
DMA1_Channel7_IRQHandler
WIFI11N_WKUP_IRQHandler
USBFS_IRQHandler
USBFS_WKUP_IRQHandler
DCI_IRQHandler
CAU_IRQHandler
HAU_TRNG_IRQHandler
FPU_IRQHandler
HPDF_INT0_IRQHandler
HPDF_INT1_IRQHandler
WIFI11N_INT0_IRQHandler
WIFI11N_INT1_IRQHandler
WIFI11N_INT2_IRQHandler
EFUSE_IRQHandler
QSPI_IRQHandler
PKCAU_IRQHandler
TSI_IRQHandler
ICACHE_IRQHandler
TZIAC_S_IRQHandler
FMC_S_IRQHandler
QSPI_S_IRQHandler

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
