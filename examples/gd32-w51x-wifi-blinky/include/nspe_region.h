/*!
    \file    nspe_region.h
    \brief   NSPE region definition for GD32W51x WiFi SDK

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

#ifndef __NSPE_REGION_H__
#define __NSPE_REGION_H__

#include "platform_def.h"

#if defined(CONFIG_TZ_ENABLED)
#include "config_gdm32.h"
    #define SRAM_DATA_BASE_ADDR                  (RE_SRAM_BASE_NS + RE_NSPE_DATA_START)
    #define LR_IROM1_ADDR                        (RE_FLASH_BASE_NS + RE_IMG_0_NSPE_OFFSET + RE_VTOR_ALIGNMENT)
    #define LR_IROM1_SIZE                        (RE_IMG_1_PROT_OFFSET - RE_IMG_0_NSPE_OFFSET)
#else /* CONFIG_TZ_ENABLED */
#include "config_gdm32_ntz.h"
    #define SRAM_DATA_BASE_ADDR                  (RE_SRAM_BASE_NS + RE_NSPE_DATA_START)    /* skip rom variables(0x200) and mbl apis(0x40) */
    #if (RE_IMG_0_NSPE_OFFSET == 0)
        #define LR_IROM1_ADDR                    (RE_FLASH_BASE_NS + RE_IMG_0_NSPE_OFFSET)  /* skip mbl and system status */
    #else
        #define LR_IROM1_ADDR                    (RE_FLASH_BASE_NS + RE_IMG_0_NSPE_OFFSET + RE_VTOR_ALIGNMENT)  /* skip mbl and system status */
    #endif
    #define LR_IROM1_SIZE                        (RE_IMG_1_NSPE_OFFSET - RE_IMG_0_NSPE_OFFSET)
#endif /* CONFIG_TZ_ENABLED */
#define RW_IRAM1_ADDR                            (SRAM_DATA_BASE_ADDR)
#define RW_IRAM1_SIZE                            (0x00070000 - RE_NSPE_DATA_START)

#endif  //__NSPE_REGION_H__
