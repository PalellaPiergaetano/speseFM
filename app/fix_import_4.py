with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

lines = content.split('\n')
seen = set()
out_lines = []
for line in lines:
    if line.startswith("import "):
        if line in seen:
            continue
        seen.add(line)
    out_lines.append(line)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write('\n'.join(out_lines))

