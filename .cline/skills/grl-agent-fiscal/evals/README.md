# Eval di grl-agent-fiscal (🧾 Marta)

La cartella contiene casi di qualità e query di attivazione. Marta deve distinguere fonte
primaria e aggregatore, verificare dati aggiornabili, chiedere il profilo minimo per un
bando e non presentarsi come commercialista abilitata.

| File | Uso |
| --- | --- |
| cases.json | quality, baseline o variant con bmad-eval-runner |
| triggers.json | trigger con bmad-eval-runner |

I near miss proteggono i confini con Aldo per contratti e licenze, Nils per la compliance
regolatoria, Vera per privacy e Kai per la sicurezza.
