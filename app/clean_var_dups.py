import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Replace duplicated state variables in SpeseApp
dup_states = """    var reminders by remember { mutableStateOf(loadPaymentReminders(context)) }
    var showSettings by remember { mutableStateOf(false) }
    var selectedExpense by remember { mutableStateOf<Expense?>(null) }
    var showRemindersScreen by remember { mutableStateOf(false) }
    var reminders by remember { mutableStateOf(loadPaymentReminders(context)) }
    var showSettings by remember { mutableStateOf(false) }
    var selectedExpense by remember { mutableStateOf<Expense?>(null) }
    var showRemindersScreen by remember { mutableStateOf(false) }"""

single_states = """    var reminders by remember { mutableStateOf(loadPaymentReminders(context)) }
    var showSettings by remember { mutableStateOf(false) }
    var selectedExpense by remember { mutableStateOf<Expense?>(null) }
    var showRemindersScreen by remember { mutableStateOf(false) }"""

content = content.replace(dup_states, single_states)

# Replace duplicated manualDate/manualTime in AddExpenseDialog
dup_dialog_vars = """    var manualDate by remember { mutableStateOf(java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())) }
    var manualTime by remember { mutableStateOf(java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())) }
    var manualDate by remember { mutableStateOf(java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())) }
    var manualTime by remember { mutableStateOf(java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())) }"""

single_dialog_vars = """    var manualDate by remember { mutableStateOf(java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())) }
    var manualTime by remember { mutableStateOf(java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())) }"""

content = content.replace(dup_dialog_vars, single_dialog_vars)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Variable duplicates cleaned.")

