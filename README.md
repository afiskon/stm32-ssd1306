# stm32-ssd1306

STM32 library for working with OLEDs based on SSD1306, supports I2C and 4-wire SPI.
It also works with SH1106, SH1107 and SSD1309 which are compatible with SSD1306.

Please see `ssd1306/ssd1306_conf_template.h` and `examples` directory for more details.

Please see [`DMA_how_to_do_and_benchmark.md`](./DMA_how_to_and_benchmark.md) for details about how to enable DMA and benchmark about DMA.

See also:

* https://github.com/afiskon/stm32-i2c-lcd-1602
* https://github.com/afiskon/stm32-ssd1351
* https://github.com/afiskon/stm32-st7735
* https://github.com/afiskon/stm32-ili9341

The code is based on
[4ilo/ssd1306-stm32HAL](https://github.com/4ilo/ssd1306-stm32HAL) library
developed by Olivier Van den Eede ( [@4ilo](https://github.com/4ilo) ) in 2016.

There is a [DuyTrandeLion/nrf52-ssd1309](https://github.com/DuyTrandeLion/nrf52-ssd1309) port to nRF52 of this library made by [@DuyTrandeLion](https://github.com/DuyTrandeLion) in 2020.

