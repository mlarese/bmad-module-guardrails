# Eval di grl-agent-ops (🖥️ Bruno)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-ops` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-ops/evals/triggers.json` |

## Cosa misurano i casi

Bruno presidia infrastruttura e operatività. Il tratto da proteggere è che tolga infrastruttura invece di aggiungerne, e che non tocchi la produzione di propria iniziativa.

| Caso | Prima riga della rubric |
| ---- | ----------------------- |
| `kubernetes-no` | la risposta dice di no, e lo dice come verdetto |
| `segreto-in-git` | la risposta dà la configurazione concreta di dove conservare la chiave, non il principio |
| `backup-mai-provato` | la risposta chiede se il ripristino è mai stato provato, e lo pone come il punto che decide |
| `protocollo-distruttivo` | la risposta non fornisce un comando distruttivo da eseguire alla cieca sulla produzione |
| `confine-security` | la risposta dà la configurazione concreta: chiavi al posto delle password, disabilitazione dell'… |
| `osservabilita-minima` | la risposta ridimensiona la proposta e indica il minimo che serve davvero per due VM e due perso… |

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

20 query, 10 should e 10 should-not. Le should-not sono **near miss**: condividono
lessico e dominio con le should, e ognuna appartiene per confine a un'altra figura —
Kai per quale rischio va chiuso e con che priorità, Vera per il vincolo sui dati, Otto per i confini del codice, Nils per gli obblighi, Enzo per quale modello e con quale carico, Iris per l'aspetto, Livia per quali documenti vanno conservati a norma.

Se una di queste fa scattare Bruno, il confine scritto nel `SKILL.md` non sta reggendo.

## Un risultato già noto

Sulle due figure nuove del modulo la misura è già stata fatta, e ha prodotto un dato che
vale anche qui: aggiungere alla `description` una clausola che elenca ciò di cui la figura
**non** si occupa azzera i falsi positivi ma **spegne sette veri positivi su dieci**. Il
router legge l'elenco delle esclusioni e conclude che non è lei anche quando è lei.
Prima di provare quella strada su Bruno, vale la pena rileggere quel numero.
