# Consegna: due output, mai uno solo

La stessa configurazione va a due lettori con bisogni opposti. Il venditore deve poter decidere; il cliente deve poter rispondere. Un output unico o espone l'interno o lascia il cliente senza domande.

Entrambi vivono in `{output_folder}/product-config/{slug}/`, accanto al `config.yaml` che li ha generati.

**Si consegnano insieme, nella stessa risposta.** Annunciare il secondo — «poi ti preparo l'interno», «vuoi che lo scriva?» — non è consegnare: chi legge resta con metà del lavoro e deve chiederlo. Se uno dei due è breve perché la configurazione è appena iniziata, resta breve, ma c'è.

## Output interno — `interno.md`

Destinatario: chi in azienda porta avanti la richiesta.

```markdown
# {cliente} — {linea} — {data}

**Esito:** valid | incomplete | invalid
**Documento:** {file}, revisione {rev}
**Catalogo:** {linea} as_of {data}, revisione di {nome}

## Configurazione

| Opzione | Valore | Origine | Riferimento |
| --- | --- | --- | --- |
| Serie | 82 mm | scritto | p. 2 r. 14 |
| Rinforzo | acciaio | imposto | requires: serie=s82 — peso anta oltre 90 kg |
| Colore interno | bianco | assunto | non citato nel documento |

## Conflitti

Uno per riga: cosa ha chiesto il cliente, quale regola lo esclude, quali alternative restano.

## Mancano

Solo ciò che blocca — obbligatorie e opzioni imposte da una regola — ordinato per impatto, con la domanda già scritta.

## Scelte ancora aperte

Le facoltative non decise, con il loro impatto. Non cambiano l'esito e vanno tenute separate dalle mancanze, altrimenti una configurazione ordinabile sembra bloccata.

## Note per il reparto

Traduzioni non ovvie, contraddizioni interne al documento, riferimenti a ordini precedenti da recuperare, punti in cui il catalogo non copre il caso.
```

Se il catalogo porta costi o alternative, stanno qui e solo qui.

## Output al cliente — `cliente.md`

Destinatario: chi ha mandato la richiesta.

```markdown
# {linea} — riepilogo della vostra richiesta

## Quello che abbiamo capito

Elenco delle scelte in linguaggio del prodotto, non in codici di catalogo.
Le opzioni imposte da una regola si dichiarano con la ragione, non come scelta:
«rinforzo in acciaio, necessario sopra i 90 kg di peso anta».

## Quello che abbiamo assunto

Ogni assunzione, in chiaro. È la sezione che evita la contestazione dopo l'ordine.

## Quello che ci serve sapere

Le domande, una per riga, in ordine di importanza. Nient'altro.

## Quello che non è possibile

Solo se c'è un conflitto: cosa è stato chiesto, perché non si può fare,
cosa si può fare al suo posto.
```

Fuori da questo file restano costi, margini, alternative scartate, note di reparto, codici interni e nomi di file del catalogo.

## Regole che valgono per entrambi

- **L'esito è lo stesso in tutti e due.** Una configurazione `incomplete` non diventa completa nella versione al cliente togliendo le domande.
- **Le assunzioni compaiono in entrambi.** È l'unico modo perché smettano di essere assunzioni.
- **Niente prezzo.** Ines non emette preventivi; il prezzo lo mette chi lo decide, a partire da questa configurazione.
- **Niente tempi di consegna.**

## Cosa resta a valle

La consegna non chiude il lavoro dell'azienda: resta l'atto commerciale, che è di una persona. Chiudi indicando in una riga qual è il prossimo passo concreto — inoltrare le domande, far confermare le assunzioni, aprire l'offerta — senza compierlo.
