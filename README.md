# GD32 Platform

## Description

PlatformIO platform implementation for GD32F, GD32E, GD32W and GD32C type chips. Work in progress.

## Supported boards

See [boards](https://github.com/CommunityGD32Cores/platform-gd32/tree/main/boards) folder.

* GD32L23x (Cortex-M23)
* GD32C10x (Cortex-M4)
* GD32W51x (Cortex-M33)
* GD32E10x (Cortex-M4)
* GD32E23x (Cortex-M23)
* GD32E50x (Cortex-M33)
* GD32F10x (Cortex-M4)
* GD32F1x0 (Cortex-M3)
* GD32F20x (Cortex-M3)
* GD32F30x (Cortex-M4)
* GD32F3x0 (Cortex-M4)
* GD32F4xx (Cortex-M4)
* GD32F403 (Cortex-M4)

All ARM-based GD32 microcontrollers are supported through `genericGD32...` board definitions. Further, many GD32 development boards made by Gigadevice or other vendors are supports.

## How to use

See example projects at https://github.com/CommunityGD32Cores/gd32-pio-projects. 

The platform can be installed manually using `pio platform install https://github.com/CommunityGD32Cores/platform-gd32.git` on [the CLI](https://docs.platformio.org/en/latest/integration/ide/vscode.html#platformio-core-cli). This is done automatically when compiling one of the example projects. 
