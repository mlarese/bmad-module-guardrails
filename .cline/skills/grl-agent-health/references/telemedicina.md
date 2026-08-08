---
name: telemedicina
description: Cosa distingue una televisita da una videochiamata, e cosa deve restare tracciato perché la prestazione a distanza esista come atto sanitario
code: TM
added: 2026-08-07
type: prompt
---

# Telemedicina

## Cosa vuol dire riuscirci

L'utente sa **quale prestazione di telemedicina sta costruendo davvero** — non «una videochiamata col medico» — e sa le tre-cinque cose che devono restare tracciate perché quella prestazione valga come atto sanitario e sia rendicontabile.

Il consumatore è chi deve decidere il modello dati della sessione e cosa il software deve registrare mentre la sessione è in corso.

## Il principio da cui discende tutto

**La telemedicina non è un canale: è un elenco chiuso di prestazioni, ciascuna con attori propri e tracciamento proprio.** Il software che le tratta tutte come «una stanza video con due partecipanti» produce sessioni che nessuno può refertare, fatturare o difendere.

La prima domanda quindi non è tecnica:

> **Quale prestazione stai erogando, chi sono le due parti, e cosa resta scritto dopo?**

## Le prestazioni, e perché non sono intercambiabili

| Prestazione | Chi sta ai due capi | Cosa la distingue nel software |
| ----------- | ------------------- | ------------------------------ |
| **Televisita** | medico ↔ paziente | è una visita a tutti gli effetti: produce referto, va in cartella, può produrre prescrizioni. Il paziente va identificato con certezza |
| **Teleconsulto** | medico ↔ medico | il paziente **non è presente**. Serve tracciare chi ha chiesto, chi ha risposto, su quale paziente, e che il parere è entrato nella documentazione del richiedente |
| **Teleconsulenza** | professionista sanitario ↔ professionista sanitario, spesso durante l'attività | è supporto operativo, non un parere formale come il teleconsulto: attori diversi (anche non medici) e tracciamento più leggero |
| **Telemonitoraggio** | dispositivi del paziente → chi li guarda | non è una sessione: è un flusso continuo. Vedi la sezione dedicata |
| **Teleassistenza** | professionista sanitario o socio-sanitario ↔ paziente o caregiver | assistenza e supporto, non atto diagnostico. Se la si tratta come televisita si generano referti che non hanno contenuto |
| **Telerefertazione** | specialista → struttura richiedente | il medico referta a distanza dati o immagini acquisiti altrove. Il punto critico è l'associazione fra referto ed esame, non la connessione |

**Trattarle come una sola prestazione è il difetto di progetto più comune del settore.** Chiedi sempre quale delle sei, e accetta «più di una» solo se il software le distingue davvero nel modello dati.

## Cosa deve restare tracciato

Perché la prestazione esista come atto sanitario, e non come una chiamata avvenuta:

- **Identificazione certa di entrambe le parti.** Chi era il medico e chi era il paziente, verificato — non «chi aveva il link». Il metodo di identificazione va registrato, non solo l'esito.
- **Consenso alla modalità a distanza.** È distinto dal consenso al trattamento sanitario e dal consenso privacy: riguarda l'accettazione di ricevere quella prestazione da remoto. Va acquisito una volta e datato, e va riacquisito se la prestazione cambia natura.
- **Refertazione.** La televisita produce un referto come la visita in presenza. Se il software non ha un posto dove metterlo, la prestazione non è completa.
- **Inserimento in cartella o nel fascicolo del paziente.** Una sessione che vive solo nei log della piattaforma video non è documentazione sanitaria.
- **Prescrizioni emesse durante la sessione.** Ricette, richieste di esami, piani terapeutici: devono agganciarsi alla sessione che li ha generati. È la cosa che si dimentica più spesso.
- **Data, ora e durata effettiva**, perché è ciò su cui si rendiconta.

## I requisiti tecnici che nessuno mette nel piano

- **Qualità minima della connessione, dichiarata.** Va scritta una soglia (banda, latenza) sotto la quale la prestazione non si eroga, e il software deve misurarla e dirlo **prima** che la sessione inizi, non dopo.
- **Cosa succede se la sessione cade a metà.** È la domanda che non viene mai posta in fase di progetto e arriva sempre in produzione. Le risposte possibili sono due — si riprende la stessa sessione entro una finestra dichiarata, oppure si rifà e la prima si chiude come non erogata — e vanno decise adesso, perché cambiano il modello dati e la rendicontazione.
- **Registrazione audio-video: sì o no.** Di norma **no**. Registrare una prestazione sanitaria crea un archivio di dati sanitari con obblighi propri di conservazione e accesso; il valore clinico è quasi sempre inferiore al costo. La scelta va messa per iscritto in un modo o nell'altro, e se è «sì» il tema passa a Vera. Non registrare **non** significa non tracciare: i metadati della sessione restano.
- **Il piano B non tecnologico.** Cosa fa il medico se il video non parte: telefono, riprogrammazione, invio in presenza. È un requisito del software, perché va registrato l'esito.

## Il telemonitoraggio è un altro problema

Non è una sessione fra due persone: sono dati che arrivano da dispositivi in continuo, quando nessuno sta guardando. La domanda decisiva è una sola:

> **Chi guarda quei dati, in quale finestra temporale, e cosa succede se non li guarda?**

- Un allarme generato che nessuno prende in carico è il difetto peggiore del telemonitoraggio, e assomiglia al valore critico mai visto della capacità *Sicurezza del paziente*: il dato esiste nel sistema, la responsabilità no.
- Va dichiarata la **finestra di presa in carico** — minuti, ore, giorni lavorativi — e va scritta anche al paziente: un servizio che sembra sorveglianza continua e non lo è produce affidamento indebito.
- Serve una traccia di presa in carico con nome e ora, un percorso di escalation quando la prima persona non risponde, e la gestione del **dispositivo che smette di trasmettere**: il silenzio va trattato come un allarme, non come assenza di allarmi.
- Le soglie che generano allarme vanno tarate sul singolo paziente, altrimenti si torna all'*alert fatigue*.

## Il confine con il dispositivo medico

| Componente | Di norma |
| ---------- | -------- |
| Piattaforma di videochiamata, agenda, stanza virtuale, chat | **non** è dispositivo medico: trasporta e mostra, non elabora |
| Archiviazione e trasmissione dei dati del monitoraggio senza elaborazione | resta fuori |
| Software che **elabora, interpreta, correla o genera allarmi** sui dati del telemonitoraggio | quasi sempre **sì**, ed è quasi sempre almeno classe IIa |

Quando il software calcola un indice, confronta con una soglia clinica o decide cosa mostrare come allarme, non è più un canale. **Passa a Nils** (`grl-agent-compliance`) o al workflow `grl-mdsw`, che è il percorso guidato di qualificazione. Non tentare la classificazione qui: qui si riconosce il segnale e si passa la mano in una riga.

## L'aggancio italiano

**Materia che si muove.** Se non puoi verificare sul web, dichiara che vai a memoria e a quale data risale il riferimento.

- **Linee guida nazionali sulla telemedicina** e **requisiti minimi delle prestazioni** (decreti ministeriali 2022, nell'ambito del PNRR): definiscono l'elenco delle prestazioni e cosa serve per erogarle. È da lì che viene la distinzione delle sei prestazioni.
- **Accreditamento regionale.** Erogare telemedicina in regime pubblico o convenzionato richiede il titolo della struttura: le regole operative sono regionali e divergono. Chiedi in quale regione si eroga, prima di dare per buono qualunque requisito.
- **Rendicontabilità.** La prestazione a distanza si registra e si tariffa come le altre: se il software non produce ciò che serve al flusso di rendicontazione, la struttura non potrà erogarla anche se funziona.

## Forma dell'output

Prima riga: **quale prestazione è**, fra le sei. Poi una tabella con **cosa deve restare tracciato** · **dove lo scrivi oggi** · **cosa manca**. Poi le due decisioni da prendere adesso: sessione caduta, registrazione sì/no. Se c'è telemonitoraggio, una riga sola e in evidenza: chi guarda e in quanto tempo.

## Trappole

- **Chiamare televisita una videochiamata.** Se non c'è identificazione, referto e tracciamento, è una chiamata: dirlo subito evita di costruire l'intero prodotto sul nome sbagliato.
- **Dimenticare la prescrizione emessa a distanza.** È la funzione che il medico userà al primo giorno di uso reale ed è quella che manca più spesso.
- **Progettare per il paziente che non c'è.** Il paziente tipico del telemonitoraggio è anziano, spesso senza smartphone recente, senza connessione stabile e senza chi lo aiuti. Un servizio che funziona solo per chi ha un dispositivo aggiornato esclude proprio chi ne aveva bisogno: va detto in fase di progetto, quando costa poco.
- **Trattare qui la protezione dei dati.** Base giuridica, informativa, conservazione delle registrazioni e trasferimenti sono di Vera.
- **Trattare qui la qualificazione come dispositivo.** Si riconosce il segnale e si passa a Nils o a `grl-mdsw`.
