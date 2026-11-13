import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update ExpenseRow trash icon to show DeleteExpenseConfirmDialog
old_row_delete = """            IconButton(
                onClick = { onDelete(expense) },
                modifier = Modifier
                    .size(32.dp)
                    .background(Terracotta.copy(alpha = 0.12f), CircleShape)
            ) {"""

new_row_delete = """            var showRowDeleteConfirm by remember { mutableStateOf(false) }
            if (showRowDeleteConfirm) {
                DeleteExpenseConfirmDialog(
                    isDarkTheme = isDark,
                    onDismiss = { showRowDeleteConfirm = false },
                    onConfirm = { onDelete(expense) }
                )
            }
            IconButton(
                onClick = { showRowDeleteConfirm = true },
                modifier = Modifier
                    .size(32.dp)
                    .background(Terracotta.copy(alpha = 0.12f), CircleShape)
            ) {"""

content = content.replace(old_row_delete, new_row_delete)

# 2. Update ReminderCard delete button to show DeleteExpenseConfirmDialog
old_reminder_delete = """                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    TextButton(onClick = onDelete, contentPadding = PaddingValues(4.dp)) {"""

new_reminder_delete = """                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    var showReminderDeleteConfirm by remember { mutableStateOf(false) }
                    if (showReminderDeleteConfirm) {
                        DeleteExpenseConfirmDialog(
                            isDarkTheme = isDark,
                            onDismiss = { showReminderDeleteConfirm = false },
                            onConfirm = onDelete
                        )
                    }
                    TextButton(onClick = { showReminderDeleteConfirm = true }, contentPadding = PaddingValues(4.dp)) {"""

content = content.replace(old_reminder_delete, new_reminder_delete)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Delete confirmations added to ExpenseRow and ReminderCard.")

