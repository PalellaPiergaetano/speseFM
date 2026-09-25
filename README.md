# Spese FM

### Trasforma le tue spese in scelte migliori.

Spese FM è il tuo centro di controllo personale per capire dove finiscono i soldi e ritrovare margine, senza complicare la vita con fogli di calcolo. Importa lo storico che hai già, registra una nuova uscita in pochi secondi e lascia che report chiari e suggerimenti mirati trasformino i numeri in decisioni concrete.

Tutto resta sul tuo dispositivo: i tuoi dati finanziari rimangono privati, disponibili anche quando non hai una connessione.

**Importa. Capisci. Risparmia.**

## Perché Spese FM

- **Parti da ciò che hai già**: importa il tuo workbook Excel o un CSV senza ricopiare mesi di movimenti.
- **Registra al volo**: scrivi una frase come `cena 24,50` e l’app riconosce importo e categoria.
- **Vedi il quadro completo**: dashboard, grafico a ciambella, medie, spesa massima e confronto tra anni.
- **Agisci sui dati**: imposta un budget e ricevi un suggerimento sulla categoria che pesa di più.
- **Proteggi ciò che conta**: biometria all’accesso e modalità privacy per nascondere gli importi in un tocco.

## Stato del progetto

Il repository contiene un MVP funzionante in Kotlin e Jetpack Compose. Il flusso attuale è pensato per un singolo dispositivo: i dati vengono salvati localmente e non vengono inviati a un server.

### Release beta

La beta corrente è `1.0-beta01` (`versionCode 2`). L’APK è disponibile nel file `Spese_FM_Beta_v1.0.apk` nella root del repository. Per installarlo su un dispositivo con debug USB attivo:

```bash
adb install -r Spese_FM_Beta_v1.0.apk
```

Funzioni disponibili:

- onboarding iniziale con guida alle funzioni;
- sblocco con biometria o credenziale del dispositivo;
- dashboard con totale, budget, progresso e suggerimento di risparmio;
- inserimento manuale e inserimento da frase naturale, ad esempio `cena 24,50`;
- riconoscimento locale di importo e categoria tramite regole;
- importazione di file `.xlsx`, `.xlsm` e `.csv`, con rilevamento del formato e del delimitatore anche quando il provider Android non restituisce l'estensione;
- filtro per mese e categoria;
- elenco movimenti con eliminazione;
- report con grafico a ciambella, percentuali, media mensile, media giornaliera e spesa massima;
- confronto aggregato per anno;
- modalità privacy per nascondere gli importi;
- esportazione dei movimenti in CSV;
- cancellazione completa dei dati dal dispositivo.

## Requisiti

- macOS, Linux o Windows;
- Android Studio recente;
- JDK 21;
- Android SDK Platform 35;
- Android SDK Build Tools 35.0.0;
- Android SDK Platform-Tools;
- connessione Internet al primo build per scaricare Gradle e dipendenze.

Il progetto usa `compileSdk = 35`, `targetSdk = 35`, `minSdk = 26`, Android Gradle Plugin 9.4.1, Kotlin 2.2.10 e il Gradle Wrapper 9.6.0. Il file `local.properties` contiene il percorso SDK della macchina e non viene versionato.

## Avvio in Android Studio

1. Clona il repository e apri la cartella in Android Studio.
2. Attendi la sincronizzazione Gradle.
3. Se richiesto, seleziona un JDK 21 in **Settings > Build, Execution, Deployment > Build Tools > Gradle**.
4. Seleziona un emulatore o collega un dispositivo con il debug USB attivo.
5. Premi **Run** sul modulo `app`.

Il primo avvio mostra l’onboarding e richiede l’autenticazione biometrica. Su un emulatore senza biometria configurata è possibile usare la credenziale del dispositivo, se impostata.

## Build da terminale

Dal root del progetto:

```bash
./gradlew assembleDebug
```

APK generato:

```text
app/build/outputs/apk/debug/app-debug.apk
```

Per installare su un dispositivo collegato:

```bash
./gradlew installDebug
```

Controlli utili:

```bash
./gradlew :app:compileDebugKotlin
./gradlew lint
./gradlew test
```

Sono presenti test JVM per il parser XLSX/CSV; `lint`, test e compilazione sono i controlli disponibili.

## Struttura

```text
.
├── app/
│   ├── build.gradle.kts
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── java/it/fm/spese/MainActivity.kt
│       └── res/values/styles.xml
├── docs/
├── tools/import_sheet.py
├── build.gradle.kts
├── settings.gradle.kts
└── gradlew
```

`MainActivity.kt` contiene attualmente UI, stato locale, persistenza, import/export, parser delle frasi e grafici. Per una crescita ulteriore conviene separare questi ruoli in `data`, `domain` e `ui`.

## Dati e privacy

Le spese, il budget, la modalità privacy e lo stato dell’onboarding vengono salvati in `SharedPreferences` con la chiave `expense_store`. I dati restano sul dispositivo. La biometria protegge l’accesso all’interfaccia, ma l’MVP non usa ancora cifratura applicativa dedicata del contenuto salvato.

Il backup CSV è creato dall’utente tramite il selettore file di Android. L’esportazione non è cifrata: trattare il file come dato finanziario sensibile.

## Importazione

L’app importa direttamente il workbook Excel originale riconoscendo i fogli mensili e le righe operative del template. È supportato anche il CSV intermedio prodotto dallo script Python. La specifica completa è in [docs/IMPORTAZIONE.md](docs/IMPORTAZIONE.md).

Per generare il CSV dal workbook usando esclusivamente il venv del progetto:

```bash
python3 -m venv .venv       # solo la prima volta
.venv/bin/python tools/import_sheet.py
```

Lo script usa solo la libreria standard Python e genera `tools/spese_importate.csv`, che è ignorato da Git.

## Documentazione tecnica

- [Funzionalità](docs/FUNZIONALITA.md)
- [Architettura e stato](docs/ARCHITETTURA.md)
- [Formato e importazione dati](docs/IMPORTAZIONE.md)

## Repository

Repository GitHub: <https://github.com/PalellaPiergaetano/speseFM>