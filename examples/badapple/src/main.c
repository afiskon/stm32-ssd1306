#include "ssd1306.h"
#include "stm32f4xx_hal.h"

extern const SSD1306_animation_t badapple;

#ifdef SSD1306_USE_I2C

I2C_HandleTypeDef SSD1306_I2C_PORT;

static void I2C_Init(void) {
  SSD1306_I2C_PORT.Instance = I2C1;
  SSD1306_I2C_PORT.Init.ClockSpeed = 400000;
  SSD1306_I2C_PORT.Init.DutyCycle = I2C_DUTYCYCLE_2;
  SSD1306_I2C_PORT.Init.OwnAddress1 = 0;
  SSD1306_I2C_PORT.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  SSD1306_I2C_PORT.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  SSD1306_I2C_PORT.Init.OwnAddress2 = 0;
  SSD1306_I2C_PORT.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  SSD1306_I2C_PORT.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  HAL_I2C_Init(&SSD1306_I2C_PORT);
}

void HAL_I2C_MspInit(I2C_HandleTypeDef *hi2c) {
  GPIO_InitTypeDef GPIO_InitStruct;
  if (hi2c->Instance == I2C1) {
    /* Peripheral clock enable */
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_I2C1_CLK_ENABLE();

    /**I2C1 GPIO Configuration
    PB8     ------> I2C1_SCL
    PB9     ------> I2C1_SDA
    */
    GPIO_InitStruct.Pin = GPIO_PIN_8 | GPIO_PIN_9;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF4_I2C1;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
  }
}

#elif defined(SSD1306_USE_SPI)

SPI_HandleTypeDef SSD1306_SPI_PORT;

static void SPI_Init(void) {
  /* SPI1 parameter configuration*/
  SSD1306_SPI_PORT.Instance = SPI1;
  SSD1306_SPI_PORT.Init.Mode = SPI_MODE_MASTER;
  SSD1306_SPI_PORT.Init.Direction = SPI_DIRECTION_2LINES;
  SSD1306_SPI_PORT.Init.DataSize = SPI_DATASIZE_8BIT;
  SSD1306_SPI_PORT.Init.CLKPolarity = SPI_POLARITY_LOW;
  SSD1306_SPI_PORT.Init.CLKPhase = SPI_PHASE_1EDGE;
  SSD1306_SPI_PORT.Init.NSS = SPI_NSS_SOFT;
  SSD1306_SPI_PORT.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_128;
  SSD1306_SPI_PORT.Init.FirstBit = SPI_FIRSTBIT_MSB;
  SSD1306_SPI_PORT.Init.TIMode = SPI_TIMODE_DISABLE;
  SSD1306_SPI_PORT.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  SSD1306_SPI_PORT.Init.CRCPolynomial = 10;
  HAL_SPI_Init(&SSD1306_SPI_PORT);
}

void HAL_SPI_MspInit(SPI_HandleTypeDef* hspi) {
  GPIO_InitTypeDef GPIO_InitStruct;

  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  HAL_GPIO_WritePin(SSD1306_CS_Port, SSD1306_CS_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(SSD1306_DC_Port, SSD1306_DC_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(SSD1306_Reset_Port, SSD1306_Reset_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : SSD1306_CS_Pin */
  GPIO_InitStruct.Pin = SSD1306_CS_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(SSD1306_CS_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : SSD1306_DC_Pin */
  GPIO_InitStruct.Pin = SSD1306_DC_Pin;
  HAL_GPIO_Init(SSD1306_DC_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : SSD1306_Reset_Pin */
  GPIO_InitStruct.Pin = SSD1306_Reset_Pin;
  HAL_GPIO_Init(SSD1306_Reset_Port, &GPIO_InitStruct);

  if (hspi->Instance == SPI1) {
    /* Peripheral clock enable */
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_SPI1_CLK_ENABLE();

    /**SPI1 GPIO Configuration
    PA5     ------> SPI1_SCK
    PA7     ------> SPI1_MOSI
    */
    GPIO_InitStruct.Pin = GPIO_PIN_5 | GPIO_PIN_7;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF5_SPI1;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
  }
}
#endif  // SSD1306_USE_I2C

int main(void) {
  HAL_Init();

  /* Initialize peripherals */
#ifdef SSD1306_USE_I2C
  I2C_Init();
#elif defined(SSD1306_USE_SPI)
  SPI_Init();
#endif  // SSD1306_USE_I2C
  ssd1306_Init();
  uint32_t tick;
  const uint32_t frametime = 306;
  while (1) {
    tick = HAL_GetTick();
    for (uint32_t i = 0; i < badapple.frames; i++) {
      tick += frametime;
      ssd1306_Fill(Black);
      ssd1306_DrawBitmap(21, 0, badapple.frame[i], badapple.w, badapple.h,
                         White);
      ssd1306_UpdateScreen();
      while (HAL_GetTick() < tick) {
      }
    }
  }
}

void SysTick_Handler(void) {
  HAL_IncTick();
  HAL_SYSTICK_IRQHandler();
}
