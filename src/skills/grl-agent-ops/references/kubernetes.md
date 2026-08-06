---
name: kubernetes
description: Il verdetto sull'adozione — spesso «no» — e, se il cluster c'è, i manifest che reggono
code: K8S
added: 2026-08-06
type: prompt
---

# Kubernetes quando serve davvero

## Cosa vuol dire riuscirci

Due esiti possibili, entrambi legittimi:

- **«Non ti serve»**, con il motivo e il segnale a cui cambiare idea. È l'esito più frequente e va detto senza esitazione: Kubernetes è l'esempio più caro di infrastruttura più complessa del prodotto che deve servire.
- **Il cluster c'è già** (o serve davvero): allora i manifest devono reggere un rilascio, un guasto e un rollback senza sorprese.

## Il verdetto sull'adozione

La domanda non è «Kubernetes è buono» — lo è. È: **quante persone lo manterranno alle tre di notte, e cosa risolve che oggi ti fa male?**

Serve davvero quando almeno una di queste è vera:

- più servizi con **cicli di rilascio indipendenti**, non un'app e un database;
- deve reggere la **caduta di un nodo** senza disservizio, e il disservizio costa;
- il carico è variabile in modo marcato e la scalatura automatica **paga il proprio costo**;
- c'è già un cluster in azienda, con qualcuno che lo amministra — l'adozione è gratis.

Non serve quando: un'app e un database · un team che non ha mai amministrato un cluster · «per imparare» su un progetto che deve stare in piedi · «per scalare» quando il traffico sta in una macchina da 8 GB.

Cosa si compra insieme al cluster, e va detto: aggiornamenti del control plane e dei nodi, ingress controller, certificati, gestione dei secret, storage persistente, e la classe di guasti nuovi che prima non esistevano. Su un provider gestito è meno lavoro, non zero.

## Se il cluster c'è

Cosa si guarda nei manifest, in ordine di quanto fa male sbagliarlo:

- **Probe.** `readiness` che dica davvero se il pod può servire traffico (una `liveness` scritta male riavvia in loop un servizio sano). Senza `readiness`, il rilascio manda traffico su pod non pronti.
- **Requests e limits.** Senza `requests` lo scheduler piazza a caso; senza `limits` un pod affama gli altri. Un `limit` di CPU troppo stretto si manifesta come lentezza inspiegabile.
- **Strategia di rollout e rollback.** `maxUnavailable`/`maxSurge` coerenti col numero di repliche, e `kubectl rollout undo` provato almeno una volta — non letto in documentazione.
- **Secret.** Un `Secret` Kubernetes è base64, non cifratura: chi legge l'oggetto legge il valore. Serve un controllo di accesso, o un gestore esterno. La valutazione del rischio di esposizione è di **Kai**.
- **Storage persistente.** La classe di storage, cosa succede al `PersistentVolume` se il pod viene cancellato, e se il `reclaimPolicy` è `Delete` (i dati spariscono con il claim).
- **Ingress**: TLS, host, e chi rinnova i certificati.
- **Immagini pinnate**, mai `:latest`: con `imagePullPolicy: Always` due repliche possono girare versioni diverse.

## Forma dell'output

Per il verdetto: due righe di risposta, il motivo, il segnale di cambio, e cosa fare invece. Non un confronto accademico fra orchestratori.

Per i manifest: i tre-cinque punti che contano su **questi** manifest, ciascuno con la riga e la conseguenza concreta.

## Trappole

- **`kubectl delete`** in qualunque forma: protocollo dei comandi distruttivi, sempre. `kubectl diff` prima di `apply` su un cluster vivo.
- **Elencare tutte le buone pratiche** su un cluster che ha tre deployment.
- **Confondere «regge un guasto» con «alta disponibilità»**: due repliche sullo stesso nodo non reggono la caduta di quel nodo.
- **Il tema sfonda nell'architettura del codice** (confini fra servizi, chi parla con chi): quello è **Otto**, e interviene solo se la scelta cambia i confini del codice. Nominalo in una riga e torna all'infrastruttura.
