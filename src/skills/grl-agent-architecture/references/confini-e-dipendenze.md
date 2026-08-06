---
name: confini-e-dipendenze
description: Dove passano i confini del codice, in che direzione puntano le dipendenze, e dove va collocata una feature nuova
code: CD
---

# Confini e dipendenze

## Com'è fatto un buon esito

L'utente sa **dove passano i confini** del suo codice e **quali dipendenze puntano dalla parte sbagliata**, con il costo concreto di ciascuna. Non un diagramma: un elenco corto di punti su cui può decidere oggi.

Se la domanda è invece *«dove metto questa feature?»*, l'esito è: dove va, cosa non va toccato, e il segnale che dirà se il confine sta cedendo.

## Guarda la struttura vera, prima di dire qualsiasi cosa

Albero delle cartelle e import reali. Se non hai accesso al codice, chiedilo o dichiara che stai ragionando sulla descrizione — non su ciò che hai davanti.

Segnali che valgono la pena di essere nominati, in ordine di gravità tipica:

| Segnale | Cosa significa | Costo se resta |
| ------- | -------------- | -------------- |
| Ciclo di import fra due moduli | non sono due moduli, è uno solo travestito da due | ogni modifica all'uno richiede di capire l'altro; i test non si isolano |
| Il dominio importa l'infrastruttura (ORM, HTTP, SDK del cloud) | il confine c'è nel nome delle cartelle, non nel codice | cambiare la persistenza o il framework significa riaprire le regole di business |
| Una cartella importata da tutte le altre (`utils/`, `common/`, `helpers/`, `core/`) | non è un confine, è una discarica | cresce senza limite, nessuno sa cosa può togliere, ogni build la ricompila |
| Ogni feature tocca gli stessi 4-5 file in cartelle diverse | il confine è nel posto sbagliato: taglia per strato ciò che cambia per feature | ogni modifica costa cinque aperture e cinque conflitti di merge |
| Un modello/DTO che attraversa tutti gli strati | non ci sono strati, c'è una struttura dati condivisa | un campo aggiunto per la UI arriva fino al database |
| Dipendenza verso l'esterno non isolata (chiamata di rete, orologio, filesystem sparsi ovunque) | niente si testa senza il mondo vero | test lenti e instabili, comportamento non riproducibile |

Assenza di segnali è un esito: dillo e chiudi.

## Cosa consegni

- **Mappa dei confini**: una tabella `confine → cosa contiene → da chi può essere importato`. Corta: se supera sei righe su un progetto piccolo, stai inventando confini.
- **Dipendenze che puntano storto**: per ciascuna, `da → a`, perché è sbagliata, **il costo di lasciarla** e l'intervento minimo per raddrizzarla. L'intervento minimo di solito è spostare un file o invertire una firma, non introdurre uno strato.

## Quando la domanda è dove collocare una feature

Rispondi in tre righe:

1. **Dove va** — cartella o modulo, e perché quello.
2. **Cosa non va toccato** — i punti che la feature sarebbe tentata di modificare e che invece devono restare fermi.
3. **Il segnale** — cosa dovrà accadere perché valga la pena rivedere il confine (es. «se questa feature finisce per importare tre moduli diversi, il confine è sbagliato e ne riparliamo»).

Se la feature sfonda un confine e non c'è modo di collocarla senza forzarlo, dillo: è la struttura che è arrivata al suo limite, non la feature a essere scritta male.

## Due cose che non si fanno

- **Nessuna riorganizzazione totale dell'albero.** Costo alto e certo, beneficio incerto: se ne parla solo quando l'utente lo chiede esplicitamente.
- **Nessun confine introdotto in anticipo** perché «un giorno ci saranno più domini». Il confine si mette quando due cose si pestano davvero.

Se una scelta di confine sposta o allarga la superficie esposta all'esterno (autenticazione, endpoint pubblici, dati che escono dal processo), nominalo in una riga e passa la palla a Kai.
