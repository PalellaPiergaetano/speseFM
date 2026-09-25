# Spese

App Android in Kotlin e Jetpack Compose per sostituire il foglio spese mensile.

## Funzioni MVP

- Dashboard del mese con totale e ultimi movimenti.
- Inserimento rapido di una spesa dal pulsante `+`.
- Report per categoria con grafico a barre.
- Suggerimento automatico sulla categoria con maggiore impatto.
- Script Python per estrarre il workbook originale in CSV.

## Ambiente Python

Il venv del progetto e `.venv` e va usato esclusivamente per gli strumenti Python:

```bash
.venv/bin/python tools/import_sheet.py
```

L'app Android viene aperta e compilata da Android Studio tramite il progetto Gradle nella cartella principale. Sul computer attuale non risultano Android SDK e Gradle nel PATH; serve configurarli in Android Studio per eseguire l'app su emulatore o dispositivo.