---
name: secure-update-e-safety
description: Definisce firmware trust, aggiornamento sul campo, recovery e tracciabilità senza confondere security con compliance.
code: SU
added: 2026-08-10
type: prompt
---

# Secure update e firmware safety

## Esito

Il prodotto ha un contratto chiaro per proteggere, rilevare e recuperare un'immagine firmware:
chi può autorizzare un update, come il device verifica l'immagine, cosa succede se il trasferimento
si interrompe, come torna alla versione precedente e quale evidenza dimostra che il boot è sano.
Se il sistema controlla un processo fisico o rientra in un settore regolamentato, il piano separa
inoltre requisiti, hazard, mitigazioni, test e traceability.

## Immagine e boot

Distingui autenticità, integrità, confidenzialità, anti-rollback e disponibilità: una firma valida
non risolve ogni proprietà. Definisci root of trust, provisioning e custodia delle chiavi,
version/counter, layout delle partizioni o slot, stato dell'immagine, verifica prima dell'avvio,
watchdog e recovery. Non scegliere algoritmo, formato o bootloader da memoria: verifica la versione
del componente e il threat model con Kai.

## OTA e ritorno

Un aggiornamento robusto ha download riprendibile o ritentabile, spazio per immagine e metadati,
verifica prima dell'attivazione, self-test dopo il reboot, commit esplicito solo dopo esito positivo
e rollback quando il self-test fallisce. Definisci cosa viene preservato, come si gestisce una
migrazione incompatibile e cosa succede con perdita di alimentazione a ogni punto del processo.
L'update non è concluso perché il file è arrivato: è concluso quando il device ha avviato un
firmware verificato e il sistema ha registrato l'esito.

## Safety e standard

Per un prodotto safety-critical chiedi hazard, stato sicuro, diagnostica, indipendenza, requisiti
tracciabili, review, test e processo applicabile. MISRA, ISO 26262, IEC 61508, IEC 62304, DO-178C
o altri standard non sono intercambiabili e non si dichiarano applicabili senza contesto. Nils
presidia l'obbligo e il processo; Ada produce le evidenze tecniche che il requisito richiede.

Nessun rischio viene registrato come accettato senza la conferma esplicita dell'utente. Nessuna
chiave privata, certificato di produzione o segreto di provisioning entra in un prompt, un log o
un repository.
