# Controlli di completezza, vigenza e attualità — fiscale

Questo riferimento definisce il contratto minimo del report. “Completo” significa **completo per
il perimetro dichiarato** (territorio, materia, categorie e date), non una garanzia assoluta su
ogni contenuto pubblicato online.

## Intestazione obbligatoria del run

Registra prima della raccolta:

```yaml
scope:
  jurisdiction: Italia | UE | altra giurisdizione esplicita
  territory: nazionale | regione/ente/settore
  topics: [...]             # imposte, lavoro, incentivi, ecc.
  categories: [...]         # norme, prassi, bandi, emendamenti...
  publication_from: YYYY-MM-DD
  publication_to: YYYY-MM-DD
  as_of: YYYY-MM-DDThh:mm:ss+TZ
coverage_status: complete_for_declared_scope | partial | blocked
```

`as_of` è il momento effettivo dell’ultimo controllo finale, con fuso orario. “Aggiornato” è una
conclusione riferita a quel momento, non una proprietà permanente del report.

## Matrice di copertura

Per ogni fonte primaria pertinente in `fonti-live.md` e per ogni categoria richiesta conserva:

```text
source_id | ente | entrypoint | query/filtri | searched_at | risultati
          | covered/empty/partial/blocked | motivo o URL del registro | final_accessed_at
```

`empty` documenta una ricerca eseguita senza risultati; non equivale a non aver cercato.
`partial` e `blocked` devono comparire nella sintesi e impediscono di chiamare il report
“completo”. Il valore `complete_for_declared_scope` è ammesso solo se ogni categoria ha almeno
una fonte primaria pertinente e tutte le fonti obbligatorie risultano `covered` o `empty`.

Usa almeno queste famiglie di query, adattandole al caso:

1. identificativo/titolo/ente dell’atto, della circolare o della misura;
2. materia + tipo di atto + periodo;
3. `modifica`, `sostituisce`, `abroga`, `proroga`, `rettifica`, `conversione`, `attuazione`,
   `decorrenza`, `riapertura`, `esaurimento risorse`;
4. archivio “ultime novità”, testo vigente/consolidato e pagina corrente della misura.

## Registro di vigenza e successione

Ogni risultato decisivo deve avere una riga di lineage:

```text
finding_id | act_or_measure_id | ente | pubblicato | efficace_da | efficace_fino_a
status_as_of | supersedes | superseded_by | amended_by | repealed_by | extended_by
conversion/corrigendum | version/current_page | last_checked
primary_url | independent_url | review_1 | review_2
```

Per circolari, risoluzioni e provvedimenti cerca la versione successiva e l’eventuale documento
che li supera o chiarisce. Per bandi e incentivi controlla anche proroghe, riaperture, risorse
esaurite, rettifiche, sospensioni, decreto applicativo e pagina del gestore. La regola vale anche
quando un portale professionale presenta il dato come ancora utilizzabile.

Lo stato `current_confirmed` (o `vigente-confermato`/`aperto-confermato`) è ammesso solo con:

- fonte primaria dell’ente competente;
- stato o testo corrente verificabile alla data `as_of`;
- catena di modifica/sostituzione/abrogazione/proroga/scadenza controllata;
- seconda verifica indipendente o versione ufficiale successiva;
- fonti decisive accessibili e copertura non `partial`/`blocked`.

Le URL decisive vanno riaperte nella sweep finale **dopo il secondo `bmad-review`** prima di
fissare `as_of`; un accesso iniziale non prova lo stato di una pagina mutabile alla fine del run.

Altrimenti usa `supersession_risk`, `stale`, `unverified`, `disputed` o `blocked`. L’accesso a un
URL e la presenza di una pagina indicizzata non provano da soli apertura, aliquota, soglia,
cumulabilità o applicabilità.

## Regola di freschezza

Nel source appendix separa `published_at`, `effective_at`, `open_at`, `close_at`, `last_modified`
e `accessed_at`. Una fonte precedente può rimanere nel report solo come lineage o contesto; non
può sostenere da sola una conclusione attuale. La prossima data di controllo va anticipata per
misure con sportello aperto, scadenza, proroga, risorse limitate o norma in conversione. Un
refresh riapre sempre anche il controllo della versione, non solo la ricerca di nuovi titoli.
