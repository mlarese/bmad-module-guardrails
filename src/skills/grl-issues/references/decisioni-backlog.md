# Decisioni sul backlog e stati dichiarati

Una discussione decide qualcosa quasi ogni volta: questa issue non si fa, quest'altra aspetta il
cliente, queste due sono la stessa, da adesso le issue senza criterio di accettazione non entrano
in sprint. Se la decisione resta nella conversazione, alla sessione dopo si ridiscute tutto.

`decisions.md` è il registro di quelle decisioni: una voce per decisione, in coda, mai riscritta.

## Le due forme di voce

```markdown
## 2026-08-11 — decisione su #42

- **decisione:** `NON_APPROVATA`
- **chi:** Mauro
- **motivo:** costo sproporzionato rispetto a quante volte capita
- **conseguenza:** stato `NON_APPROVATA`; si riapre solo se il cliente lo chiede per iscritto
- **origine:** discussione del 2026-08-11

## 2026-08-11 — convenzione di backlog

- **decisione:** senza criterio di accettazione una issue resta `DA_CHIARIRE`
- **chi:** Mauro
- **motivo:** due giorni persi sulla #31, che non diceva cosa guardare
- **conseguenza:** vale su tutte le issue, anche quelle già valutate
- **origine:** discussione del 2026-08-11
```

La prima cita un numero e cambia lo stato di una issue. La seconda non cita nessuna issue e cambia
come si valutano tutte.

## Regole

- ogni voce porta chi ha deciso, quando, perché e cosa cambia; una decisione senza autore non è una
  decisione, è un'opinione rimasta agli atti;
- una decisione non si cancella. Se cambia, si aggiunge una voce nuova che cita quella superata;
- le decisioni che riguardano il progetto e non il backlog restano in
  `{project-root}/_bmad/memory/grl-shared/decisions.md`;
- non si registra il contenuto della discussione, solo l'esito e il motivo in una riga.

**Una convenzione può solo irrigidire il gate di chiarezza.** Se qualcuno decide che un criterio
bloccante non serve più, quella non è una voce di `decisions.md`: è una modifica a
`blocking_criteria` nell'override di `grl-issue-readiness`. Segnalalo invece di applicarlo in
silenzio, altrimenti il gate ha due autorità che dicono cose diverse.

## `decide` — registra una decisione

1. Raccogli i quattro dati della regola. Se manca l'autore o il motivo, chiedili.
2. Accoda la voce a `decisions.md`.
3. Se la decisione riguarda una issue, scrivi lo stato con il rimando alla voce:

   ```bash
   uv run {skill-root}/scripts/registry.py set \
     --path {workflow.registry_path}/{slug}/registry.json \
     --issue 42 --status NON_APPROVATA --note "Mauro, 2026-08-11: costo sproporzionato"
   ```

Se la decisione va comunicata all'autore della issue, il commento lo prepara `grl-issue-readiness`.

## `set-status` — dichiara uno stato a mano

Serve quando il fatto non è leggibile da GitHub: il lavoro è iniziato in locale, la richiesta è
stata rifiutata a voce, la issue aspetta una risposta arrivata per email.

1. Chiedi lo stato. Per `IN_ATTESA` chiedi anche **cosa lo toglie**, per `NON_APPROVATA` **chi** ha
   deciso: senza questi due dati la voce diventa un blocco senza uscita.
2. Scrivi con `registry.py set --status … --note …`, che marca `status_source: dichiarato`.
   Per un'attesa usa anche `--hold-who` e `--hold-clears`; per toglierla, `--clear-hold`.
3. Per `NON_APPROVATA` e `IN_ATTESA` accoda anche la voce in `decisions.md`: sono i due stati che
   qualcuno rimetterà in discussione, e senza il motivo scritto si ricomincia da capo.

Uno stato dichiarato regge finché un fatto letto da GitHub non lo contraddice. Lo script applica la
precedenza e restituisce la contraddizione; dichiararla è compito tuo.
