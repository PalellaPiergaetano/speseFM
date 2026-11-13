import os
import lz4.block

with open('/Users/piergaetanopalella/Library/Caches/Google/AndroidStudio2026.1.4/LocalHistory/changes.storageData', 'rb') as f:
    data = f.read()

# Try to find LZ4 block headers or just try to decompress every offset?
# LZ4 block doesn't have a strict magic number without the frame format.
# Let's search for "package it.fm.spese" in the compressed data? No, LZ4 compresses strings if they appear previously.
# But often "package it.fm.spese" is a literal.
# Let's see if we can find it as a literal.
idx = data.find(b'package it.fm.spese')
if idx != -1:
    print("Found 'package it.fm.spese' at", idx)

