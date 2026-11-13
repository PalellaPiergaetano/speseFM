import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

target = """                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.padding(padding)"""

replacement = """                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            reminders = reminders,
                            onOpenSettingsClick = { showSettings = true },
                            onOpenRemindersClick = { showRemindersScreen = true },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(padding)"""

content = content.replace(target, replacement)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("SpeseApp Dashboard call fixed phase 2.")

