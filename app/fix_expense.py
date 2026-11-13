import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Replace Expense
content = content.replace(
"""data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = "settembre 26"
)""",
"""data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = "settembre 26",
    val date: String = "",
    val time: String = "",
    val description: String = ""
)""")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

