# Image to C code converter

`img2code` script converts images to C byte array (bitmap)

```bash
./img2code.py image.png
```

Which can be drawn on display by library

**Example:**

```c
extern const SSD1306_bitmap_t bitmap;
ssd1306_DrawBitmap(0, 0, bitmap.bitmap, bitmap.w, bitmap.h, White);
ssd1306_UpdateScreen();
```

## Animation

You can even convert GIF files!

```bash
./img2code.py animation.gif
```

This generates a bitmap for each frame, which can be accessed by index

**Example:**

```c
extern const SSD1306_animation_t animation;
for(uint32_t i = 0; i < animation.frames; i++)
{
    ssd1306_DrawBitmap(0, 0, animation.frame[i], animation.w, animation.h,
                         White);
    ssd1306_UpdateScreen();
    delay_ms(200);
}
```
