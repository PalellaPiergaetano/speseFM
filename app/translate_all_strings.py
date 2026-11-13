import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

replacements = [
    ('"Sblocca con Impronta"', 'AppStrings.get(AppStrings.sblocca_con_impronta, LocalAppLanguage.current)'),
    ('"Cancella tutti i dati"', 'AppStrings.get(AppStrings.cancella_tutti_i_dati, LocalAppLanguage.current)'),
    ('"Cancella tutto"', 'AppStrings.get(AppStrings.cancella_tutto, LocalAppLanguage.current)'),
    ('"Annulla"', 'AppStrings.get(AppStrings.annulla, LocalAppLanguage.current)'),
    ('"Salta"', 'AppStrings.get(AppStrings.salta, LocalAppLanguage.current)'),
    ('"Indietro"', 'AppStrings.get(AppStrings.indietro, LocalAppLanguage.current)'),
    ('"Panoramica Spese"', 'AppStrings.get(AppStrings.panoramica_spese, LocalAppLanguage.current)'),
    ('"Ultimi Movimenti"', 'AppStrings.get(AppStrings.ultimi_movimenti, LocalAppLanguage.current)'),
    ('"Nessuna spesa presente"', 'AppStrings.get(AppStrings.nessuna_spesa_presente, LocalAppLanguage.current)'),
    ('"Gestione & Sicurezza"', 'AppStrings.get(AppStrings.gestione_sicurezza, LocalAppLanguage.current)'),
    ('"Privacy"', 'AppStrings.get(AppStrings.privacy, LocalAppLanguage.current)'),
    ('"Sicurezza"', 'AppStrings.get(AppStrings.sicurezza, LocalAppLanguage.current)'),
    ('"Blocca ora"', 'AppStrings.get(AppStrings.blocca_ora, LocalAppLanguage.current)'),
    ('"Importa"', 'AppStrings.get(AppStrings.importa, LocalAppLanguage.current)'),
    ('"XLS / CSV"', 'AppStrings.get(AppStrings.xls_csv, LocalAppLanguage.current)'),
    ('"Esporta"', 'AppStrings.get(AppStrings.esporta, LocalAppLanguage.current)'),
    ('"Backup CSV"', 'AppStrings.get(AppStrings.backup_csv, LocalAppLanguage.current)'),
    ('"Guida"', 'AppStrings.get(AppStrings.guida, LocalAppLanguage.current)'),
    ('"Tutorial app"', 'AppStrings.get(AppStrings.tutorial_app, LocalAppLanguage.current)'),
    ('"Svuota"', 'AppStrings.get(AppStrings.svuota, LocalAppLanguage.current)'),
    ('"Reset dati"', 'AppStrings.get(AppStrings.reset_dati, LocalAppLanguage.current)'),
    ('"Categorie principali"', 'AppStrings.get(AppStrings.categorie_principali, LocalAppLanguage.current)'),
    ('"Suggerimento Intelligente"', 'AppStrings.get(AppStrings.suggerimento_intelligente, LocalAppLanguage.current)'),
    ('"Movimenti"', 'AppStrings.get(AppStrings.movimenti, LocalAppLanguage.current)'),
    ('"Tutte le tue uscite"', 'AppStrings.get(AppStrings.tutte_le_tue_uscite, LocalAppLanguage.current)'),
    ('"Cerca tra le spese..."', 'AppStrings.get(AppStrings.cerca_tra_le_spese, LocalAppLanguage.current)'),
    ('"Nessuna spesa trovata"', 'AppStrings.get(AppStrings.nessuna_spesa_trovata, LocalAppLanguage.current)'),
    ('"Prova a modificare la ricerca o il filtro"', 'AppStrings.get(AppStrings.prova_a_modificare_la_ricerca_o_il_filtro, LocalAppLanguage.current)'),
    ('"Report & Statistiche"', 'AppStrings.get(AppStrings.report_statistiche, LocalAppLanguage.current)'),
    ('"Analisi dettagliata e KPI della tua spesa"', 'AppStrings.get(AppStrings.analisi_dettagliata_e_kpi_della_tua_spesa, LocalAppLanguage.current)'),
    ('"Media / Giorno"', 'AppStrings.get(AppStrings.media_giorno, LocalAppLanguage.current)'),
    ('"Spesa Max"', 'AppStrings.get(AppStrings.spesa_max, LocalAppLanguage.current)'),
    ('"Andamento per Anno"', 'AppStrings.get(AppStrings.andamento_per_anno, LocalAppLanguage.current)'),
    ('"Distribuzione Spese"', 'AppStrings.get(AppStrings.distribuzione_spese, LocalAppLanguage.current)'),
    ('"Nuova Spesa"', 'AppStrings.get(AppStrings.nuova_spesa, LocalAppLanguage.current)'),
    ('"Inserimento IA"', 'AppStrings.get(AppStrings.inserimento_ia, LocalAppLanguage.current)'),
    ('"Manuale"', 'AppStrings.get(AppStrings.manuale, LocalAppLanguage.current)'),
    ('"Suggerimenti rapidi:"', 'AppStrings.get(AppStrings.suggerimenti_rapidi, LocalAppLanguage.current)'),
    ('"Anteprima IA"', 'AppStrings.get(AppStrings.anteprima_ia, LocalAppLanguage.current)'),
    ('"Descrizione"', 'AppStrings.get(AppStrings.descrizione, LocalAppLanguage.current)'),
    ('"Importo (€)"', 'AppStrings.get(AppStrings.importo, LocalAppLanguage.current)'),
    ('"Categoria"', 'AppStrings.get(AppStrings.categoria, LocalAppLanguage.current)'),
    ('"Seleziona categoria"', 'AppStrings.get(AppStrings.seleziona_categoria, LocalAppLanguage.current)'),
    ('"Budget Mensile"', 'AppStrings.get(AppStrings.budget_mensile, LocalAppLanguage.current)'),
    ('"Salva"', 'AppStrings.get(AppStrings.salva, LocalAppLanguage.current)')
]

for old, new in replacements:
    content = content.replace(old, new)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("All hardcoded strings translated successfully.")

