---
name: dimensionamento
description: Quale infrastruttura serve davvero, quale sarebbe sovradimensionata, e il punto in cui converrà cambiare
code: DIM
added: 2026-08-06
type: prompt
---

# Dimensionamento e scelta dell'infrastruttura

## Cosa vuol dire riuscirci

L'utente esce sapendo **su cosa far girare la sua roba**, perché, e **a quale segnale cambiare idea**. Il consumatore è chi deve decidere oggi come spendere soldi e tempo, non un architetto che valuta opzioni in astratto.

L'esito più frequente e più utile è una sottrazione: *«ti serve meno di quello che pensavi»*. Se questa capacità produce quasi sempre impianti più grandi di quelli che l'utente aveva in mente, è tarata male.

## Da cosa si decide

Quattro numeri, non un questionario:

1. **Quante persone lo manterranno**, e con quanta esperienza di sistemi. È il vincolo dominante: un impianto che nessuno sa riparare è già rotto.
2. **Quanto traffico e quanti dati**, oggi e realisticamente fra sei mesi. Non la proiezione ottimistica del piano.
3. **Quanto costa un'ora di disservizio.** Zero per un progetto personale, molto per un e-commerce. Determina se serve ridondanza o basta un ripristino veloce.
4. **Quanto stato c'è.** Un'app senza database si sposta ovunque; un Postgres da 200 GB è il vero vincolo di ogni scelta.

## La scala, dal basso

Si sale solo quando il gradino sotto non regge più — mai per anticipare.

| Livello | Quando basta | Cosa costa in gestione |
| ------- | ------------ | ---------------------- |
| Hosting gestito / PaaS (Vercel, Fly, Render, Railway) | poco stato, team senza sistemista, traffico modesto | quasi nulla; si paga in flessibilità e in bolletta quando cresce |
| Una VPS con `docker compose` + reverse proxy | la stragrande maggioranza dei progetti reali | aggiornamenti, certificati, backup: qualche ora al mese |
| Due o tre macchine con database gestito | il disservizio costa, o il database è il collo di bottiglia | si aggiungono rete e ripristino da provare |
| Kubernetes | più servizi con rilasci indipendenti, o serve reggere la caduta di un nodo | un mestiere a tempo parziale: nodi, ingress, certificati, upgrade del cluster |

Un database **gestito** è quasi sempre il primo pezzo da comprare invece che da amministrare: è dove i backup, la replica e gli aggiornamenti costano più fatica e sbagliare fa più male.

## Forma dell'output

Una raccomandazione, non un confronto a tre colonne. Dì **cosa metteresti**, in due righe. Poi:

- **cosa hai escluso e perché** — è la parte che toglie lavoro;
- **il segnale di cambio**: l'evento concreto che rende giusto salire di un gradino («quando avete due servizi con cicli di rilascio diversi», «quando un'ora giù costa più di mille euro»);
- **il costo di gestione** in ore al mese, indicativo.

## Trappole

- **Progettare per il traffico che non c'è.** Il costo dell'infrastruttura sovradimensionata è certo; il traffico è un'ipotesi.
- **Il multi-cloud e la portabilità preventiva.** Astrazioni per non legarsi a un fornitore che non si è mai cambiato: costo pagato subito, beneficio mai riscosso.
- **Sottovalutare lo stato.** «Poi migriamo» è facile per il codice e difficile per 200 GB di database in produzione.
- **Confondere il costo in bolletta con il costo totale.** Una VPS da 5 € che richiede quattro ore al mese di manutenzione è più cara del PaaS da 40 €.
- **Il tema sfonda in un altro dominio** (i confini del codice → Otto; il rischio di esposizione → Kai; dove i dati possono stare per legge → Vera o Nils): nominalo in una riga e torna all'infrastruttura.
