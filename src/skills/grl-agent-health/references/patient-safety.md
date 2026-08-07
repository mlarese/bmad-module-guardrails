---
name: patient-safety
description: I punti del software in cui un errore arriva al paziente sbagliato o alla dose sbagliata, ordinati per probabilità reale
code: PS
added: 2026-08-07
type: prompt
---

# Sicurezza del paziente

## Cosa vuol dire riuscirci

L'utente sa i **tre-cinque punti** del suo software in cui un errore non resta un errore di dati ma arriva a una persona, e ha per ciascuno il rimedio più economico. Ordinati per probabilità reale, non per gravità teorica: il rischio raro e catastrofico si nomina dopo quello frequente e serio.

Questa capacità si esercita **a qualsiasi severità**, anche su un prototipo. I prototipi sanitari finiscono in reparto.

## Il principio da cui discende tutto

**Gli errori clinici gravi quasi mai nascono da un bug: nascono da un'interfaccia che ha reso più veloce la strada sbagliata.** Il default preselezionato, la lista ordinata male, il paziente che resta aperto in una scheda, la conferma che si clicca senza leggere.

La domanda giusta è:

> **Qual è qui la cosa sbagliata più facile da fare?**

## I punti caldi, in ordine di frequenza

**1. Identificazione del paziente.** È il primo per distacco.

- Due pazienti omonimi nella stessa lista, distinti solo da una data di nascita in fondo alla riga.
- Il contesto paziente che resta attivo dopo che l'operatore ha cambiato attività: si scrive in una cartella credendo di essere in un'altra. La sessione va **legata al paziente**, non solo all'utente.
- Due schede o due finestre aperte su due pazienti diversi.
- Ricerca che accetta un cognome parziale e mostra il primo risultato in evidenza.

Rimedi che reggono: nome, data di nascita e un secondo identificatore sempre visibili nell'intestazione, non solo nella lista di scelta · cambio paziente esplicito e visibile · avviso quando esistono omonimi · nessuna azione che scrive senza un paziente confermato nel passo immediatamente precedente.

**2. Farmaci e dosi.**

- Unità di misura assente o modificabile a testo libero (vedi la capacità *Modello dati clinico*).
- Nomi simili nella stessa lista a discesa (l'errore *look-alike / sound-alike*): due farmaci diversi che iniziano allo stesso modo, adiacenti nell'elenco.
- Zero terminale (`1,0 mg` letto come `10 mg`) e zero mancante (`,5 mg` letto come `5 mg`).
- Calcoli di dose per peso o per superficie corporea fatti dal software: se sbaglia, sbaglia in silenzio e sempre.
- Ordini duplicati: la stessa terapia inserita due volte da due persone diverse.

Rimedi: liste che mostrano principio attivo **e** dosaggio nella stessa riga · nessuna dose libera dove esiste un dosaggio standard · limiti massimi per età e peso con blocco, non solo avviso · doppia conferma **solo** sui pochi casi che la meritano.

**3. Risultati e referti.**

- Un valore critico prodotto ma mai visto da nessuno: il risultato esiste nel sistema, nessuno lo ha in carico. È il difetto più grave e il più invisibile in fase di progetto.
- Referto associato all'esame sbagliato o al paziente sbagliato.
- Referto modificato dopo l'emissione senza che chi l'ha già letto lo sappia.
- Immagini e referti disallineati (il testo dice una cosa, l'immagine è di un'altra serie).

Rimedi: ogni risultato fuori soglia critica ha un destinatario e una traccia di presa in carico · le versioni successive di un referto sono numerate e la precedente resta leggibile · nessuna emissione senza doppia associazione verificata.

**4. Allarmi.**

L'*alert fatigue* è un difetto di progetto, non degli utenti: un sistema che avvisa su tutto viene ignorato su tutto, incluso ciò che conta. Se il software genera più di pochi avvisi per sessione, il problema non è che gli utenti non li leggono.

Rimedi: pochi avvisi bloccanti, molti informativi · nessun avviso che non abbia un'azione associata · misurare quanti vengono chiusi senza leggere è il modo per accorgersene.

**5. Copia e incolla clinico.** Anamnesi ereditate da una visita all'altra, campi precompilati con l'ultimo valore inserito, template di referto pieni di frasi già pronte. Il testo passa da un paziente all'altro e diventa falso senza che nessuno lo scriva mai. Se il software offre precompilazione, deve mostrare **da dove viene** il testo e datarlo.

**6. Fallimenti silenziosi.** In sanità un errore che non arriva all'utente è peggio di un errore visibile: la prescrizione che non parte, il messaggio HL7 rifiutato dal sistema ricevente, il documento non arrivato al FSE. Ogni integrazione ha bisogno di una risposta visibile a chi ha fatto l'azione, non solo di una riga di log.

## Forma dell'output

Massimo cinque punti. Per ciascuno: **cosa può succedere qui** · **cosa lo rende facile nel tuo software** · **rimedio minimo**, con il costo. Se un punto si chiude togliendo una funzione invece di aggiungerne una, dillo per primo.

## Trappole

- **Elencare tutti e sei i punti su un software che ne tocca uno.** Se non ci sono farmaci, non si parla di dosi.
- **Chiamare in causa la sicurezza informatica.** Accessi, permessi e tracciamento sono di Kai: qui si parla di errori che nascono dall'uso corretto del sistema, non dall'abuso.
- **Trasformarlo in un'analisi di rischio formale.** ISO 14971 e la gestione del rischio del dispositivo medico sono materia di Nils. Qui si parla, non si compila.
- **Il moralismo.** Nessuna frase sul fatto che sono in gioco delle vite. È ovvio, e non aiuta a decidere.
