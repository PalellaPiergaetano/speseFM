import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Bottom Navigation Bar labels
bottom_bar_target = """                                listOf(
                                    "Home" to Icons.Default.Home,
                                    "Movimenti" to Icons.AutoMirrored.Filled.ReceiptLong,
                                    "Report" to Icons.Default.BarChart
                                ).forEachIndexed { index, item ->"""

bottom_bar_repl = """                                val appLang = LocalAppLanguage.current
                                listOf(
                                    AppStrings.get(AppStrings.panoramica_spese, appLang) to Icons.Default.Home,
                                    AppStrings.get(AppStrings.movimenti, appLang) to Icons.AutoMirrored.Filled.ReceiptLong,
                                    AppStrings.get(AppStrings.report_statistiche, appLang) to Icons.Default.BarChart
                                ).forEachIndexed { index, item ->"""
content = content.replace(bottom_bar_target, bottom_bar_repl)

# 2. Dashboard hardcoded strings
dash_target = """    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)"""
dash_repl = """    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val appLang = LocalAppLanguage.current"""
content = content.replace(dash_target, dash_repl)

content = content.replace('Text("Ultimi Movimenti"', 'Text(AppStrings.get(AppStrings.ultimi_movimenti, appLang)')
content = content.replace('Text("Nessuna spesa presente"', 'Text(AppStrings.get(AppStrings.nessuna_spesa_presente, appLang)')

# 3. Movements hardcoded strings
mov_target = """    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)"""
# We can add appLang to Movements if not already present
if "val appLang = LocalAppLanguage.current" not in content.split("private fun Movements(")[1].split("{")[1]:
    content = content.replace(
        """    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)""",
        """    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    val appLang = LocalAppLanguage.current"""
    )

content = content.replace('Text("Movimenti"', 'Text(AppStrings.get(AppStrings.movimenti, appLang)')
content = content.replace('Text("Tutte le tue uscite"', 'Text(AppStrings.get(AppStrings.tutte_le_tue_uscite, appLang)')
content = content.replace('placeholder = { Text("Cerca tra le spese..."', 'placeholder = { Text(AppStrings.get(AppStrings.cerca_tra_le_spese, appLang)')

# 4. Reports hardcoded strings
reports_target = """    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)"""
reports_repl = """    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    val appLang = LocalAppLanguage.current"""
content = content.replace(reports_target, reports_repl)

content = content.replace('Text("Report & Statistiche"', 'Text(AppStrings.get(AppStrings.report_statistiche, appLang)')
content = content.replace('Text("Analisi dettagliata e KPI della tua spesa"', 'Text(AppStrings.get(AppStrings.analisi_dettagliata_e_kpi_della_tua_spesa, appLang)')

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

