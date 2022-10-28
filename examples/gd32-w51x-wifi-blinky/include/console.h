/*!
    \file    console.h
    \brief   Command console for GD32W51x WiFi SDK

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

#ifndef _CONSOLE_H_
#define _CONSOLE_H_

/*============================ INCLUDES ======================================*/
#include "wrapper_os.h"
/*============================ MACROS ========================================*/
#define CONSOLE_TASK_STK_SIZE                  512
#define CONSOLE_TASK_QUEUE_SIZE                4
#define CONSOLE_TASK_PRIO                      (TASK_PRIO_APP_BASE + TASK_PRIO_HIGHER(3))
/*============================ MACRO FUNCTIONS ===============================*/
/*============================ TYPES =========================================*/
/*============================ GLOBAL VARIABLES ==============================*/
extern os_task_t console_task_tcb;
extern uint32_t console_task_stk[CONSOLE_TASK_STK_SIZE] __ALIGNED(8);
/*============================ LOCAL VARIABLES ===============================*/
/*============================ PROTOTYPES ====================================*/
void console_init(void);
void console_task(void *p_arg);
extern void command_handler(void);
/*============================ IMPLEMENTATION ================================*/

#endif  // _CONSOLE_H_
