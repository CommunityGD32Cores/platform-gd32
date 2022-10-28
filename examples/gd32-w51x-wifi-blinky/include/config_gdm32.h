/*!
    \file    config_gdm32.h
    \brief   Configuration file for GD32W51x WiFi SDK

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

/* REGION DEFINE */
#define RE_FLASH_BASE_S       0x0C000000    /* !Keep unchanged! */
#define RE_FLASH_BASE_NS      0x08000000    /* !Keep unchanged! */
#define RE_SRAM_BASE_S        0x30000000    /* !Keep unchanged! */
#define RE_SRAM_BASE_NS       0x20000000    /* !Keep unchanged! */

/* SRAM LAYOUT */
#define RE_SHARED_DATA_START  0x0200        /* !Keep unchanged! */
#define RE_MBL_DATA_START     0x0A00        /* !Keep unchanged! */
#define RE_PROT_DATA_START    0x0A20
#define RE_AROT_DATA_START    0xE000
#define RE_NSPE_DATA_START    0xE000  // 0x4B00

/* FLASH LAYEROUT */
#define RE_VTOR_ALIGNMENT     0x200         /* !Keep unchanged! */
#define RE_SYS_SET_OFFSET     0x0           /* !Keep unchanged! */
#define RE_MBL_OFFSET         0x1000        /* !Keep unchanged! */
#define RE_SYS_STATUS_OFFSET  0x8000
#define RE_IMG_0_PROT_OFFSET  0xA000
#define RE_IMG_0_AROT_OFFSET  0x3A000
#define RE_IMG_0_NSPE_OFFSET  0x3A000  // 0xA000
#define RE_IMG_1_PROT_OFFSET  0xF0000
#define RE_IMG_1_AROT_OFFSET  0x120000
#define RE_IMG_1_NSPE_OFFSET  0x120000  // 0x100000
#define RE_IMG_1_END_OFFSET   0x1D6000
#define RE_SST_OFFSET         0x1F5000
#define RE_AUDIT_OFFSET       0x1FF000

/* FW_VERSION */
#define RE_MBL_VERSION        0x01000002
#define RE_PROT_VERSION       0x01000002
#define RE_AROT_VERSION       0x00000002
#define RE_NSPE_VERSION       0x01000002
