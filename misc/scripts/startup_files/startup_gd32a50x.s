;/*!
;    \file    startup_gd32a50x.s
;    \brief   start up file
;
;    \version 2024-12-06, V1.4.0, firmware for GD32A50x
;*/
;
;/*
; * Copyright (c) 2009-2018 Arm Limited. All rights reserved.
; * Copyright (c) 2024 GigaDevice Semiconductor Inc.
; *
; * SPDX-License-Identifier: Apache-2.0
; *
; * Licensed under the Apache License, Version 2.0 (the License); you may
; * not use this file except in compliance with the License.
; * You may obtain a copy of the License at
; *
; * www.apache.org/licenses/LICENSE-2.0
; *
; * Unless required by applicable law or agreed to in writing, software
; * distributed under the License is distributed on an AS IS BASIS, WITHOUT
; * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
; * See the License for the specific language governing permissions and
; * limitations under the License.
; */
;
;/* This file refers the CMSIS standard, some adjustments are made according to GigaDevice chips */

; <h> Stack Configuration
;   <o> Stack Size (in Bytes) <0x0-0xFFFFFFFF:8>
; </h>

Stack_Size      EQU     0x00000800

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
                DCD     0                                 ; Reserved
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
                DCD     0                                 ; 18:Reserved
                DCD     RTC_IRQHandler                    ; 19:RTC
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
                DCD     ADC0_1_IRQHandler                 ; 34:ADC0 and ADC1
                DCD     CAN0_Message_IRQHandler           ; 35:CAN0 Interrupt for message buffer
                DCD     CAN0_Busoff_IRQHandler            ; 36:CAN0 Interrupt for bus off/bus off done
                DCD     CAN0_Error_IRQHandler             ; 37:CAN0 Interrupt for error
                DCD     CAN0_FastError_IRQHandler         ; 38:CAN0 Interrupt for error in fast transmission
                DCD     CAN0_TEC_IRQHandler               ; 39:CAN0 Interrupt for transmit warning
                DCD     CAN0_REC_IRQHandler               ; 40:CAN0 Interrupt for receive warning
                DCD     CAN0_WKUP_IRQHandler              ; 41:CAN0 wakeup through EXTI Line detection interrupt
                DCD     TIMER0_BRK_UP_TRG_CMT_IRQHandler  ; 42:TIMER0 Break Update Trigger and Commutation
                DCD     TIMER0_Channel_IRQHandler         ; 43:TIMER0 Channel Capture Compare
                DCD     TIMER1_IRQHandler                 ; 44:TIMER1
                DCD     TIMER19_BRK_UP_TRG_CMT_IRQHandler ; 45:TIMER19 Break Update Trigger and Commutation
                DCD     TIMER19_Channel_IRQHandler        ; 46:TIMER19 Channel Capture Compare
                DCD     I2C0_EV_IRQHandler                ; 47:I2C0 Event
                DCD     I2C0_ER_IRQHandler                ; 48:I2C0 Error
                DCD     I2C1_EV_IRQHandler                ; 49:I2C1 Event
                DCD     I2C1_ER_IRQHandler                ; 50:I2C1 Error
                DCD     SPI0_IRQHandler                   ; 51:SPI0
                DCD     SPI1_IRQHandler                   ; 52:SPI1
                DCD     USART0_IRQHandler                 ; 53:USART0
                DCD     USART1_IRQHandler                 ; 54:USART1
                DCD     USART2_IRQHandler                 ; 55:USART2
                DCD     EXTI10_15_IRQHandler              ; 56:EXTI Line10-15
                DCD     EXTI5_9_IRQHandler                ; 57:EXTI Line5-9
                DCD     TAMPER_IRQHandler                 ; 58:BKP Tamper
                DCD     TIMER20_BRK_UP_TRG_CMT_IRQHandler ; 59:TIMER20 Break Update Trigger and Commutation
                DCD     TIMER20_Channel_IRQHandler        ; 60:TIMER20 Channel Capture Compare
                DCD     TIMER7_BRK_UP_TRG_CMT_IRQHandler  ; 61:TIMER7 Break Update Trigger and Commutation
                DCD     TIMER7_Channel_IRQHandler         ; 62:TIMER7 Channel Capture Compare
                DCD     DMAMUX_IRQHandler                 ; 63:DMANUX
                DCD     SRAMC_ECCSE_IRQHandler            ; 64:Syscfg interrupt(sramc eccse)
                DCD     CMP_IRQHandler                    ; 65:CMP through EXTI Line
                DCD     0                                 ; 66:Reserved
                DCD     OVD_IRQHandler                    ; 67:OVD
                DCD     0                                 ; 68:Reserved
                DCD     0                                 ; 69:Reserved
                DCD     TIMER5_DAC_IRQHandler             ; 70:TIMER5 and DAC
                DCD     TIMER6_IRQHandler                 ; 71:TIMER6
                DCD     DMA1_Channel0_IRQHandler          ; 72:DMA1 Channel0
                DCD     DMA1_Channel1_IRQHandler          ; 73:DMA1 Channel1
                DCD     DMA1_Channel2_IRQHandler          ; 74:DMA1 Channel2
                DCD     DMA1_Channel3_IRQHandler          ; 75:DMA1 Channel3
                DCD     DMA1_Channel4_IRQHandler          ; 76:DMA1 Channel4
                DCD     0                                 ; 77:Reserved
                DCD     CAN1_WKUP_IRQHandler              ; 78:CAN1 wakeup through EXTI Line detection interrupt
                DCD     CAN1_Message_IRQHandler           ; 79:CAN1 Interrupt for message buffer
                DCD     CAN1_Busoff_IRQHandler            ; 80:CAN1 Interrupt for bus off/bus off done
                DCD     CAN1_Error_IRQHandler             ; 81:CAN1 Interrupt for error
                DCD     CAN1_FastError_IRQHandler         ; 82:CAN1 Interrupt for error in fast transmission
                DCD     CAN1_TEC_IRQHandler               ; 83:CAN1 Interrupt for transmit warning
                DCD     CAN1_REC_IRQHandler               ; 84:CAN1 Interrupt for receive warning
                DCD     FPU_IRQHandler                    ; 85:FPU
                DCD     MFCOM_IRQHandler                  ; 86:MFCOM

__Vectors_End

__Vectors_Size  EQU     __Vectors_End - __Vectors

                AREA    |.text|, CODE, READONLY

;/* reset Handler */
Reset_Handler   PROC
                EXPORT  Reset_Handler                     [WEAK]

                LDR     r0, =0x1FFFF7E0
                LDR     r2, [r0]
                LDR     r0, = 0xFFFF0000
                AND     r2, r2, r0
                LSR     r2, r2, #16
                LSL     r2, r2, #10
                LDR     r1, =0x20000000
                MOV     r0, #0x00
SRAM_INIT       STM     r1!, {r0}
                SUBS    r2, r2, #4
                CMP     r2, #0x00
                BNE     SRAM_INIT

                IMPORT  SystemInit
                IMPORT  __main
                LDR     R0, =SystemInit
                BLX     R0
                LDR     R0, =__main
                BX      R0
                ENDP

;/* dummy Exception Handlers */
NMI_Handler     PROC
                EXPORT  NMI_Handler                       [WEAK]
                B       .
                ENDP
HardFault_Handler\
                PROC
                EXPORT  HardFault_Handler                 [WEAK]
                B       .
                ENDP
MemManage_Handler\
                PROC
                EXPORT  MemManage_Handler                 [WEAK]
                B       .
                ENDP
BusFault_Handler\
                PROC
                EXPORT  BusFault_Handler                  [WEAK]
                B       .
                ENDP
UsageFault_Handler\
                PROC
                EXPORT  UsageFault_Handler                [WEAK]
                B       .
                ENDP
SVC_Handler     PROC
                EXPORT  SVC_Handler                       [WEAK]
                B       .
                ENDP
DebugMon_Handler\
                PROC
                EXPORT  DebugMon_Handler                  [WEAK]
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
                EXPORT  WWDGT_IRQHandler                  [WEAK]
                EXPORT  LVD_IRQHandler                    [WEAK]
                EXPORT  RTC_IRQHandler                    [WEAK]
                EXPORT  FMC_IRQHandler                    [WEAK]
                EXPORT  RCU_IRQHandler                    [WEAK]
                EXPORT  EXTI0_IRQHandler                  [WEAK]
                EXPORT  EXTI1_IRQHandler                  [WEAK]
                EXPORT  EXTI2_IRQHandler                  [WEAK]
                EXPORT  EXTI3_IRQHandler                  [WEAK]
                EXPORT  EXTI4_IRQHandler                  [WEAK]
                EXPORT  DMA0_Channel0_IRQHandler          [WEAK]
                EXPORT  DMA0_Channel1_IRQHandler          [WEAK]
                EXPORT  DMA0_Channel2_IRQHandler          [WEAK]
                EXPORT  DMA0_Channel3_IRQHandler          [WEAK]
                EXPORT  DMA0_Channel4_IRQHandler          [WEAK]
                EXPORT  DMA0_Channel5_IRQHandler          [WEAK]
                EXPORT  DMA0_Channel6_IRQHandler          [WEAK]
                EXPORT  ADC0_1_IRQHandler                 [WEAK]
                EXPORT  CAN0_Message_IRQHandler           [WEAK]
                EXPORT  CAN0_Busoff_IRQHandler            [WEAK]
                EXPORT  CAN0_Error_IRQHandler             [WEAK]
                EXPORT  CAN0_FastError_IRQHandler         [WEAK]
                EXPORT  CAN0_TEC_IRQHandler               [WEAK]
                EXPORT  CAN0_REC_IRQHandler               [WEAK]
                EXPORT  CAN0_WKUP_IRQHandler              [WEAK]
                EXPORT  TIMER0_BRK_UP_TRG_CMT_IRQHandler  [WEAK]
                EXPORT  TIMER0_Channel_IRQHandler         [WEAK]
                EXPORT  TIMER1_IRQHandler                 [WEAK]
                EXPORT  TIMER19_BRK_UP_TRG_CMT_IRQHandler [WEAK]
                EXPORT  TIMER19_Channel_IRQHandler        [WEAK]
                EXPORT  I2C0_EV_IRQHandler                [WEAK]
                EXPORT  I2C0_ER_IRQHandler                [WEAK]
                EXPORT  I2C1_EV_IRQHandler                [WEAK]
                EXPORT  I2C1_ER_IRQHandler                [WEAK]
                EXPORT  SPI0_IRQHandler                   [WEAK]
                EXPORT  SPI1_IRQHandler                   [WEAK]
                EXPORT  USART0_IRQHandler                 [WEAK]
                EXPORT  USART1_IRQHandler                 [WEAK]
                EXPORT  USART2_IRQHandler                 [WEAK]
                EXPORT  EXTI10_15_IRQHandler              [WEAK]
                EXPORT  EXTI5_9_IRQHandler                [WEAK]
                EXPORT  TAMPER_IRQHandler                 [WEAK]
                EXPORT  TIMER20_BRK_UP_TRG_CMT_IRQHandler [WEAK]
                EXPORT  TIMER20_Channel_IRQHandler        [WEAK]
                EXPORT  TIMER7_BRK_UP_TRG_CMT_IRQHandler  [WEAK]
                EXPORT  TIMER7_Channel_IRQHandler         [WEAK]
                EXPORT  DMAMUX_IRQHandler                 [WEAK]
                EXPORT  SRAMC_ECCSE_IRQHandler            [WEAK]
                EXPORT  CMP_IRQHandler                    [WEAK]
                EXPORT  OVD_IRQHandler                    [WEAK]
                EXPORT  TIMER5_DAC_IRQHandler             [WEAK]
                EXPORT  TIMER6_IRQHandler                 [WEAK]
                EXPORT  DMA1_Channel0_IRQHandler          [WEAK]
                EXPORT  DMA1_Channel1_IRQHandler          [WEAK]
                EXPORT  DMA1_Channel2_IRQHandler          [WEAK]
                EXPORT  DMA1_Channel3_IRQHandler          [WEAK]
                EXPORT  DMA1_Channel4_IRQHandler          [WEAK]
                EXPORT  CAN1_WKUP_IRQHandler              [WEAK]
                EXPORT  CAN1_Message_IRQHandler           [WEAK]
                EXPORT  CAN1_Busoff_IRQHandler            [WEAK]
                EXPORT  CAN1_Error_IRQHandler             [WEAK]
                EXPORT  CAN1_FastError_IRQHandler         [WEAK]
                EXPORT  CAN1_TEC_IRQHandler               [WEAK]
                EXPORT  CAN1_REC_IRQHandler               [WEAK]
                EXPORT  FPU_IRQHandler                    [WEAK]
                EXPORT  MFCOM_IRQHandler                  [WEAK]

;/* external interrupts handler */
WWDGT_IRQHandler
LVD_IRQHandler
RTC_IRQHandler
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
ADC0_1_IRQHandler
CAN0_Message_IRQHandler
CAN0_Busoff_IRQHandler
CAN0_Error_IRQHandler
CAN0_FastError_IRQHandler
CAN0_TEC_IRQHandler
CAN0_REC_IRQHandler
CAN0_WKUP_IRQHandler
TIMER0_BRK_UP_TRG_CMT_IRQHandler
TIMER0_Channel_IRQHandler
TIMER1_IRQHandler
TIMER19_BRK_UP_TRG_CMT_IRQHandler
TIMER19_Channel_IRQHandler
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
EXTI5_9_IRQHandler
TAMPER_IRQHandler
TIMER20_BRK_UP_TRG_CMT_IRQHandler
TIMER20_Channel_IRQHandler
TIMER7_BRK_UP_TRG_CMT_IRQHandler
TIMER7_Channel_IRQHandler
DMAMUX_IRQHandler
SRAMC_ECCSE_IRQHandler
CMP_IRQHandler
OVD_IRQHandler
TIMER5_DAC_IRQHandler
TIMER6_IRQHandler
DMA1_Channel0_IRQHandler
DMA1_Channel1_IRQHandler
DMA1_Channel2_IRQHandler
DMA1_Channel3_IRQHandler
DMA1_Channel4_IRQHandler
CAN1_WKUP_IRQHandler
CAN1_Message_IRQHandler
CAN1_Busoff_IRQHandler
CAN1_Error_IRQHandler
CAN1_FastError_IRQHandler
CAN1_TEC_IRQHandler
CAN1_REC_IRQHandler
FPU_IRQHandler
MFCOM_IRQHandler
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
