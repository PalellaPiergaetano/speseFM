import re

# 1. Add keys to AppStrings.kt
with open("src/main/java/it/fm/spese/AppStrings.kt", "r") as f:
    strings_content = f.read()

new_keys = """
    val superato = mapOf(
        AppLanguage.ITALIAN to "Superato!",
        AppLanguage.ENGLISH to "Exceeded!",
        AppLanguage.FRENCH to "Dépassé !",
        AppLanguage.SPANISH to "¡Superado!"
    )
    val rimanente = mapOf(
        AppLanguage.ITALIAN to "Rim.",
        AppLanguage.ENGLISH to "Rem.",
        AppLanguage.FRENCH to "Rest.",
        AppLanguage.SPANISH to "Rest."
    )
    val media_mese = mapOf(
        AppLanguage.ITALIAN to "Media / Mese",
        AppLanguage.ENGLISH to "Average / Month",
        AppLanguage.FRENCH to "Moyenne / Mois",
        AppLanguage.SPANISH to "Promedio / Mes"
    )
    val totale_mese = mapOf(
        AppLanguage.ITALIAN to "Totale Mese",
        AppLanguage.ENGLISH to "Monthly Total",
        AppLanguage.FRENCH to "Total Mensuel",
        AppLanguage.SPANISH to "Total Mensual"
    )
    val anno = mapOf(
        AppLanguage.ITALIAN to "anno",
        AppLanguage.ENGLISH to "year",
        AppLanguage.FRENCH to "an",
        AppLanguage.SPANISH to "año"
    )
    val anni = mapOf(
        AppLanguage.ITALIAN to "anni",
        AppLanguage.ENGLISH to "years",
        AppLanguage.FRENCH to "ans",
        AppLanguage.SPANISH to "años"
    )
    val mesi_registrati = mapOf(
        AppLanguage.ITALIAN to "mesi registrati",
        AppLanguage.ENGLISH to "months recorded",
        AppLanguage.FRENCH to "mois enregistrés",
        AppLanguage.SPANISH to "meses registrados"
    )
    val media_mensile = mapOf(
        AppLanguage.ITALIAN to "Media mensile",
        AppLanguage.ENGLISH to "Monthly average",
        AppLanguage.FRENCH to "Moyenne mensuelle",
        AppLanguage.SPANISH to "Promedio mensual"
    )
    val prossima_scadenza = mapOf(
        AppLanguage.ITALIAN to "Prossima Scadenza",
        AppLanguage.ENGLISH to "Next Deadline",
        AppLanguage.FRENCH to "Prochaine Échéance",
        AppLanguage.SPANISH to "Próximo Vencimiento"
    )
    val scadenza_colon = mapOf(
        AppLanguage.ITALIAN to "Scadenza:",
        AppLanguage.ENGLISH to "Due date:",
        AppLanguage.FRENCH to "Échéance :",
        AppLanguage.SPANISH to "Vencimiento:"
    )
    val rate_colon = mapOf(
        AppLanguage.ITALIAN to "Rate:",
        AppLanguage.ENGLISH to "Installments:",
        AppLanguage.FRENCH to "Versements :",
        AppLanguage.SPANISH to "Cuotas:"
    )
    val al_mese = mapOf(
        AppLanguage.ITALIAN to "/ mese",
        AppLanguage.ENGLISH to "/ month",
        AppLanguage.FRENCH to "/ mois",
        AppLanguage.SPANISH to "/ mes"
    )
"""

if "val superato =" not in strings_content:
    strings_content = strings_content.replace("    fun get(", new_keys + "    fun get(")
    with open("src/main/java/it/fm/spese/AppStrings.kt", "w") as f:
        f.write(strings_content)

# 2. Update MainActivity.kt
with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Replace Prossima Scadenza
content = content.replace(
    'Text("Prossima Scadenza", color = Terracotta, fontSize = 11.sp, fontWeight = FontWeight.Bold)',
    'Text(AppStrings.get(AppStrings.prossima_scadenza, LocalAppLanguage.current), color = Terracotta, fontSize = 11.sp, fontWeight = FontWeight.Bold)'
)
content = content.replace(
    'Text("Scadenza: ${nextReminder.dueDate}"',
    'Text("${AppStrings.get(AppStrings.scadenza_colon, LocalAppLanguage.current)} ${nextReminder.dueDate}"'
)

# Replace SummaryCard pill text
content = content.replace(
    'if (budgetRemaining >= 0) "Rim.: ${formatAmount(budgetRemaining, isPrivacyMode)}" else "Superato!"',
    'val appLang = LocalAppLanguage.current\nif (budgetRemaining >= 0) "${AppStrings.get(AppStrings.rimanente, appLang)}: ${formatAmount(budgetRemaining, isPrivacyMode)}" else AppStrings.get(AppStrings.superato, appLang)'
)

# Replace Reports media_mese / totale_mese
content = content.replace(
    'Text(if (numMonths > 1) "Media / Mese" else "Totale Mese", color = subTextColor, fontSize = 11.sp, fontWeight = FontWeight.Medium)',
    'val appLang = LocalAppLanguage.current\nText(if (numMonths > 1) AppStrings.get(AppStrings.media_mese, appLang) else AppStrings.get(AppStrings.totale_mese, appLang), color = subTextColor, fontSize = 11.sp, fontWeight = FontWeight.Medium)'
)

# Replace Reports year stats
content = content.replace(
    '"${yearlyGrouped.size} ${if (yearlyGrouped.size == 1) "anno" else "anni"}"',
    '"${yearlyGrouped.size} " + (if (yearlyGrouped.size == 1) AppStrings.get(AppStrings.anno, LocalAppLanguage.current) else AppStrings.get(AppStrings.anni, LocalAppLanguage.current))'
)
content = content.replace(
    '"$yearMonths mesi registrati"',
    '"$yearMonths " + AppStrings.get(AppStrings.mesi_registrati, LocalAppLanguage.current)'
)
content = content.replace(
    '"Media mensile $year:"',
    'AppStrings.get(AppStrings.media_mensile, LocalAppLanguage.current) + " $year:"'
)
content = content.replace(
    '"${formatAmount(yearMonthlyAvg, isPrivacyMode)} / mese"',
    'formatAmount(yearMonthlyAvg, isPrivacyMode) + " " + AppStrings.get(AppStrings.al_mese, LocalAppLanguage.current)'
)

# Replace Reports "Mostra tutti"
content = content.replace(
    'Text(\n                                    "Mostra tutti",',
    'Text(\n                                    AppStrings.get(AppStrings.mostra_tutti, LocalAppLanguage.current),'
)

# Replace ReminderCard Scadenza and Rate
content = content.replace(
    'Text("Scadenza: ${reminder.dueDate}", color = subTextColor, fontSize = 12.sp)',
    'Text("${AppStrings.get(AppStrings.scadenza_colon, appLang)} ${reminder.dueDate}", color = subTextColor, fontSize = 12.sp)'
)
content = content.replace(
    'Text("Rate: ${reminder.paymentsMade}/${reminder.maxPayments}", color = subTextColor, fontSize = 11.sp)',
    'Text("${AppStrings.get(AppStrings.rate_colon, appLang)} ${reminder.paymentsMade}/${reminder.maxPayments}", color = subTextColor, fontSize = 11.sp)'
)

# Replace NavigationBar items labels
content = content.replace(
    '"Home" to Icons.Default.Home',
    'AppStrings.get(AppStrings.panoramica_spese, LocalAppLanguage.current) to Icons.Default.Home'
)
content = content.replace(
    '"Report" to Icons.Default.BarChart',
    'AppStrings.get(AppStrings.report_statistiche, LocalAppLanguage.current) to Icons.Default.BarChart'
)

# Replace InsightCard top category sentence
old_insight_sentence = 'Text(\n                    if (top != null) "${top.key} e la spesa maggiore (${formatAmount(top.value.sumOf { it.amount }, isPrivacyMode)}). Prova a fissare un limite mensile!"\n                    else "Aggiungi le prime spese per ricevere analisi personalizzate.",'
new_insight_sentence = """val appLang = LocalAppLanguage.current
                val topCatName = if (top != null) AppStrings.translateCategory(top.key, appLang) else ""
                Text(
                    if (top != null) "$topCatName " + (if (appLang == AppLanguage.ENGLISH) "is your highest expense" else "è la spesa maggiore") + " (${formatAmount(top.value.sumOf { it.amount }, isPrivacyMode)})."
                    else "Aggiungi le prime spese per ricevere analisi personalizzate.\","""

content = content.replace(old_insight_sentence, new_insight_sentence)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Full translation fix script executed successfully.")

