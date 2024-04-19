from argparse import ArgumentParser
from PIL import Image, ImageSequence

arg_parser = ArgumentParser(
    description='Generate C code from image',
)
arg_parser.add_argument('-v', '--version', action='version', version="0.0.1")
arg_parser.add_argument('-o', '--output', type=str,
                        default='img.c', help='Path to output file')
arg_parser.add_argument('--height', type=int, help='Resize height')
arg_parser.add_argument('imgpath', type=str, help='Path to image file')
args = arg_parser.parse_args()

im = Image.open(args.imgpath)
with open(args.output, 'w', encoding='utf-8') as fd:
    fd.write("/** Generated file by img2code.py*/\n"
             "#include \"ssd1306.h\"\n\n")
    if (im.format == 'GIF'):
        for idx, frame in enumerate(ImageSequence.Iterator(im)):
            frame = frame.convert('1')
            if args.height:
                ratio = frame.size[0]/frame.size[1]
                frame = frame.resize((int(args.height*ratio), args.height))
            fd.write(f"static const unsigned char frame_{idx}[] = {{\n")
            for byte in frame.tobytes():
                fd.write(f"0x{byte:02X}, ")
            fd.write("\n};\n\n")
        fd.write("static const unsigned char* frame[] = {\n")
        for idx in range(idx + 1):
            fd.write(f"  frame_{idx},\n")
        fd.write("};\n\n"
                 f"/** {args.imgpath} animation "
                 f"{frame.size[0]}x{frame.size[1]} */\n"
                 "const SSD1306_animation_t animation = {\n"
                 "  .frame = (unsigned char**)frame,\n"
                 f"  .frames = {idx + 1},\n"
                 f"  .w = {frame.size[0]},\n"
                 f"  .h = {frame.size[1]},\n"
                 "};\n")
    else:
        if args.height:
            ratio = im.size[0]/im.size[1]
            im = im.resize((int(args.height*ratio), args.height))
        im = im.convert('1')
        fd.write("static const unsigned char bytes[] = {\n")
        for byte in im.tobytes():
            fd.write(f"0x{byte:02X}, ")
        fd.write("\n};\n\n")
        fd.write(f"/** {args.imgpath} bitmap {im.size[0]}x{im.size[1]} */\n"
                 "const SSD1306_bitmap_t bitmap = {\n"
                 "  .bitmap = bytes,\n"
                 f"  .w = {im.size[0]},\n"
                 f"  .h = {im.size[1]},\n"
                 "};\n")
im.close()
