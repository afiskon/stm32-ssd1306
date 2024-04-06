from PIL import Image, ImageDraw, ImageFont
from argparse import ArgumentParser
from math import ceil
from sys import hexversion as python_version

if python_version < 0x030A00F0:
    raise RuntimeError('Unsupported Python version. Python 3.10+ required')

arg_parser = ArgumentParser(
    description='Generate C code from TrueType font',
)
arg_parser.add_argument('-v', '--version', action='version', version="0.0.2")
arg_parser.add_argument('-f', '--font', required=True,
                        type=str, help="Font file with extension (arial.ttf)")
arg_parser.add_argument('-s', '--size', required=True, type=int,
                        help="Size of font in px. Note: actual size of bitmap may be different")
arg_parser.add_argument('-p', '--proportional', action='store_true', 
                        help="Generate array of char width (for non-monospaced fonts)")
arg_parser.add_argument('-a', '--atlas', type=str,
                        help="Font atlas file with extension (e.g. atlas.png)")
arg_parser.add_argument('--charset', default="ascii", type=str,
                        help="Specific charset (not suported by library)")
arg_parser.add_argument('--string', type=str)
args = arg_parser.parse_args()

""" Charsets """
ascii = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
cp1251 = ascii + " ЂЃ‚ѓ„…†‡€‰Љ‹ЊЌЋЏђ‘’“”•–— ™љ›њќћџ ЎўЈ¤Ґ¦§Ё©Є«¬ ®Ї°±Ііґµ¶·ё№є»јЅѕїАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя"

match args.charset:
    case "ascii":
        charset = ascii
    case "cp1251":
        charset = cp1251
    case _:
        with open(args.charset, 'r', encoding='utf-8') as file:
            charset = file.read()
charset = [char for char in charset]

try:
    fnt = ImageFont.truetype(args.font, args.size)
except OSError:
    print("Cannot open font")
    exit(1)

""" Find font boundary box """
x_min = args.size * 3
x_max = 0
y_min = args.size * 3
y_max = 0
widths = []
for char in charset:
    bbox = fnt.getbbox(char, '1')
    if bbox:
        x_min = min(x_min, bbox[0])
        y_min = min(y_min, bbox[1])
        x_max = max(x_max, bbox[2])
        y_max = max(y_max, bbox[3])
        widths.append(bbox[2])
    else:
        widths.append(0)
widths = [w - x_min if w >= x_min else 0 for w in widths]

max_width = x_max - x_min
res = (ceil(max_width / 16) * 16, y_max - y_min)

""" Convert font to bytes """
pixels = []
for char in charset:
    out = Image.new("1", res, 0)
    d = ImageDraw.Draw(out)
    d.text((-x_min, -y_min), char, font=fnt, fill=1)
    pixels.append(out.tobytes())

""" Generate C code """
if not args.string:
    with open("font.c", "w", encoding='utf-8') as fd:
        fnt_name = fnt.getname()
        fd.write(f"/** Generated {fnt_name[0]} {fnt_name[1]} {args.size} "
                 "file by generate.py*/\n")
        words = [[(char[byte], char[byte + 1] if len(char) >= byte else 0)
                  for byte in range(0, len(char), 2)] for char in pixels]
        fd.write("#include <stdint.h>\n")
        fd.write("#include \"ssd1306_fonts.h\"\n\n")
        fd.write(f"static const uint16_t Font{max_width}x{res[1]} [] = {{\n")
        for index, char in enumerate(words):
            assert (len(char) == (res[1] * ceil(max_width / 16)))
            fd.write(f"/** {charset[index]} **/\n")
            for word in char:
                fd.write(f"0x{word[0]:02X}{word[1]:02X},")
            fd.write("\n")
        fd.write("};\n\n")
        if args.proportional:
            fd.write("static const uint8_t char_width[] = {\n")
            for index, width in enumerate(widths):
                fd.write(f"  {width},  /** {charset[index]} **/\n")
            fd.write("};\n\n")
        fd.write(f"/** Generated {fnt_name[0]} {fnt_name[1]} {args.size} */\n")
        fd.write(f"const SSD1306_Font_t Font_{max_width}x{res[1]} = "
                 f"{{{max_width}, {res[1]}, Font{max_width}x{res[1]}, ")
        if args.proportional:
            fd.write("char_width")
        else:
            fd.write("NULL")
        fd.write("};\n")

""" Generate string bitmap """
if args.string:
    with open("string.c", "w", encoding='utf-8') as fd:
        mask = fnt.getmask(args.string, '1')
        out = Image.new('1', mask.size)
        out.im.paste(1, (0, 0) + mask.size, mask)
        fnt_name = fnt.getname()
        fd.write(f"/** Generated string \"{args.string}\" with "
                 f"{fnt_name[0]} {fnt_name[1]} {args.size} "
                 "file by generate.py*/\n\n")
        fd.write(
            f"/** \"{args.string}\" bitmap {mask.size[0]}x{mask.size[1]} */\n")
        fd.write(f"const unsigned char string_{
                 mask.size[0]}x{mask.size[1]} [] = {{\n")
        for byte in out.tobytes():
            fd.write(f"0x{byte:02X}, ")
        fd.write("};\n")
        out.save('string.png')


""" Atlas """
if args.atlas:
    atlas_res = (max_width * 16 + 17, (res[1] + 1) *
                 ceil(len(charset) / 16) + 1)
    atlas = Image.new("RGB", atlas_res, 0)
    d = ImageDraw.Draw(atlas)
    for index in range(len(pixels)):
        x = int(index % 16)
        y = int(index / 16)
        char_img = Image.frombytes("1", res, pixels[index])
        atlas.paste(char_img, ((max_width + 1) * x + 1, (res[1] + 1) * y + 1))

    """ Draw line separator """
    for x in range(0, atlas_res[0], max_width+1):
        d.line([(x, 0), (x, atlas_res[1])], fill=128, width=1)
    for y in range(0, atlas_res[1], res[1]+1):
        d.line([(0, y), (atlas_res[0], y)], fill=128, width=1)
    if args.proportional:
        for index, width in enumerate(widths):
            x = (max_width + 1) * int(index % 16) + width
            y = (res[1] + 1) * int(index / 16)
            d.line([(x, y), (x, y + res[1])], fill=0xFFFF, width=1)
    atlas.save(args.atlas)
