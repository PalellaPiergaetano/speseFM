import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Define a function to remove duplicates
def remove_duplicate_lines(text):
    lines = text.split('\n')
    seen_textColor = False
    for i in range(len(lines)):
        if "val textColor =" in lines[i]:
            if seen_textColor:
                lines[i] = ""
            else:
                seen_textColor = True
        elif line_starts_with_fun(lines[i]):
            seen_textColor = False
    return '\n'.join(lines)

def line_starts_with_fun(line):
    return line.strip().startswith("fun ") or line.strip().startswith("private fun ")

# Actually, I'll just find AddExpenseDialog and SetBudgetDialog and clean them manually.
# In AddExpenseDialog:
content = content.replace(
"""private fun AddExpenseDialog(
    currentMonth: String,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (Expense) -> Unit
) {
    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)""",
"""private fun AddExpenseDialog(
    currentMonth: String,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (Expense) -> Unit
) {""")

# Wait, let's also remove ExperimentalMaterial3Api error
content = content.replace("This material API is experimental and is likely to change or to be removed in the future.", "")

# We can just annotate `fun SpeseApp()` with `@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)`.
content = content.replace("@androidx.compose.material3.ExperimentalMaterial3Api\nprivate fun SpeseApp(", "@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\nprivate fun SpeseApp(")


with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

