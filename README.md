# stm32-ssd1306

STM32 library for working with OLED LCDs based on SSD1306, supports I2C and
4-wire SPI.

Tested on STM32F1 and STM32F4 MCUs, with 4 random LCDs from eBay. Probably will
work with other MCUs and LCDs based on SH1106 or SSD1309.

Please see `examples` directory and `ssd1306/ssd1306.h` for more details.

The code is based on
[4ilo/ssd1306-stm32HAL](https://github.com/4ilo/ssd1306-stm32HAL) library
developed by Olivier Van den Eede ( [@4ilo](https://github.com/4ilo) ) in 2016.

![stm32-ssd1306 library usage example](https://eax.me/files/2018/04/stm32-ssd1306-lcd.jpg)
