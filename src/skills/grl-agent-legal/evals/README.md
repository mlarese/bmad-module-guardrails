# Eval di grl-agent-legal (⚖️ Aldo)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-legal` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-legal/evals/triggers.json` |

## Cosa misurano i casi

Aldo presidia legale, licenze e contratti, ed è il riferimento del modulo sull'AI Act generale.
FRIA, bias, basi giuridiche, minimizzazione, retention e spiegazione nell'intersezione AI Act-GDPR
restano di Vera. Due tratti da proteggere: Aldo non rinvia mai a un altro legale — l'esperto è lui
— e non rimanda a Nils la classificazione generale di un sistema AI, che dal passaggio della materia
è sua; sulle richieste miste separa invece l'handoff verso Vera.

| Caso | Prima riga della rubric |
| ---- | ----------------------- |
| `agpl-nel-saas` | la risposta dice che sì, l'AGPL scatta anche senza distribuzione, perché copre l'uso via rete |
| `non-ci-sono-vincoli` | la risposta dice che sì, si può vendere senza pubblicare il codice, e lo dice come verdetto |
| `codice-generato-da-ai` | la risposta dice che l'output generato da un modello di norma non ottiene protezione d'autore in… |
| `fine-tuning-multi-cliente` | la risposta dice che il modello risultante può restituire a un cliente i dati di un altro, e lo … |
| `trasparenza-e-classificazione` | la risposta classifica il sistema invece di rimandare la classificazione a un'altra figura |
| `capitolato-del-committente` | la risposta segnala che la clausola come scritta porterebbe via anche il framework riusabile, ch… |
| `white-label-del-sistema-ai` | la risposta dice che mettendoci il proprio marchio il cliente diventa fornitore ai fini dell'AI … |
| `white-label-ai-act` | la risposta dice che chi mette il proprio marchio sul sistema diventa fornitore ai fini dell'art… |
| `corso-art-4` | la risposta conferma che l'obbligo di alfabetizzazione dell'art. 4 esiste e vale anche per uno s… |
| `azienda-da-mettere-in-regola` | la risposta parte dall'inventario dei sistemi e dice che è il primo deliverable |
| `algoritmo-sui-dipendenti` | la risposta dice che il sistema è alto rischio per l'Allegato III, perché valuta e monitora pers… |
| `incidente-e-notifica` | la risposta distingue i due regimi: data breach da un lato, incidente grave dall'altro |

I quattro casi su docenza, consulenza aziendale, lavoratori e incidenti misurano il tratto
opposto a quello delle licenze: lì il rischio è tacere, qui è **produrre adempimenti che non
esistono**. Le rubric lo controllano per nome — nessun attestato riconosciuto, nessun
responsabile IA obbligatorio, nessuna ISO 42001 spacciata per obbligo.

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

39 query, 26 should e 13 should-not. Le should-not sono **near miss**: condividono
lessico e dominio con le should, e ognuna appartiene per confine a un'altra figura —
Nils per accessibilità, NIS2, CRA e obblighi settoriali, Vera per la base giuridica e la FRIA, Kai per le vulnerabilità e il prompt injection, Enzo per la scelta tecnica del modello, Bruno per dove gira, Otto per i confini, Livia per il dominio clinico.

Le dodici should nuove coprono la materia arrivata con l'AI Act: classificazione, trasparenza,
adeguamento aziendale, corsi e art. 4, sicurezza, lavoratori, incidenti. Sono le stesse query
che negli eval di Nils compaiono ora come should-not: se scattano su entrambi, il travaso della
materia non è stato pulito.

Se una di queste fa scattare Aldo, il confine scritto nel `SKILL.md` non sta reggendo.

## Confini misurabili

La description separa AI Act generale e intersezione AI Act-GDPR: Aldo prende classificazione,
ruoli e obblighi generali; Vera prende FRIA, bias, basi giuridiche, minimizzazione, retention e
spiegazione collegata al GDPR. Le richieste miste devono produrre due handoff distinti, non uno
scarto totale della richiesta.
