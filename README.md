# stm32-ssd1306

STM32 library for working with OLEDs based on SSD1306, supports I2C and 4-wire SPI.
It also works with SH1106, SH1107 and SSD1309 which are compatible with SSD1306.

A [detailed video-tutorial](https://www.youtube.com/watch?v=z1Px6emHIeg) is available on
[hacksOnTable](https://www.youtube.com/channel/UC4gg1OCwn1rjZ8SbRWt7d1g) YouTube-channel.
If you want to create a custom font, please read [Creating Custom Fonts](https://github.com/afiskon/stm32-ssd1306/tree/master/examples/custom-fonts).
For even more details please see `ssd1306/ssd1306_conf_template.h` and `examples` directory.

The code is based on
[4ilo/ssd1306-stm32HAL](https://github.com/4ilo/ssd1306-stm32HAL) library
developed by Olivier Van den Eede ( [@4ilo](https://github.com/4ilo) ) in 2016.

## Ports

There is a [DuyTrandeLion/nrf52-ssd1309](https://github.com/DuyTrandeLion/nrf52-ssd1309) port to nRF52 of this library made by [@DuyTrandeLion](https://github.com/DuyTrandeLion) in 2020.

There is also a [kirsche-ctrl/xmc2go-ssd1306](https://github.com/kirsche-ctrl/xmc2go-ssd1306) port to XMC made by [@kirsche-ctrl](https://github.com/kirsche-ctrl) in 2022.

## Other Libraries

For other displays there are separate libraries available:

* https://github.com/afiskon/stm32-i2c-lcd-1602
* https://github.com/afiskon/stm32-ssd1351
* https://github.com/afiskon/stm32-st7735
* https://github.com/afiskon/stm32-ili9341