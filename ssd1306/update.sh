#!/bin/sh

set -e

rm *.h
rm *.c

wget https://raw.githubusercontent.com/4ilo/ssd1306-stm32HAL/master/Inc/ssd1306.h
wget https://raw.githubusercontent.com/4ilo/ssd1306-stm32HAL/master/Inc/fonts.h
wget https://raw.githubusercontent.com/4ilo/ssd1306-stm32HAL/master/Src/ssd1306.c
wget https://raw.githubusercontent.com/4ilo/ssd1306-stm32HAL/master/Src/fonts.c
