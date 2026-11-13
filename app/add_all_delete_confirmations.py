import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. ExpenseRow confirmation dialog before deletion
old_row_iconbutton = """            IconButton(
                onClick = { onDelete(expense) },
                modifier = Modifier
                    .size(32.dp)
                    .background(Terracotta.copy(alpha = 0.12f), CircleShape)
            ) {"""

new_row_iconbutton = """            var showRowDeleteConfirm by remember { mutableStateOf(false) }
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

content = content.replace(old_row_iconbutton, new_row_iconbutton)

# 2. ReminderCard confirmation dialog before deletion
old_reminder_delete_btn = """                    TextButton(onClick = onDelete, contentPadding = PaddingValues(4.dp)) {"""

new_reminder_delete_btn = """                    var showReminderDeleteConfirm by remember { mutableStateOf(false) }
                    if (showReminderDeleteConfirm) {
                        DeleteExpenseConfirmDialog(
                            isDarkTheme = isDark,
                            onDismiss = { showReminderDeleteConfirm = false },
                            onConfirm = onDelete
                        )
                    }
                    TextButton(onClick = { showReminderDeleteConfirm = true }, contentPadding = PaddingValues(4.dp)) {"""

content = content.replace(old_reminder_delete_btn, new_reminder_delete_btn)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Delete confirmation dialogs added to ExpenseRow and ReminderCard successfully.")

