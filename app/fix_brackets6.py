import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# At line 1020: Syntax error: Expecting a top level declaration.
# At line 1236: Syntax error: Expecting a top level declaration.
# The error means there are extra `}`!
lines = content.split('\n')
for line_num in [481, 482, 1020, 1021, 1236, 1237]:
    idx = line_num - 1
    if idx < len(lines):
        if "}" in lines[idx]:
            lines[idx] = ""

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write('\n'.join(lines))

