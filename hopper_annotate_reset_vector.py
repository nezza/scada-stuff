# Script by Thomas Roth, 2017
# code@stacksmashing.net - github.com/stacksmashing
# Annotates the reset vector

doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()

vectors = [
	[0x0, "IV Reset"],
	[0x4, "IV Undefined instruction"],
	[0x8, "IV SWI (Soft interrupt)"],
	[0xc, "IV Prefetch abort"],
	[0x10, "IV Data abort"],
	[0x18, "IV Interrupt (nIRQ)"],
	[0x1c, "IV Fast interrupt (FIQ)"]
]

doc.log("-- Annotating reset vector --")
for vector in vectors:
	comment = vector[1]
	current_comment = seg.getCommentAtAddress(adr+vector[0])
	if current_comment:
		comment += " - " + current_comment
	doc.log(comment)
	seg.markAsCode(adr+vector[0])
	seg.setCommentAtAddress(adr+vector[0], comment)
