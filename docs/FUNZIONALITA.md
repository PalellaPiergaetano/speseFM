# Funzionalità dell'App Spese FM

## 1. Gestione Spese e Movimenti
- **Aggiunta manuale**: Dialog per l'inserimento di titolo, importo, categoria e data/mese.
- **Lista movimenti**: Visualizzazione cronologica/per mese delle spese effettuate.
- **Filtri e ricerca**: Filtraggio per mese e per categoria direttamente dalla dashboard.
- **Cancellazione**: Azione di eliminazione dalla lista dei movimenti.
- **Aggiunta IA (Smart)**: Analisi automatica del titolo della spesa per suggerire la categoria più appropriata.
- **Dettaglio movimento**: Visualizzazione di data, ora, categoria, importo e descrizione quando disponibili.

## 2. Promemoria e Lingue
- **Promemoria pagamenti**: Creazione di scadenze, importo, ricorrenza e numero massimo di pagamenti.
- **Pagamento da promemoria**: Registrazione del pagamento come nuova spesa e aggiornamento della ricorrenza.
- **Interfaccia multilingua**: Italiano, inglese, francese e spagnolo tramite `AppStrings.kt`.
- **Impostazioni**: Cambio lingua, privacy, sicurezza biometrica e accesso alla guida.

## 3. Dashboard e Statistiche (Report)
- **Riepilogo Mese**: Totale speso nel mese selezionato.
- **Budget**: Impostazione di un budget mensile, calcolo del rimanente e percentuale di utilizzo.
- **Categorie Principali**: Spesa, Trasporti, Bar/Ristoranti, con i rispettivi subtotali.
- **Suggerimento Intelligente**: Messaggi motivazionali o consigli basati sullo stato delle spese (es. "Sei nel budget", "Riduci le uscite").
- **Grafico a Torta (Pie Chart)**: Visualizzazione grafica della distribuzione delle spese.
- **Riepilogo Annuale**: Media mensile, mese di massima spesa e totale annuo.

## 4. Sicurezza e Privacy
- **Blocco Biometrico (Impronta/Volto)**: Richiesta di autenticazione per accedere all'app e ai dati sensibili.
- **Modalità Privacy (Cifre Nascoste)**: Pulsante per oscurare gli importi in tutta l'interfaccia (mostra `•••• €`), utile in luoghi pubblici.

## 5. Importazione (Da zero)
- **Supporto XLSX/XLSM**: Lettura nativa dei file Excel OpenXML ZIP senza dipendenze Excel sul dispositivo. Il vecchio formato binario `.xls` non è supportato.
- **Supporto CSV Intelligente**: Gestione delle virgolette, delle virgole decimali, del BOM e dei CSV senza estensione quando il contenuto è riconoscibile.
- **Due tracciati CSV**: Importazione del CSV intermedio generato da `tools/import_sheet.py` e del CSV di backup esportato dall'app.

## 6. Esportazione e Gestione Dati
- **Salvataggio Locale**: Utilizzo di SharedPreferences per la memorizzazione persistente locale.
- **Export CSV**: Esportazione sicura di tutte le spese in formato CSV di backup.
- **Reset Dati**: Opzione per eliminare tutte le transazioni con conferma di sicurezza.
