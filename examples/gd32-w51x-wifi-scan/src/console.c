#include "wrapper_os.h"
#include "debug_print.h"
#include "console.h"

// BSP code references this task in the UART RX interrupts.
// we don't use UART RX in in this demo, so we just need to define this 
// symbol but not do anything with it.
os_task_t console_task_tcb;