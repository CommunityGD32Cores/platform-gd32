/*!
    \file    app_cfg.h
    \brief   application configuration for GD32W51x WiFi SDK

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

#ifndef _APP_CFG_H
#define _APP_CFG_H

/* Console Related */
#define CONFIG_CONSOLE_ENABLE
#ifdef CONFIG_CONSOLE_ENABLE
// #define CONFIG_INTERNAL_DEBUG
// #define CONFIG_RF_TEST_SUPPORT
#define CONFIG_BASECMD
//#define CONFIG_ATCMD
#endif

#define CONFIG_IPERF_TEST

#define CONFIG_EXTEND_MEMORY

#define CONFIG_JOIN_GROUP_SUPPORT

// #define CONFIG_SOFTAP_CALLBACK_ENABLED

// #define CONFIG_TELNET_SERVER
// #define CONFIG_WIFI_HIGH_PERFORMANCE

// #define CONFIG_SSL_TEST

// #define CONFIG_AIRKISS_SUPPORT
// #define CONFIG_GAGENT_TEST

// #define CONFIG_FATFS_SUPPORT

// #define CONFIG_IPV6_SUPPORT

#define USE_MBL_API

// #define CONFIG_ALICLOUD_SUPPORT
#if defined(CONFIG_ALICLOUD_SUPPORT) && !defined(CONFIG_EXTEND_MEMORY)
#error CONFIG_ALICLOUD_SUPPORT and CONFIG_EXTEND_MEMORY should enabled at the same time
#endif

#define START_TASK_STK_SIZE                    1024
#define START_TASK_PRIO                        (TASK_PRIO_APP_BASE + TASK_PRIO_HIGHER(4))

#define WIFI_ROAMING_TASK_STK_SIZE             256
#define WIFI_ROAMING_TASK_PRIO                 TASK_PRIO_APP_BASE
#define WIFI_ROAMING_QUEUE_SIZE                4

#define TCP_TEST_STACK_SIZE                    256  // 128
#define TCP_TEST_SERVER_PRIO                   TASK_PRIO_APP_BASE
#define TCP_TEST_CLIENT_PRIO                   TASK_PRIO_APP_BASE

#define UDP_TEST_STACK_SIZE                    256  // 128
#define UDP_TEST_SERVER_PRIO                   TASK_PRIO_APP_BASE
#define UDP_TEST_CLIENT_PRIO                   TASK_PRIO_APP_BASE


#ifdef CONFIG_JOIN_GROUP_SUPPORT
#define JOIN_GROUP_STACK_SIZE                  256
#define JOIN_GROUP_TASK_PRIO                   TASK_PRIO_APP_BASE
#endif

#ifdef CONFIG_SSL_TEST
#define SSL_CLIENT_TASK_STK_SIZE               2048  /* 3072 */
#define SSL_CLIENT_TASK_PRIO                   (TASK_PRIO_APP_BASE + TASK_PRIO_LOWER(1))
#endif

#ifdef CONFIG_TELNET_SERVER
#define TELNET_TASK_PRIO                       (TASK_PRIO_APP_BASE + TASK_PRIO_LOWER(1))
#endif

#ifdef CONFIG_AIRKISS_SUPPORT
#define AIRKISS_FINISH_STACK_SIZE              512
#define AIRKISS_FINISH_TASK_PRIO               TASK_PRIO_APP_BASE
#endif
#ifdef CONFIG_GAGENT_TEST
#define GAGENT_STACK_SIZE                      1024
#define GAGENT_TASK_PRIO                       TASK_PRIO_APP_BASE
#endif
#ifdef CONFIG_ALICLOUD_SUPPORT
#define ALICLOUD_STACK_SIZE                    2048
#define ALICLOUD_TASK_PRIO                     TASK_PRIO_APP_BASE
#endif

#ifdef CONFIG_IPERF_TEST
#define IPERF_TASK_MAX                         1
#ifdef CONFIG_PRINT_IN_SEQUENCE
#define IPERF_STACK_SIZE                       1024
#else
#define IPERF_STACK_SIZE                       512
#endif
#define IPERF_TASK_PRIO                        TASK_PRIO_APP_BASE
#endif

#include "platform_def.h"

#endif
