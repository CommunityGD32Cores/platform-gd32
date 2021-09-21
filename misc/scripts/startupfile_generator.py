#!/usr/bin/env python3
import os
from typing import Tuple, List
import shutil
import re
from pathlib import Path

def get_file_contents(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def write_file_contents(filepath, contents):
    with open(filepath, 'wb') as f:
        f.write(contents.encode('utf-8'))

def get_isr_table(startupfile):
    isr_regex = r"DCD[\s]+([\S]+)[\s]+;([0-9A-Za-z :]+)"
    res = re.findall(isr_regex, startupfile)
    # supress first entry (which is "Top of Stack") -- is already in template
    return res[1::]

def transform_to_gcc_isr_table(isr_table):
    transformed_table = []
    for func, comment in isr_table:
        transformed_table += [f'                .word     {func}\t\t/*{comment} */\n']
    return transformed_table

def generate_header(cpu_type):
    # startup file which initializes BSS and DATA segment, works with Cortex-M3, M4, M23 and M33
    header = """  .syntax unified
  .cpu cortex-m4
  .fpu softvfp
  .thumb
  
.global  g_pfnVectors
.global  Default_Handler

/* start address for the initialization values of the .data section.
defined in linker script */
.word _sidata
/* start address for the .data section. defined in linker script */
.word _sdata
/* end address for the .data section. defined in linker script */
.word _edata
/* start address for the .bss section. defined in linker script */
.word _sbss
/* end address for the .bss section. defined in linker script */
.word _ebss

.section  .text.Reset_Handler
  .weak  Reset_Handler
  .type  Reset_Handler, %function
Reset_Handler:  

/* Copy the data segment initializers from flash to SRAM */  
  movs  r1, #0
  b  LoopCopyDataInit

CopyDataInit:
  ldr  r3, =_sidata
  ldr  r3, [r3, r1]
  str  r3, [r0, r1]
  adds  r1, r1, #4
    
LoopCopyDataInit:
  ldr  r0, =_sdata
  ldr  r3, =_edata
  adds  r2, r0, r1
  cmp  r2, r3
  bcc  CopyDataInit
  ldr  r2, =_sbss
  b  LoopFillZerobss
/* Zero fill the bss segment. */  
FillZerobss:
  movs  r3, #0
  str  r3, [r2]
  adds r2, r2, #4
    
LoopFillZerobss:
  ldr  r3, = _ebss
  cmp  r2, r3
  bcc  FillZerobss

/* Call the clock system initialization function.*/
  bl  SystemInit   
/* Call into static constructors (C++) */
  bl __libc_init_array
/* Call the application's entry point.*/
  bl  main
  bx  lr    
.size  Reset_Handler, .-Reset_Handler

/**
 * @brief  This is the code that gets called when the processor receives an 
 *         unexpected interrupt.  This simply enters an infinite loop, preserving
 *         the system state for examination by a debugger.
 * @param  None     
 * @retval None       
*/
    .section  .text.Default_Handler,"ax",%progbits
Default_Handler:
Infinite_Loop:
  b  Infinite_Loop
  .size  Default_Handler, .-Default_Handler
/******************************************************************************
*
* The minimal vector table for a Cortex M4. Note that the proper constructs
* must be placed on this to ensure that it ends up at physical address
* 0x0000.0000.
* 
*******************************************************************************/
   .section  .isr_vector,"a",%progbits
  .type  g_pfnVectors, %object
  .size  g_pfnVectors, .-g_pfnVectors

g_pfnVectors:
                .word     _estack                            /* Top of Stack */
"""
    header = header.replace("cortex-m4", cpu_type)
    return header

def get_after_isr_table_text():
    return """
/*******************************************************************************
*
* Provide weak aliases for each Exception handler to the Default_Handler. 
* As they are weak aliases, any function with the same name will override 
* this definition.
*
*******************************************************************************/
"""

def generate_default_handlers(isr_table):
    default_handlers = ""
    for i in range(len(isr_table)):
        funcname, _ = isr_table[i]
        if funcname not in ["0", "Reset_Handler", "__initial_sp"]:
            default_handlers += f".weak {funcname}\n.thumb_set {funcname},Default_Handler\n\n"
    return default_handlers

def autodetect_cpu_type(filename):
    filename = Path(filename).stem
    # unique identifiers by which we can see to which CPU type this file belongs.
    filename_to_cpu = {
        "gd32e10x": "cortex-m3",  # GD32E10x_Firmware_Library_V1.2.1
        "gd32e23x": "cortex-m23", # GD32E23x_Firmware_Library_V1.1.1
        "gd32f1x0": "cortex-m3",  # GD32F1x0_Firmware_Library_V3.3.2
        "gd32f3x0": "cortex-m4",  # GD32F3x0_Firmware_Library_V2.1.2
        "gd32f4" : "cortex-m4",   # covers gd32f{405,407, 450} from GD32F4xx_Firmware_Library_V2.1.3
                                  # and gd32f403 from GD32F403_Firmware_Library_V2.1.2,
        "gd32f10x": "cortex-m3",  # GD32F10x_Firmware_Library_V2.2.1
        "gd32f20x": "cortex-m3",  # GD32F20x_Firmware_Library_V2.2.1
        "gd32f30x": "cortex-m4",  # GD32F30x_Firmware_Library_V2.1.2
        "gd32e50x": "cortex-m33", # GD32E50x_Firmware_Library_V1.2.1
        "gd32e508": "cortex-m33",
        "gd32eprt": "cortex-m33"
    }
    for key in filename_to_cpu.keys():
        print("checking against " + str(key))
        if key in filename:
            return filename_to_cpu[key]
    raise Exception("Could not identify CPU type from filename " + str(filename))

def convert_arm_to_gcc_startup(src_file, output_file):
    src_file_content = get_file_contents(src_file)
    isr_table = get_isr_table(src_file_content)
    #for entry in isr_table:
    #    print(isr_table)
    transformed_table = transform_to_gcc_isr_table(isr_table)
    #print("".join(transformed_table))
    cpu_type = autodetect_cpu_type(src_file)
    #print(cpu_type)
    header = generate_header(cpu_type)
    #print(header)
    default_handlers = generate_default_handlers(isr_table)
    #print(default_handlers)

    full_startup_file = header + "".join(transformed_table) + get_after_isr_table_text() + default_handlers
    print("==== FULL STARTUP FILE for %s ====" % src_file)
    print(full_startup_file)
    print("=== END OF FULL STARTUP FILE %s === " % output_file)

    write_file_contents(output_file, full_startup_file)

def main():
    this_script_path = os.path.dirname(os.path.realpath(__file__))
    outpath_folder = os.path.join(this_script_path, "startup_files_converted")
    inpath_folder = os.path.join(this_script_path, "startup_files")
    if os.path.exists(outpath_folder):
        shutil.rmtree(outpath_folder)
    os.mkdir(outpath_folder)
    cnt = 0
    print("Converting all startup files in %s to GCC compatible assembler." % (inpath_folder))    
    for root, dirs, files in os.walk(inpath_folder):
        for src_file in files:
            src_file = os.path.join(inpath_folder, src_file)
            out_file =  os.path.join(outpath_folder, Path(src_file).stem + ".S")
            convert_arm_to_gcc_startup(src_file, out_file)
            cnt += 1
    print("Done, wrote %d startup files to %s." % (cnt, outpath_folder))

if __name__ == '__main__':
    main()
