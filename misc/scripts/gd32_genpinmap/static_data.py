# dump site for static string data
# mostly headers. keeps the code tidy.

gigadevice_header = """/*
    Copyright (c) 2020, GigaDevice Semiconductor Inc.

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

"""

spl_family_b_peripheral_pins_c_header = """#include "PeripheralPins.h"
#include "gd32xxyy.h"

/*  void pin_function(PinName pin, int function);
    configure the speed, mode,and remap function of pins
    the parameter function contains the configuration information,show as below
    bit 0:2   gpio mode
    bit 3:8   remap
    bit 9:10  gpio speed
    bit 11:15 adc  /timer channel
*/
const int GD_GPIO_PULL_UP_DOWN[] = {
    GPIO_PUPD_NONE,             /* 0 */
    GPIO_PUPD_PULLUP,           /* 1 */
    GPIO_PUPD_PULLDOWN,         /* 2 */
};

const int GD_GPIO_OUTPUT_MODE[] = {
    GPIO_OTYPE_PP,             /* 0 */
    GPIO_OTYPE_OD,             /* 1 */
};

const int GD_GPIO_AF[] = {
    GPIO_AF_0,             /* 0 */
    GPIO_AF_1,             /* 1 */
    GPIO_AF_2,             /* 2 */
    GPIO_AF_3,             /* 3 */
    GPIO_AF_4,             /* 4 */
    GPIO_AF_5,             /* 5 */
    GPIO_AF_6,             /* 6 */
    GPIO_AF_7,             /* 7 */
#if !defined(GD32F330) /* not available on GD32F330 */
    GPIO_AF_9,             /* 8 */
    GPIO_AF_11             /* 9 */
#endif
};

/* pin descriptions only reference the index in the array, so
 * to get e.g. AF11 one must give it index = 9. provide 
 * convenience macros here.
 * for all other arrays, the value is also equivalent to the index,
 * so there doesn't need to be anything done more.
 */
#define IND_GPIO_AF_0 0
#define IND_GPIO_AF_1 1
#define IND_GPIO_AF_2 2
#define IND_GPIO_AF_3 3
#define IND_GPIO_AF_4 4
#define IND_GPIO_AF_5 5
#define IND_GPIO_AF_6 6
#define IND_GPIO_AF_7 7
#define IND_GPIO_AF_9 8
#define IND_GPIO_AF_11 9

/* GPIO MODE */
const int GD_GPIO_MODE[] = {
    GPIO_MODE_INPUT,             /* 0 */
    GPIO_MODE_OUTPUT,            /* 1 */
    GPIO_MODE_AF,                /* 2 */
    GPIO_MODE_ANALOG,            /* 3 */
};

/* GPIO SPEED */
const int GD_GPIO_SPEED[] = {
    GPIO_OSPEED_2MHZ,             /* 0 */
    GPIO_OSPEED_10MHZ,            /* 1 */
    0,                            /* 2 (unused) */
    GPIO_OSPEED_50MHZ,            /* 3 */
};

"""

community_copyright_header = """/*
    Copyright (c) 2021, CommunityGD32Cores

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

"""

peripheralnames_h_header_start = """#ifndef PERIPHERALNAMES_H
#define PERIPHERALNAMES_H

#include "gd32xxyy.h"

#ifdef __cplusplus
extern "C" {
#endif

"""

peripheralnames_h_header_end = """
#ifdef __cplusplus
}
#endif

#endif
"""

pinnamesvar_h_empty_header = """#ifndef _PINNAMESVAR_H_
#define _PINNAMESVAR_H_

#endif /* _PINNAMESVAR_H_ */"""

variant_h_header_start = """#ifndef _VARIANT_
#define _VARIANT_

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

/* GPIO pins definitions */
"""

variant_h_header_end = """#ifdef __cplusplus
} // extern "C"
#endif

#ifdef __cplusplus
    /* Port which normally prints to the Arduino Serial Monitor */
    #define SERIAL_PORT_MONITOR     Serial
    /* Hardware serial port, physical RX & TX pins. */
    #define SERIAL_PORT_HARDWARE    Serial1
#endif

#endif /* _VARIANT_ */
"""

variant_cpp_start = """#include "pins_arduino.h"

#ifdef __cplusplus
extern "C" {
#endif

/* digital pins for pinmap list */
const PinName digital_pins[] = {
"""

variant_cpp_end = """#ifdef __cplusplus
}
#endif
"""