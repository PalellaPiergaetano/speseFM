# Architettura

## Panoramica

Spese FM è una app Android single-activity. L’interfaccia è costruita con Jetpack Compose; lo stato applicativo viene mantenuto nella composable principale e salvato localmente dopo ogni modifica.

```text
MainActivity
  └── SpeseAppWithSecurity
        ├── BiometricPrompt
        └── SpeseApp
              ├── Dashboard
              ├── Movimenti
              ├── Reports
              ├── AddExpenseDialog
              ├── XlsSheetImporter (XLSX/CSV)
              └── SharedPreferences (expense_store)
```

La logica è oggi concentrata in `app/src/main/java/it/fm/spese/MainActivity.kt`. Questa scelta mantiene piccolo l’MVP, ma aumenta la dimensione del file. I parser hanno test JVM in `app/src/test/java/it/fm/spese/ImporterTest.kt`.

## Modello dati

Ogni movimento è rappresentato da:

```kotlin
data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = "settembre 26"
)
```

Le categorie standard sono `Spesa`, `Trasporti`, `Bar / Ristoranti / Uscite`, `Mediche`, `Fitto / Bollette / Casa`, `Regali`, `Ricorrenti` e `Altro`. Il mapping riconosce anche varianti del foglio originale, come `BAR/RISTORANTI/LOCALI` e `FITTO/BOLLETTE`.

## Persistenza

La lista viene serializzata in una stringa con campi separati da tabulazione e righe separate da newline. Sono salvate anche queste impostazioni:

- `monthly_budget`;
- `privacy_mode`;
- `is_first_launch`.

Il budget è una singola impostazione globale dell’MVP, non un budget distinto per ogni mese. La cancellazione completa elimina movimenti e preferenze dell’app.

## Sicurezza

All’avvio viene mostrato `BiometricPrompt` con autenticatore biometrico forte o credenziale del dispositivo. Il lock è un controllo d’accesso all’interfaccia; i dati non sono sincronizzati e non esiste un account utente.

La modalità privacy nasconde gli importi nella UI, ma non modifica i dati memorizzati né i file esportati.

## Analisi e suggerimenti

I report calcolano aggregazioni in memoria:

- totale del filtro attivo;
- distribuzione per categoria;
- media mensile e giornaliera;
- spesa massima;
- totale e media mensile per anno.

Il suggerimento della dashboard è euristico: identifica la categoria con il totale più alto e propone di fissare un tetto mensile. Il parser delle frasi non chiama servizi AI: estrae importi e categorie con espressioni regolari e parole chiave locali.

## Evoluzione consigliata

Per trasformare l’MVP in una versione più robusta:

1. spostare modello e accesso dati in una `RoomDatabase`;
2. introdurre `ViewModel` e stato osservabile per separare UI e logica;
3. aggiungere identificativo, data completa, nota e valuta al movimento;
4. rendere il budget dipendente dal mese;
5. cifrare il database o usare storage cifrato per dati finanziari;
6. aggiungere test per aggregazioni, persistenza e casi di errore UI;
7. aggiungere backup/import con schema versionato;
8. valutare sincronizzazione cloud solo dopo aver definito autenticazione e modello privacy.