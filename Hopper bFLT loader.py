# This is a (basic) port of https://github.com/nihilus/bflt-utils/blob/master/ida/bfltldr.py to Hopper
# Because of shortcomings in the Hopper API it is not able to create all the different segments yet
#
# Original copyright:
# Craig Heffner
# Tactical Network Solutions
# 06-March-2011
#
# Hopper port:
# Thomas Roth code@stacksmashing.net
# 17. October 2017

doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()

doc.log("--bFLT loader--")

BFLT_VERSION          = 4
BFLT_MAGIC            = "bFLT"
BFLT_HEADER_SIZE      = 0x40
FLAGS_RAM             = 0x01
FLAGS_GOTPIC          = 0x02
FLAGS_GZIP            = 0x04
DEFAULT_CPU           = "ARM"
DEBUG                 = True

def read_bytes(seg, addr, count):
	doc.log("Reading %d bytes" % count)
	ret = []
	for i in range(0, count):
		doc.log(str(i))
		# doc.log(seg.readByte(addr+i))
		ret.append(seg.readByte(addr+i))

	doc.log("Bytes: (%d) %s" % (len(ret), str(ret)))
	f = "".join(map(chr, ret))
	#
	return f

# Read bFLT header
hdr_data = read_bytes(seg, 0x0, 4*10)

full_file = seg.readBytes(0x0, seg.getLength())

hdr_data = full_file[:4*10]

if hdr_data[:4] != BFLT_MAGIC:
	raise ValueError("Not a bFLT file")

(magic, version, entry, data_start, data_end, bss_end, stack_size, reloc_start, reloc_count, flags) = struct.unpack(">IIIIIIIIII", hdr_data)	

doc.log("Magic: %s" % magic)
doc.log("Version: %d" % version)

if (flags & FLAGS_GZIP) == FLAGS_GZIP:
	doc.log("Code/data is GZIP compressed. You probably want to decompress the bFLT file with the flthdr or gunzip_bflt utilities before loading it into IDA.")
	raise ValueError("")

if (flags & FLAGS_GOTPIC) == FLAGS_GOTPIC:
	doc.log("Got GOT, not supported.")
	raise ValueError("")

doc.log("Segments: ")
doc.log("\t.text   0x%.8X - 0x%.8X" % (entry, data_start))
doc.log("\t.data   0x%.8X - 0x%.8X" % (data_start, data_end))
doc.log("\t.bss    0x%.8X - 0x%.8X" % (data_end, bss_end))

seg.setCommentAtAddress(entry, ".text (CODE)")
seg.setCommentAtAddress(data_start, ".data (DATA)")
seg.setCommentAtAddress(data_end, ".bss (BSS)")


doc.log("Patching relocations")
for i in range(0, reloc_count):
	seek = reloc_start + (i*4)
	reloc_offset = struct.unpack(">I", seg.readBytes(seek, 4))[0] + BFLT_HEADER_SIZE
	# doc.log("Reloc offset: 0x%x" % reloc_offset)

	# Sanity check
	if reloc_offset < bss_end:
		reloc_data_offset = struct.unpack(">I", seg.readBytes(reloc_offset, 4))[0] + BFLT_HEADER_SIZE
		
		packed = struct.pack("<I", reloc_data_offset)
		doc.log("Writing to 0x%.8x value %s" % (reloc_offset, reloc_data_offset))
		seg.writeBytes(reloc_offset, packed)
	else:
		doc.log("Relocation entry outside of defined file section")
doc.log("Done!")