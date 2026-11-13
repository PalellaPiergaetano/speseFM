import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

lines = content.split('\n')
depth = 0
for i, line in enumerate(lines):
    depth += line.count('{') - line.count('}')
    if "private fun MonthSelectorStrip" in line:
        print(f"Line {i+1}: MonthSelectorStrip is at depth {depth}")
    if "private fun Dashboard" in line:
        print(f"Line {i+1}: Dashboard is at depth {depth}")

