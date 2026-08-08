---
name: grl-setup
description: Installa il modulo Guardrails in un progetto. Usa quando l'utente chiede di installare il modulo grl, configurare Guardrails, registrare le figure Guardrails, o dice "setup Guardrails".
---

# Setup del modulo Guardrails

Installi Guardrails in un progetto: due domande all'utente, l'applicazione della selezione delle
figure, la registrazione nel roster delle sole figure installate, le stanze tematiche di party
mode e l'avvio della profilazione. I sette workflow si installano sempre, qualunque cosa venga
spuntato. L'esito che conta non è il file di config — è che l'utente
esca da qui con `grl-profile` già eseguito, perché senza profilo di progetto le figure parlano
per luoghi comuni.

Identità del modulo, variabili e roster stanno in `./assets/module.yaml`: leggilo, non dedurli.
La mappa gruppo → skill sta in `./assets/groups.toml`.

**Il passo che non puoi saltare.** L'installer BMad copia sul disco tutte le skill del modulo:
il formato `module.yaml` non ha modo di escluderne alcune dalla copia, e non ha hook eseguibili.
Le spunte raccolte durante l'installazione diventano effettive solo qui, con
`./scripts/apply-selection.py`. Finché non gira, una figura che l'utente non ha voluto è ancora
sul disco e può attivarsi da sola alla prima frase che assomiglia alla sua `description`.

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
4. **Recupero da un'installazione fatta con l'installer BMad 6.10.0.** Quella versione scrive la
   configurazione del modulo in `{project-root}/_bmad/grl/config.yaml`, che il resolver a quattro
   layer non legge: il valore c'è ma nessuna figura lo vede. Dalla 6.10.1 finisce anche in
   `[modules.grl]` del TOML e il problema non si pone. Quindi:

   ```bash
   uv run {project-root}/_bmad/scripts/resolve_config.py -p "{project-root}" -k modules.grl
   ```

   Se il risultato è vuoto **e** `{project-root}/_bmad/grl/config.yaml` esiste e contiene un
   `strictness_override` valorizzato, prendi quel valore come risposta e **non fare la domanda**:
   l'utente l'aveva già data all'installer, richiederla sarebbe solo fastidio. Dichiaralo nel
   riepilogo finale — «recuperato il livello *{valore}* scelto durante l'installazione, che
   l'installer aveva scritto in un file non letto dalle figure».

   Se `strictness_override` è vuoto o assente, non c'è niente da recuperare: prosegui normalmente.

Se l'utente passa argomenti (`--headless`, `accetta i default`, o direttamente un valore),
usa quelli e salta le domande. Mostra comunque il riepilogo finale.

## Le domande da fare

### 1. Quali figure installare

È la multi-select `enabled_groups` di `module.yaml`: cinque caselle, tutte spuntate per default.
Presentala come spunte, non come scelta singola — se ne possono tenere quante se ne vuole.

> Quali figure Guardrails vuoi installare? Spunta i gruppi che ti servono; gli altri restano fuori
> dal progetto e si possono aggiungere dopo rieseguendo `grl-setup`.

Le etichette e la composizione di ogni gruppo stanno in `./assets/groups.toml`: leggile da lì e
mostrale, così l'utente sa quali figure sta spuntando.

**I sette workflow non compaiono fra le opzioni**: sono in `always` e si installano sempre. Se
l'utente chiede di escluderne uno, digli che la selezione governa le figure, non i lavori — un
workflow si invoca per nome quando serve e non si attiva da solo, quindi toglierlo produrrebbe
solo un comando mancante.

**Se l'installer ha già raccolto la risposta**, non ripetere la domanda: leggila da
`enabled_groups` di `modules.grl` nel config risolto e dichiara nel riepilogo che stai usando la
scelta fatta durante l'installazione.

```bash
uv run {project-root}/_bmad/scripts/resolve_config.py -p "{project-root}" -k modules.grl
```

**Chiedi conferma solo in riconfigurazione.** Se `enabled_groups` esiste già e la nuova scelta
toglie gruppi che erano attivi, elenca le figure che stai per disattivare e fatti confermare:
lì stai togliendo qualcosa che il progetto sta usando. In prima installazione nessuna conferma —
le spunte *sono* la conferma.

### 2. Quanto sono severe

Quella di `strictness_override` in `module.yaml`:

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

**L'ordine conta.** `apply-selection.py` va per primo: toglie dal disco le figure dei gruppi
esclusi, così tutto quello che viene dopo lavora su ciò che resta davvero installato. Risolvi
`{project-root}` prima di eseguire.

```bash
python3 ./scripts/apply-selection.py \
  --project-root "{project-root}" \
  --groups "{gruppi-scelti}" \
  --groups-map ./assets/groups.toml
```

`{gruppi-scelti}` è la lista separata da virgola degli `id` spuntati (es. `governance,web`);
`all` li tiene tutti. Lo script è idempotente: se il disco è già così, non tocca niente ed esce
con `changed: false`. Prima di applicare puoi mostrare l'effetto con `--dry-run`.

Dal suo output JSON prendi `skills_active`: è l'elenco che serve ai due comandi seguenti. Chiama
`{figure-attive}` le sole voci `grl-agent-*` di quell'elenco, e `{skill-attive}` l'elenco intero.

Poi le scritture di configurazione. Ometti `--strictness` se l'utente non ha scelto un livello
(senza il flag l'impostazione non viene toccata; con `--strictness ""` viene scritta
esplicitamente come "deriva dal profilo").

```bash
python3 ./scripts/register-agents.py \
  --project-root "{project-root}" \
  --module-yaml ./assets/module.yaml \
  --only "{figure-attive}" \
  --strictness "{valore-scelto}"

python3 ./scripts/merge-party-groups.py \
  --project-root "{project-root}" \
  --source ./assets/party-groups.toml \
  --only-agents "{figure-attive}"
```

Cosa fa, e perché così:

- **Selezione** → le figure dei gruppi esclusi finiscono in `{project-root}/_bmad/grl/.disabled/`,
  fuori da `.claude/skills/` e da ogni altra cartella che gli agenti leggono. Niente viene
  cancellato: sono spostamenti, e rispuntare un gruppo le riporta da dove erano venute — lo
  script ripristina prima e disattiva dopo, nella stessa passata. La selezione applicata viene
  scritta in `[modules.grl] enabled_groups` di `_bmad/custom/config.toml`, che è il layer di
  team: quali gruppi servono dipende dal progetto, non dalla persona.
- **`--only` su `register-agents.py`** è una cintura di sicurezza, non il meccanismo: le figure
  disattivate non sono più su disco, quindi non verrebbero trovate comunque. Serve nel caso in
  cui lo script ripieghi su `module.yaml`, che elenca tutte e undici le figure a prescindere.
- **`--only-agents` su `merge-party-groups.py`** toglie dalle stanze tematiche le figure non
  installate e salta i gruppi che restano senza nessuna figura Guardrails. I membri di altri
  moduli (es. `bmad-agent-ux-designer`) restano dove sono.
- **Roster** → `{project-root}/_bmad/custom/config.toml`, una tabella `[agents.grl-agent-*]`
  per figura installata. È il passo che le porta nel party mode: `resolve_party.py` costruisce
  la stanza di default dagli agenti registrati nel config, senza filtrare per modulo o per team.
  Si scrive nel layer `custom/` perché `_bmad/config.toml` e `_bmad/config.user.toml` sono
  rigenerati dall'installer a ogni installazione, mentre `custom/` non viene toccato mai.
- **Severità** → `{project-root}/_bmad/custom/config.user.toml`, sezione `[modules.grl]` — la
  stessa convenzione con cui l'installer scrive `[modules.bmm]` e `[modules.bmb]`, ed è dove le
  figure la cercano. Una eventuale sezione `[grl]` scritta da una versione precedente viene
  rimossa nella stessa passata.
- I metadati delle figure sono letti dai `customize.toml` delle skill installate, che restano
  la fonte di verità; `--module-yaml` serve solo da ripiego se le skill non si trovano su disco.
- I gruppi tematici vengono scritti in `{project-root}/_bmad/custom/bmad-party-mode.toml`.
  Il merger sostituisce solo il blocco marcato da Guardrails e preserva gli override e i gruppi
  creati dall'utente fuori da quel blocco.
- Le scritture sono anti-zombie e idempotente: le tabelle `grl` precedenti vengono rimosse prima
  di riscrivere, e il risultato viene riparsato prima di toccare il disco.

Poi registra le voci di help **nel catalogo che BMad legge davvero**:

```bash
python3 ./scripts/merge-help-csv.py \
  --target "{project-root}/_bmad/_config/bmad-help.csv" \
  --source ./assets/module-help.csv \
  --only-skills "{skill-attive}" \
  --module-code Guardrails
```

`--only-skills` scarta le righe delle figure non installate: senza, `bmad-help` elencherebbe
capacità che il progetto non ha, e l'utente le chiederebbe invano. Le voci dei sette workflow
restano sempre, perché i workflow ci sono sempre.

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

Devono comparire le chiavi `grl-agent-*` dei gruppi scelti, accanto agli agenti già installati —
tutte e undici se l'utente ha spuntato tutto. Se ne manca una che doveva esserci, il party mode
non la vedrà: mostra l'output e fermati, invece di chiudere il setup. Se ne compare una che
doveva restare fuori, `apply-selection.py` non ha girato o è girato dopo: rieseguilo nell'ordine
giusto.

Stessa verifica per la severità e per i gruppi, con `-k modules.grl`. Nota per chi legge questa configurazione
dalle skill del modulo: va letta dal config **risolto** (`resolve_config.py`), che fonde i
quattro layer TOML, non aprendo `_bmad/config.toml` e `_bmad/config.user.toml` direttamente —
il valore vive nel layer `custom/`, che una lettura dei soli file base non vedrebbe.

## Percorso YAML

Su un'installazione più vecchia valgono gli script generici del template:

```bash
python3 ./scripts/apply-selection.py --project-root "{project-root}" --groups "{gruppi-scelti}" --groups-map ./assets/groups.toml
python3 ./scripts/merge-config.py --config-path "{project-root}/_bmad/config.yaml" --user-config-path "{project-root}/_bmad/config.user.yaml" --module-yaml ./assets/module.yaml --answers {file-temp} --legacy-dir "{project-root}/_bmad"
python3 ./scripts/merge-help-csv.py --target "{project-root}/_bmad/module-help.csv" --source ./assets/module-help.csv --only-skills "{skill-attive}" --legacy-dir "{project-root}/_bmad" --module-code grl
python3 ./scripts/merge-party-groups.py --project-root "{project-root}" --source ./assets/party-groups.toml --only-agents "{figure-attive}"
```

`apply-selection.py` funziona anche qui: sposta cartelle e scrive in `_bmad/custom/config.toml`,
che esiste in entrambi i formati. Va comunque per primo.

Il file temporaneo delle risposte ha forma `{"module": {"strictness_override": "..."}}` (più
una chiave `core` se i valori di base non sono ancora stati raccolti), e i valori conservano il
token `{project-root}` letterale.

Avverti però l'utente di un limite reale: `merge-config.py` scrive la sezione del modulo ma
**non** la tabella degli agenti. Su un'installazione YAML le figure vanno quindi registrate
con il meccanismo di quella versione di BMad, altrimenti non compaiono nel party mode.
`register-agents.py` non copre questo caso e lo dichiara invece di fingere.

## Cosa il setup non fa

- **Non crea `{project-root}/_bmad/memory/grl-shared/`.** La crea `grl-profile` alla prima
  esecuzione, quando ha qualcosa da scriverci. Una cartella vuota in `_bmad/memory/` è rumore.
- **Non imposta una stanza di default.** Le figure installate restano nella stanza principale
  insieme agli agenti BMM; in più `grl-setup` installa le stanze tematiche dei gruppi scelti,
  richiamabili con `bmad-party-mode --party <id>`. Il default resta quello deciso dal progetto
  o dal team.
- **Non tocca i workflow.** Tutti e sette si installano sempre: la selezione governa le figure.
- **Non cancella le figure escluse.** Le sposta in `_bmad/grl/.disabled/`, da dove tornano
  rieseguendo il setup e rispuntando il gruppo. Se l'utente vuole liberare spazio, può
  cancellare quella cartella a mano — ma allora per riaverle dovrà reinstallare il modulo.
- **Non tocca le skill BMM.** Vedi il passo facoltativo qui sotto.

## Chiusura

1. Mostra cosa è stato scritto: i gruppi installati e le figure registrate (nome, icona, titolo),
   il valore di `strictness_override`, le voci di help aggiunte, e i file toccati.
   Se qualche gruppo è rimasto fuori, dillo esplicitamente: quali figure sono state disattivate,
   dove sono finite, e che si riattivano rieseguendo `grl-setup`.
2. Mostra il `module_greeting` di `module.yaml`.
3. **Proponi `grl-profile` e, se l'utente accetta, eseguilo subito.** È il passo che rende utile
   tutto il resto: otto campi, pochi minuti, quasi tutti pre-compilati leggendo il repository.
   L'unico che deve dichiarare l'utente è la criticità del progetto, perché è quella che regola
   quanto saranno severe tutte le figure installate. Se rifiuta, va bene: digli che ogni figura
   proporrà la profilazione da sé quando troverà il profilo mancante.
4. Nomina il passo **facoltativo e reversibile**, senza eseguirlo: le figure possono essere
   consultate automaticamente dentro i flussi BMM (`bmad-prd`, `bmad-architecture`, `bmad-ux`,
   `bmad-code-review`) aggiungendo override di customizzazione con `bmad-customize` in
   `{project-root}/_bmad/custom/`. Spiega che toccano il comportamento di skill che non
   appartengono a questo modulo, e che si tolgono cancellando il file di override. Non scrivere
   nulla in `_bmad/custom/` per conto tuo: è una scelta dell'utente, da fare quando la vuole.
