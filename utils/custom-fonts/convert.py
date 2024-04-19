#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser(
    description='Convert the input file to C code'
)

parser.add_argument(
    '-x', '--width', metavar='X', type=int,
    required = True,
    help='input symbol width')
parser.add_argument(
    '-y', '--height', metavar='Y', type=int,
    required = True,
    help='input symbol height')
parser.add_argument(
    '-f', '--file', metavar='F', type=str,
    required = True,
    help='input file')
args = parser.parse_args()

def process_symbol(lines):
    if len(lines) != args.height:
        raise RuntimeError("Invalid symbol height", len(lines), lines)

    for l in lines:
        l = l.replace(" ", "0")
        print("0x{:04X}, ".format(int(l, 2)), end = "")
    print("")


w = str(args.width)
h = str(args.height)
print("const SSD1306_Font_t Font_" + w + "x" + h +
    " = {" + w + ", " + h +
    ", Font" + w + "x" + h + ", NULL};")

print("static const uint16_t Font" + 
    w + "x" + h + " [] = {")

lines = []
with open(args.file) as f:
    for line in f:
        line = line.rstrip()
        if line.startswith("--"):
            # process the latest symbol, if there is any
            if len(lines) != 0:
                process_symbol(lines)
                lines = []
            print("/* " + line + " */")
            continue

        if len(line) > args.width:
            raise RuntimeError("Invalid symbol width", len(line), line)

        while len(line) < args.width:
            line = line + " "

        lines += [line]

if len(lines):
    raise RuntimeError("Data doesn't belong to any symbol", len(lines), lines)

print("};")