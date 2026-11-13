import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Remove duplicate declarations of `val appLang = LocalAppLanguage.current` within the same function
def remove_dup_applang(body):
    lines = body.split('\n')
    seen = False
    new_lines = []
    for line in lines:
        if "val appLang = LocalAppLanguage.current" in line:
            if not seen:
                seen = True
                new_lines.append(line)
            else:
                # skip duplicate
                continue
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

# Split by fun definitions
parts = re.split(r'(?=\nfun |\nprivate fun |@Composable\nprivate fun |@OptIn.*?@Composable\nprivate fun |@OptIn.*?@Composable\nfun )', content)
new_parts = [remove_dup_applang(p) for p in parts]
content = ''.join(new_parts)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

