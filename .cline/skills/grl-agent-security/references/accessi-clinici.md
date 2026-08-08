---
name: accessi-clinici
description: Il controllo degli accessi in un sistema sanitario — accesso legittimo abusivo, audit trail consultabile, break-the-glass, superfici tipiche del sanitario
code: AC
added: 2026-08-07
type: prompt
---

# Accessi clinici

## Cosa vuol dire riuscirci

L'utente sa **chi può aprire la cartella di un paziente nel suo sistema, e se domani può dimostrare chi l'ha aperta e perché**. Non un modello di ruoli teorico: i due o tre punti in cui oggi non saprebbe rispondere.

Il consumatore è chi costruisce o gestisce un sistema che contiene dati clinici.

## Il principio

In sanità il rischio principale **non è l'intruso esterno**: è l'**accesso legittimo abusivo** — personale autorizzato che apre la cartella di qualcuno che non sta curando. Il collega, il vicino di casa, il personaggio pubblico ricoverato, l'ex partner.

La difesa non è impedirlo. Bloccare troppo mette a rischio le cure, ed è la ragione per cui i controlli rigidi vengono aggirati entro una settimana. La difesa è renderlo **visibile e attribuibile**.

La domanda da fare per prima:

> **Se domani qualcuno chiede chi ha aperto questa cartella e perché, sai rispondere?**

Se la risposta è no, tutto il resto viene dopo.

## Audit trail

Cosa registrare, per ogni accesso: **chi** (persona fisica, non ruolo generico) · **cosa** ha visto o modificato · **quando** · **quale paziente** · **da dove** (postazione, IP) · **in che veste** (reparto, presa in carico, motivo).

Tre requisiti, e il terzo è quello che quasi tutti saltano:

1. **Immodificabile dall'applicazione stessa.** Se il codice che scrive la cartella può anche riscrivere il log, il log non prova niente. Append-only, o su un sistema separato con credenziali diverse.
2. **Conservato a lungo.** I tempi sono un vincolo settoriale: chiedili a **Nils**. Che sia molto più della retention applicativa ordinaria è certo.
3. **Effettivamente consultabile.** Un log che nessuno può interrogare non serve a niente. Serve poter rispondere in minuti a «tutti gli accessi al paziente X negli ultimi due anni» e a «tutti i pazienti aperti dall'operatore Y ieri». Se questo oggi richiede un ticket a un fornitore e tre giorni, l'audit trail non esiste come strumento.

**Registrare anche le letture, non solo le scritture.** È il punto specifico del sanitario: in un gestionale ordinario conta chi ha modificato, qui conta **chi ha guardato**. Un audit trail che traccia solo le scritture non intercetta l'abuso tipico di questo dominio.

## Break-the-glass

L'accesso in emergenza a dati normalmente non accessibili al singolo operatore. **Serve, non va tolto**: senza, il pronto soccorso non funziona.

Va progettato: motivazione obbligatoria inserita al momento (testo libero, non menu a tendina) · registrazione distinta dagli accessi ordinari · notifica a chi di dovere · **revisione a posteriori** da parte di qualcuno che la fa davvero.

Un sistema senza break-the-glass non è più sicuro: produce **account condivisi** e credenziali prestate, cioè tracciamento zero.

## Il modello di autorizzazione

**Il ruolo non basta.** «Medico» dà accesso a tutte le cartelle dell'ospedale, ed è esattamente il problema.

Serve la **relazione di cura**: questo operatore, questo paziente, in questo momento, per questo motivo. Gli ancoraggi disponibili sono reparto, presa in carico, episodio di ricovero, prenotazione, turno.

La regola pratica: accesso ordinario limitato dalla relazione di cura, tutto il resto tramite break-the-glass tracciato. **Chi clinicamente deve poter vedere cosa** è di **Livia** (`grl-agent-health`); come si realizza il vincolo è di Kai.

## Account condivisi e postazioni comuni

È la causa numero uno di tracciamento inutile. Il PC del reparto con la sessione sempre aperta a nome di chi ha timbrato per primo la mattina rende ogni riga di audit trail priva di valore.

- Separare **autenticazione della postazione** e **identificazione dell'operatore**: la macchina è in sessione, l'operatore si identifica sopra.
- Sessioni corte con **riautenticazione veloce** — badge, PIN, prossimità — non logout completo.
- Il logout completo con reinserimento di username e password è ciò che produce l'account sempre aperto: un timeout aggressivo **senza** riautenticazione veloce peggiora la situazione invece di migliorarla.

## Identità

- **Cittadino**: SPID, CIE, CNS per il portale del paziente e i servizi al pubblico.
- **Operatore**: credenziali della struttura, non identità pubbliche.
- **Personale esterno e fornitori** con accesso da remoto: sono spesso il canale meno controllato e il più permissivo. Account nominali, non condivisi; accesso a tempo, non permanente.
- **Dismissione**: il turnover in sanità è alto (specializzandi, interinali, consulenti). Un processo di disattivazione che dipende da qualcuno che si ricordi di aprire un ticket lascia account vivi per anni. Va agganciato al sistema del personale.

## Le superfici tipiche del sanitario

In ordine di frequenza reale:

- **Pannelli di amministrazione** che mostrano l'anagrafica completa, spesso raggiungibili con un ruolo tecnico e senza vincolo di relazione di cura.
- **Integrazioni HL7** su rete interna: in chiaro, senza autenticazione, con l'assunto che la rete sia fidata.
- **PACS e visualizzatori DICOM esposti.** I visualizzatori raggiungibili da internet senza autenticazione sono un caso ricorrente, non un'ipotesi: se il progetto ne ha uno, è il primo posto da guardare.
- **Portali di refertazione con identificativi di documento indovinabili.** Numero progressivo nell'URL, ritiro del referto con codice fiscale più data: è IDOR con dati clinici dentro.
- **Export e report** generati per un'esigenza una tantum e mai più controllati: CSV su una condivisione di rete, report schedulati via email.
- **Dispositivi medici collegati in rete** che non si possono aggiornare perché l'aggiornamento invalida la certificazione. Non si patcha: si segrega la rete. Il come è di **Bruno**.

## Ransomware

In sanità l'indisponibilità è un **danno clinico immediato**, non un disservizio. Da qui una sola conseguenza pratica, ed è la domanda da fare:

> **Cosa si fa mentre il sistema è fermo?**

La risposta è organizzativa prima che tecnica: quale copia cartacea, quale procedura di degrado, chi decide di attivarla. Backup, ripristino e tempi di recupero si configurano con **Bruno** (`grl-agent-ops`).

## Trappole

- **Confondere tracciamento e blocco.** La risposta all'accesso abusivo è renderlo visibile, non stringere i permessi finché il reparto non lavora più.
- **Loggare il contenuto clinico dentro i log applicativi.** Payload HL7 o FHIR interi, corpo delle risposte, query con parametri. È un problema di **Vera**: nominalo e fermati.
- **Pensare che la rete interna sia fidata.** In ospedale ci sono prese di rete nei corridoi, dispositivi di fornitori, personale esterno e Wi-Fi condivisi.
- **Un audit trail scritto e mai interrogato.** Esiste per l'adempimento, non risponde a nessuna domanda: dillo esplicitamente quando lo vedi.

## Confini

| Questione | Chi parla |
| --------- | --------- |
| Obblighi normativi settoriali, NIS2 sanità, tempi di conservazione dell'audit trail | **Nils** (`grl-agent-compliance`) |
| Base giuridica, oscuramento, retention dei dati sanitari, contenuto clinico nei log | **Vera** (`grl-agent-privacy`) |
| Chi *clinicamente* deve poter vedere cosa, deleghe, relazione di cura | **Livia** (`grl-agent-health`) |
| Configurazione di server, rete, segregazione, backup e ripristino | **Bruno** (`grl-agent-ops`) |
