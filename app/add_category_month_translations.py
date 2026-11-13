import re

with open("src/main/java/it/fm/spese/AppStrings.kt", "r") as f:
    content = f.read()

helpers = """
    fun translateCategory(category: String, lang: AppLanguage): String {
        return when (category) {
            "Spesa" -> when (lang) {
                AppLanguage.ITALIAN -> "Spesa"
                AppLanguage.ENGLISH -> "Groceries"
                AppLanguage.FRENCH -> "Courses"
                AppLanguage.SPANISH -> "Compras"
            }
            "Trasporti" -> when (lang) {
                AppLanguage.ITALIAN -> "Trasporti"
                AppLanguage.ENGLISH -> "Transport"
                AppLanguage.FRENCH -> "Transports"
                AppLanguage.SPANISH -> "Transporte"
            }
            "Bar / Ristoranti / Uscite" -> when (lang) {
                AppLanguage.ITALIAN -> "Bar / Ristoranti / Uscite"
                AppLanguage.ENGLISH -> "Dining & Outings"
                AppLanguage.FRENCH -> "Restaurants & Sorties"
                AppLanguage.SPANISH -> "Restaurantes y Salidas"
            }
            "Mediche" -> when (lang) {
                AppLanguage.ITALIAN -> "Mediche"
                AppLanguage.ENGLISH -> "Health & Medical"
                AppLanguage.FRENCH -> "Santé & Médical"
                AppLanguage.SPANISH -> "Salud y Médicos"
            }
            "Fitto / Bollette / Casa" -> when (lang) {
                AppLanguage.ITALIAN -> "Fitto / Bollette / Casa"
                AppLanguage.ENGLISH -> "Rent & Bills"
                AppLanguage.FRENCH -> "Loyer & Factures"
                AppLanguage.SPANISH -> "Alquiler y Facturas"
            }
            "Regali" -> when (lang) {
                AppLanguage.ITALIAN -> "Regali"
                AppLanguage.ENGLISH -> "Gifts"
                AppLanguage.FRENCH -> "Cadeaux"
                AppLanguage.SPANISH -> "Regalos"
            }
            "Ricorrenti" -> when (lang) {
                AppLanguage.ITALIAN -> "Ricorrenti"
                AppLanguage.ENGLISH -> "Subscriptions"
                AppLanguage.FRENCH -> "Abonnements"
                AppLanguage.SPANISH -> "Suscripciones"
            }
            "Altro" -> when (lang) {
                AppLanguage.ITALIAN -> "Altro"
                AppLanguage.ENGLISH -> "Other"
                AppLanguage.FRENCH -> "Autre"
                AppLanguage.SPANISH -> "Otro"
            }
            else -> category
        }
    }

    fun translateMonth(rawMonth: String, lang: AppLanguage): String {
        val parts = rawMonth.trim().split(" ")
        if (parts.isEmpty()) return rawMonth
        val name = parts[0].lowercase()
        val year = if (parts.size > 1) " " + parts[1] else ""
        
        val translatedName = when (name) {
            "gennaio" -> mapOf(AppLanguage.ITALIAN to "Gennaio", AppLanguage.ENGLISH to "January", AppLanguage.FRENCH to "Janvier", AppLanguage.SPANISH to "Enero")[lang]
            "febbraio" -> mapOf(AppLanguage.ITALIAN to "Febbraio", AppLanguage.ENGLISH to "February", AppLanguage.FRENCH to "Février", AppLanguage.SPANISH to "Febrero")[lang]
            "marzo" -> mapOf(AppLanguage.ITALIAN to "Marzo", AppLanguage.ENGLISH to "March", AppLanguage.FRENCH to "Mars", AppLanguage.SPANISH to "Marzo")[lang]
            "aprile" -> mapOf(AppLanguage.ITALIAN to "Aprile", AppLanguage.ENGLISH to "April", AppLanguage.FRENCH to "Avril", AppLanguage.SPANISH to "Abril")[lang]
            "maggio" -> mapOf(AppLanguage.ITALIAN to "Maggio", AppLanguage.ENGLISH to "May", AppLanguage.FRENCH to "Mai", AppLanguage.SPANISH to "Mayo")[lang]
            "giugno" -> mapOf(AppLanguage.ITALIAN to "Giugno", AppLanguage.ENGLISH to "June", AppLanguage.FRENCH to "Juin", AppLanguage.SPANISH to "Junio")[lang]
            "luglio" -> mapOf(AppLanguage.ITALIAN to "Luglio", AppLanguage.ENGLISH to "July", AppLanguage.FRENCH to "Juillet", AppLanguage.SPANISH to "Julio")[lang]
            "agosto" -> mapOf(AppLanguage.ITALIAN to "Agosto", AppLanguage.ENGLISH to "August", AppLanguage.FRENCH to "Août", AppLanguage.SPANISH to "Agosto")[lang]
            "settembre" -> mapOf(AppLanguage.ITALIAN to "Settembre", AppLanguage.ENGLISH to "September", AppLanguage.FRENCH to "Septembre", AppLanguage.SPANISH to "Septiembre")[lang]
            "ottobre" -> mapOf(AppLanguage.ITALIAN to "Ottobre", AppLanguage.ENGLISH to "October", AppLanguage.FRENCH to "Octobre", AppLanguage.SPANISH to "Octubre")[lang]
            "novembre" -> mapOf(AppLanguage.ITALIAN to "Novembre", AppLanguage.ENGLISH to "November", AppLanguage.FRENCH to "Novembre", AppLanguage.SPANISH to "Noviembre")[lang]
            "dicembre" -> mapOf(AppLanguage.ITALIAN to "Dicembre", AppLanguage.ENGLISH to "December", AppLanguage.FRENCH to "Décembre", AppLanguage.SPANISH to "Diciembre")[lang]
            else -> parts[0].replaceFirstChar { it.uppercase() }
        }
        return (translatedName ?: parts[0]) + year
    }
"""

if "fun translateCategory" not in content:
    content = content.replace("    fun get(", helpers + "\n    fun get(")

with open("src/main/java/it/fm/spese/AppStrings.kt", "w") as f:
    f.write(content)

print("Translation helpers added to AppStrings.kt.")

