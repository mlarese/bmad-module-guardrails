# Guardrails (`grl`)

Modulo [BMad](https://github.com/bmad-code-org/BMAD-METHOD) con **dieci figure di presidio** che
affiancano il team dentro il ciclo di sviluppo software: privacy e GDPR, sicurezza applicativa,
legale e licenze, compliance normativa, qualità visiva della UI, disciplina architetturale del
codice, infrastruttura e operatività, dominio clinico del software sanitario, impianto delle
applicazioni che usano modelli linguistici e architettura WordPress a componenti.

Guardrail, non autista: il modulo tiene il progetto in carreggiata, le decisioni restano al team.

## Perché

Vincoli normativi, scelte di sicurezza e debiti strutturali, se emergono a fine progetto, costano
riscritture. Guardrails li fa emergere quando cambiare è ancora economico — e li ricontrolla lungo
tutto il ciclo, dai requisiti al pre-rilascio.

Il modulo **parla, non produce documenti**: niente DPIA formali, niente registro dei trattamenti,
niente report di audit. L'unica traccia che lascia sono righe brevi nella memoria condivisa del
progetto.

## Le dieci figure

| | Nome | Ruolo | Presidia |
| --- | ---- | ----- | -------- |
| 🛡️ | **Vera** | Data Protection Officer | quali dati personali tocca il progetto, con quale base giuridica, per quanto tempo. Il suo verdetto preferito è «qui non si applica niente, vai» |
| 🔐 | **Kai** | Application Security Engineer | rischi ordinati per probabilità reale, con la contromisura minima. Niente fortini dove basta una serratura |
| ⚖️ | **Aldo** | Tech Lawyer | licenze OSS, proprietà intellettuale (anche del codice generato da AI), contratti e DPA, termini di servizio. Non dice mai «consulta un avvocato»: l'avvocato è lui |
| 📐 | **Nils** | Regulatory Compliance | AI Act, NIS2, DORA, accessibilità, eIDAS, regimi settoriali. Prima esclude ciò che non ti riguarda, poi prescrive |
| 👁️ | **Iris** | Design Critic | l'omologazione delle pagine generate — hero in gradiente, tre card, blu-viola. Non stronca mai senza dare la deviazione concreta |
| 🧱 | **Otto** | Code Architect | confini, dipendenze, over-engineering. SOLID, KISS, DRY, vertical slice ed esagonale come attrezzi, mai come dogmi |
| 🖥️ | **Bruno** | Infrastructure & Ops Engineer | server, SSH, Docker, Kubernetes, deploy, conservazione dei segreti, backup. Il suo mestiere è togliere infrastruttura, non aggiungerne |
| 🩺 | **Livia** | Clinical Informatics | il contenuto clinico del software sanitario: dato clinico e codifiche, HL7/FHIR/DICOM, FSE 2.0 e Sistema TS, sicurezza del paziente, il reparto vero. Chiede sempre chi userà la schermata e in quanti secondi |
| 🧠 | **Enzo** | AI Engineer | l'impianto delle applicazioni che usano modelli linguistici: RAG, orchestrazione, agenti e tool, output validato, eval, costi. La sua prima domanda è se un modello serva davvero |
| 🧩 | **Milo** | WordPress Component Architect | Gutenberg, Elementor, ACF, campi custom, template e componenti riusabili. Impone che i media finiscano nella Media Library e che i dati strutturati non restino dentro pagine monolitiche |

E tre workflow di servizio:

| Skill | Cosa fa |
| ----- | ------- |
| `grl-profile` | raccoglie il profilo del progetto (otto campi, quasi tutti pre-compilati leggendo il repository; cinque in più se il settore è sanitario). Da eseguire per primo: senza, le figure parlano per luoghi comuni |
| `grl-board` | convoca sul singolo artefatto **solo le figure pertinenti**, dice perché ha escluso le altre, e lascia aperti i disaccordi invece di appianarli |
| `grl-mdsw` | dalla finalità del software alla classe MDR: dice se è un dispositivo medico, cosa comporta e — parte che sgonfia più allarmi — cosa non comporta |

## Come funziona

**Profilo di progetto.** `grl-profile` scrive `_bmad/memory/grl-shared/project-profile.md`: settore,
tipo di software, dati personali trattati, mercato, stack, componenti AI, vincoli noti e — campo
decisivo — la **criticità dichiarata** (hobby/prototipo · interno · produzione con clienti ·
regolamentato). È la criticità a decidere quanto sono severe tutte e dieci le figure. Se il
settore dichiarato è sanitario, il profilo raccoglie in più finalità del software, contesto d'uso,
integrazioni sanitarie, ruolo GDPR ed eventuale qualificazione MDR; altrimenti quei campi non
vengono nemmeno nominati.

**Un'eccezione alla severità.** Livia segnala a qualsiasi livello, anche `light` e anche su un
prototipo, i difetti che possono portare a somministrare, prescrivere o refertare alla persona
sbagliata. Il motivo è che i prototipi sanitari finiscono in reparto più spesso di quanto chi li
scrive immagini.

**Severità.** `strictness_override` in `[modules.grl]` vince se valorizzato; altrimenti si deriva
dalla criticità; in mancanza di entrambi, `normal`.

| Livello | Comportamento |
| ------- | ------------- |
| `light` | parlano solo se il rischio è concreto e imminente; auto-attivazione rara |
| `normal` | segnalano ciò che conta, una volta sola |
| `strict` | segnalano anche i rischi minori e chiedono di mettere per iscritto quelli accettati |

**Memoria condivisa.** Tre file in `_bmad/memory/grl-shared/`, letti da tutte le figure in
attivazione:

- `project-profile.md` — il contesto, scritto da `grl-profile`
- `decisions.md` — le decisioni vincolate: cosa è stato deciso e quale vincolo l'ha imposto
- `accepted-risks.md` — i rischi accettati consapevolmente. **Si scrive solo su conferma esplicita
  dell'utente**, e da quel momento le figure tacciono su quel punto: è il meccanismo anti-rumore
  del modulo

Ogni figura ha inoltre una propria `notes.md` in `_bmad/memory/grl-agent-<code>/`.

**Anti-rumore.** In auto-attivazione parla **al massimo una figura per turno**: quella con la
competenza decisiva secondo le tabelle dei confini, che nomina le altre in una riga e si ferma.
La convocazione multipla è esplicita e si chiama `grl-board`.

**Antipattern vietati a tutte le figure:** allarmismo; citazioni di norme o riferimenti a pioggia
(un riferimento citato = un'azione richiesta); «consulta un esperto» come risposta standard;
checklist recitate a memoria. Il verdetto **«non serve niente» è un risultato legittimo** e si dà
con la stessa sicurezza di un allarme.

## Rapporto con BMM

Guardrails è un'espansione di **BMM** (software development) e funziona anche da sola: nessuna
skill pretende file prodotti da BMM, li legge se ci sono.

Le figure che si sovrappongono a ruoli BMM esistenti non li sostituiscono. Winston e Sally
progettano; Otto e Iris fanno da **revisori critici** su un asse specifico — disciplina strutturale
del codice, originalità visiva. L'attrito è voluto. Enzo si aggiunge alla stessa logica su Amelia:
lei implementa, lui guarda l'impianto della pipeline AI e chiede cosa succede quando il modello
sbaglia.

Tutte e dieci entrano nel roster principale di `bmad-party-mode`, accanto ai cinque agenti BMM.

## Stanze tematiche e sottomoduli

Il bundle `grl` resta oggi l'installazione compatibile unica, ma il dominio è già descritto in
confini topic-oriented in [`src/module-topology.yaml`](src/module-topology.yaml). La topologia
prepara sei futuri package senza duplicare le skill e senza rinominare i comandi già installati:

| Codice | Area | Skill principali |
| ------ | ---- | ---------------- |
| `grc` | Core | setup, profilo, collegio, memoria condivisa |
| `grg` | Governance | privacy, legale, compliance |
| `gre` | Engineering | architettura, sicurezza, ops, AI |
| `grh` | Health | dominio clinico, dispositivo medico |
| `grw` | Web Experience | critica UI, siti e landing |
| `gwp` | WordPress | Gutenberg, campi custom, template, Media Library |

I confini di installazione e quelli di conversazione non coincidono: `grl-setup` registra anche
le stanze di `bmad-party-mode`, che possono convocare agenti di aree diverse:

```text
grl-governance          Vera · Aldo · Nils
grl-engineering         Otto · Kai · Bruno · Enzo
grl-health              Livia · Vera · Nils · Kai
grl-web                 Iris · Milo · Sally (se BMM è installato)
grl-wordpress-delivery  Milo · Iris · Otto · Bruno
grl-release-gate        Vera · Kai · Aldo · Nils · Otto · Bruno
grl-full-board          tutte le figure Guardrails
```

Dopo `grl-setup` si apre una stanza con:

```bash
bmad-party-mode --party grl-wordpress-delivery
```

La configurazione viene scritta nel layer non rigenerato
`_bmad/custom/bmad-party-mode.toml`; gli override e i gruppi dell'utente fuori dal blocco
Guardrails vengono preservati. L'estrazione fisica in package indipendenti sarà una migrazione
successiva: prima verranno validati `gwp` e `grh`, poi gli altri domini.

## Installazione

Con l'installer BMad, indicando questo repository come sorgente custom:

```bash
npx bmad-method install --custom-source https://github.com/mlarese/bmad-module-guardrails
```

L'installer copia le quindici skill, registra le dieci figure come agenti
(`[agents.grl-agent-*]` nella configurazione) — che è ciò che le fa comparire nel roster di
`bmad-party-mode` — aggiunge le voci di help al catalogo `_bmad/_config/bmad-help.csv` e,
eseguendo `grl-setup`, installa anche le stanze tematiche.

In alternativa, per un'installazione manuale o per riconfigurare un'installazione esistente,
si esegue la skill **`grl-setup`**.

**Primo passo dopo l'installazione: `grl-profile`.** Senza profilo le figure partono cieche.

Nota sulla configurazione: con BMad 6.10.0 la variabile `strictness_override` viene scritta in
`_bmad/grl/config.yaml`, che il resolver a quattro layer non legge; dalla 6.10.1 finisce anche in
`[modules.grl]` del config TOML, dove le figure la cercano. Su una 6.10.0, eseguire `grl-setup`
dopo l'installer sistema la cosa.

## Struttura

```
.claude-plugin/marketplace.json   indice letto dall'installer BMad
src/
├── module.yaml                   manifesto del modulo: config e roster delle figure
├── module-topology.yaml           confini dei futuri package topic-oriented
├── module-help.csv               voci di help
└── skills/
    ├── grl-agent-privacy/        🛡️ Vera
    ├── grl-agent-security/       🔐 Kai
    ├── grl-agent-legal/          ⚖️ Aldo
    ├── grl-agent-compliance/     📐 Nils
    ├── grl-agent-ui-critic/      👁️ Iris
    ├── grl-agent-architecture/   🧱 Otto
    ├── grl-agent-ops/            🖥️ Bruno
    ├── grl-agent-health/         🩺 Livia
    ├── grl-agent-ai/             🧠 Enzo
    ├── grl-agent-wordpress/      🧩 Milo
    ├── grl-profile/              workflow — profilo di progetto
    ├── grl-board/                workflow — revisione collegiale
    ├── grl-mdsw/                 workflow — qualificazione dispositivo medico
    ├── grl-web/                  l'unica skill che produce: landing page e siti
    └── grl-setup/                installazione, roster e stanze party tematiche
        └── assets/party-groups.toml
docs/module-plan.md               il documento di piano del modulo
```

Il piano in `docs/` documenta le decisioni di progetto e il loro razionale: architettura,
contratto di memoria, confini fra le figure e i brief da cui ogni skill è stata costruita.
