import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

injection = """
private fun loadAppLanguage(context: Context): AppLanguage {
    val code = context.getSharedPreferences(ExpenseStore, 0).getString("app_language", "it") ?: "it"
    return AppLanguage.entries.find { it.code == code } ?: AppLanguage.ITALIAN
}

private fun saveAppLanguage(context: Context, lang: AppLanguage) {
    context.getSharedPreferences(ExpenseStore, 0).edit().putString("app_language", lang.code).apply()
}
"""

content = content.replace("private fun clearAllData(context: Context) {", injection + "\nprivate fun clearAllData(context: Context) {")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

