/*!
    \file    app_type.h
    \brief   application type definition for GD32W51x WiFi SDK

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

#ifndef _APP_TYPE_H
#define _APP_TYPE_H

/*============================ INCLUDES ======================================*/
#include <stdint.h>

/*============================ TYPES =========================================*/
//typedef int32_t int32_t;
//typedef int16_t s16;
//typedef int8_t int8_t;

// typedef const int32_t sc32;  /*!< Read Only */
// typedef const int16_t sc16;  /*!< Read Only */
// typedef const int8_t sc8;   /*!< Read Only */

// typedef volatile int32_t  vs32;
// typedef volatile int16_t  vs16;
// typedef volatile int8_t   vs8;

// typedef volatile const int32_t vsc32;  /*!< Read Only */
// typedef volatile const int16_t vsc16;  /*!< Read Only */
// typedef volatile const int8_t vsc8;   /*!< Read Only */

//typedef uint32_t uint32_t;
//typedef uint16_t uint16_t;
//typedef uint8_t  uint8_t;

/*============================ MACROS ========================================*/
#ifndef __PACKED
#if defined(__CC_ARM)
    #define __PACKED           __attribute__ ((packed))
#elif defined(__ICCARM__)
    #define __PACKED           __attribute__((packed, aligned(1)))
#elif defined(__ARMCC_VERSION) && (__ARMCC_VERSION >= 6010050)
    #define __PACKED           __attribute__((packed, aligned(1)))
#elif defined ( __GNUC__ )
    #define __PACKED            __attribute__((packed, aligned(1))) // __attribute__ ((__packed__))
#endif
#endif

#ifndef __INLINE
#if defined(__CC_ARM)
    #define __INLINE         __inline
#elif defined(__ICCARM__)
    #define __INLINE         inline
#elif defined(__ARMCC_VERSION) && (__ARMCC_VERSION >= 6010050)
    #define __INLINE         __inline
#elif defined ( __GNUC__ )
    #define __INLINE         __inline
#endif
#endif

#ifndef __WEAK
#if defined(__CC_ARM)
    #define __WEAK         __attribute__((weak))
#elif defined(__ICCARM__)
    #define __WEAK         __weak
#elif defined(__ARMCC_VERSION) && (__ARMCC_VERSION >= 6010050)
    #define __WEAK          __attribute__((weak))
#elif defined ( __GNUC__ )
    #define __WEAK         __attribute__((weak))
#endif
#endif

#ifndef __AT
#if defined(__CC_ARM)
    #define __AT(addr) __attribute__((at(addr)))
#elif defined(__ICCARM__)
    #define __AT(addr) @(addr)
#elif defined(__ARMCC_VERSION) && (__ARMCC_VERSION >= 6010050)
    /* unknown attribute 'at', not find the alternative yet, so use sct file to specify address */
    #define __AT(addr)
#elif defined ( __GNUC__ )
    #define __AT(addr) __attribute__((at(addr)))
#endif
#endif

#ifndef SECTION
#if defined(__CC_ARM) || defined (__ARMCC_VERSION)
    #define SECTION(x) __attribute__((section(x)))
    /* Not used now since One ELF Section per Function used */
    #define SECTION_RAM_CODE
#elif defined(__ICCARM__)
    #define SECTION(x)                  @x
    // #define STRINGIFY(s) #s
    // #define SECTION(x) _Pragma(STRINGIFY(location = x))
    #define SECTION_RAM_CODE            SECTION(".ram_code")
#elif defined(__GNUC__)
    #define SECTION_RAM_CODE
    #define SECTION(x) __attribute__((section(x)))
#endif
#endif

/* Todo: aligned attribute for IAR */
#ifndef   __ALIGNED
#define __ALIGNED(x)                           __attribute__((aligned(x)))
#endif

/*============================ MACRO FUNCTIONS ===============================*/
#ifndef ARRAY_SIZE
#define ARRAY_SIZE(arr)     (sizeof(arr)/sizeof(arr[0]))
#endif

#define COMPILE_TIME_ASSERT(constant_expr)\
do {                                      \
    switch(0) {                           \
        case 0:                           \
        case constant_expr:               \
        ;                                 \
    }                                     \
} while(0)

#if 0//ndef isprint
#define in_range(c, lo, up)  ((uint8_t)c >= lo && (uint8_t)c <= up)
#define isprint(c)           in_range(c, 0x20, 0x7f)
#define isdigit(c)           in_range(c, '0', '9')
#define isxdigit(c)          (isdigit(c) || in_range(c, 'a', 'f') || in_range(c, 'A', 'F'))
#define islower(c)           in_range(c, 'a', 'z')
#define isspace(c)           (c == ' ' || c == '\f' || c == '\n' || c == '\r' || c == '\t' || c == '\v')
#endif

/*============================ GLOBAL VARIABLES ==============================*/
/*============================ LOCAL VARIABLES ===============================*/
/*============================ PROTOTYPES ====================================*/

#endif
