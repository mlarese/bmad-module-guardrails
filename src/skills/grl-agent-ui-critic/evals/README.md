# Eval di grl-agent-ui-critic (👁️ Iris)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-ui-critic` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-ui-critic/evals/triggers.json` |

## Cosa misurano i casi

Iris presidia critica di design. Il tratto da proteggere è che non stronchi mai senza dare la deviazione concreta, con dei valori dentro.

| Caso | Prima riga della rubric |
| ---- | ----------------------- |
| `riconosce-i-tic` | la risposta riconosce almeno tre segni specifici dell'estetica generata e li nomina per quello c… |
| `va-bene-cosi` | la risposta dice che così va bene, e lo dice come verdetto invece di proporre miglioramenti di c… |
| `identita-visiva-direzioni` | la risposta propone due o tre direzioni distinte fra cui scegliere, non una sola |
| `accessibilita-senza-imbruttire` | la risposta dice che il colore del brand non va cambiato, e propone di cambiare il testo sopra o… |
| `confine-conversione` | la risposta riconosce che il problema riguarda cosa la pagina dice e in che ordine, e lo passa a… |
| `memoria-nessuna-scrittura-non-confermata` | la risposta non scrive nulla in accepted-risks.md senza aver chiesto conferma esplicita all'uten… |

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

20 query, 10 should e 10 should-not. Le should-not sono **near miss**: condividono
lessico e dominio con le should, e ognuna appartiene per confine a un'altra figura —
grl-web per cosa la pagina dice e in che ordine, Nils per l'obbligo di accessibilità, Otto per i confini del codice, Livia per quale informazione clinica deve essere raggiungibile e in quanti secondi, Enzo per cosa mostrare durante lo streaming.

Se una di queste fa scattare Iris, il confine scritto nel `SKILL.md` non sta reggendo.

## Confini misurabili

La description mantiene il confine fra critica visiva, copy/conversione e accessibilità normativa.
Le richieste miste non vengono scartate in blocco: Iris prende la parte visiva e passa a Sally o
Nils la parte di loro competenza. Le should-not restano near miss, così il router può distinguere
un vero problema di aspetto da una richiesta che usa solo lo stesso lessico.
