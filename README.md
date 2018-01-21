# scada-stuff

## Hopper bFLT loader

A lot of ICS devices use uClinux/eCos which uses the bFLT format. The `hopper_bflt_loader.py` implements basic bFLT support for Hopper. Open a binary with the settings:

```
Base address: 0x0
Entry point: 0x0
File offset: 0x0
CPU: ARMv6 Little endian
```

and then run the script on it.

The script is based on the IDA Pro loader written by Craig Heffner from Tactical Network Solutions

## moxa_parse_fw.py

Extracts the firmware images of the simple Mgate and Nport devices without wireless capability.

Firmware images compatible with this tool can be found on the Moxa website.

### Usage

```
moxa_parse_fw.py <firmware_file> <output_directory>
```

### Output description

The output directory will contain all extracted files in a flat format. The binary firmware itself is saved to `<output_directory>/fw.bin`.

Note that, depending on the device, different CPU architectures are used. Mgate devices seem to use ARM-based CPUs which can be directly loaded into Hopper/IDA Pro/Radare2 with the following settings:

```
Base address: 0x0
Entry point: 0x0
File offset: 0x0
CPU: ARMv6 Little endian
```

The NPort devices with a Moxa labelled chip are based on the [R8822](http://www.paradigmtools.com/docs/R8822.PDF) (Thanks [K. Reid Wightman](https://twitter.com/ReverseICS)!)
 architecture.


## Moxa NPort W2150 Firmware

The firmware files for the Moxa NPort W2x50 can be loaded directlry into a disassembler with the following settings:

```
Base address: 0x0
Entry point: 0x0
File offset: 0x58
CPU: ARMv6 Little endian
```

Note that this only loads the Linux bootlaoder which uncompresses the kernel. The filesystems themselves can be extracted using `binwalk -e`.

Starting with firmware version 2 the firmware is encrypted.

## Advantech ADAM 4570 Firmware

The firmware file (e.g. `ADAM-4570-BE_FW_D1.70_268D671C.bin`) can be directly loaded into a disassembler.

