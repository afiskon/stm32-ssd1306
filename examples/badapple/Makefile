# Tools
CC=arm-none-eabi-gcc
LD=arm-none-eabi-gcc

# Code Paths
BUILD_DIR = build
SSD1306_DIR = ../../ssd1306
LDSCRIPT = STM32F411CEUx_FLASH.ld
STARTUP = startup_stm32f411xe.s

# SSD1306 flags
SSD1306_MCU = STM32F4
SSD1306_I2C = hi2c1
SSD1306_SPI = hspi1
SSD1306_FLAGS= -D${SSD1306_MCU}
SSD1306_FLAGS+= -DSSD1306_I2C_PORT=${SSD1306_I2C}
SSD1306_FLAGS+= -DSSD1306_SPI_PORT=${SSD1306_SPI}

# Sources
SRCS =  \
${STARTUP} \
src/main.c \
src/badapple.c \
src/system_stm32f4xx.c \
${SSD1306_DIR}/ssd1306.c
SRCS+=$(wildcard Drivers/STM32F4xx_HAL_Driver/Src/*.c)

# Objects
OBJS=$(patsubst %.c,%.o,$(patsubst %.s,%.o,$(SRCS)))
OBJECTS=$(addprefix $(BUILD_DIR)/,$(notdir $(OBJS)))
vpath %.c $(sort $(dir $(SRCS)))

# CPU
CPU = -mcpu=cortex-m4
FPU = 
FLOAT-ABI = 
MCU = $(CPU) -mthumb $(FPU) $(FLOAT-ABI)

# CMSIS
DEVICE = Drivers/CMSIS/Device/ST/STM32F4xx/Include
CORE = Drivers/CMSIS/Include

# HAL
HAL = Drivers/STM32F4xx_HAL_Driver/Inc

# Compilation Flags
LDFLAGS= -T${LDSCRIPT} ${MCU} --specs=nosys.specs -flto -Wl,--gc-sections -Wl,--print-memory-usage
CFLAGS= ${MCU} --specs=nosys.specs -fdata-sections -ffunction-sections -Og -g -gdwarf-2
CFLAGS+= -I$(DEVICE) -I$(CORE) -I${HAL} -I$(SSD1306_DIR) -Ibuild -Isrc
CFLAGS+= -DUSE_HAL_DRIVER -DSTM32F411xE
CFLAGS+= $(SSD1306_FLAGS)

# Build executable 

.PHONY: i2c
i2c: CFLAGS+= -DSSD1306_USE_I2C
i2c: $(BUILD_DIR)/i2c.elf

.PHONY: spi
spi: CFLAGS+= -DSSD1306_USE_SPI
spi: $(BUILD_DIR)/spi.elf

$(BUILD_DIR)/ssd1306_conf.h: $(BUILD_DIR)
	touch $(BUILD_DIR)/ssd1306_conf.h

$(BUILD_DIR)/%.o: %.c Makefile | $(BUILD_DIR)
	$(CC) -c $(CFLAGS) $< -o $@

$(BUILD_DIR)/%.o: %.s Makefile | $(BUILD_DIR)
	$(CC) -c $(CFLAGS) $< -o $@

$(BUILD_DIR)/%.elf: $(BUILD_DIR)/ssd1306_conf.h $(OBJECTS) Makefile
	$(CC) $(OBJECTS) $(LDFLAGS) -o $@

$(BUILD_DIR):
	mkdir $@
	