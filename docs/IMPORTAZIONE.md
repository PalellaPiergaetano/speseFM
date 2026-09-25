# Importazione dati

## Importazione dall’app

Nella dashboard il comando di importazione apre il selettore file Android. L’app legge il nome quando disponibile e controlla anche la firma del contenuto:

- file con estensione `.csv`, o contenuto testuale senza estensione: parser CSV;
- file `.xlsx` o `.xlsm`: parser Excel OpenXML;
- il vecchio formato binario `.xls` non è supportato: va salvato da Excel come `.xlsx`.

Il controllo della firma evita che un CSV venga interpretato come XLSX quando il `DocumentProvider` restituisce un URI senza `DISPLAY_NAME`. Un file OpenXML viene riconosciuto dalla firma ZIP `PK`.

Un file non leggibile o privo di movimenti validi produce un messaggio di errore e non modifica i dati già presenti.

## Workbook Excel supportato

Il parser `.xlsx` legge direttamente il formato OpenXML senza dipendenze Excel sul dispositivo. Per ogni foglio:

1. legge `xl/workbook.xml` e le relazioni verso i worksheet;
2. risolve le stringhe condivise in `xl/sharedStrings.xml`;
3. ignora i fogli `template`, `RIEPILOGO` e `SOMMARIO`;
4. usa la riga 2 come intestazione delle categorie;
5. legge le righe 3-39 e le colonne A-F;
6. ignora la colonna `TOTALE`;
7. usa la colonna H come nota per gli elementi della categoria `Altro`;
8. conserva il nome del foglio come mese del movimento.

Il template originale contiene fogli mensili come `settembre 26`, `agosto 26` e `luglio 24`. Le intestazioni vengono normalizzate in categorie dell’app.

## CSV intermedio

Lo script `tools/import_sheet.py` usa solo la libreria standard Python e crea questo schema:

```csv
mese,riga,valori
settembre 26,2,"SPESA | TRASPORTI | BAR/RISTORANTI/LOCALI | ..."
```

`valori` contiene le celle della riga unite con ` | `. Il parser CSV dell’app:

- interpreta la riga 2 come intestazione;
- legge le righe 3-39;
- usa le prime sei colonne come categorie/importi;
- usa la colonna 8 come descrizione per `ALTRO`;
- ignora importi vuoti, non numerici o minori/uguali a zero.

Per generare il file:

```bash
python3 -m venv .venv
.venv/bin/python tools/import_sheet.py \
  "Foglio spese.xlsx" \
  tools/spese_importate.csv
```

Il file di output è locale e ignorato da Git.

## Numeri e formati

Sono accettati importi con punto o virgola decimale, con o senza simbolo `€`, ad esempio:

- `12.50`;
- `12,50`;
- `€ 12,50`.

Quando sono presenti sia punto sia virgola, l’ultimo separatore viene trattato come separatore decimale. Gli importi non interpretabili vengono scartati.

## Limiti noti

- il parser lavora sulle righe 3-39 del template mensile;
- il formato legacy `.xls` non è supportato;
- file Excel con layout diverso possono importare zero movimenti o categorie errate;
- l’importazione aggiunge i movimenti a quelli esistenti e non deduplica;
- il CSV esportato dall’app è un backup semplice e non è lo stesso CSV intermedio accettato dal parser;
- non viene salvata una data giornaliera, ma il nome del mese del foglio.