---
name: mappa-dati
description: Mappa quali dati personali il sistema tocca, dove entrano, dove finiscono e chi li vede
code: MD
added: 2026-08-06
type: prompt
---

# Mappa dei dati

L'esito è un elenco parlato dei flussi di dati personali del sistema: dove entrano, dove si fermano, dove escono, chi li vede. Il consumatore è chi dovrà poi cambiare qualcosa — uno sviluppatore, non un giurista: nomina i dati come esistono davvero (campo, tabella, endpoint, servizio) e mai per categoria astratta.

Lavora su ciò che c'è: PRD, schema del database, modelli, integrazioni verso servizi terzi, variabili d'ambiente, codice. Se non c'è nulla da leggere, ricostruisci il flusso con poche domande secche — non un questionario.

Tre cose che nessuno racconta spontaneamente e che devi andare a cercare:

- **Le uscite.** Analytics, mail transazionali, error tracking, LLM, CRM, pagamenti, backup: ogni servizio terzo è un flusso di dati personali finché non provi il contrario.
- **Chi vede.** Un pannello di amministrazione che mostra tutto, un ruolo di supporto con accesso completo, la produzione aperta agli sviluppatori. La domanda «chi li vede» dà quasi sempre più risultati della domanda «quali dati».
- **Le categorie particolari.** Salute, opinioni, orientamento, biometrici, dati di minori. Cambiano il gioco, e spesso entrano di contrabbando dentro un campo `note` a testo libero o un allegato.

Marca solo i punti critici, e dì perché sono critici. Un flusso normale non ha bisogno di commento.

Se dalla mappa emerge un dato che sta dove nessuno ha deciso che stesse, non risolverlo qui: nominalo e indica la capacità *Dati dove non dovrebbero stare* (FP). Se emerge profilazione su larga scala, monitoraggio sistematico o categorie particolari in quantità, dillo e proponi *Pre-DPIA* (DP).
