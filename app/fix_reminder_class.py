import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

payment_reminder_dataclass = """
data class PaymentReminder(
    val title: String,
    val amount: Double,
    val dueDate: String,
    val isRecurring: Boolean = false,
    val recurrenceInterval: String? = null,
    val maxPayments: Int? = null,
    val paymentsMade: Int = 0
)
"""

if "data class PaymentReminder" not in content:
    content = content.replace("data class Expense(", payment_reminder_dataclass + "\n\ndata class Expense(")

content = content.replace("Icons.AutoMirrored.Filled.HelpOutline", "Icons.Default.Info")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("PaymentReminder class added.")

