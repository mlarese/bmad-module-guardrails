# Controlli di completezza, vigenza e attualità — legale

Questo riferimento definisce il contratto minimo del report. La parola “completo” significa
**completo per il perimetro dichiarato**, non completo di tutto il web o di ogni possibile
interpretazione.

## Intestazione obbligatoria del run

Salva sempre questi campi prima della ricerca:

```yaml
scope:
  jurisdiction: Italia | UE | altra giurisdizione esplicita
  territory: nazionale | regione/comune/settore
  topics: [...]             # materia e parole chiave
  categories: [...]         # atti, prassi, giurisprudenza, emendamenti...
  publication_from: YYYY-MM-DD
  publication_to: YYYY-MM-DD
  as_of: YYYY-MM-DDThh:mm:ss+TZ | pending
coverage_status: complete_for_declared_scope | partial | blocked
```

`as_of` è il momento reale in cui termina il controllo finale, con fuso orario. Non usare “oggi”
senza trasformarlo in una data e un’ora verificabili. Una fonte consultata dopo `as_of`, o una
fonte senza data di accesso, non può essere usata per quel run.

## Matrice di copertura

Per ogni categoria e per ogni fonte primaria pertinente in `fonti-live.md` registra una riga:

```text
source_id | editore | entrypoint | query/filtri usati | searched_at | risultati
          | covered/empty/partial/blocked | motivo o URL del registro | final_accessed_at
```

`empty` è un risultato valido: significa che la ricerca è stata eseguita e non ha prodotto atti.
`partial` indica che sono stati controllati solo alcuni archivi/serie; `blocked` indica una
pagina, una banca dati o un archivio decisivo non accessibile. Il report può dire
`complete_for_declared_scope` solo quando tutte le righe obbligatorie sono `covered` o `empty` e
ogni categoria richiesta ha almeno una fonte primaria pertinente. Altrimenti deve mostrare
`partial` o `blocked` in apertura.

Usa almeno quattro famiglie di interrogazioni, adattate alla materia:

1. identificativo/titolo/ente dell’atto;
2. parole chiave della materia + tipo di atto;
3. `modifica`, `sostituisce`, `abroga`, `proroga`, `rettifica`, `conversione`, `attuazione`,
   `entrata in vigore`, `decorrenza`;
4. archivio “ultimi atti” o testo vigente/consolidato della fonte responsabile.

## Registro di vigenza e successione

Ogni finding load-bearing ha una riga di lineage, anche quando il risultato è “nessuna novità”:

```text
finding_id | act_id | titolo | pubblicato | efficace_da | efficace_fino_a
status_as_of | supersedes | superseded_by | amended_by | repealed_by
conversion/corrigendum | testo_vigente/consolidato | last_checked
primary_url | independent_url | review_1 | review_2
```

Per un atto trovato in una fonte secondaria, fai il percorso all’indietro fino alla pubblicazione
ufficiale e poi in avanti fino alla versione vigente alla data `as_of`. Cerca l’atto successivo
anche se il risultato iniziale sembra recente. Controlla in particolare leggi di conversione,
decreti attuativi, proroghe, abrogazioni espresse o implicite, rettifiche e testi multivigenti.

Lo stato `current_confirmed` (o l’equivalente italiano `vigente-confermato`) è ammesso solo se:

- esiste la pubblicazione ufficiale;
- esiste il testo vigente/consolidato o un’indicazione ufficiale dello stato a `as_of`;
- la catena di modifica, sostituzione, conversione, abrogazione e scadenza è stata cercata;
- un secondo controllo indipendente ha confermato la conclusione;
- le fonti decisive sono accessibili e la matrice di copertura non è `partial`/`blocked`.

Le URL decisive devono essere riaperte nella sweep finale **dopo il secondo `bmad-review` oppure dopo il secondo gate `manual_review` di fallback** prima
di fissare `as_of`; un `accessed_at` iniziale non basta per una pagina che può cambiare durante il
run.

In tutti gli altri casi usa `supersession_risk`, `stale`, `unverified`, `disputed` o `blocked`.
Un URL raggiungibile non è da solo una prova di vigenza: servono stato/versione e data.

## Regola di freschezza

Nel source appendix separa sempre `published_at`, `effective_at`, eventuale `last_modified` e
`accessed_at`. Una fonte vecchia può essere necessaria per la lineage, ma non può essere
presentata come novità corrente senza il successivo controllo ufficiale. Se il finding è fuori
dalla finestra ma serve a spiegare una sostituzione, va nella sezione contesto/lineage e non nella
tabella delle novità.

La “prossima data di controllo” deve essere ravvicinata quando l’atto è pendente, a termine,
contestato o soggetto a conversione/proroga. Un refresh deve riaprire la lineage, non limitarsi a
cercare nuove parole chiave.
