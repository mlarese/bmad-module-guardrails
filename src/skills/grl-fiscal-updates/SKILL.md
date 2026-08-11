---
name: grl-fiscal-updates
description: Monitora novità fiscali e finanziarie recenti. Usa quando l'utente chiede «ultime novità fiscali», «aggiornamenti del commercialista», «circolari», «bollettini», «bandi», «incentivi» o emendamenti per periodo.
---

# grl-fiscal-updates 🧾

## Panoramica

Questo workflow produce un digest verificabile delle novità fiscali, contabili, previdenziali e
di finanza agevolata pubblicate nel periodo richiesto. Il destinatario deve poter distinguere
una norma applicabile da una prassi, un bando aperto da un annuncio e un emendamento da una regola
già efficace.

Agisci come coordinatore della ricerca fiscale. Parti dalla fonte dell'ente che emette o gestisce la
misura, usa fonti professionali solo per trovare piste o spiegare il contesto e non sostituire
mai la verifica live con una risposta ricordata.

## Regole di risoluzione

- I percorsi nudi come `references/fonti-live.md` si risolvono dalla radice di questa skill.
- `{project-root}` è la directory del progetto.
- `{date}` è la data corrente risolta dalla configurazione BMad: è il riferimento per «oggi» nel controllo della finestra, nella data del report e in `as_of`.
- La configurazione si risolve con `uv run {project-root}/_bmad/scripts/resolve_config.py -p {project-root} -k core`;
  se fallisce, leggi `{project-root}/_bmad/config.toml` e `{project-root}/_bmad/config.user.toml`, con
  italiano come lingua di default.
- Il report va in `{output_folder}/research/`, e si chiama `fiscal-updates-{dal}_{al}.md`, con le date in
  ISO. Se `{output_folder}` non è risolvibile, vale `{project-root}/_bmad-output/research`. Mai un
  percorso indeterminato. Il percorso `planning_artifacts` non serve qui: vive sotto `[modules.bmm]`
  e il comando di risoluzione qui sopra legge solo `core`.

## Capability preflight e fallback

Prima di chiamare una skill o un tool, verifica le capability realmente esposte dal runtime e
registra nel run almeno:

```yaml
capability_preflight:
  bmad_deep_recon: available | unavailable | error
  bmad_review: available | unavailable | error
  web_live: available | unavailable | error
  primary_sources: available | partial | blocked
```

Il nome di una skill scritto in questo documento, in un prompt o in una guida non dimostra che la
capability sia esposta. Se il runtime non rende verificabile la sua presenza, marcala
`unavailable`, registra `missing_capability` con nome, motivo e prossimo passo, e non tentare la
chiamata. Invoca `bmad-deep-recon` o `bmad-review` solo quando il preflight li marca `available`.
Se una chiamata esposta fallisce, registra `error` e non scrivere nel report che il passaggio è
stato completato. Un fallback deve dichiarare il proprio modo (`live_manual`,
`materials_only` o `manual_review`); non deve creare tool call, transcript o esiti attribuiti a una
skill non disponibile.

Applica questa sequenza:

1. Se `bmad_deep_recon=available` e `web_live=available`, invocalo direttamente con `type=domain`
   e conserva la risposta effettiva. Se è `unavailable` o `error` e `web_live=available`, usa
   `live_manual`: stesso brief, stessa mappa delle fonti, ricerca nelle fonti ufficiali,
   query/filtri, URL, timestamp e stato `covered`, `empty`, `partial` o `blocked`. Se
   `web_live=unavailable|error`, imposta `collection_mode: materials_only`, usa solo i materiali
   forniti e lascia `coverage_status: blocked`; non produrre un verdetto corrente.
2. Se `bmad_review=available`, esegui le due invocazioni separate descritte sotto e registra le
   chiamate reali. Se è `unavailable` o `error`, registra `missing_capability: bmad-review` e, se
   il web e le fonti decisive sono accessibili, esegui due gate `manual_review` distinti marcati
   `fallback_review`: il primo su evidenza/vigenza, il secondo da zero su completezza e fonti
   indipendenti. Registra per ciascuno checklist, URL o versione controllata, timestamp, correzioni
   ed esito; il secondo controllo non può contare lo stesso URL come verifica indipendente. Se il
   web o una fonte decisiva mancano, registra il gate come `blocked` e conserva i finding in
   `unverified`, `disputed` o `blocked`.
3. Fissa `as_of` solo dopo un secondo gate effettivamente concluso e la sweep finale delle URL
   decisive. Se il run è `partial` o `blocked`, lascia `as_of` non fissato (`pending` nel riepilogo)
   e dichiara cosa manca; una data di esecuzione non trasforma materiali vecchi in verifica corrente.

## In attivazione

Registra `run_started_at`; fissa `as_of` solo dopo il secondo gate e la sweep conclusiva. Leggi il
report eventuale dello stesso argomento e
instrada la richiesta:
nuova finestra → raccolta; stessa finestra già presente → refresh tramite la capability esposta
(`bmad-deep-recon` se disponibile, altrimenti `live_manual`); sola richiesta di controllo → i due
gate disponibili (`bmad-review` se esposto, altrimenti `manual_review`) sul report esistente. Se
il preflight segnala web o fonti decisive mancanti, conserva `blocked` invece di simulare il
refresh o i gate. Se mancano territorio o periodo esplicito, applica i default qui sotto e chiedi
solo il dato economico che cambia il verdetto.

## Periodo e dati minimi

Il periodo è inclusivo e termina oggi, salvo un termine esplicito. Senza `dal`, usa **un mese di
calendario prima di oggi**; se il giorno corrispondente non esiste, usa l'ultimo giorno del mese
precedente. Accetta `dal YYYY-MM-DD`, `dal DD/MM/YYYY` e `al ...`, poi mostra le date normalizzate
in ISO. Rifiuta date malformate, `dal > al` e una finestra futura; non correggere l'input in
silenzio. In headless segnala `blocked/invalid_scope` e non produrre un verdetto corrente. Se
l'utente chiede solo un bollettino generale, non inventare un profilo
aziendale; per dire se una misura vale per qualcuno chiedi forma giuridica, sede, ATECO/regime,
dimensione, anno d'imposta e tipo di spesa solo quando cambiano il verdetto.

Assumi Italia e, quando pertinente, UE. Per regione, ente previdenziale specifico o settore
particolare chiedi il territorio minimo. Separa sempre data di pubblicazione, entrata in vigore,
periodo d'imposta, apertura/chiusura dello sportello e scadenza di rendicontazione.

Classifica ogni risultato come norma vigente, prassi amministrativa, bando/strumento, annuncio,
emendamento/proposta, sentenza o fonte secondaria. Un aggregatore non dimostra apertura, aliquota,
percentuale, cumulabilità o ammissibilità.

## Garanzia di attualità e completezza

Leggi `references/assurance-controls.md` e apri il run con `scope` e `as_of: pending`: “completo” significa
solo completo per territorio, materie, categorie, fonti e finestra dichiarati. Per ogni fonte
primaria registra query/filtri, ora di ricerca e stato `covered`, `empty`, `partial` o `blocked`.
Una fonte dell'Agenzia, dell'ente previdenziale o del gestore non accessibile, quando è decisiva,
porta il report a `blocked`; non si colma con un articolo professionale.

Per ogni norma, circolare, provvedimento, bando o incentivo costruisci la lineage della versione:
pubblicazione, efficacia, modifica, sostituzione, conversione, abrogazione, proroga, rettifica,
chiusura o esaurimento risorse. Un risultato è `vigente-confermato`/`aperto-confermato` solo con
fonte primaria, stato o testo corrente a `as_of`, catena successiva controllata, verifica
indipendente e due gate superati. Altrimenti usa `supersession_risk`, `stale`, `unverified`,
`disputed` o `blocked`.

## Raccolta live

Carica `references/fonti-live.md` e `references/assurance-controls.md`, poi applica il capability
preflight. Con `bmad_deep_recon=available` invoca **`bmad-deep-recon` direttamente**, con tipo
`domain`. Non usare `bmad-domain-research`: è deprecato e inoltra alla stessa skill. Nel brief
indica periodo, territorio, temi fiscali e questo obiettivo: costruire un registro corrente di
norme, circolari, risoluzioni, bollettini, emendamenti e misure agevolative, potando le dimensioni
del pack domain a “regole del gioco” e “cambiamenti pendenti”.

Con `bmad_deep_recon=unavailable|error` non tentare una chiamata inventata: se `web_live=available`
esegui il fallback `live_manual` con lo stesso brief e la stessa mappa delle fonti. Una ricerca
manuale è verificabile solo se conserva query/filtri, URL ufficiali aperte, ora di ricerca e stato
di ogni fonte; non chiamarla Deep Recon. Se il web non è disponibile, passa a `materials_only`,
separa i materiali forniti dalla verifica mancante e lascia il report `blocked`.

Se `bmad_deep_recon=available`, usa il preset `standard`, `validation = max`, ricerca web live e
`red_team = on`: per materia fiscale e incentivi il controllo massimo è il default, anche se
aumenta tempi e consumo. Nel fallback `live_manual` applica la stessa checklist e severità, ma non
attribuire a Deep Recon preset, assistenti o risultati che non sono stati eseguiti. Gli assistenti
possono dividersi per Agenzia/ente, previdenza e incentivi, ma il lead deve eliminare duplicati e
comunicati che rinviano allo stesso atto e compilare la matrice di copertura.

Ogni finding deve avere fonte primaria aperta, ente, atto o misura, data, stato, destinatari,
condizioni economiche e URL diretto, oltre alla versione/lineage e alla data di ultima verifica.
Per un incentivo controlla almeno beneficiari, territorio,
ATECO o attività, spese, intensità, cumulo/de minimis, risorse, apertura, chiusura, erogazione e
rendicontazione. La verifica interna della raccolta, sia `deep_recon` sia `live_manual`, non
sostituisce i due gate `bmad_review` o `manual_review`.
Registra anche le categorie di fonti consultate senza risultato e usa richiami inline che
risolvono a una riga del source appendix: un elenco vuoto non dimostra che non esistano novità.
Dopo il secondo gate, riapri le URL decisive e registra `final_accessed_at` prima di `as_of`;
altrimenti il finding non è corrente-confermato.

## Doppio gate bmad-review

Quando report e source appendix sono completi e `bmad_review=available`, esegui due invocazioni
separate di **`bmad-review`**, in contesto fresco:

1. **Gate evidenza e vigenza.** Lenti `adversarial,edge-case-hunter`: aprire ogni URL, verificare
   fonte primaria, date, versione dell'atto, stato della misura, lineage di modifiche/sostituzioni/
   abrogazioni/proroghe e date dello sportello. Cercare percentuali, soglie, scadenze, cumulo,
   risorse e ammissibilità senza prova, anche quando un portale professionale li dà per attuali.
2. **Gate indipendente di completezza.** Dopo le correzioni, nuova invocazione in contesto fresco
   con le lenti `verification-gap,adversarial`: ripetere da zero il controllo dei finding decisivi,
   la matrice di copertura e la ricerca di atti contrari o successivi usando un editore diverso o
   una versione ufficiale successiva. Lo stesso URL non conta due volte. Verificare `as_of`, periodo
   richiesto, proroghe, riaperture, esaurimento risorse e che ogni stato “confermato” rispetti il
   reference.

Se `bmad_review=unavailable|error`, sostituisci le due chiamate con due gate `manual_review`:

1. **Gate manuale evidenza e vigenza.** Ripeti il controllo di URL, fonte primaria, date, versione,
   stato, lineage e condizioni economiche con la checklist del primo gate.
2. **Gate manuale indipendente di completezza.** Riparti dai finding decisivi e dalla source matrix,
   cerca un editore diverso o una versione ufficiale successiva, registra le correzioni e non usare
   il verdetto del primo gate come prova. Lo stesso URL non conta due volte.

Un finding decisivo senza fonte primaria, senza seconda verifica indipendente, con lineage
incompleta, matrice `partial`/`blocked`, gate discordanti, pagina non accessibile o
gate manuale non eseguibile resta `unverified`/`disputed`/`blocked`; il workflow lo dichiara con il
passaggio mancante. Non si risolve scegliendo la fonte più ottimistica. Se una fonte
professionale (CNDCEC/FNC, Eutekne, IPSOA o Contributi Europa) anticipa un dato, usala come lead e
poi sostituiscila con l'atto dell'ente competente. La data di accesso non prova da sola che la
pagina sia la versione più recente.

## Output

Conserva nella sua cartella il report prodotto dal modo effettivo di raccolta (`deep_recon`,
`live_manual` o `materials_only`) e restituisci un riepilogo breve.
Includi:

- periodo, territorio e criteri di ricerca;
- `as_of` e `coverage_status` (`complete_for_declared_scope`, `partial` o `blocked`);
- tabella di norme, prassi, bollettini, emendamenti, bandi e incentivi;
- tabella di lineage/versione con atti sostitutivi, modificativi, abrogativi, proroghe e stato
  corrente;
- per ogni misura: chi, cosa, quanto solo se verificato, quando, vincoli, liquidità e
  rendicontazione;
- **stato della misura**: `vigente`, `efficace`, `aperto`, `chiuso`, `prorogato`, `esaurito` o
  `proposto` — dice cosa fa la norma;
- **stato di verifica**: `vigente-confermato`/`aperto-confermato`, `supersession_risk`, `stale`,
  `unverified`, `disputed` o `blocked` — dice quanto regge la prova. I due assi si scrivono
  sempre entrambi: un bando aperto mai confermato non è un bando aperto verificato;
- risultati esclusi o fuori periodo;
- `capability_preflight`, modo effettivo di raccolta (`deep_recon`, `live_manual` o
  `materials_only`) e modo effettivo dei gate (`bmad_review`, `manual_review` o `blocked`);
- registro dei due gate `bmad-review` oppure dei due gate `manual_review`, senza attribuire a un
  tool non esposto passaggi non eseguiti, e delle correzioni;
- fonti con ente, URL, data di pubblicazione, data di accesso, ruolo della fonte (primaria o
  indipendente) e confidenza;
- source matrix con fonti controllate senza risultato e query/filtri usati;
- prossima data di ricontrollo/staleness map.

Invoca Marta (`grl-agent-fiscal`) per tradurre i finding confermati in impatto pratico o
pre-screening: non può completare dati mancanti, promettere la concessione di un incentivo o
firmare una dichiarazione. Applica il fallback definito nel capability preflight senza attribuire
a Deep Recon o a `bmad-review` passaggi non eseguiti. Non dichiarare attuali aliquote, soglie o
scadenze a memoria.

## Revisione editoriale finale

Prima di consegnare, rileggi ogni output destinato a una persona e correggi solo la prosa:
chiarezza, grammatica, coesione, tono e terminologia. Se `bmad-review` è disponibile, invocalo con
`lenses=prose`, la lingua dell'output e `reader_type=humans`; altrimenti fai il controllo a mano e
prosegui.

Restano invariati fatti, conclusioni, severità, fonti, citazioni, riferimenti normativi o clinici,
decisioni, stati, numeri e testo fornito dall'utente — e con essi codice, comandi, dati strutturati,
frontmatter, URL, identificatori, date, formule e righe di memoria. Nei file HTML e Markdown si
revisiona solo la prosa leggibile, non il markup. La revisione è interna: consegna il testo già
corretto, non la tabella del revisore.
