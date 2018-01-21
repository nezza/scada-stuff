#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <key> <firmware_file>"
    exit
fi

FIRMWARE_KEY="$1"
FIRMWARE_FILE="$2"

echo "Decrypting firmware..."
dd if="$FIRMWARE_FILE" of="$FIRMWARE_FILE.offset" bs=1 skip=8 2>/dev/null
openssl aes-128-ecb -d -K "$FIRMWARE_KEY" -in $FIRMWARE_FILE.offset -out $FIRMWARE_FILE.decrypted 2>/dev/null
rm $FIRMWARE_FILE.offset

echo "Firmware decrypted to: $FIRMWARE_FILE.decrypted"

