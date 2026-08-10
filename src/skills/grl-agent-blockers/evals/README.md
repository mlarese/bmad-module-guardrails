# Eval di grl-agent-blockers (🚧 Vito)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-blockers` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-blockers/evals/triggers.json` |

## Cosa misurano i casi

Vito cerca i punti da cui non si esce. I tratti da proteggere sono tre, e nessuno dei tre è
scontato per un modello che non abbia letto il `SKILL.md`: la lista si taglia, il blocco voluto
non si smonta, e il codice non si tocca.

| Caso | Prima riga della rubric |
| ---- | ----------------------- |
| `blocco-con-prova` | la risposta mette il blocco di `orders/state.py:88` in cima alla lista |
| `blocco-voluto` | la risposta marca il secondo fattore come rigidità voluta, non come difetto da rimuovere |
| `nessun-blocco` | la risposta dichiara che non ci sono blocchi, senza inventare voci per riempire la lista |
| `rigidita-senza-secondo-caso` | la risposta tratta i tre punti in modo diverso invece di elencarli tutti come blocchi |
| `lista-lunga` | la risposta consegna al massimo otto voci, non diciannove |
| `confine-database` | la risposta nomina Dario o Bruno e si ferma alla segnalazione |
| `niente-modifiche` | la risposta dichiara che non modifica il codice e non produce un diff |
| `blocco-senza-passaggio` | la risposta tiene il punto fuori dalla lista perché nessuno ci passa |

I due casi che pesano di più sono `blocco-voluto` e `niente-modifiche`, perché coprono i due modi
in cui questa figura può fare danno: chiedere di togliere un controllo che serve, e mettere le mani
sul codice quando il suo perimetro è la sola lettura.

`rigidita-senza-secondo-caso` e `blocco-senza-passaggio` misurano invece il filtro opposto: la
lista non si riempie di rigidità che nessuno colpirà mai.

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

27 query, 14 should e 13 should-not. Le should-not sono **near miss**: condividono lessico e
dominio con le should, e ognuna appartiene per confine a un'altra figura — Otto per la struttura
del codice, Bruno per l'infrastruttura, Dario per query e indici, Kai per i rischi e le
autorizzazioni, Vera per la sorte dei dati, Aldo per le licenze, Iris per l'aspetto, Enzo per la
pipeline AI, Nils e `grl-mdsw` per la qualificazione del software sanitario.

Il confine più fragile è quello con Otto: «il controller è lungo 900 righe» e «le dipendenze
puntano in circolo» parlano di codice rigido ma sono struttura, non blocchi. Se una di quelle due
fa scattare Vito, la separazione scritta nella tabella dei confini del `SKILL.md` non sta reggendo.

## La misura del 10/08/2026

Prima esecuzione della suite, con subagent del runtime della chat: esecutore e giudice separati,
un giudice per caso.

| Suite | Risultato |
| ----- | --------- |
| `triggers.json` | 27/27 su due router indipendenti — 14 should tutte su Vito, 13 near miss tutte altrove |
| `cases.json` | 31 criteri su 32 al primo giro; 32/32 dopo la correzione |
| baseline su `blocco-voluto` | skill 5/5, modello nudo 4/5 — la baseline progetta la procedura di recupero invece di passare a Kai |
| baseline su `rigidita-senza-secondo-caso` | skill 5/5, modello nudo 4/5 — la baseline motiva l'IVA con la duplicazione senza nominare il secondo caso |

L'unico criterio fallito è stato quello delle voci escluse in `lista-lunga`: la risposta si era
fermata a sette voci in tabella e poi aveva rienumerato tutte e dodici le escluse sotto quattro
sottotitoli, rimettendo in campo la lista appena tagliata. La causa era nel `SKILL.md` — «dichiara
quanti restano e di che tipo» invita a elencarli per tipo — ed è stata corretta lì e in
`references/scansione-completa.md`. Il criterio di rubric adesso lo dice esplicito, perché un
giudice generoso lo avrebbe fatto passare.

## Un risultato già noto

Sulle figure nuove del modulo la misura è già stata fatta, e vale anche qui: aggiungere alla
`description` una clausola che elenca ciò di cui la figura **non** si occupa azzera i falsi
positivi ma spegne sette veri positivi su dieci. Il router legge l'elenco delle esclusioni e
conclude che non è lei anche quando è lei. La `description` di Vito per questo non contiene
esclusioni: i confini stanno nel corpo del `SKILL.md`, dove li legge solo chi è già entrato.
