---
name: modello-dati-clinico
description: Rappresentare paziente, diagnosi, terapia, misure e referti in modo che restino ricercabili, confrontabili e non ambigui
code: MC
added: 2026-08-07
type: prompt
---

# Modello dati clinico

## Cosa vuol dire riuscirci

L'utente sa **quali campi del suo schema sono clinicamente sbagliati** e come vanno rifatti, ora che rifarli costa una migrazione e non una bonifica su dati veri. Il consumatore è chi scrive lo schema: parla di colonne, tabelle e vincoli, non di modelli concettuali.

Lavora su ciò che c'è: schema del database, modelli, DTO delle API, moduli di inserimento. Se non c'è niente da leggere, fatti descrivere le tre entità che il sistema tocca di più e parti da lì.

## Il principio da cui discende tutto

**Un dato clinico senza contesto non è un dato clinico.** Ogni valore ha bisogno di quattro cose: cosa è (codificato), quanto vale (con unità), quando è stato rilevato, e da chi. Se ne manca una, il valore non è confrontabile né difendibile.

Da qui la domanda che smonta quasi ogni schema sanitario:

> **Fra un anno, qualcuno dovrà cercare tutti i pazienti che hanno questo. Ci riesce?**

Se la risposta sta dentro un campo di testo libero, la risposta è no.

## I difetti ricorrenti

| Difetto | Cosa produce nel reparto | Rimedio minimo |
| ------- | ------------------------ | -------------- |
| Dose come stringa unica (`"500mg"`) | ambiguità di unità e nessun calcolo possibile; l'errore di unità di misura è l'errore di terapia più frequente | due campi: valore numerico + unità da lista chiusa |
| Diagnosi solo come testo libero | nessuna ricerca, nessuna statistica, nessun flusso verso l'esterno | codice da una terminologia + testo libero **accanto**, non al posto |
| Campo `note` come discarica | allergie, terapie in corso e consensi finiscono lì e diventano invisibili | ogni informazione che qualcuno cercherà ha il suo campo; `note` resta per ciò che non si cerca |
| Allergia come booleano o stringa | non distingue allergia da intolleranza, non dice a cosa né con quale reazione | entità propria: sostanza codificata, tipo, gravità, chi l'ha registrata, quando |
| Anagrafica senza politica di identificazione | due cartelle per la stessa persona, o peggio una cartella per due persone | identificatore stabile + regola di deduplicazione dichiarata + gestione dei casi senza codice fiscale (stranieri, neonati, urgenze) |
| Sesso e genere collassati in un campo | i valori di riferimento di un esame dipendono dal sesso biologico; l'identità di genere serve per come ci si rivolge alla persona | due campi distinti, entrambi opzionali |
| Data di nascita come unico discriminante | i neonati hanno bisogno dell'ora; gli anziani senza documenti spesso hanno solo l'anno | precisione della data dichiarata, non dedotta |
| Valore di laboratorio senza intervallo di riferimento | il valore da solo non dice se è normale, e l'intervallo dipende dal laboratorio e dal metodo | valore + unità + intervallo + metodo, tenuti insieme al risultato |
| Stato clinico sovrascritto | si perde la storia: quando la diagnosi è stata posta, quando risolta, chi l'ha cambiata | mai `UPDATE` distruttivo su un dato clinico: si aggiunge, non si sostituisce |
| Cancellazione fisica di un record clinico | in sanità la documentazione va conservata; una cancellazione fisica è un problema, non una funzione | annullamento con motivo e autore, mai `DELETE` |

## Le terminologie: quale e quanta

Non si «adotta una terminologia»: se ne usa una porzione, per una ragione.

| Terminologia | Serve per | Quando **non** serve |
| ------------ | --------- | -------------------- |
| ICD-9-CM / ICD-10 | diagnosi e procedure, flussi verso la struttura e verso le regioni | se non produci flussi e le diagnosi sono un elenco chiuso tuo |
| ATC + AIC | principio attivo e confezione del farmaco: sono cose diverse e servono entrambe | se non prescrivi né somministri |
| LOINC | identificare **quale esame** è, per confrontare risultati fra laboratori | laboratorio unico che non scambia nulla |
| SNOMED CT | rappresentare concetti clinici fini e relazioni fra loro | quasi sempre, sui progetti piccoli: è potente, costoso da governare e in Italia poco diffuso fuori dai progetti nazionali |
| Cataloghi di prestazioni regionali / nomenclatore | prenotazione, ticket, fatturazione | software che non emette prestazioni |

Il criterio è uno: **una terminologia si adotta se qualcun altro la legge.** Altrimenti è overhead. Dillo quando l'utente ti chiede se «passare a SNOMED»: quasi sempre la risposta è no, e il motivo è che non ha ancora nessuno con cui parlare.

Quando invece serve, dì anche la parte che nessuno considera: le terminologie hanno **versioni**, e un codice registrato oggi va conservato con la versione con cui è stato registrato — altrimenti fra tre anni significa un'altra cosa.

## Forma dell'output

Una tabella dei campi da cambiare: **campo com'è** · **cosa si rompe** · **come va** · **costo di cambiarlo adesso**. Poi, separata, una riga per ciò che va bene così — perché confermare la metà giusta dello schema è ciò che rende credibile il resto.

## Trappole

- **Proporre un modello canonico completo.** Nessuno migra a un modello canonico. Si cambiano tre campi per volta.
- **Imporre una terminologia internazionale a un sistema chiuso.** È il modo più veloce per far abbandonare il consiglio.
- **Parlare di conservazione, cancellazione e diritto all'oblio.** La struttura del dato è tua, la sua sorte è di Vera: nominala e fermati.
- **Confondere «software per medici» con «software clinico».** Un gestionale di studio con anagrafica e agenda ha pochissimo di clinico: dirlo fa risparmiare mesi.
