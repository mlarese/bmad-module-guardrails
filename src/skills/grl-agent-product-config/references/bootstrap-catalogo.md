# Costruire o importare il catalogo

Senza catalogo non esiste configurazione validabile, solo una lettura del documento. Questo è il lavoro che si fa una volta per linea di prodotto, e che rende tutto il resto ripetibile.

La forma di arrivo è sempre quella di `references/schema-catalogo.md`. Cambia solo da dove si parte.

## Primo passo: rileva lo stato

Chiedi una cosa sola, e la risposta sceglie il percorso: **dove sono scritte oggi le regole di compatibilità?**

| Risposta | Percorso |
| --- | --- |
| «da nessuna parte, le sappiamo» | Intervista |
| «nelle schede tecniche, nei listini, nei preventivi vecchi» | Estrazione |
| «nel gestionale, nel configuratore, in un Excel» | Importazione |

Le tre non si escludono: quasi sempre l'estrazione copre l'80% e l'intervista chiude il resto. Non tentare di coprire tutta la linea di prodotto al primo giro.

Qualunque sia il percorso, il punto di partenza del file è `{skill-root}/assets/catalogo-scheletro.yaml`: copialo nella cartella dei cataloghi e riempilo. Contiene la struttura attesa — `line`, `options`, `rules` — con i campi obbligatori già al loro posto.

## Intervista

Non chiedere «quali sono le regole». Nessuno le sa elencare a freddo. Chiedi configurazioni.

1. **Il prodotto più venduto.** Fatti dire com'è fatto, opzione per opzione. Da qui esce l'elenco delle `options` e i valori più comuni.
2. **L'ultimo ordine che è tornato indietro.** Cosa aveva di sbagliato? Quella è una regola, quasi sempre un `excludes`.
3. **La domanda che fate sempre al cliente.** Quella è un `required_if` o un'opzione `required`.
4. **La combinazione che il cliente chiede e voi rifiutate.** `excludes`, con il `because` già pronto nelle parole di chi risponde.
5. **Cosa cambia se sceglie la versione grande.** Da qui escono i `requires`.

Rileggi ogni regola a voce, con il suo `because`, e falla confermare prima di scriverla. Una regola che chi risponde non riconosce quando gliela ripeti è una regola che hai capito male.

## Estrazione da documenti

Ogni regola estratta porta la citazione: file, pagina, riga. Serve alla revisione, che altrimenti dovrebbe rileggere tutto.

Ordine di lavoro:

1. Prima le opzioni e i valori ammessi (tabelle, listini, matrici di prodotto). Sono la parte più affidabile.
2. Poi i vincoli di dominio (`min`, `max`, unità). Stanno nelle schede tecniche, spesso in nota.
3. Per ultime le regole. Sono la parte che i documenti dicono peggio: compaiono come asterischi, note a piè di pagina, «non disponibile per», «solo su richiesta».

Segna come **incerta** ogni regola che deriva da una nota ambigua, invece di normalizzarla. «Solo su richiesta» non è né un `excludes` né un via libera: è una domanda per la revisione.

Non estrarre prezzi. Non sono nel catalogo.

## Importazione da fonte strutturata

Un export di gestionale è dati, non regole verificate. Prima di usarlo:

- mappa i campi sullo schema, e dichiara quali campi restano fuori;
- verifica che i codici siano stabili (un codice che cambia a ogni revisione del listino rompe ogni configurazione salvata);
- cerca le regole che il gestionale **non** contiene: quasi sempre la compatibilità vive nella testa dell'ufficio tecnico anche quando l'anagrafica è completa.

Importato non è revisionato. Il campo `reviewed_by` va compilato lo stesso.

## Revisione umana: cosa passa a chi

Non consegnare il file YAML a chi conosce il prodotto. Consegna un elenco leggibile, in cui ogni riga si possa confermare o correggere:

```
R-01  Se serie = 82 mm → rinforzo in acciaio obbligatorio
      perché: peso anta oltre 90 kg
      da: listino 2026 rev.3, p. 7, nota 2
      [ ] confermo   [ ] è sbagliata   [ ] è incompleta: ______
```

Chi conferma va scritto in `reviewed_by`, con la data. Se la revisione copre solo una parte della linea, il catalogo dichiara la copertura nel campo `source` e Ines lo dice a ogni configurazione fuori da quella parte.

## Quando fermarsi

Il catalogo è utilizzabile quando copre le configurazioni che l'azienda vende davvero, non quando è completo. Il criterio pratico: prendi tre richieste reali già evase e prova a riprodurle. Se passano, il catalogo serve; se una si blocca su una regola mancante, quella regola è il prossimo lavoro.

Prima di consegnare, esegui `uv run {skill-root}/scripts/config_validator.py catalog <path>`. Un catalogo con contraddizioni interne fallisce lì, non alla prima richiesta di un cliente.

## Modificare un catalogo esistente

Le modifiche si propongono, non si applicano. Mostra la riga vecchia, la riga nuova e la ragione; applica su conferma di chi in azienda risponde di quella regola; aggiorna `as_of` e `reviewed_on`.

Una regola rimossa va segnata, non cancellata in silenzio: le configurazioni salvate che la citano vanno rilette.
