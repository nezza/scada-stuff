#!/usr/bin/env python
# All rights reserved
# Thomas Roth 2017 <code@stacksmashing.net>

import sys
import struct
import os

if len(sys.argv) != 3:
	print "Usage: %s <firmware_image> <output_directory>" % sys.argv[0]
	sys.exit()

print "Loading firmware: %s" % sys.argv[1]




FILE_TABLE_OFFSET=0x160
FILE_TABLE_INTERVAL=0x1e0-0x1a0

FILE_INDICATORS = [
['\x00', '\x05', '"', '1', '\xe1', '\x07', '\x03', '\x07'],
['\x00', '\x05', '!', '6', '\xe1', '\x07', '\x03', '\x07'],
['\x00', '\r', '2', '\x1b', '\xe1', '\x07', '\t', '\x01'],
['\x00', '\r', '4', '\x08', '\xe1', '\x07', '\t', '\x01'],
['\x00', '\x12', '\x13', '\x04', '\xe1', '\x07', '\x02', '\x11'], # NP54x0
['\x00', '\r', '9', '\x16', '\xd2', '\x07', '\x0c', '\x13'], # NP5400
['\x00', '\x0f', ')', '\x08', '\xd7', '\x07', '\x01', '\x03'], # NP5400
]

FILE_METADATA_INDICATOR_SHORT = ['\x00', '\x05']
FILE_POSITION_OFFSET=0x60

BINARY_FIRMWARE_LOCATION_POINTER = 0x00000054

outdir = sys.argv[2]


def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == chr(0):
            return "".join(chars)
        chars.append(c)

class FileInfo:
	def __init__(self, name, length, position):
		self.name = name
		self.length = length
		self.position = position

	def __unicode__(self):
		print self.name

	def __str__(self):
		return self.__unicode__()

files = []
with open(sys.argv[1], 'rb') as fwf:
	print "Seek to beginning of file table"
	fwf.seek(FILE_TABLE_OFFSET, 0)

	while True:
		pre_string = fwf.tell()	
		filename = readString(fwf)
		print "Checking address: 0x%08x" % pre_string
		

		fwf.seek(pre_string + 0x30, 0)

		d = list(fwf.read(len(FILE_INDICATORS[0])))
		if not d in FILE_INDICATORS:
			#if d[:2] != FILE_METADATA_INDICATOR_SHORT:
			print "\tReached end of file table"
			print d
			break

		print "\tFilename: %s" % filename

		file_length = struct.unpack("<I", fwf.read(4))[0]
		print "\tFile length: %d" % file_length

		file_position = struct.unpack("<I", fwf.read(4))[0]
		print "\tFile position: 0x%08x" % (file_position+FILE_POSITION_OFFSET)

		files.append(FileInfo(filename, file_length, file_position+FILE_POSITION_OFFSET))


	print "Number of files: %d" % len(files)

	for file in files:
		print "Writing to: %s" % file.name
		path = os.path.join(outdir, file.name)
		path_dir = os.path.dirname(path)
		try:
			os.makedirs(path_dir)
		except OSError:
			if not os.path.isdir(path_dir):
				raise
		with open(os.path.join(outdir, file.name), "w") as outfile:
			fwf.seek(file.position, 0)
			data = fwf.read(file.length)

			outfile.write(data)

	OTHER_DATA_START = 0x00028b40
	# Get position of binary data
	fwf.seek(BINARY_FIRMWARE_LOCATION_POINTER)
	binary_firmware_location = struct.unpack("<I", fwf.read(4))[0]
	print "Firmware is at: 0x%08x" % binary_firmware_location

	# header
	fwf.seek(binary_firmware_location, 0)

	# Binary data
	fwf.seek(binary_firmware_location, 0)
	with open(os.path.join(outdir, "fw.bin"), "w") as fwbin_file:
		fwbin = fwf.read()
		fwbin_file.write(fwbin)
