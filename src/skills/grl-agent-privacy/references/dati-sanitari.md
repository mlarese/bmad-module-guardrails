---
name: dati-sanitari
description: Il GDPR applicato ai dati sulla salute — base giuridica dell'art. 9, oscuramento, retention imposta, uso secondario — per chi costruisce software sanitario
code: DS
added: 2026-08-07
type: prompt
---

# Dati sanitari

L'esito è, per il software che si sta costruendo: quali dati sono dati sulla salute (anche quando non sembrano), su quale base giuridica si reggono, e quali due o tre cose vanno progettate adesso perché dopo non si possono aggiungere.

Il consumatore è chi scrive un gestionale di reparto, un portale del paziente, un'app di prenotazione, un'integrazione con il FSE. Vuole sapere cosa cambia nel codice, non cosa dice l'articolo.

## Il principio

I dati sulla salute sono **categoria particolare** (art. 9). Il trattamento è **vietato salvo eccezione**: una base dell'art. 6 non basta, ne serve **anche** una dell'art. 9.

La domanda che smonta il problema:

> **Chi tratta, in quale veste, e per quale finalità di cura?**

Senza queste tre risposte non si sceglie la base, e ogni discorso sul consenso è prematuro.

## Il consenso non è la base normale

Per la cura vale l'**art. 9.2.h**: finalità di cura, da parte di un professionista soggetto a segreto professionale. Non serve consenso privacy.

Il **consenso al trattamento sanitario** (l'atto medico) e il **consenso privacy** sono due cose diverse. Confonderli è l'errore più diffuso nel software sanitario: produce spunte che non servono, e che se revocate non si possono onorare senza interrompere la cura.

Il consenso serve invece per ciò che sta **fuori** dalla cura:

| Caso | Serve consenso |
| ---- | -------------- |
| Cartella clinica, refertazione, prescrizione | no — art. 9.2.h |
| FSE per finalità diverse dalla cura | sì |
| Ricerca, in molte configurazioni | sì, o base alternativa da verificare |
| Comunicazioni promozionali, newsletter, sondaggi | sì |
| App di benessere fuori da un contesto di cura | sì — non c'è nessun 9.2.h da invocare |

## Titolare e responsabile

La struttura sanitaria è **titolare**. La software house che gestisce o ospita il sistema è quasi sempre **responsabile**.

Cambia in concreto: chi risponde delle scelte di trattamento, chi scrive e consegna l'informativa al paziente, chi riceve e istruisce le richieste degli interessati (accesso, rettifica, oscuramento), chi decide su una richiesta di cancellazione.

Il contratto e il DPA sono di **Aldo** (`grl-agent-legal`). Qui si fa emergere la configurazione dei ruoli: se il team non sa dire chi è titolare, tutto il resto è indefinito.

## Cosa è dato sulla salute anche se non sembra

Il dato **deducibile** è dato sulla salute:

- un appuntamento in un reparto specialistico (oncologia, psichiatria, malattie infettive)
- una prescrizione, un codice di esenzione
- il fatto stesso di essere paziente di una certa struttura
- un file DICOM: i dati identificativi stanno nei metadati, non solo nell'immagine
- l'oggetto di un'email, il nome di un file allegato, il testo di un SMS di promemoria
- un campo `note` a testo libero in qualunque punto del sistema

Conseguenza pratica: notifiche, promemoria e nomi di file vanno progettati per non rivelare il contenuto clinico.

**Dati genetici e biometrici** hanno un regime proprio. I dati genetici riguardano anche i **familiari** dell'interessato, che non hanno mai avuto contatti con il sistema: se il progetto ne tratta, va detto subito perché cambia il perimetro degli interessati.

## Oscuramento

In sanità l'interessato può chiedere che un dato non sia **visibile** a certi soggetti — tipicamente sul FSE — senza che venga cancellato.

**Va progettato prima.** Tocca il modello di autorizzazione e ogni flusso in uscita: viste, export, referti, integrazioni, ricerca full-text, report. Un'architettura che non lo prevede non lo aggiunge dopo con una patch.

Il punto che quasi tutti saltano: **anche l'oscuramento va oscurato**. Non deve essere deducibile che qualcosa è stato oscurato — un buco nella cronologia, un contatore che non torna, un ID mancante nella sequenza rivelano l'esistenza del dato nascosto. Questo è il **requisito**, ed è di Vera; **come** lo si realizza nel modello di accesso è di Kai.

## Retention: in sanità il ragionamento si ribalta

Fuori dalla sanità si parte dal cancellare il prima possibile. In sanità la conservazione della documentazione è spesso **imposta**, non facoltativa, e i tempi della cartella clinica sono lunghissimi.

Conseguenza: una richiesta di cancellazione su documentazione sanitaria di norma **non si può onorare**, e il prodotto deve saperlo dire all'utente invece di promettere un pulsante che non funziona.

Il vincolo settoriale preciso — quale documento, quanti anni, con quale fonte — è di **Nils** (`grl-agent-compliance`). Qui si dice che esiste e che va chiesto prima di scrivere qualunque job di cancellazione.

Su ciò che **non** è documentazione sanitaria obbligatoria (log, analytics, dati di contatto per il marketing, code di messaggi) vale la capacità `MR` (`references/minimizzazione-retention.md`) senza sconti.

## Minori e capacità

Chi accede per conto di chi — genitori, tutori, amministratori di sostegno, caregiver delegati — e con quale titolo: questa è la regola di Vera. Con essa il **cambio di regime con l'età**: al compimento della maggiore età l'accesso dei genitori decade, e ci sono casi intermedi in cui il minore ha diritto a riservatezza verso i genitori.

Come il portale si comporta di conseguenza — cosa mostra, cosa nasconde, come gestisce il passaggio — è di **Livia** (`grl-agent-health`), insieme al meccanismo delle deleghe e alle sue regole cliniche.

## DPIA

In ambito sanitario la soglia si supera quasi sempre: categorie particolari su larga scala, spesso con soggetti vulnerabili. Non rifare il ragionamento qui — carica la capacità `DP` (`references/pre-dpia.md`) e lavora lì.

## Uso secondario e ricerca

Dati raccolti per la cura e riusati per ricerca, statistica, controllo di gestione o addestramento di un modello sono un **trattamento diverso**, con finalità propria e base propria. Non si eredita la base della cura.

**La pseudonimizzazione non è anonimizzazione.** Un dataset clinico pseudonimizzato resta dato personale: la reidentificazione con poche variabili (data di nascita, comune, data di ricovero, diagnosi rara) è realistica. Se il team dice «li abbiamo anonimizzati», chiedi con quale procedura e chi tiene la chiave.

**EHDS** (European Health Data Space, il regolamento europeo su uso primario e secondario dei dati sanitari): esiste e riguarda direttamente questo tema. **Verifica lo stato di applicazione prima di citarlo** — la materia si muove, e le date di decorrenza sono scaglionate.

## Trappole

- **Chiedere consenso dove non serve.** Poi il paziente lo revoca e non lo si può onorare senza interrompere la cura. Il consenso di troppo è un debito, non una cautela.
- **Trattare un'app di benessere come se fosse sanitaria, o il contrario.** Il passo tracker senza contesto di cura non ha un 9.2.h da invocare; il diario dei sintomi collegato a un reparto sì.
- **Ambienti di test con dati reali di pazienti.** In sanità è la fuga più frequente e la più semplice da chiudere. Vedi la capacità `FP` (`references/dati-fuori-posto.md`).
- **Log applicativi che registrano il contenuto clinico**: payload HL7 o FHIR completi, corpo delle risposte API, query con parametri, stack trace con l'oggetto in memoria. Stessa capacità `FP`.
- **Notifiche e promemoria che dicono il reparto.** L'SMS «appuntamento in oncologia domani alle 9» è una comunicazione di dato sanitario a chiunque guardi lo schermo bloccato.

## Confini

| Questione | A chi appartiene |
| --------- | ---------------- |
| Qualificazione come dispositivo medico, MDR, conservazione imposta dal settore | **Nils** (`grl-agent-compliance`) e il workflow `grl-mdsw` |
| Struttura del dato clinico, codifiche, interoperabilità, meccanismo delle deleghe | **Livia** (`grl-agent-health`) |
| Audit trail, break-the-glass, come si realizza l'oscuramento nel modello di accesso | **Kai** (`grl-agent-security`) |
| Contratto, DPA, nomina a responsabile | **Aldo** (`grl-agent-legal`) |
