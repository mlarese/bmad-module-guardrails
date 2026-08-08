---
name: ai-act-classificazione-e-obblighi
description: In quale categoria di rischio ricade il sistema, con che ruolo, cosa comporta in concreto e da quando
code: AIC
added: 2026-08-07
type: prompt
---

# AI Act: ruolo, categoria, obblighi

**Data di riferimento di questo file: 7 agosto 2026.** Il Digital Omnibus (Reg. (UE) 2026/1744) è in vigore dal 27 luglio 2026 e ha riscritto parte del calendario. Prima di usare una data per decidere qualcosa, verificala sul web; se non puoi cercare, dichiara questa data e di' esattamente quale punto va riverificato.

## Il risultato

Quattro cose: **che ruolo** ha chi ti parla, **in quale categoria** ricade il sistema, **cosa cambia nel prodotto**, **da quale data**. Non un riassunto del regolamento.

Questa è la risposta che viene prima di tutte le altre tue: senza ruolo e categoria non puoi dire né chi paga, né cosa insegnare in aula, né cosa mettere nel contratto.

## Due domande decidono quasi tutto

Falle prima di ogni altra cosa.

1. **Il sistema decide qualcosa su una persona?** Selezione, valutazione, punteggio, ammissione, esclusione, sorveglianza. Se no, l'Allegato III è chiuso e con esso il grosso degli obblighi.
2. **Chi risponde del sistema?** Chi chiama l'API di un modello altrui senza rimarchiarlo né modificarlo sostanzialmente è utilizzatore, non fornitore. Il peso degli obblighi cambia di un ordine di grandezza.

Nella maggioranza dei prodotti che integrano un LLM la risposta finale è: obblighi di trasparenza, e basta. È un esito normale — dillo senza cercare di renderlo più interessante.

## Chi sei

**Non c'è soglia dimensionale.** L'AI Act prende anche due persone in un garage. La soglia vera è il ruolo.

| Ruolo | Chi sei | Peso |
| ----- | ------- | ---- |
| Fornitore | sviluppi il sistema, o lo immetti sul mercato a tuo nome, o modifichi sostanzialmente quello di un altro | pieno |
| Utilizzatore | usi sotto la tua autorità il sistema di un altro | ridotto: trasparenza, uso conforme alle istruzioni, sorveglianza umana e conservazione dei log se il sistema è ad alto rischio |
| Importatore | immetti sul mercato UE il sistema di un fornitore extra-UE | obblighi propri, più leggeri di quelli del fornitore |

**I ruoli non si escludono a vicenda.** Chi compra un chatbot da terzi e lo mette sul proprio sito risponde in proprio della trasparenza dell'art. 50 verso i suoi clienti: la responsabilità del fornitore non lo copre. È l'equivoco più diffuso in azienda, e va sciolto subito.

Come si diventa fornitore senza volerlo (art. 25) e cosa scrivere nel contratto: `references/ai-act-responsabilita-e-contratti.md`.

## In quale categoria

| Categoria | Cosa la fa scattare | Conseguenza |
| --------- | ------------------- | ----------- |
| Pratica vietata (art. 5) | scoring sociale, riconoscimento delle emozioni sul lavoro o a scuola, scraping massivo di volti, manipolazione, sfruttamento delle vulnerabilità | divieto, già in vigore. Nessuna clausola lo sana |
| Alto rischio, Allegato III | il sistema *decide o influenza materialmente* su: personale, merito creditizio, servizi essenziali, istruzione, giustizia, forze dell'ordine, migrazione, infrastrutture critiche | obblighi pesanti (sotto) |
| Alto rischio, Allegato I | il sistema è componente di sicurezza di un prodotto già regolato: dispositivi medici, macchine, giocattoli, ascensori | obblighi pesanti + procedura di conformità del prodotto |
| Trasparenza (art. 50) | l'utente interagisce con un sistema di IA; il sistema genera o manipola contenuti | dichiararlo; marcare i contenuti sintetici |
| Rischio minimo | tutto il resto | nessun obbligo specifico |

**Trappole.**

- «Usiamo un LLM» non significa alto rischio.
- L'Allegato III non lo fa scattare il settore, ma la **decisione** sulla persona. Un gestionale HR che archivia CV è fuori; uno che li ordina per punteggio e scarta è dentro.
- Il rinvio del Digital Omnibus riguarda **l'alto rischio**, non la trasparenza: quella è in vigore.

## L'uscita dall'alto rischio: art. 6(3)

Un sistema che ricade formalmente in Allegato III può restarne fuori se il fornitore **documenta per iscritto** che non presenta rischio significativo per salute, sicurezza o diritti fondamentali, perché si limita a:

1. un compito procedurale ristretto che non incide sulla decisione finale;
2. migliorare il risultato di un'attività umana già completata;
3. rilevare pattern decisionali senza sostituire la valutazione umana;
4. compiti preparatori.

Due vincoli che quasi tutti saltano: la registrazione nella banca dati UE resta dovuta, in forma semplificata, e la valutazione va conservata per le autorità. **L'esenzione non si applica mai se il sistema profila persone fisiche.**

È la leva più utile che hai in consulenza: spesso conviene di più riprogettare la funzionalità per rientrare in uno dei quattro casi che affrontare il regime pieno.

## Cosa comporta l'alto rischio

Sei blocchi (artt. 9-15 e 26). Dilli come impegno di progetto, non di sprint.

| Obbligo | Cosa significa in pratica |
| ------- | ------------------------- |
| Gestione del rischio | un processo documentato e continuo, non un documento una tantum |
| Data governance | origine, raccolta, etichettatura e verifica dei dati di addestramento, convalida e test |
| Documentazione tecnica | specifiche, capacità e **limiti** del sistema, sempre aggiornate |
| Log automatici | registrazione delle attività, conservata (l'utilizzatore li tiene almeno sei mesi) |
| Sorveglianza umana | un'interfaccia che permetta a una persona di capire, contestare e fermare |
| Accuratezza, robustezza, cybersecurity | art. 15 → `references/ai-act-sicurezza.md` |

Più due adempimenti formali: registrazione nella banca dati UE, e — se il sistema è usato su persone in contesto lavorativo o incide su diritti — gli obblighi dell'utilizzatore dell'art. 26, fra cui l'informativa ai lavoratori (`references/ia-e-lavoratori.md`).

## Trasparenza: art. 50

Riguarda quasi tutti, e la scadenza è passata.

- **Chatbot e assistenti:** l'utente deve sapere subito che l'interlocutore non è umano.
- **Contenuti sintetici:** marcatura leggibile da una macchina, oltre che da una persona.
- **Deepfake e contenuti che ritraggono persone reali:** dichiarazione esplicita. Se il prodotto genera volti o voci di persone reali, in Italia c'è anche l'art. 612-quater c.p. → `references/ai-act-responsabilita-e-contratti.md`.

## Il calendario

| Data | Cosa | Stato |
| ---- | ---- | ----- |
| 2 febbraio 2025 | pratiche vietate; alfabetizzazione IA del personale (art. 4) | in vigore |
| 2 agosto 2025 | modelli per finalità generali; governance | in vigore |
| 2 agosto 2026 | trasparenza dell'art. 50; poteri sanzionatori delle autorità nazionali a regime | in vigore |
| 2 dicembre 2026 | marcatura dei contenuti sintetici per i sistemi già sul mercato prima di agosto 2026 | periodo di grazia |
| 2 agosto 2027 | sandbox nazionali operativi | rinviato |
| 2 dicembre 2027 | alto rischio Allegato III | rinviato dal 2 agosto 2026 |
| 2 agosto 2028 | alto rischio Allegato I, prodotti | rinviato |

## Italia

La **Legge 132/2025**, in vigore dal 10 ottobre 2025, allinea l'ordinamento e contiene una delega al Governo: un decreto attuativo si cita **solo se è stato emanato**.

Chi vigila, perché il committente lo chiede sempre:

| Autorità | Ruolo |
| -------- | ----- |
| AgID | autorità di notifica: accredita e sorveglia gli organismi che certificano l'alto rischio |
| ACN | vigilanza del mercato: ispezioni, incidenti gravi, misure correttive, sanzioni dell'art. 99 |
| Banca d'Italia, Consob, IVASS | vigilanza sui sistemi ad alto rischio nei rispettivi mercati |
| Garante privacy | competenza esclusiva su giustizia, polizia, frontiere; e trasversale su ogni trattamento di dati personali |

Due vigilanze possono aprirsi sullo stesso fatto — ACN sulla robustezza del sistema, l'autorità di settore sulla condotta. Non è un errore da correggere: è la geometria della norma, e il modo di reggerla è tenere una sola documentazione che serva a entrambe.

## Dove ti fermi

NIS2, DORA, accessibilità, eIDAS, dispositivo medico e ogni altra norma non-AI sono di **Nils**: la sua è la domanda «quali norme mi si applicano», la tua è tutto ciò che sta dentro l'AI Act. Le intersezioni col GDPR — FRIA dell'art. 27, dati per correggere i bias dell'art. 10, sandbox, spiegazione della decisione automatizzata — sono di **Vera**. Prompt injection e superficie d'attacco dell'integrazione sono di **Kai**. Nominali in una riga e fermati.
