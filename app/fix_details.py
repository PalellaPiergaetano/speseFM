import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix ExpenseDetailScreen
target = """val catInfo = mapColumnToCategory(expense.category)
                    Box(
                        modifier = Modifier
                            .size(64.dp)
                            .background(catInfo.color.copy(alpha = 0.2f), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(catInfo.emoji, fontSize = 32.sp)
                    }"""

repl = """val catInfo = getCategoryMeta(expense.category)
                    Box(
                        modifier = Modifier
                            .size(64.dp)
                            .background(catInfo.color.copy(alpha = 0.2f), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(catInfo.icon, contentDescription = null, tint = catInfo.color, modifier = Modifier.size(32.dp))
                    }"""
content = content.replace(target, repl)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)
