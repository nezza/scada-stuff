#!/usr/bin/env python3

import sys
import csv

if len(sys.argv) != 3:
	print("Converts Saleae's Logic Analyzer CSV output into a text/bin file.")
	print(f"Usage: {sys.argv[0]} <file.csv/.txt> <outfile.txt>")
	sys.exit(1)


try:
	input_file = open(sys.argv[1], "r")
	output_file = open(sys.argv[2], "wb")
	parsed_csv = csv.DictReader(input_file)
	# print(c["Value"])
	for line in parsed_csv:
		value = line["Value"]

		# Replace space (indicated by ' ') with real space
		value = value.replace("' '", " ")

		# Non-ASCII characters are encoded with '23'
		if value.startswith("'") and len(value) > 1:
			value = value.replace("'", "")
			value = chr(int(value))
		else:
			# Commas are encoded as COMMA
			value = value.replace("COMMA", ",")

			# Needed to parse \r \n etc
			value = bytearray(value, 'ascii').decode('unicode_escape')

		byte_value = ord(value)

		output_file.write(bytes([byte_value]))

	print(f"Wrote {output_file.tell()} bytes to {sys.argv[2]}.")
except FileNotFoundError as e:
	print(f"Can't open: {e}")
	sys.exit(1)

except PermissionError as e:
	print(f"Permission problem: {sys.argv[2]}: {e}")
	sys.exit(1)
