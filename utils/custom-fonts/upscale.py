#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser(
	description='Upscale the input file by the given scale factor'
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
    '-s', '--scale', metavar='S', type=int,
    required = True,
    help='scale factor')
parser.add_argument(
    '-f', '--file', metavar='F', type=str,
    required = True,
    help='input file')
args = parser.parse_args()

def process_symbol(lines):
	if len(lines) != args.height:
		raise RuntimeError("Invalid symbol height", len(lines), lines)

	for l in lines:
		# scale X
		l = l.replace(" ", " " * args.scale)
		l = l.replace("1", "1" * args.scale)
		# scale Y
		for n in range(0, args.scale):
			print(l)

lines = []
with open(args.file) as f:
    for line in f:
    	line = line.rstrip()
    	if line.startswith("--"):
    		# process the latest symbol, if there is any
    		if len(lines) != 0:
    			process_symbol(lines)
    			lines = []
    		print(line)
    		continue

    	if len(line) > args.width:
    		raise RuntimeError("Invalid symbol width", len(line), line)

    	while len(line) < args.width:
    		line = line + " "

    	lines += [line]

if len(lines):
	raise RuntimeError("Data doesn't belong to any symbol", len(lines), lines)