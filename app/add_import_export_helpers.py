import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

helpers = """
fun importXlsToExpenses(context: Context, uri: Uri, onResult: (List<Expense>) -> Unit) {
    try {
        val imported = XlsSheetImporter.importFromUri(context, uri)
        if (imported.isNotEmpty()) {
            Toast.makeText(context, "Importati ${imported.size} movimenti con successo!", Toast.LENGTH_LONG).show()
            onResult(imported)
        } else {
            Toast.makeText(context, "Nessun movimento trovato nel file.", Toast.LENGTH_LONG).show()
            onResult(emptyList())
        }
    } catch (e: Exception) {
        Toast.makeText(context, "Errore durante l'importazione", Toast.LENGTH_SHORT).show()
        onResult(emptyList())
    }
}

fun exportCsv(context: Context, uri: Uri, expenses: List<Expense>) {
    val ok = exportExpensesToCsv(context, uri, expenses)
    if (ok) {
        Toast.makeText(context, "Backup CSV esportato con successo!", Toast.LENGTH_LONG).show()
    } else {
        Toast.makeText(context, "Errore durante l'esportazione CSV.", Toast.LENGTH_SHORT).show()
    }
}
"""

if "fun importXlsToExpenses" not in content:
    content = content.replace("private const val ExpenseStore = \"expense_store\"", helpers + "\n\nprivate const val ExpenseStore = \"expense_store\"")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Import and Export helpers added.")

