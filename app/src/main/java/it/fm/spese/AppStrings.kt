package it.fm.spese

import android.content.Context
import androidx.compose.runtime.staticCompositionLocalOf

enum class AppLanguage(val code: String, val displayName: String, val flag: String) {
    ITALIAN("it", "Italiano", "🇮🇹"),
    ENGLISH("en", "English", "🇬🇧"),
    FRENCH("fr", "Français", "🇫🇷"),
    SPANISH("es", "Español", "🇪🇸")
}

val LocalAppLanguage = staticCompositionLocalOf { AppLanguage.ITALIAN }

fun loadAppLanguage(context: Context): AppLanguage {
    val prefs = context.getSharedPreferences("app_settings", Context.MODE_PRIVATE)
    val code = prefs.getString("language_code", "it") ?: "it"
    return AppLanguage.values().find { it.code == code } ?: AppLanguage.ITALIAN
}

fun saveAppLanguage(context: Context, language: AppLanguage) {
    val prefs = context.getSharedPreferences("app_settings", Context.MODE_PRIVATE)
    prefs.edit().putString("language_code", language.code).apply()
}

object AppStrings {
    val aggiungi_una_nuova_spesa_con_il_pulsante_oppure_importa_un_file_xls_csv_con_lo_strumento_di_importazione = mapOf(
        AppLanguage.ITALIAN to "Aggiungi una nuova spesa con il pulsante + oppure importa un file XLS/CSV con lo strumento di importazione.",
        AppLanguage.ENGLISH to "Add a new expense with the + button or import an XLS/CSV file with the import tool.",
        AppLanguage.FRENCH to "Ajoutez une nouvelle dépense avec le bouton + ou importez un fichier XLS/CSV.",
        AppLanguage.SPANISH to "Agregue un nuevo gasto con el botón + o importe un archivo XLS/CSV."
    )
    val analisi_dettagliata_e_kpi_della_tua_spesa = mapOf(
        AppLanguage.ITALIAN to "Analisi dettagliata e KPI della tua spesa",
        AppLanguage.ENGLISH to "Detailed analysis and KPIs of your spending",
        AppLanguage.FRENCH to "Analyse détaillée et KPI de vos dépenses",
        AppLanguage.SPANISH to "Análisis detallado y KPIs de sus gastos"
    )
    val andamento_per_anno = mapOf(
        AppLanguage.ITALIAN to "Andamento per anno",
        AppLanguage.ENGLISH to "Yearly trend",
        AppLanguage.FRENCH to "Tendance annuelle",
        AppLanguage.SPANISH to "Tendencia anual"
    )
    val annulla = mapOf(
        AppLanguage.ITALIAN to "Annulla",
        AppLanguage.ENGLISH to "Cancel",
        AppLanguage.FRENCH to "Annuler",
        AppLanguage.SPANISH to "Cancelar"
    )
    val anteprima_ia = mapOf(
        AppLanguage.ITALIAN to "Anteprima IA",
        AppLanguage.ENGLISH to "AI Preview",
        AppLanguage.FRENCH to "Aperçu IA",
        AppLanguage.SPANISH to "Vista previa IA"
    )
    val app_bloccata = mapOf(
        AppLanguage.ITALIAN to "App Bloccata",
        AppLanguage.ENGLISH to "App Locked",
        AppLanguage.FRENCH to "Application verrouillée",
        AppLanguage.SPANISH to "Aplicación bloqueada"
    )
    val backup_csv = mapOf(
        AppLanguage.ITALIAN to "Backup CSV",
        AppLanguage.ENGLISH to "CSV Backup",
        AppLanguage.FRENCH to "Sauvegarde CSV",
        AppLanguage.SPANISH to "Copia de seguridad CSV"
    )
    val blocca_ora = mapOf(
        AppLanguage.ITALIAN to "Blocca ora",
        AppLanguage.ENGLISH to "Lock now",
        AppLanguage.FRENCH to "Verrouiller maintenant",
        AppLanguage.SPANISH to "Bloquear ahora"
    )
    val budget_mensile = mapOf(
        AppLanguage.ITALIAN to "Budget mensile",
        AppLanguage.ENGLISH to "Monthly budget",
        AppLanguage.FRENCH to "Budget mensuel",
        AppLanguage.SPANISH to "Presupuesto mensual"
    )
    val budget_aggiornato = mapOf(
        AppLanguage.ITALIAN to "Budget aggiornato!",
        AppLanguage.ENGLISH to "Budget updated!",
        AppLanguage.FRENCH to "Budget mis à jour !",
        AppLanguage.SPANISH to "¡Presupuesto actualizado!"
    )
    val cancella_tutti_i_dati = mapOf(
        AppLanguage.ITALIAN to "Cancella tutti i dati",
        AppLanguage.ENGLISH to "Clear all data",
        AppLanguage.FRENCH to "Effacer toutes les données",
        AppLanguage.SPANISH to "Borrar todos los datos"
    )
    val cancella_tutto = mapOf(
        AppLanguage.ITALIAN to "Cancella tutto",
        AppLanguage.ENGLISH to "Clear all",
        AppLanguage.FRENCH to "Tout effacer",
        AppLanguage.SPANISH to "Borrar todo"
    )
    val categoria = mapOf(
        AppLanguage.ITALIAN to "Categoria",
        AppLanguage.ENGLISH to "Category",
        AppLanguage.FRENCH to "Catégorie",
        AppLanguage.SPANISH to "Categoría"
    )
    val categorie_principali = mapOf(
        AppLanguage.ITALIAN to "Categorie principali",
        AppLanguage.ENGLISH to "Main categories",
        AppLanguage.FRENCH to "Principales catégories",
        AppLanguage.SPANISH to "Categorías principales"
    )
    val cerca_tra_le_spese = mapOf(
        AppLanguage.ITALIAN to "Cerca tra le spese...",
        AppLanguage.ENGLISH to "Search expenses...",
        AppLanguage.FRENCH to "Rechercher des dépenses...",
        AppLanguage.SPANISH to "Buscar gastos..."
    )
    val chiudi = mapOf(
        AppLanguage.ITALIAN to "Chiudi",
        AppLanguage.ENGLISH to "Close",
        AppLanguage.FRENCH to "Fermer",
        AppLanguage.SPANISH to "Cerrar"
    )
    val conferma = mapOf(
        AppLanguage.ITALIAN to "Conferma",
        AppLanguage.ENGLISH to "Confirm",
        AppLanguage.FRENCH to "Confirmer",
        AppLanguage.SPANISH to "Confirmar"
    )
    val data_gg_mm_aaaa = mapOf(
        AppLanguage.ITALIAN to "Data (gg/mm/aaaa)",
        AppLanguage.ENGLISH to "Date (dd/mm/yyyy)",
        AppLanguage.FRENCH to "Date (jj/mm/aaaa)",
        AppLanguage.SPANISH to "Fecha (dd/mm/aaaa)"
    )
    val data_scadenza_gg_mm_aaaa = mapOf(
        AppLanguage.ITALIAN to "Data scadenza (gg/mm/aaaa)",
        AppLanguage.ENGLISH to "Due date (dd/mm/yyyy)",
        AppLanguage.FRENCH to "Date d'échéance (jj/mm/aaaa)",
        AppLanguage.SPANISH to "Fecha de vencimiento (dd/mm/aaaa)"
    )
    val descrizione_pagamento = mapOf(
        AppLanguage.ITALIAN to "Descrizione pagamento",
        AppLanguage.ENGLISH to "Payment description",
        AppLanguage.FRENCH to "Description du paiement",
        AppLanguage.SPANISH to "Descripción del pago"
    )
    val distribuzione_spese = mapOf(
        AppLanguage.ITALIAN to "Distribuzione spese",
        AppLanguage.ENGLISH to "Expense distribution",
        AppLanguage.FRENCH to "Distribution des dépenses",
        AppLanguage.SPANISH to "Distribución de gastos"
    )
    val errore_durante_l_esportazione = mapOf(
        AppLanguage.ITALIAN to "Errore durante l'esportazione.",
        AppLanguage.ENGLISH to "Error during export.",
        AppLanguage.FRENCH to "Erreur lors de l'exportation.",
        AppLanguage.SPANISH to "Error durante la exportación."
    )
    val esporta = mapOf(
        AppLanguage.ITALIAN to "Esporta",
        AppLanguage.ENGLISH to "Export",
        AppLanguage.FRENCH to "Exporter",
        AppLanguage.SPANISH to "Exportar"
    )
    val file_csv_esportato_con_successo = mapOf(
        AppLanguage.ITALIAN to "File CSV esportato con successo!",
        AppLanguage.ENGLISH to "CSV file exported successfully!",
        AppLanguage.FRENCH to "Fichier CSV exporté avec succès !",
        AppLanguage.SPANISH to "¡Archivo CSV exportado con éxito!"
    )
    val gestione_sicurezza = mapOf(
        AppLanguage.ITALIAN to "Gestione & Sicurezza",
        AppLanguage.ENGLISH to "Management & Security",
        AppLanguage.FRENCH to "Gestion & Sécurité",
        AppLanguage.SPANISH to "Gestión y Seguridad"
    )
    val guida = mapOf(
        AppLanguage.ITALIAN to "Guida",
        AppLanguage.ENGLISH to "Guide",
        AppLanguage.FRENCH to "Guide",
        AppLanguage.SPANISH to "Guía"
    )
    val i_tuoi_dati_finanziari_sono_protetti_con_la_sicurezza_biometrica = mapOf(
        AppLanguage.ITALIAN to "I tuoi dati finanziari sono protetti con la sicurezza biometrica.",
        AppLanguage.ENGLISH to "Your financial data is protected with biometric security.",
        AppLanguage.FRENCH to "Vos données financières sont protégées par la sécurité biométrique.",
        AppLanguage.SPANISH to "Sus datos financieros están protegidos con seguridad biométrica."
    )
    val importa = mapOf(
        AppLanguage.ITALIAN to "Importa",
        AppLanguage.ENGLISH to "Import",
        AppLanguage.FRENCH to "Importer",
        AppLanguage.SPANISH to "Importar"
    )
    val importo = mapOf(
        AppLanguage.ITALIAN to "Importo",
        AppLanguage.ENGLISH to "Amount",
        AppLanguage.FRENCH to "Montant",
        AppLanguage.SPANISH to "Importe"
    )
    val imposta_il_tetto_di_spesa_desiderato_per_ciascun_mese_l_anello_di_progresso_si_aggiorner_automaticamente = mapOf(
        AppLanguage.ITALIAN to "Imposta il tetto di spesa desiderato per ciascun mese. L'anello di progresso si aggiornerà automaticamente.",
        AppLanguage.ENGLISH to "Set the desired spending limit for each month. The progress ring will update automatically.",
        AppLanguage.FRENCH to "Définissez la limite de dépenses pour chaque mois.",
        AppLanguage.SPANISH to "Establezca el límite de gasto para cada mes."
    )
    val impostazioni = mapOf(
        AppLanguage.ITALIAN to "Impostazioni",
        AppLanguage.ENGLISH to "Settings",
        AppLanguage.FRENCH to "Paramètres",
        AppLanguage.SPANISH to "Ajustes"
    )
    val impostazioni_lingua = mapOf(
        AppLanguage.ITALIAN to "Impostazioni Lingua",
        AppLanguage.ENGLISH to "Language Settings",
        AppLanguage.FRENCH to "Paramètres de langue",
        AppLanguage.SPANISH to "Configuración de idioma"
    )
    val indietro = mapOf(
        AppLanguage.ITALIAN to "Indietro",
        AppLanguage.ENGLISH to "Back",
        AppLanguage.FRENCH to "Retour",
        AppLanguage.SPANISH to "Volver"
    )
    val inserimento_ia = mapOf(
        AppLanguage.ITALIAN to "Inserimento IA",
        AppLanguage.ENGLISH to "AI Entry",
        AppLanguage.FRENCH to "Saisie IA",
        AppLanguage.SPANISH to "Entrada IA"
    )
    val lingua = mapOf(
        AppLanguage.ITALIAN to "Lingua",
        AppLanguage.ENGLISH to "Language",
        AppLanguage.FRENCH to "Langue",
        AppLanguage.SPANISH to "Idioma"
    )
    val manuale = mapOf(
        AppLanguage.ITALIAN to "Manuale",
        AppLanguage.ENGLISH to "Manual",
        AppLanguage.FRENCH to "Manuel",
        AppLanguage.SPANISH to "Manual"
    )
    val media_giorno = mapOf(
        AppLanguage.ITALIAN to "Media / giorno",
        AppLanguage.ENGLISH to "Average / day",
        AppLanguage.FRENCH to "Moyenne / jour",
        AppLanguage.SPANISH to "Promedio / día"
    )
    val mostra_tutti = mapOf(
        AppLanguage.ITALIAN to "Mostra tutti",
        AppLanguage.ENGLISH to "Show all",
        AppLanguage.FRENCH to "Tout afficher",
        AppLanguage.SPANISH to "Mostrar todos"
    )
    val movimenti = mapOf(
        AppLanguage.ITALIAN to "Movimenti",
        AppLanguage.ENGLISH to "Transactions",
        AppLanguage.FRENCH to "Mouvements",
        AppLanguage.SPANISH to "Movimientos"
    )
    val nessun_movimento_valido_trovato_nel_file = mapOf(
        AppLanguage.ITALIAN to "Nessun movimento valido trovato nel file.",
        AppLanguage.ENGLISH to "No valid transactions found in the file.",
        AppLanguage.FRENCH to "Aucun mouvement valide trouvé dans le fichier.",
        AppLanguage.SPANISH to "No se encontraron transacciones válidas en el archivo."
    )
    val nessun_promemoria_attivo_aggiungine_uno_per_non_dimenticare_le_tue_scadenze = mapOf(
        AppLanguage.ITALIAN to "Nessun promemoria attivo. Aggiungine uno per non dimenticare le tue scadenze.",
        AppLanguage.ENGLISH to "No active reminders. Add one to remember your due dates.",
        AppLanguage.FRENCH to "Aucun rappel actif. Ajoutez-en un pour vos échéances.",
        AppLanguage.SPANISH to "No hay recordatorios activos. Agregue uno para sus fechas de vencimiento."
    )
    val nessuna_spesa_presente = mapOf(
        AppLanguage.ITALIAN to "Nessuna spesa presente",
        AppLanguage.ENGLISH to "No expenses present",
        AppLanguage.FRENCH to "Aucune dépense présente",
        AppLanguage.SPANISH to "No hay gastos presentes"
    )
    val nessuna_spesa_trovata = mapOf(
        AppLanguage.ITALIAN to "Nessuna spesa trovata",
        AppLanguage.ENGLISH to "No expenses found",
        AppLanguage.FRENCH to "Aucune dépense trouvée",
        AppLanguage.SPANISH to "No se encontraron gastos"
    )
    val numero_max_pagamenti_mese = mapOf(
        AppLanguage.ITALIAN to "Numero max pagamenti/rate",
        AppLanguage.ENGLISH to "Max payments/installments",
        AppLanguage.FRENCH to "Nombre max de paiements",
        AppLanguage.SPANISH to "Número máx de pagos"
    )
    val nuova_spesa = mapOf(
        AppLanguage.ITALIAN to "Nuova spesa",
        AppLanguage.ENGLISH to "New expense",
        AppLanguage.FRENCH to "Nouvelle dépense",
        AppLanguage.SPANISH to "Nuevo gasto"
    )
    val nuovo_promemoria = mapOf(
        AppLanguage.ITALIAN to "Nuovo promemoria",
        AppLanguage.ENGLISH to "New reminder",
        AppLanguage.FRENCH to "Nouveau rappel",
        AppLanguage.SPANISH to "Nuevo recordatorio"
    )
    val paga_ora = mapOf(
        AppLanguage.ITALIAN to "Paga ora",
        AppLanguage.ENGLISH to "Pay now",
        AppLanguage.FRENCH to "Payer maintenant",
        AppLanguage.SPANISH to "Pagar ahora"
    )
    val panoramica_spese = mapOf(
        AppLanguage.ITALIAN to "Panoramica Spese",
        AppLanguage.ENGLISH to "Expense overview",
        AppLanguage.FRENCH to "Aperçu des dépenses",
        AppLanguage.SPANISH to "Resumen de gastos"
    )
    val privacy = mapOf(
        AppLanguage.ITALIAN to "Privacy",
        AppLanguage.ENGLISH to "Privacy",
        AppLanguage.FRENCH to "Confidentialité",
        AppLanguage.SPANISH to "Privacidad"
    )
    val promemoria = mapOf(
        AppLanguage.ITALIAN to "Promemoria",
        AppLanguage.ENGLISH to "Reminders",
        AppLanguage.FRENCH to "Rappels",
        AppLanguage.SPANISH to "Recordatorios"
    )
    val promemoria_pagamenti = mapOf(
        AppLanguage.ITALIAN to "Promemoria Pagamenti",
        AppLanguage.ENGLISH to "Payment Reminders",
        AppLanguage.FRENCH to "Rappels de paiement",
        AppLanguage.SPANISH to "Recordatorios de pagos"
    )
    val promemoria_salvato = mapOf(
        AppLanguage.ITALIAN to "Promemoria salvato!",
        AppLanguage.ENGLISH to "Reminder saved!",
        AppLanguage.FRENCH to "Rappel enregistré !",
        AppLanguage.SPANISH to "¡Recordatorio guardado!"
    )
    val prova_a_modificare_la_ricerca_o_il_filtro = mapOf(
        AppLanguage.ITALIAN to "Prova a modificare la ricerca o il filtro",
        AppLanguage.ENGLISH to "Try modifying the search or filter",
        AppLanguage.FRENCH to "Essayez de modifier la recherche ou le filtre",
        AppLanguage.SPANISH to "Intente modificar la búsqueda o el filtro"
    )
    val report_statistiche = mapOf(
        AppLanguage.ITALIAN to "Report & Statistiche",
        AppLanguage.ENGLISH to "Reports & Statistics",
        AppLanguage.FRENCH to "Rapports et statistiques",
        AppLanguage.SPANISH to "Informes y estadísticas"
    )
    val reset_dati = mapOf(
        AppLanguage.ITALIAN to "Reset dati",
        AppLanguage.ENGLISH to "Reset data",
        AppLanguage.FRENCH to "Réinitialiser les données",
        AppLanguage.SPANISH to "Restablecer datos"
    )
    val ricorrenza = mapOf(
        AppLanguage.ITALIAN to "Ricorrenza mensile",
        AppLanguage.ENGLISH to "Monthly recurrence",
        AppLanguage.FRENCH to "Récurrence mensuelle",
        AppLanguage.SPANISH to "Recurrencia mensual"
    )
    val salta = mapOf(
        AppLanguage.ITALIAN to "Salta",
        AppLanguage.ENGLISH to "Skip",
        AppLanguage.FRENCH to "Passer",
        AppLanguage.SPANISH to "Omitir"
    )
    val salva = mapOf(
        AppLanguage.ITALIAN to "Salva",
        AppLanguage.ENGLISH to "Save",
        AppLanguage.FRENCH to "Enregistrer",
        AppLanguage.SPANISH to "Guardar"
    )
    val salva_promemoria = mapOf(
        AppLanguage.ITALIAN to "Salva promemoria",
        AppLanguage.ENGLISH to "Save reminder",
        AppLanguage.FRENCH to "Enregistrer le rappel",
        AppLanguage.SPANISH to "Guardar recordatorio"
    )
    val sblocca_con_impronta = mapOf(
        AppLanguage.ITALIAN to "Sblocca con impronta",
        AppLanguage.ENGLISH to "Unlock with fingerprint",
        AppLanguage.FRENCH to "Déverrouiller avec empreinte",
        AppLanguage.SPANISH to "Desbloquear con huella"
    )
    val scadenze = mapOf(
        AppLanguage.ITALIAN to "Scadenze",
        AppLanguage.ENGLISH to "Deadlines",
        AppLanguage.FRENCH to "Échéances",
        AppLanguage.SPANISH to "Vencimientos"
    )
    val scegli_la_tua_lingua_preferita_per_l_interfaccia_dell_applicazione = mapOf(
        AppLanguage.ITALIAN to "Scegli la tua lingua preferita per l'interfaccia dell'applicazione",
        AppLanguage.ENGLISH to "Choose your preferred language for the application interface",
        AppLanguage.FRENCH to "Choisissez votre langue préférée",
        AppLanguage.SPANISH to "Elija su idioma preferido"
    )
    val scrivi_o_incolla_la_spesa_in_testo_libero_es_pranzo_di_lavoro_18_50_euro_al_ristorante = mapOf(
        AppLanguage.ITALIAN to "Scrivi o incolla la spesa in testo libero (es. 'Pranzo di lavoro 18.50 euro al ristorante'):",
        AppLanguage.ENGLISH to "Write or paste the expense in free text (e.g., 'Lunch 18.50 euro'):",
        AppLanguage.FRENCH to "Écrivez ou collez la dépense en texte libre :",
        AppLanguage.SPANISH to "Escriba o pegue el gasto en texto libre:"
    )
    val sei_sicuro_di_voler_eliminare_definitivamente_tutte_le_spese_registrate_nell_app_l_operazione_non_e_reversibile = mapOf(
        AppLanguage.ITALIAN to "Sei sicuro di voler eliminare definitivamente tutte le spese registrate nell'app? L'operazione non è reversibile.",
        AppLanguage.ENGLISH to "Are you sure you want to permanently delete all expenses? This operation cannot be undone.",
        AppLanguage.FRENCH to "Êtes-vous sûr de vouloir supprimer définitivement toutes les dépenses ?",
        AppLanguage.SPANISH to "¿Está seguro de que desea eliminar permanentemente todos los gastos?"
    )
    val seleziona_categoria = mapOf(
        AppLanguage.ITALIAN to "Seleziona categoria",
        AppLanguage.ENGLISH to "Select category",
        AppLanguage.FRENCH to "Sélectionner une catégorie",
        AppLanguage.SPANISH to "Seleccionar categoría"
    )
    val sicurezza = mapOf(
        AppLanguage.ITALIAN to "Sicurezza",
        AppLanguage.ENGLISH to "Security",
        AppLanguage.FRENCH to "Sécurité",
        AppLanguage.SPANISH to "Seguridad"
    )
    val spesa_max = mapOf(
        AppLanguage.ITALIAN to "Spesa max",
        AppLanguage.ENGLISH to "Max expense",
        AppLanguage.FRENCH to "Dépense max",
        AppLanguage.SPANISH to "Gasto máx"
    )
    val spesa_eliminata = mapOf(
        AppLanguage.ITALIAN to "Spesa eliminata",
        AppLanguage.ENGLISH to "Expense deleted",
        AppLanguage.FRENCH to "Dépense supprimée",
        AppLanguage.SPANISH to "Gasto eliminado"
    )
    val suggerimenti_rapidi = mapOf(
        AppLanguage.ITALIAN to "Suggerimenti rapidi:",
        AppLanguage.ENGLISH to "Quick suggestions:",
        AppLanguage.FRENCH to "Suggestions rapides :",
        AppLanguage.SPANISH to "Sugerencias rápidas:"
    )
    val suggerimento_intelligente = mapOf(
        AppLanguage.ITALIAN to "Suggerimento Intelligente",
        AppLanguage.ENGLISH to "Smart Suggestion",
        AppLanguage.FRENCH to "Suggestion intelligente",
        AppLanguage.SPANISH to "Sugerencia inteligente"
    )
    val svuota = mapOf(
        AppLanguage.ITALIAN to "Svuota",
        AppLanguage.ENGLISH to "Clear",
        AppLanguage.FRENCH to "Vider",
        AppLanguage.SPANISH to "Vaciar"
    )
    val tutorial_app = mapOf(
        AppLanguage.ITALIAN to "Tutorial app",
        AppLanguage.ENGLISH to "App tutorial",
        AppLanguage.FRENCH to "Tutoriel de l'application",
        AppLanguage.SPANISH to "Tutorial de la app"
    )
    val tutte_le_categorie = mapOf(
        AppLanguage.ITALIAN to "Tutte le categorie",
        AppLanguage.ENGLISH to "All categories",
        AppLanguage.FRENCH to "Toutes les catégories",
        AppLanguage.SPANISH to "Todas las categorías"
    )
    val tutte_le_tue_uscite = mapOf(
        AppLanguage.ITALIAN to "Tutte le tue uscite",
        AppLanguage.ENGLISH to "All your expenses",
        AppLanguage.FRENCH to "Toutes vos dépenses",
        AppLanguage.SPANISH to "Todos sus gastos"
    )
    val tutti_i_mesi = mapOf(
        AppLanguage.ITALIAN to "Tutti i mesi",
        AppLanguage.ENGLISH to "All months",
        AppLanguage.FRENCH to "Tous les mois",
        AppLanguage.SPANISH to "Todos los meses"
    )
    val tutti_i_dati_sono_stati_cancellati = mapOf(
        AppLanguage.ITALIAN to "Tutti i dati sono stati cancellati!",
        AppLanguage.ENGLISH to "All data has been cleared!",
        AppLanguage.FRENCH to "Toutes les données ont été effacées !",
        AppLanguage.SPANISH to "¡Todos los datos han sido borrados!"
    )
    val ultimi_movimenti = mapOf(
        AppLanguage.ITALIAN to "Ultimi Movimenti",
        AppLanguage.ENGLISH to "Recent transactions",
        AppLanguage.FRENCH to "Derniers mouvements",
        AppLanguage.SPANISH to "Últimos movimientos"
    )
    val vedi_tutte = mapOf(
        AppLanguage.ITALIAN to "Vedi tutte",
        AppLanguage.ENGLISH to "See all",
        AppLanguage.FRENCH to "Voir tout",
        AppLanguage.SPANISH to "Ver todo"
    )
    val xls_csv = mapOf(
        AppLanguage.ITALIAN to "XLS / CSV",
        AppLanguage.ENGLISH to "XLS / CSV",
        AppLanguage.FRENCH to "XLS / CSV",
        AppLanguage.SPANISH to "XLS / CSV"
    )
    val es_spesa_supermercato_35_40 = mapOf(
        AppLanguage.ITALIAN to "es. Spesa supermercato 35.40€",
        AppLanguage.ENGLISH to "e.g. Supermarket expense 35.40€",
        AppLanguage.FRENCH to "ex. Supermarché 35.40€",
        AppLanguage.SPANISH to "ej. Supermercado 35.40€"
    )
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
    val elimina = mapOf(
        AppLanguage.ITALIAN to "Elimina",
        AppLanguage.ENGLISH to "Delete",
        AppLanguage.FRENCH to "Supprimer",
        AppLanguage.SPANISH to "Eliminar"
    )
    val descrizione = mapOf(
        AppLanguage.ITALIAN to "Descrizione",
        AppLanguage.ENGLISH to "Description",
        AppLanguage.FRENCH to "Description",
        AppLanguage.SPANISH to "Descripción"
    )
    val mese = mapOf(
        AppLanguage.ITALIAN to "Mese",
        AppLanguage.ENGLISH to "Month",
        AppLanguage.FRENCH to "Mois",
        AppLanguage.SPANISH to "Mes"
    )


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
    fun get(map: Map<AppLanguage, String>, lang: AppLanguage): String = map[lang] ?: map[AppLanguage.ITALIAN]!!
}
