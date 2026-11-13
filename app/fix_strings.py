import re

with open("src/main/java/it/fm/spese/AppStrings.kt", "r") as f:
    content = f.read()

missing_strings = """
    val nascondi_saldi = mapOf(
        AppLanguage.ITALIAN to "Nascondi saldi",
        AppLanguage.ENGLISH to "Hide balances",
        AppLanguage.FRENCH to "Masquer les soldes",
        AppLanguage.SPANISH to "Ocultar saldos"
    )
    val dettagli_spesa = mapOf(
        AppLanguage.ITALIAN to "Dettagli spesa",
        AppLanguage.ENGLISH to "Expense details",
        AppLanguage.FRENCH to "Détails de la dépense",
        AppLanguage.SPANISH to "Detalles del gasto"
    )
    val data = mapOf(
        AppLanguage.ITALIAN to "Data",
        AppLanguage.ENGLISH to "Date",
        AppLanguage.FRENCH to "Date",
        AppLanguage.SPANISH to "Fecha"
    )
    val ora = mapOf(
        AppLanguage.ITALIAN to "Ora",
        AppLanguage.ENGLISH to "Time",
        AppLanguage.FRENCH to "Heure",
        AppLanguage.SPANISH to "Hora"
    )
    val descrizione = mapOf(
        AppLanguage.ITALIAN to "Descrizione",
        AppLanguage.ENGLISH to "Description",
        AppLanguage.FRENCH to "Description",
        AppLanguage.SPANISH to "Descripción"
    )
    val elimina = mapOf(
        AppLanguage.ITALIAN to "Elimina",
        AppLanguage.ENGLISH to "Delete",
        AppLanguage.FRENCH to "Supprimer",
        AppLanguage.SPANISH to "Eliminar"
    )
"""

if "val nascondi_saldi =" not in content:
    content = content.replace("fun get(", missing_strings + "\n    fun get(")

with open("src/main/java/it/fm/spese/AppStrings.kt", "w") as f:
    f.write(content)
