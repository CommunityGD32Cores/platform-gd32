/*!
    \file    platform_def.h
    \brief   Platform definition for GD32W51x WiFi SDK

    \version 2021-10-30, V1.0.0, firmware for GD32W51x
*/

/*
    Copyright (c) 2021, GigaDevice Semiconductor Inc.

    Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.
    3. Neither the name of the copyright holder nor the names of its contributors
       may be used to endorse or promote products derived from this software without
       specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
OF SUCH DAMAGE.
*/

#ifndef _PLATFORM_DEF_H
#define _PLATFORM_DEF_H

#define PLATFORM_FPGA_3210X        1
#define PLATFORM_ASIC_32W51X       101

#define CONFIG_PLATFORM            PLATFORM_ASIC_32W51X

#ifndef CONFIG_PLATFORM
#error "CONFIG_PLATFORM must be defined!"
#elif CONFIG_PLATFORM >= PLATFORM_ASIC_32W51X
#define CONFIG_PLATFORM_ASIC
#else
#define CONFIG_PLATFORM_FPGA
#endif

#define PLATFORM_BOARD_32W515T_START    0
#define PLATFORM_BOARD_32W515P_EVAL     1
#ifdef CONFIG_PLATFORM_ASIC
#define CONFIG_BOARD            PLATFORM_BOARD_32W515T_START
#endif

#define XIP_FLASH_SIP   0
#define XIP_FLASH_EXT   1
#define CONFIG_XIP_FLASH        XIP_FLASH_SIP

#ifndef CONFIG_XIP_FLASH
#error "CONFIG_XIP_FLASH must be defined!"
#elif (CONFIG_XIP_FLASH == XIP_FLASH_EXT)
#define QSPI_FLASH_1_LINE        0
#define QSPI_FLASH_2_LINES       1
#define QSPI_FLASH_4_LINES       2
#define QSPI_FLASH_MODE          QSPI_FLASH_4_LINES
#endif

#define CRYSTAL_26M             0
#define CRYSTAL_40M             1
#define PLATFORM_CRYSTAL        CRYSTAL_40M

#if defined(CONFIG_BOARD) && (CONFIG_BOARD == PLATFORM_BOARD_32W515P_EVAL)
#define LOG_UART USART2
#else
#define LOG_UART USART1
#endif

#ifdef CONFIG_PLATFORM_FPGA
#define RFAD_SPI SPI0
#endif

#define TOTAL_SRAM_SIZE         (448 * 1024)

#define CONFIG_HW_SECURITY_ENGINE

#endif /* _PLATFORM_DEF_H */
