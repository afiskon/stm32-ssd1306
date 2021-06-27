# How to correctly enable DMA in STM32CubeMX

## 1 Enable I2C event interrupt or SPI global interrupt

Otherwise hard fault interrupt will occur.

### 1.1 I2C

<img src="./pictures/enable I2C event interrupt.png" />
### 1.2 SPI

<img src="./pictures/enable SPI global interrupt.png" />

## 2 Ensure the interrupts' priority is high enough

The ISR (interrupt service routine) of DMA and I2C or SPI can unlock I2C or SPI hardware, so that I2C or SPI hardware can process the next transmit after the current transmit is completed. So you must ensure that those ISRs above can always be executed.

For example, assume that `ssd1306_UpdateScreen()` can trigger DMA's ISR `DMA1_Channel6_IRQHandler()` and I2C's ISR `I2C1_EV_IRQHandler()`.
If `ssd1306_UpdateScreen()` is called in another ISR, perhaps EXTI's ISR `EXTI0_IRQHandler()`,  then you must ensure that both DMA's and I2C's interrupts has higher priority than EXTI line0's.
Smaller number means higher priority.

<img src="./pictures/interrupt priority.png" />

# FPS benchmark

All tests is done with a STM32F103C8T6@72 MHz with I2C@400 kHz and SPI@18 MHz, and OLED12864, using `ssd1306_TestFPS()`.
|Condition|FPS|
| -------------------- | ------------------------------------------------------------ |
| DMA off, I2C@400 kHz | 36 FPS <img src="./pictures/I2C no DMA.jpg" style="zoom:50%;" /> |
| DMA on, I2C@400 kHz  | 38 FPS <img src="./pictures/I2C DMA.jpg" style="zoom:50%;" /> |
| DMA off, SPI@18 MHz  | 439 FPS <img src="./pictures/SPI no DMA.jpg" style="zoom:50%;" /> |
| DMA on, SPI@18 MHz   | 459 FPS <img src="./pictures/SPI DMA.jpg" style="zoom:50%;" /> |

