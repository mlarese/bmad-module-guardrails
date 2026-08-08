---
name: threat-model
description: Da dove verrebbe l'attacco vero, in ordine di probabilità, con la contromisura minima per ciascuna strada
code: TM
added: 2026-08-06
type: prompt
---

# Threat model leggero

## Cosa vuol dire riuscirci

L'utente esce sapendo le **tre-cinque strade** con cui il suo sistema verrebbe realmente attaccato, **in ordine di probabilità**, e cosa costa chiudere ciascuna.

Il consumatore è chi lunedì mattina ha mezza giornata e deve decidere dove spenderla. Se la prima voce non è quella da cui arriverebbe l'attacco vero, il lavoro è fallito anche se l'elenco è completo.

## Come si ordina

Per **probabilità reale**, non per gravità teorica.

Alzano la probabilità: l'attacco è automatizzabile e già automatizzato (credential stuffing, scanner di segreti su GitHub, bot che provano `/admin` e `/.env`) · basta un browser per tentarlo · la superficie è pubblica e indicizzabile · c'è un guadagno diretto (dati rivendibili, calcolo gratis, invio di email a spese altrui).

Abbassano la probabilità: serve già un accesso privilegiato per arrivarci · il sistema sta dietro rete interna o VPN · l'attaccante deve essere interessato *a questo* bersaglio in particolare.

Conseguenza da dire ad alta voce quando succede: **una vulnerabilità critica non raggiungibile viene dopo una debolezza media esposta al pubblico.** È il punto in cui il threat model batte la checklist.

## Da dove partire quando l'input è scarno

Tre domande, non un questionario:

1. chi può raggiungere il sistema senza credenziali?
2. cosa c'è dentro che vale la pena prendere?
3. cosa succede se un utente legittimo diventa ostile?

## Forma dell'output

Elenco ordinato o tabella. Per ogni scenario: **come entrerebbe** (una frase concreta, sul sistema che hai davanti, non in astratto) · **cosa otterrebbe** · **contromisura minima** con il costo indicativo.

Chiudi con **cosa non ti preoccupa e perché**. È la parte che rende credibile il resto e che evita al team di spendere tempo dove non serve.

## Trappole

- **Il sistema senza attaccanti plausibili.** Un tool interno da tre persone non ha un threat model. Dillo e fermati.
- **Il diagramma STRIDE completo.** È esattamente il documento che questo modulo ha deciso di non produrre.
- **L'attaccante onnipotente.** Se lo scenario regge solo assumendo un avversario statuale, non è il primo della lista.
- **Lo scenario che sfonda in un altro dominio** (il dato personale in sé, la licenza, lo strato di astrazione): nominalo alla figura giusta in una riga e torna alla superficie.
