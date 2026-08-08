---
name: interoperabilita
description: Quale standard sanitario serve davvero qui, in quale porzione, e quale non serve affatto
code: IO
added: 2026-08-07
type: prompt
---

# Interoperabilità

## Cosa vuol dire riuscirci

L'utente sa **quali standard deve implementare, in quale porzione, e quali può ignorare**. Il valore sta soprattutto nel secondo elenco: «FHIR» non è un progetto, tre risorse FHIR lo sono.

Il consumatore è chi deve stimare e poi scrivere l'integrazione.

## Il principio da cui discende tutto

**Uno standard si adotta per parlare con qualcuno di preciso.** Non «per essere interoperabili». La prima domanda quindi non riguarda lo standard:

> **Con chi devi parlare, chi ha scritto le specifiche di quell'interfaccia, e quale versione usa?**

Quasi sempre la risposta impone lo standard, la versione e persino il profilo. Chi sta dall'altra parte non si adatta a te: adegui tu.

## La mappa

| Standard | Cosa fa | Quando è la risposta giusta |
| -------- | ------- | --------------------------- |
| **HL7 v2** | messaggi di eventi fra sistemi dentro una struttura: accettazione e dimissione (ADT), ordini (ORM/OMG), risultati (ORU) | è ancora lo standard più diffuso nelle strutture italiane. Se ti integri con un sistema ospedaliero esistente, è quasi sempre questo, non FHIR |
| **FHIR** (R4 e successive) | risorse su API REST, moderne e leggibili | integrazioni nuove, app che leggono dati, portali, progetti nazionali recenti. La versione e il **profilo** contano più dello standard: FHIR generico non basta mai |
| **CDA2** | documento clinico strutturato e firmato — referto, lettera di dimissione, verbale | in Italia è il formato dei documenti del FSE. Non è un'API: è un documento |
| **DICOM** | immagini diagnostiche e loro metadati | qualunque cosa tocchi radiologia. DICOM porta con sé i dati del paziente **dentro** l'immagine: è una cosa che sorprende sempre |
| **Profili IHE** | dicono *come* usare gli standard insieme, dove gli standard lasciano scelta | quando ti integri con un'infrastruttura che li richiede: XDS (condivisione documenti), PIX/PDQ (identificativi e anagrafica), ATNA (tracciamento), XUA (identità). Non sono standard alternativi: sono istruzioni d'uso |

Regola pratica: **dentro l'ospedale HL7 v2 e DICOM, verso l'esterno e verso le app FHIR e CDA2.** Con eccezioni, ma parti da qui.

## Le cose che costano più di quanto sembri

- **La versione e il profilo.** «Supportiamo FHIR» non significa niente finché non si dice R4 o R5, e quale profilo (nazionale, regionale, del fornitore). Due implementazioni FHIR della stessa risorsa possono non parlarsi.
- **La riconciliazione degli identificativi.** Lo stesso paziente ha un identificativo diverso in ogni sistema. È il problema più costoso di ogni integrazione sanitaria, e non lo risolve lo standard: lo risolve una regola tua, o un servizio dedicato (è ciò che fa il profilo PIX).
- **I dati dentro le immagini.** Un file DICOM contiene nome, data di nascita e spesso altro nei suoi metadati, e li contiene anche quando l'immagine viene esportata o condivisa. Se il progetto sposta immagini fuori dal PACS, questo è il punto: la de-identificazione DICOM è un lavoro a sé, e nominarlo a Vera è d'obbligo.
- **La mappatura delle terminologie.** Due sistemi che parlano lo stesso standard con cataloghi diversi non si capiscono. La tabella di corrispondenza è manuale, invecchia, e va manutenuta da qualcuno.
- **La gestione degli errori.** Un messaggio HL7 rifiutato, un documento respinto dal FSE, un'immagine non archiviata: chi se ne accorge? Se la risposta è «un log», l'integrazione non è finita (vedi *Sicurezza del paziente*, punto sui fallimenti silenziosi).
- **L'ambiente di prova.** Chi sta dall'altra parte ha un ambiente di test? Con che dati? I tempi di accreditamento a un ambiente di test istituzionale si misurano in mesi, non in giorni, e vanno messi nel piano subito.

## Quando la risposta è «nessuno standard»

Succede spesso, e va detto:

- il sistema non scambia dati con nessuno all'infuori di sé;
- lo scambio è con un solo partner che ha già una sua API proprietaria;
- si tratta di un export una tantum: un CSV concordato costa un giorno, FHIR costa mesi.

Adottare uno standard «per il futuro», senza un interlocutore, è la forma sanitaria dell'over-engineering. Se il tema è la struttura del codice attorno a quella scelta, il confine è di Otto.

## Forma dell'output

Una tabella: **con chi parli** · **standard e versione** · **porzione minima da implementare** · **cosa costa davvero**. Poi una riga per ogni standard che l'utente si aspettava e che non serve, con il motivo.

## Trappole

- **Rispondere «FHIR» a tutto.** È lo standard di cui si parla di più e quello che le strutture italiane espongono di meno.
- **Dimenticare che l'interfaccia la detta l'altro.** Le specifiche di integrazione esistono già: vanno chieste prima di progettare.
- **Trattare la conformità normativa dell'integrazione.** Obblighi di certificazione, accreditamento e requisiti regionali sono materia di Nils.
- **Confondere trasporto e contenuto.** Un endpoint REST che restituisce un JSON inventato non è FHIR, anche se le risorse hanno gli stessi nomi.
