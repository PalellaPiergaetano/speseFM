import re

with open("src/main/java/it/fm/spese/AppStrings.kt", "r") as f:
    content = f.read()

new_keys = """
    val conferma_eliminazione = mapOf(
        AppLanguage.ITALIAN to "Conferma eliminazione",
        AppLanguage.ENGLISH to "Confirm deletion",
        AppLanguage.FRENCH to "Confirmer la suppression",
        AppLanguage.SPANISH to "Confirmar eliminación"
    )
    val sei_sicuro_di_voler_eliminare_questa_spesa = mapOf(
        AppLanguage.ITALIAN to "Sei sicuro di voler eliminare questa spesa?",
        AppLanguage.ENGLISH to "Are you sure you want to delete this expense?",
        AppLanguage.FRENCH to "Êtes-vous sûr de vouloir supprimer cette dépense ?",
        AppLanguage.SPANISH to "¿Está seguro de que desea eliminar este gasto?"
    )
    val modifica = mapOf(
        AppLanguage.ITALIAN to "Modifica",
        AppLanguage.ENGLISH to "Edit",
        AppLanguage.FRENCH to "Modifier",
        AppLanguage.SPANISH to "Editar"
    )
    val modifica_spesa = mapOf(
        AppLanguage.ITALIAN to "Modifica spesa",
        AppLanguage.ENGLISH to "Edit expense",
        AppLanguage.FRENCH to "Modifier la dépense",
        AppLanguage.SPANISH to "Editar gasto"
    )
"""

if "val modifica =" not in content:
    content = content.replace("    fun get(", new_keys + "\n    fun get(")
    with open("src/main/java/it/fm/spese/AppStrings.kt", "w") as f:
        f.write(content)

print("Edit and delete confirmation strings added to AppStrings.kt.")

