/*!
    \file    console.c
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

#include "wrapper_os.h"
#include "debug_print.h"
#include "console.h"

/*============================ INCLUDES ======================================*/
/*============================ MACROS ========================================*/
/*============================ MACRO FUNCTIONS ===============================*/
/*============================ TYPES =========================================*/
/*============================ GLOBAL VARIABLES ==============================*/
os_task_t console_task_tcb;
uint32_t console_task_stk[CONSOLE_TASK_STK_SIZE] __ALIGNED(8);
/*============================ LOCAL VARIABLES ===============================*/
/*============================ PROTOTYPES ====================================*/
/*============================ IMPLEMENTATION ================================*/

/*!
    \brief      initialize console
    \param[in]  none
    \param[out] none
    \retval     none
*/
void console_init(void)
{
    void *handle;

    handle = sys_task_create(&console_task_tcb, (const uint8_t *)"console", &console_task_stk[0],
                    CONSOLE_TASK_STK_SIZE, CONSOLE_TASK_QUEUE_SIZE, CONSOLE_TASK_PRIO,
                    (task_func_t)console_task, NULL);
    if (handle == NULL) {
        DEBUGPRINT("create console task failed\r\n");
    }
}

/*!
    \brief      start console task
    \param[in]  p_arg: the pointer of parameters
    \param[out] none
    \retval     none
*/
void console_task(void *p_arg)
{
    uint32_t cycle_cnt = 0;

    DEBUGPRINT("\r\n# ");

    for (;;) {
        command_handler();
        sys_ms_sleep(10000);
        cycle_cnt++;
        if (cycle_cnt >= 1000) {
            break;
        }
    }

    sys_task_delete(NULL);
}
