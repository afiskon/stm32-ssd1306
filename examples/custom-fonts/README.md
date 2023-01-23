# Making Custom Fonts

This directory contains an example of making custom fonts with Python.

Here we are creating Font_16x24. This is an upscaled HD44780 5x8 font.
Its main purpose is to simulate 0802 LCDs.

The source font is stored in hd44780-small.txt which is upscaled using
upscale.py:

```
./upscale.py -f ./hd44780-small.txt -x 5 -y 8 -s 3 > hd44780-large.txt
```

This script creates hd44780-large.txt. The C code is created from
hd44780-large.txt using generate.py script:

```
./convert.py -f ./hd44780-large.txt -x 16 -y 24
```

Font encoding is pretty straightforward. Let's consider Font_6x8 as the smallest
one:

```
FontDef Font_6x8 = {6,8,Font6x8};

// ...

static const uint16_t Font6x8 [] = {
0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  // sp
0x2000, 0x2000, 0x2000, 0x2000, 0x2000, 0x0000, 0x2000, 0x0000,  // !
// ... etc ...
```

First 8 values in the array (where 8 is the height of the given font) encode
the first symbol one line after another. Next 8 values encode the second symbol,
etc. Each bit encodes one pixel. Since values are of type uint16_t, the font
width is limited to 16 pixels.

For instance, the exclamation mark is encoded as:

```
0x2000, 0x2000, 0x2000, 0x2000, 0x2000, 0x0000, 0x2000, 0x0000,  // !

```

... or:

```
0x2000 // line 1
0x2000 // line 2
0x2000 // line 3
0x2000 // line 4
0x2000 // line 5
0x0000 // line 6
0x2000 // line 7
0x0000 // line 8
```

... which in binary form is:

```
001000
001000
001000
001000
001000
000000
001000
000000
```

If we remove zeroes:

```
  1
  1
  1
  1
  1

  1

```

... you can clearly see a 6x8 pixels exclamation mark. The rest of the symbols
are encoded the same way.

Knowing this you can make any custom fonts and modify convert.py if necessary.