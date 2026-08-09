---
name: revisione-database
description: Revisiona schema, query e architettura esistenti separando finding osservati da ipotesi e ordinandoli per impatto.
code: RV
added: 2026-08-09
type: prompt
---

# Revisione di un database esistente

## Esito

Da tre a cinque finding prioritizzati che il team può verificare e correggere: path o oggetto
preciso, evidenza, conseguenza sul workload, intervento minimo, costo, rischio e criterio di
successo. Se il sistema è sano, dillo senza inventare problemi.

## Materiale utile

Chiedi solo ciò che cambia il verdetto: DDL, query lente e frequenti, piani `EXPLAIN`, metriche
per percentile, schema/indice, volume e crescita, lock/deadlock, replica, backup/restore,
versione/edizione e modalità managed. Non chiedere dump di dati personali; bastano schema,
cardinalità aggregate e campioni anonimizzati.

## Regola di lettura

Prima marca **osservato** ciò che è nel materiale, poi **ipotesi** ciò che va misurato. Ordina per
impatto × probabilità × costo di intervento. Un indice duplicato, una query non sargable, un
confine transazionale perso, una chiave calda o un restore mai provato contano più di una lista
astratta di best practice. Ogni finding deve finire con una prova o con `da verificare`.

Per un bug o una regressione difficile usa questo ciclo stretto:

1. costruisci un test, replay o query minima che fallisce in modo ripetibile;
2. scrivi da tre a cinque ipotesi falsificabili, senza presentarle come cause;
3. misura una variabile per volta — piano, cardinalità, lock, I/O, latenza o dato — e scarta le
   ipotesi che non reggono;
4. applica la modifica minima e aggiungi una regressione al confine che protegge l'invariante;
5. rimuovi la strumentazione temporanea e annota cosa renderebbe la diagnosi nuovamente valida.
