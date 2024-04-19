# Bad Apple!! Demo

Touhou - Bad Apple!! ~3FPS animation demo.

Tested with BlackPill STM32F411CEU6 and CH1115 128X64.

## Requirements

- MCU with at least 512 KB Flash memory
- 128x64 OLED display
- ARM GNU Toolchain
- make
- STM32F4 HAL
- Linker script and startup assembler

## Build

Feel free to edit `Makefile` for your configuration
(I2C/SPI port, resolution, etc.).

**I2C:**

```bash
make i2c
```

**SPI:**

```bash
make spi
```

## Disclaimer

The rights to the graphic materials used belong to
[Alstroemeria Records](https://youtu.be/i41KoE0iMYU?si=yKNadXjtwOtBxE6J).
