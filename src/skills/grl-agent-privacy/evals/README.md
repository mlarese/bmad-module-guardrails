# Eval di grl-agent-privacy (🛡️ Vera)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-privacy` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-privacy/evals/triggers.json` |

## Cosa misurano i casi

Vera presidia privacy e GDPR. Vera parla e non produce documenti: le rubric guardano il testo della risposta e la memoria condivisa.

| Caso | Prima riga della rubric |
| ---- | ----------------------- |
| `non-si-applica-niente` | la risposta dice che qui il GDPR non si applica, e lo dice come verdetto in una riga invece di e… |
| `base-giuridica-non-consenso` | la risposta dice che per la creazione dell'account non serve il consenso, perché il trattamento … |
| `dati-fuori-posto-nei-log` | la risposta segnala che nei log finiscono dati personali che nessuno ha deciso di raccogliere lì |
| `dpia-verdetto-negativo` | la risposta dice che qui la DPIA non serve, senza scuse e senza raccomandazioni di ripiego |
| `cancellazione-e-backup` | la risposta dice che no, la cancellazione non è completa, e nomina entrambe le copie: backup e d… |
| `confine-sicurezza-e-ops` | la risposta pone il vincolo di trasferimento extra-UE come questione di sua competenza, in poche… |
| `memoria-nessuna-scrittura-non-confermata` | la risposta non scrive nulla in accepted-risks.md senza aver chiesto conferma esplicita all'uten… |

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

20 query, 10 should e 10 should-not. Le should-not sono **near miss**: condividono
lessico e dominio con le should, e ognuna appartiene per confine a un'altra figura —
Nils per le norme di settore, Kai per come si cifra e per le superfici esposte, Aldo per licenze e DPA, Bruno per dove i dati vivono, Iris per il cookie banner, Livia per la struttura del dato clinico, Enzo per il retrieval.

Se una di queste fa scattare Vera, il confine scritto nel `SKILL.md` non sta reggendo.

## Un risultato già noto

Sulle due figure nuove del modulo la misura è già stata fatta, e ha prodotto un dato che
vale anche qui: aggiungere alla `description` una clausola che elenca ciò di cui la figura
**non** si occupa azzera i falsi positivi ma **spegne sette veri positivi su dieci**. Il
router legge l'elenco delle esclusioni e conclude che non è lei anche quando è lei.
Prima di provare quella strada su Vera, vale la pena rileggere quel numero.
