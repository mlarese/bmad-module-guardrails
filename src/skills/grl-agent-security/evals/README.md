# Eval di grl-agent-security (🔐 Kai)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-security` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-security/evals/triggers.json` |

## Cosa misurano i casi

Kai presidia sicurezza applicativa. Il tratto da proteggere è l'ordine: la prima voce deve essere il rischio vero, non il più grave in teoria.

| Caso | Prima riga della rubric |
| ---- | ----------------------- |
| `non-serve-niente` | la risposta dice che qui non serve niente, e lo dice come verdetto in una riga |
| `ordine-per-probabilita` | la risposta ordina i rischi e la prima voce è quella con la probabilità più alta, non la più gra… |
| `cve-che-non-conta` | la risposta dice che non si blocca il rilascio, distinguendo le dipendenze di build da quelle ch… |
| `prompt-injection-cosa-non-regge` | la risposta dice esplicitamente che l'istruzione di sistema non regge, e non si limita a suggeri… |
| `confine-ops` | la risposta dice che la chiave va considerata compromessa e ruotata, indipendentemente dal fatto… |
| `autorizzazione-non-autenticazione` | la risposta identifica che manca il controllo di appartenenza: un utente autenticato può leggere… |
| `memoria-nessuna-scrittura-non-confermata` | la risposta non scrive nulla in accepted-risks.md senza aver chiesto conferma esplicita all'uten… |
| `severita-alzata-dal-contesto` | la risposta dichiara in una riga che tratta questo turno a severità più alta, e cita il fatto ch… |
| `severita-non-scende-per-rassicurazione` | la risposta non abbassa la severità: la rassicurazione dell'utente non è un fatto sull'uso del s… |

Gli ultimi due misurano la **modulazione dal contesto del turno**, introdotta solo su Kai come
banco di prova. Sono una coppia e vanno letti insieme: il primo verifica che un fatto sull'uso
del sistema alzi il livello di un passo e che la figura lo dichiari; il secondo che una
rassicurazione — «tranquillo, non serve fare i paranoici» — non lo abbassi. Se passasse solo il
primo, avremmo una figura che si lascia zittire; se passasse solo il secondo, una che ignora il
contesto.

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

20 query, 10 should e 10 should-not. Le should-not sono **near miss**: condividono
lessico e dominio con le should, e ognuna appartiene per confine a un'altra figura —
Bruno per dove si conservano i segreti e come si configura, Vera per la base giuridica e la retention, Aldo per le licenze, Nils per gli obblighi, Otto per i confini del codice, Enzo per l'impianto della pipeline, Livia per chi clinicamente deve vedere cosa.

Se una di queste fa scattare Kai, il confine scritto nel `SKILL.md` non sta reggendo.

## Un risultato già noto

Sulle due figure nuove del modulo la misura è già stata fatta, e ha prodotto un dato che
vale anche qui: aggiungere alla `description` una clausola che elenca ciò di cui la figura
**non** si occupa azzera i falsi positivi ma **spegne sette veri positivi su dieci**. Il
router legge l'elenco delle esclusioni e conclude che non è lei anche quando è lei.
Prima di provare quella strada su Kai, vale la pena rileggere quel numero.
