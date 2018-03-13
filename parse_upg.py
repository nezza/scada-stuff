#!/usr/bin/env python3

# This script can parse .upg firmware files as used by some
# Schneider Electric RTUs.
# Copyright: Thomas Roth <code@stacksmashing.net>

import sys

if len(sys.argv) != 3:
	print(f"Usage: {sys.argv[0]} <firmware.upg> <outfile.bin>")

f = open(sys.argv[1], "r")
o = open(sys.argv[2], "wb")

for l in f.readlines():
	if l.startswith("PML: "):
		print(f"Metadata: {l[5:-1]}")
		continue
	elif l.startswith("CRC16: "):
		print(f"Metadata: {l[:-1]}")
		continue
	elif not l.startswith("S355"):
		continue
	h = l[len("S355FF800000"):-1]
	b = bytearray.fromhex(h)
	o.write(b)

print(f"Firmware written to {sys.argv[2]}")