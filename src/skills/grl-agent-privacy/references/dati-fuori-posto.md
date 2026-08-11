---
name: dati-fuori-posto
description: Trova i dati personali finiti in log, analytics, prompt verso un LLM, ambienti di test o backup, con il rimedio minimo
code: FP
added: 2026-08-06
type: prompt
---

# Dati personali dove non dovrebbero stare

L'esito è l'elenco dei punti in cui dati personali finiscono dove nessuno ha deciso che dovessero stare, ciascuno con il suo rimedio. **Minimo** è la parola che conta: il rimedio giusto è quasi sempre una riga di configurazione, un campo tolto o un flag cambiato — non un progetto.

Dove guardare davvero, in ordine di frequenza:

- **Log.** L'oggetto utente intero stampato in console, lo stack trace che porta con sé il corpo della richiesta, i log di accesso con la query string che contiene la mail, e i servizi esterni di logging o error tracking che replicano tutto fuori.
- **Analytics.** L'identificativo utente che è la mail, i campi custom, il session replay che registra i moduli mentre vengono compilati.
- **Prompt verso un LLM.** Il contenuto dell'utente inviato al modello, i prompt conservati dal fornitore, e l'impostazione che consente o meno l'uso di quei dati per l'addestramento.
- **Ambienti di test, staging e demo.** Una copia della produzione usata come seed: il caso più comune e il più grave, perché moltiplica gli accessi.
- **Backup.** Chi li ha, dove stanno, per quanto, chi può leggerli.
- **URL e referrer.** Token, mail o identificativi in query string finiscono nei log di ogni intermediario e nel referrer dei siti di destinazione.
- **Email e notifiche interne** che contengono il contenuto dell'utente.

Lavora sui file veri quando ci sono: configurazione del logging, chiamate al client di analytics, integrazione con il modello, script di seed, pipeline, variabili d'ambiente.

Per ogni punto trovato dì quattro cose: cosa esce, dove finisce, chi lo vede, qual è il rimedio più corto. Ordina per quanto è probabile che qualcuno lo legga davvero, non per gravità teorica.

Se il problema non è il dato ma il fatto che quel log o quell'archivio sia **esposto** verso l'esterno, la superficie non è materia tua: nominala e passa la palla a Kai (`grl-agent-security`) in una riga.

## Quando i dati escono dall'UE

Un dato che finisce su un server fuori dallo Spazio economico europeo — o presso un fornitore che lo replica lì — è un **trasferimento**, e serve uno strumento che lo regga. Si decide in tre passi:

1. **Il paese ha una decisione di adeguatezza?** Se sì, il trasferimento sta in piedi da solo. L'elenco cambia: verificalo, non ricordarlo.
2. **Se no, quale strumento?** Nella pratica sono le clausole contrattuali tipo (SCC) nel contratto col fornitore, o le norme vincolanti d'impresa dentro un gruppo. Senza uno dei due, il trasferimento non ha base.
3. **Le SCC bastano da sole?** No: serve una valutazione del trasferimento, che guarda la legge del paese di destinazione e chi può accedere ai dati lì. Se l'accesso delle autorità locali svuota le garanzie, servono misure in più — cifratura con chiavi tenute in UE, pseudonimizzazione — oppure il trasferimento non si fa.

Tre cose che non sono un trasferimento regolare: «il fornitore è americano ma i server sono in Irlanda» va verificato nel contratto, non creduto; «tanto sono dati pseudonimizzati» resta un trasferimento; l'accesso da remoto per assistenza è un trasferimento anche senza copia.

Dove finiscono fisicamente i dati e come si configura la regione è di Bruno (`grl-agent-ops`): tu poni il vincolo, lui lo realizza.
