---
name: grl-setup
description: Installa il modulo Guardrails in un progetto. Usa quando l'utente chiede di installare il modulo grl, configurare Guardrails, registrare le figure Guardrails, o dice "setup Guardrails".
---

# Setup del modulo Guardrails

Installi Guardrails in un progetto: una domanda all'utente, la registrazione delle sette
figure nel roster degli agenti, e l'avvio della profilazione. L'esito che conta non è il file
di config — è che l'utente esca da qui con `grl-profile` già eseguito, perché senza profilo
di progetto le figure parlano per luoghi comuni.

Identità del modulo, variabili e roster stanno in `./assets/module.yaml`: leggilo, non dedurli.

## Regole di risoluzione

- I percorsi nudi (es. `./scripts/register-agents.py`) si risolvono dalla cartella di
  installazione di questa skill.
- `{project-root}` è un **token letterale** nei *valori* di configurazione: nei file di config
  si scrive così com'è, perché segnala che il percorso è relativo alla radice del progetto.
  Negli **argomenti degli script** (`--project-root`, `--config-path`, `--target`, …) è invece
  un percorso vero: risolvilo alla radice reale prima di eseguire, altrimenti gli script si
  fermano con un errore.

## In attivazione

1. Leggi `./assets/module.yaml`: `code` (`grl`), identità, variabili, blocco `agents`.
2. Riconosci il formato di configurazione del progetto — decide tutto il resto:
   - `{project-root}/_bmad/config.toml` esiste → **installazione TOML** (BMad 6.10+), il caso
     normale. Segui *Percorso TOML*.
   - esiste solo `{project-root}/_bmad/config.yaml` → **installazione YAML**, più vecchia.
     Segui *Percorso YAML*.
   - non esiste né l'uno né l'altro → il progetto non ha un'installazione BMad. Dillo e fermati.
3. Se il config contiene già una sezione `grl`, avvisa che questa è una riconfigurazione, non
   una prima installazione.

Se l'utente passa argomenti (`--headless`, `accetta i default`, o direttamente un valore),
usa quelli e salta le domande. Mostra comunque il riepilogo finale.

## La domanda da fare

Una sola, quella di `strictness_override` in `module.yaml`:

> Livello di severità delle figure Guardrails? Lascia vuoto per farlo derivare dalla criticità
> del progetto (consigliato).

Quattro risposte ammesse — vuoto, `light`, `normal`, `strict` — con le etichette che trovi in
`module.yaml`. Il default è vuoto, ed è la risposta giusta per quasi tutti: la severità si
deriva allora dalla criticità che l'utente dichiara in `grl-profile`, che è il posto dove
quella informazione appartiene. È un'impostazione personale, quindi finisce nel layer utente
del config, non in quello di team.

Non chiedere altro. Tutto il resto del contesto (settore, dati trattati, mercato, stack,
criticità, vincoli) vive nella memoria condivisa del progetto, non nella configurazione: la
config è unica per installazione, il profilo cambia da progetto a progetto.

## Percorso TOML

Un solo comando fa entrambe le scritture. Risolvi `{project-root}` prima di eseguirlo, e
ometti `--strictness` se l'utente non ha scelto un livello (senza il flag l'impostazione non
viene toccata; con `--strictness ""` viene scritta esplicitamente come "deriva dal profilo").

```bash
python3 ./scripts/register-agents.py \
  --project-root "{project-root}" \
  --module-yaml ./assets/module.yaml \
  --strictness "{valore-scelto}"
```

Cosa fa, e perché così:

- **Roster** → `{project-root}/_bmad/custom/config.toml`, una tabella `[agents.grl-agent-*]`
  per figura. È il passo che porta le sette figure nel party mode: `resolve_party.py` costruisce
  la stanza di default dagli agenti registrati nel config, senza filtrare per modulo o per team.
  Si scrive nel layer `custom/` perché `_bmad/config.toml` e `_bmad/config.user.toml` sono
  rigenerati dall'installer a ogni installazione, mentre `custom/` non viene toccato mai.
- **Severità** → `{project-root}/_bmad/custom/config.user.toml`, sezione `[modules.grl]` — la
  stessa convenzione con cui l'installer scrive `[modules.bmm]` e `[modules.bmb]`, ed è dove le
  figure la cercano. Una eventuale sezione `[grl]` scritta da una versione precedente viene
  rimossa nella stessa passata.
- I metadati delle figure sono letti dai `customize.toml` delle skill installate, che restano
  la fonte di verità; `--module-yaml` serve solo da ripiego se le skill non si trovano su disco.
- Le scritture sono anti-zombie e idempotente: le tabelle `grl` precedenti vengono rimosse prima
  di riscrivere, e il risultato viene riparsato prima di toccare il disco.

Poi registra le voci di help **nel catalogo che BMad legge davvero**:

```bash
python3 ./scripts/merge-help-csv.py \
  --target "{project-root}/_bmad/_config/bmad-help.csv" \
  --source ./assets/module-help.csv \
  --module-code Guardrails
```

Tre cose da sapere, tutte verificate sul campo:

- **Il catalogo è `_bmad/_config/bmad-help.csv`**, non `_bmad/module-help.csv`. È il file che
  `bmad-help` dichiara di leggere («assembled manifest of all installed module skills»), ed è
  quello in cui compaiono le voci di Core, BMad Method e BMad Builder. Scrivere solo in
  `_bmad/module-help.csv` — come fa il comando del template generico — lascia le voci in un file
  che nessuno consulta.
- **La colonna `module` porta il nome leggibile del modulo**, `Guardrails`, non il codice `grl`:
  è la convenzione del catalogo, dove gli altri moduli compaiono come `Core`, `BMad Method`,
  `BMad Builder`. Da qui `--module-code Guardrails`, che è anche la chiave con cui le righe
  vecchie vengono rimosse prima di riscrivere.
- **Niente `--legacy-dir`.** Quel flag non migra nulla: cancella `{project-root}/_bmad/core/module-help.csv`
  e `{project-root}/_bmad/{codice}/module-help.csv`. Sul CSV del core significa **perdere le voci
  di help del core** senza averle prima copiate altrove. Se il tuo progetto ha già subìto questa
  cancellazione, il file si recupera da un'altra installazione BMad o reinstallando.

Limite dichiarato, non nascosto: `_bmad/_config/` è gestito dall'installer e viene rigenerato a
ogni installazione o aggiornamento di BMad. Le voci di Guardrails vanno quindi riscritte dopo un
reinstall — basta rieseguire questo setup.

Se il comando esce con codice diverso da zero, mostra l'errore e fermati.

**Non eseguire `./scripts/merge-config.py` su un'installazione TOML**: scrive `config.yaml`, che
il resolver a quattro layer non legge — la configurazione finirebbe in un file che nessuno guarda.

**Verifica prima di dichiarare fatto.** Il roster va controllato, non dato per scritto:

```bash
python3 {project-root}/_bmad/scripts/resolve_config.py -p "{project-root}" -k agents
```

Devono comparire tutte e sette le chiavi `grl-agent-*` accanto agli agenti già installati. Se
mancano, il party mode non le vedrà: mostra l'output e fermati, invece di chiudere il setup.

Stessa verifica per la severità, con `-k modules.grl`. Nota per chi legge questa configurazione
dalle skill del modulo: va letta dal config **risolto** (`resolve_config.py`), che fonde i
quattro layer TOML, non aprendo `_bmad/config.toml` e `_bmad/config.user.toml` direttamente —
il valore vive nel layer `custom/`, che una lettura dei soli file base non vedrebbe.

## Percorso YAML

Su un'installazione più vecchia valgono gli script generici del template:

```bash
python3 ./scripts/merge-config.py --config-path "{project-root}/_bmad/config.yaml" --user-config-path "{project-root}/_bmad/config.user.yaml" --module-yaml ./assets/module.yaml --answers {file-temp} --legacy-dir "{project-root}/_bmad"
python3 ./scripts/merge-help-csv.py --target "{project-root}/_bmad/module-help.csv" --source ./assets/module-help.csv --legacy-dir "{project-root}/_bmad" --module-code grl
```

Il file temporaneo delle risposte ha forma `{"module": {"strictness_override": "..."}}` (più
una chiave `core` se i valori di base non sono ancora stati raccolti), e i valori conservano il
token `{project-root}` letterale.

Avverti però l'utente di un limite reale: `merge-config.py` scrive la sezione del modulo ma
**non** la tabella degli agenti. Su un'installazione YAML le sette figure vanno quindi registrate
con il meccanismo di quella versione di BMad, altrimenti non compaiono nel party mode.
`register-agents.py` non copre questo caso e lo dichiara invece di fingere.

## Cosa il setup non fa

- **Non crea `{project-root}/_bmad/memory/grl-shared/`.** La crea `grl-profile` alla prima
  esecuzione, quando ha qualcosa da scriverci. Una cartella vuota in `_bmad/memory/` è rumore.
- **Non crea gruppi di party mode.** Le sette figure stanno nella stanza principale insieme ai
  cinque agenti BMM: una sola stanza, dodici partecipanti, per scelta esplicita.
- **Non tocca le skill BMM.** Vedi il passo facoltativo qui sotto.

## Chiusura

1. Mostra cosa è stato scritto: le sette figure registrate (nome, icona, titolo), il valore di
   `strictness_override`, le voci di help aggiunte, e i file toccati.
2. Mostra il `module_greeting` di `module.yaml`.
3. **Proponi `grl-profile` e, se l'utente accetta, eseguilo subito.** È il passo che rende utile
   tutto il resto: otto campi, pochi minuti, quasi tutti pre-compilati leggendo il repository.
   L'unico che deve dichiarare l'utente è la criticità del progetto, perché è quella che regola
   quanto saranno severe tutte e sette le figure. Se rifiuta, va bene: digli che ogni figura
   proporrà la profilazione da sé quando troverà il profilo mancante.
4. Nomina il passo **facoltativo e reversibile**, senza eseguirlo: le figure possono essere
   consultate automaticamente dentro i flussi BMM (`bmad-prd`, `bmad-architecture`, `bmad-ux`,
   `bmad-code-review`) aggiungendo override di customizzazione con `bmad-customize` in
   `{project-root}/_bmad/custom/`. Spiega che toccano il comportamento di skill che non
   appartengono a questo modulo, e che si tolgono cancellando il file di override. Non scrivere
   nulla in `_bmad/custom/` per conto tuo: è una scelta dell'utente, da fare quando la vuole.
