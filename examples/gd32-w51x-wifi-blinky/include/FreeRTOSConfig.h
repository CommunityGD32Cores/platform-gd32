/*
    FreeRTOS V7.3.0 - Copyright (C) 2012 Real Time Engineers Ltd.

    FEATURES AND PORTS ARE ADDED TO FREERTOS ALL THE TIME.  PLEASE VISIT
    http://www.FreeRTOS.org TO ENSURE YOU ARE USING THE LATEST VERSION.

    ***************************************************************************
     *                                                                       *
     *    FreeRTOS tutorial books are available in pdf and paperback.        *
     *    Complete, revised, and edited pdf reference manuals are also       *
     *    available.                                                         *
     *                                                                       *
     *    Purchasing FreeRTOS documentation will not only help you, by       *
     *    ensuring you get running as quickly as possible and with an        *
     *    in-depth knowledge of how to use FreeRTOS, it will also help       *
     *    the FreeRTOS project to continue with its mission of providing     *
     *    professional grade, cross platform, de facto standard solutions    *
     *    for microcontrollers - completely free of charge!                  *
     *                                                                       *
     *    >>> See http://www.FreeRTOS.org/Documentation for details. <<<     *
     *                                                                       *
     *    Thank you for using FreeRTOS, and thank you for your support!      *
     *                                                                       *
    ***************************************************************************


    This file is part of the FreeRTOS distribution.

    FreeRTOS is free software; you can redistribute it and/or modify it under
    the terms of the GNU General Public License (version 2) as published by the
    Free Software Foundation AND MODIFIED BY the FreeRTOS exception.
    >>>NOTE<<< The modification to the GPL is included to allow you to
    distribute a combined work that includes FreeRTOS without being obliged to
    provide the source code for proprietary components outside of the FreeRTOS
    kernel.  FreeRTOS is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
    more details. You should have received a copy of the GNU General Public
    License and the FreeRTOS license exception along with FreeRTOS; if not it
    can be viewed here: http://www.freertos.org/a00114.html and also obtained
    by writing to Richard Barry, contact details for whom are available on the
    FreeRTOS WEB site.

    1 tab == 4 spaces!

    ***************************************************************************
     *                                                                       *
     *    Having a problem?  Start by reading the FAQ "My application does   *
     *    not run, what could be wrong?"                                     *
     *                                                                       *
     *    http://www.FreeRTOS.org/FAQHelp.html                               *
     *                                                                       *
    ***************************************************************************


    http://www.FreeRTOS.org - Documentation, training, latest versions, license
    and contact details.

    http://www.FreeRTOS.org/plus - A selection of FreeRTOS ecosystem products,
    including FreeRTOS+Trace - an indispensable productivity tool.

    Real Time Engineers ltd license FreeRTOS to High Integrity Systems, who sell
    the code with commercial support, indemnification, and middleware, under
    the OpenRTOS brand: http://www.OpenRTOS.com.  High Integrity Systems also
    provide a safety engineered and independently SIL3 certified version under
    the SafeRTOS brand: http://www.SafeRTOS.com.
*/

#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H

/* Use a guard to ensure the following few definitions are'nt included in
assembly files that include this header file. */
#if defined ( __CC_ARM ) || defined ( __ARMCC_VERSION ) || defined ( __ICCARM__ ) || defined ( __GNUC__ )
    #include <stdint.h>
    extern uint32_t SystemCoreClock;
#endif


/*-----------------------------------------------------------
 * Application specific definitions.
 *
 * These definitions should be adjusted for your particular hardware and
 * application requirements.
 *
 * THESE PARAMETERS ARE DESCRIBED WITHIN THE 'CONFIGURATION' SECTION OF THE
 * FreeRTOS API DOCUMENTATION AVAILABLE ON THE FreeRTOS.org WEB SITE.
 *
 * See http://www.freertos.org/a00110.html.
 *----------------------------------------------------------*/

#define configUSE_PREEMPTION			1
#define configUSE_IDLE_HOOK				1
#define configUSE_TICK_HOOK				0
#define configCPU_CLOCK_HZ				( SystemCoreClock )
#define configTICK_RATE_HZ				( ( uint32_t ) 1000 )
//#define configSYSTICK_CLOCK_HZ			32768
#define configMINIMAL_STACK_SIZE		( ( unsigned short ) 256 ) //( ( unsigned short ) 512 )
//#define configTOTAL_HEAP_SIZE			( ( size_t ) ( 80 * 1024 ) )
#define configMAX_TASK_NAME_LEN			( 16 )
#define configUSE_16_BIT_TICKS			0
#define configIDLE_SHOULD_YIELD			0
#define configUSE_CO_ROUTINES 			1
#define configUSE_MUTEXES				1
#define configUSE_TIMERS                		1

#define configSUPPORT_STATIC_ALLOCATION	1
#define configSUPPORT_DYNAMIC_ALLOCATION	1
#define configMAX_PRIORITIES				(56) //( 24 )

#define configMAX_CO_ROUTINE_PRIORITIES 	( 2 )

#define configUSE_COUNTING_SEMAPHORES 	1
#define configUSE_ALTERNATIVE_API 		0
#define configCHECK_FOR_STACK_OVERFLOW	2
#define configUSE_RECURSIVE_MUTEXES		1
#define configQUEUE_REGISTRY_SIZE		0
#define configGENERATE_RUN_TIME_STATS		1
#if configGENERATE_RUN_TIME_STATS
#define configUSE_STATS_FORMATTING_FUNCTIONS 1
#define portCONFIGURE_TIMER_FOR_RUN_TIME_STATS() //( ulHighFrequencyTimerTicks = 0UL )
#define portGET_RUN_TIME_COUNTER_VALUE() xTickCount //ulHighFrequencyTimerTicks
#define configUSE_TRACE_FACILITY			1
#define portCONFIGURE_STATS_PEROID_VALUE	1000 //unit Ticks
#endif

#define INCLUDE_xTaskGetHandle		1

#define configTIMER_TASK_PRIORITY       (20) //( 28 )
#define configTIMER_QUEUE_LENGTH        ( 10 )
#define configTIMER_TASK_STACK_DEPTH    (256) //( 512 )     //USE_MIN_STACK_SIZE modify from 512 to 256

#define configTIMER_MAX_BLOCK_TIME		1000

#define configENABLE_FPU				1
#define configENABLE_MPU				0
#define configENABLE_TRUSTZONE			0
#define configRECORD_STACK_HIGH_ADDRESS	1

#if (__IASMARM__ != 1)

extern void freertos_pre_sleep_processing(unsigned int *expected_idle_time);
extern void freertos_post_sleep_processing(unsigned int *expected_idle_time);
extern int  freertos_ready_to_sleep(void);

/* Enable tickless power saving. */
#define configUSE_TICKLESS_IDLE                 1

#define configEXPECTED_IDLE_TIME_BEFORE_SLEEP   5

#define configPRE_SLEEP_PROCESSING( x )         ( freertos_pre_sleep_processing((unsigned int *)&x) )
// #define configPRE_SLEEP_PROCESSING( x )

#define configPOST_SLEEP_PROCESSING( x )        ( freertos_post_sleep_processing((unsigned int *)&x) )
// #define configPOST_SLEEP_PROCESSING( x )

// #define freertos_ready_to_sleep()		(1)

#define traceLOW_POWER_IDLE_BEGIN();            do { \
                                                        if (!freertos_ready_to_sleep()) { \
                                                            mtCOVERAGE_TEST_MARKER(); \
                                                            break; \
                                                        }

                                                        // portSUPPRESS_TICKS_AND_SLEEP( xExpectedIdleTime );

#define traceLOW_POWER_IDLE_END();              } while (0);

/* It's FreeRTOS related feature but it's not included in FreeRTOS design. */
#define configUSE_WAKELOCK_PMU                  1

#endif // #if (__IASMARM__ != 1)

/* Set the following definitions to 1 to include the API function, or zero
to exclude the API function. */
#define INCLUDE_vTaskPrioritySet				1
#define INCLUDE_uxTaskPriorityGet				1
#define INCLUDE_vTaskDelete						1
#define INCLUDE_vTaskCleanUpResources			0
#define INCLUDE_vTaskSuspend					1
#define INCLUDE_vTaskDelayUntil					1
#define INCLUDE_vTaskDelay						1
#define INCLUDE_pcTaskGetTaskName				1
#define INCLUDE_xTimerPendFunctionCall			1
#define INCLUDE_uxTaskGetStackHighWaterMark		1
#define INCLUDE_xTaskGetCurrentTaskHandle		1
#define INCLUDE_xSemaphoreGetMutexHolder		1
#define INCLUDE_eTaskGetState					1
#define INCLUDE_xTaskGetSchedulerState			1

/* Cortex-M specific definitions. */
#ifdef __NVIC_PRIO_BITS
	/* __BVIC_PRIO_BITS will be specified when CMSIS is being used. */
	#define configPRIO_BITS       		__NVIC_PRIO_BITS
#else
	#define configPRIO_BITS       		4        /* 15 priority levels */
#endif


/* The lowest interrupt priority that can be used in a call to a "set priority"
function. */
#define configLIBRARY_LOWEST_INTERRUPT_PRIORITY			0x0f

/* The highest interrupt priority that can be used by any interrupt service
routine that makes calls to interrupt safe FreeRTOS API functions.  DO NOT CALL
INTERRUPT SAFE FREERTOS API FUNCTIONS FROM ANY INTERRUPT THAT HAS A HIGHER
PRIORITY THAN THIS! (higher priorities are lower numeric values. */
#define configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY	5


/* Interrupt priorities used by the kernel port layer itself.  These are generic
to all Cortex-M ports, and do not rely on any particular library functions. */
#define configKERNEL_INTERRUPT_PRIORITY 		( configLIBRARY_LOWEST_INTERRUPT_PRIORITY << (8 - configPRIO_BITS) )
/* !!!! configMAX_SYSCALL_INTERRUPT_PRIORITY must not be set to zero !!!!
See http://www.FreeRTOS.org/RTOS-Cortex-M3-M4.html. */
#define configMAX_SYSCALL_INTERRUPT_PRIORITY 	( configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY << (8 - configPRIO_BITS) )

#define configNUM_THREAD_LOCAL_STORAGE_POINTERS		1

/* map the FreeRTOS port interrupt handlers to CMSIS standard names */
#define vPortSVCHandler 		SVC_Handler
#define xPortPendSVHandler 	PendSV_Handler
#define xPortSysTickHandler 	SysTick_Handler

#endif /* FREERTOS_CONFIG_H */
