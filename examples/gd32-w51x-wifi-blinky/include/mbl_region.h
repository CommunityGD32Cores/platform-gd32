/*!
    \file    mbl_region.h
    \brief   MBL region definition for GD32W51x WiFi SDK

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

#ifndef __MBL_REGION_H__
#define __MBL_REGION_H__

#if defined (__ARM_FEATURE_CMSE) && (__ARM_FEATURE_CMSE == 3U)
#if defined(PLATFORM_MSP_AN521)
#include "config_an521.h"
#elif defined(PLATFORM_GDM32)
#include "config_gdm32.h"
#endif

/* MBL: code and ro data */
#define MBL_BASE_ADDRESS                 (RE_FLASH_BASE_S + RE_MBL_OFFSET + RE_VTOR_ALIGNMENT)
#define MBL_CODE_START                   MBL_BASE_ADDRESS
#define MBL_CODE_SIZE                    (28 * 1024 - RE_VTOR_ALIGNMENT)   /* 28 KB */

/* SRAM: shared SRAM, store initial boot state */
#define MBL_SHARED_DATA_START            (RE_SRAM_BASE_S + RE_SHARED_DATA_START)  // the same as IBL_SHARED_DATA_START
#define MBL_SHARED_DATA_SIZE             (RE_MBL_DATA_START - RE_SHARED_DATA_START)

/* SRAM: STACK, HEAP and other Global varaiables */
#define MBL_DATA_START                   (RE_SRAM_BASE_S + RE_MBL_DATA_START)  /* skip rom variables and shared data */
#define MBL_BUF_SIZE                     0x3000
#define MBL_MSP_STACK_SIZE               0x400
#else  /* __ARM_FEATURE_CMSE */
#include "config_gdm32_ntz.h"

/* MBL: code and ro data */
#define MBL_BASE_ADDRESS                 RE_FLASH_BASE_NS
#define MBL_CODE_START                   MBL_BASE_ADDRESS
#define MBL_CODE_SIZE                    (31 * 1024)   /* 31 KB */
#define MBL_API_START                    (MBL_BASE_ADDRESS + 31 * 1024)
#define MBL_API_SIZE                     (256)          /* unit: byte, skip lock word */

/* SRAM: Global varaiables, STACK, HEAP*/
#define MBL_DATA_START                    (RE_SRAM_BASE_NS + RE_MBL_DATA_START)  /* skip rom variables */
#define MBL_MSP_STACK_SIZE                0x1000

#endif  /* __ARM_FEATURE_CMSE */

#endif  // __MBL_REGION_H__
