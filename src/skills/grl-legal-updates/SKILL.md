---
name: grl-legal-updates
description: Monitora novità normative e giurisprudenziali recenti. Usa quando l'utente chiede «ultime normative», «nuove leggi», «bollettini», «emendamenti» o una ricerca legale per periodo.
---

# grl-legal-updates ⚖️

## Panoramica

Questo workflow produce un digest verificabile delle novità legali pubblicate nel periodo
richiesto: leggi, decreti, regolamenti, bollettini, circolari, sentenze rilevanti e stato degli
emendamenti. Il destinatario deve poter distinguere in pochi minuti ciò che è stato pubblicato,
ciò che è già efficace, ciò che è ancora proposto e ciò che non è stato confermato.

Agisci come coordinatore della ricerca legale. Usa ricerca web live e fonti primarie; non trasformare un
risultato di ricerca, una newsletter o un commento professionale in una norma.

## Regole di risoluzione

- I percorsi nudi come `references/fonti-live.md` si risolvono dalla radice di questa skill.
- `{project-root}` è la directory del progetto.
- `{date}` è la data corrente risolta dalla configurazione BMad; nelle risposte usa sempre la data
  effettivamente verificata, non una data ricordata.
- La configurazione si risolve con `uv run {project-root}/_bmad/scripts/resolve_config.py -p {project-root} -k core`;
  se fallisce, leggi `{project-root}/_bmad/config.toml` e `{project-root}/_bmad/config.user.toml`, con
  italiano come lingua di default.
- `{planning_artifacts}` è il percorso degli artefatti di pianificazione dichiarato dalla
  configurazione core. Se la configurazione non lo espone, la cartella di ricerca è
  `{output_folder}/research`; se manca anche `{output_folder}`, è `{project-root}/_bmad-output/research`.
  Il report va lì, mai in un percorso indeterminato.

## In attivazione

Registra `run_started_at` ed esegui prima un **capability preflight**. Nel run annota almeno:

```yaml
capability_preflight:
  bmad_deep_recon: available | unavailable | error
  bmad_review: available | unavailable | error
  web_live: available | unavailable | error
  primary_sources: available | partial | blocked
```

Per ogni capability mancante registra `missing_capability` con nome, motivo, impatto e prossimo
passo. Per ogni fonte primaria decisiva registra `accessible` o `blocked`.

Non confondere una skill descritta nel prompt con una capability invocabile nel runtime: se non
puoi aprire o invocare una capability, registrala come `unavailable` e non dichiarare di averla
usata. Fissa `as_of` solo dopo il secondo gate e la sweep conclusiva. Leggi il report eventuale
dello stesso argomento e instrada la richiesta:
nuova finestra → raccolta; stessa finestra già presente → `Refresh` di Deep Recon se disponibile
insieme a `web_live=available`, altrimenti `Refresh` di `live_manual`; senza web usa
`collection_mode: materials_only` sui soli materiali forniti; sola richiesta di controllo → i due gate `bmad-review` o i
due passaggi manuali sul report esistente. Se mancano giurisdizione o periodo
esplicito, applica i default qui sotto senza inventare un settore.

## Capability preflight e fallback

La modalità di raccolta dipende dal preflight e viene sempre riportata nel report:

1. **`bmad_deep_recon=available` e `web_live=available`**: invoca `bmad-deep-recon` direttamente con
   tipo `domain`, preset `standard`, `validation = max` e `red_team = on`.
2. **`bmad_deep_recon=unavailable|error` e `web_live=available`**: usa il fallback `live_manual`. Cerca
   direttamente sulle fonti primarie con lo stesso brief, apri gli atti e compila manualmente
   source matrix, lineage e registro delle verifiche. Non chiamare questa raccolta Deep Recon e
   non attribuirle una verifica che non è stata fatta.
3. **`web_live=unavailable|error`**: imposta `collection_mode: materials_only` e usa solo fonti
   ufficiali già fornite dall'utente o presenti nei materiali locali. Se manca una fonte primaria
   decisiva o la verifica indipendente, imposta `coverage_status=blocked` e
   `status=blocked`/`unverified`; non produrre un verdetto corrente.
4. **Né web né fonti ufficiali accessibili**: il run è `blocked/no_live_sources`. Restituisci solo
   il limite, i dati necessari per riprovare e il fallback operativo; niente norme, date, stati o
   scadenze ricordati o ricavati da una fonte secondaria.

Per i gate: usa due invocazioni separate di `bmad-review` quando `bmad_review=available`; se è
`unavailable|error`, registra `missing_capability: bmad-review` ed esegui due passaggi manuali separati
con le stesse lenti e checklist, marcando entrambi `fallback_review` e `review_mode=manual`. Se
non è possibile eseguire né la review disponibile né quella manuale, il finding resta `blocked` e
il report non si chiude come corrente-confermato.

## Periodo e perimetro

Il periodo è inclusivo e ha fine oggi, salvo un termine esplicito dell'utente. Se manca una data
iniziale, usa **un mese di calendario prima di oggi**, non una stima a memoria di 30 giorni; se il
giorno corrispondente non esiste, usa l'ultimo giorno del mese precedente. Accetta `dal YYYY-MM-DD`,
`dal DD/MM/YYYY` e, se fornito, `al ...`; normalizza poi tutto in ISO nel report. Rifiuta date
malformate, un intervallo con `dal > al` o una finestra futura: non correggere in silenzio l'input
e non cercare dati che non possono ancora esistere.

Se la data iniziale è esplicita, non aggiungere materiale precedente solo perché è importante:
puoi citarlo in una nota di contesto separata, marcata fuori periodo. Se manca la giurisdizione,
assumi Italia e includi solo atti UE direttamente pertinenti; per una regione, un comune, un
settore regolato o un Paese diverso chiedi il perimetro minimo prima di cercare.

Distingui sempre:

- data di pubblicazione o emissione;
- data di entrata in vigore, applicazione, scadenza o abrogazione;
- atto vigente, atto approvato ma non efficace, proposta, emendamento presentato e emendamento
  approvato.

## Garanzia di attualità e completezza

Leggi `references/assurance-controls.md` e apri il run con una scheda `scope`/`as_of`: il report
può essere dichiarato `complete_for_declared_scope` solo per giurisdizione, materie, categorie,
fonti e finestra elencate nella scheda. Non promettere completezza assoluta del web. Per ogni
fonte primaria pertinente registra query/filtri, ora di ricerca e `covered`, `empty`, `partial` o
`blocked`; una fonte decisiva non accessibile rende il report `blocked`, non “aggiornato”.

Per ogni atto costruisci la catena `pubblicato → efficace → modificato/sostituito/convertito →
abrogato/scaduto` e annota eventuali rettifiche, proroghe, decreti attuativi e testo
vigente/multivigente. Un atto precedente può comparire come contesto di lineage, mai come regola
corrente senza una verifica ufficiale successiva. `vigente-confermato` è ammesso solo quando
pubblicazione, versione/stato a `as_of`, catena di successione, seconda fonte indipendente e due
gate sono tutti presenti; altrimenti usa `supersession_risk`, `stale`, `unverified`, `disputed` o
`blocked`.

## Raccolta live

Carica `references/fonti-live.md` e `references/assurance-controls.md`. Quando il preflight
segnala `deep_recon=available` e `web_live=available`, invoca **`bmad-deep-recon` direttamente**,
con tipo `domain`. Non invocare `bmad-domain-research`: è uno shim deprecato che inoltra alla
stessa skill e non aggiunge capacità. Negli altri casi applica il fallback dichiarato sopra e
registra la modalità effettivamente usata.

Quando usi Deep Recon, passa un brief che contenga giurisdizione, periodo, settori/parole chiave e
questo obiettivo: costruire un registro di aggiornamenti legali correnti, con priorità alle
dimensioni “regole del gioco” e “cambiamenti pendenti” del pack domain. Usa il preset `standard`,
`validation = max`, ricerca web live e `red_team = on`: il controllo massimo è il default. Dividi
gli assistenti per fonte/atto; il lead deduplica e compila la matrice di copertura. Nel fallback
`live_manual` usa lo stesso brief come piano di ricerca e compila gli stessi registri senza
attribuirli a Deep Recon.

Ogni elemento entra nel registro solo con:

- fonte primaria aperta e URL diretto;
- ente emittente, tipo e identificativo dell'atto;
- data pubblicazione e stato alla fine del periodo;
- spiegazione breve di cosa cambia e per chi;
- fonte indipendente di controllo o versione ufficiale successiva;
- registro di lineage con sostituzioni, modifiche, conversioni, abrogazioni, scadenze e ultima
  verifica;
- confidenza e motivo di eventuale stato `unverified` o `disputed`.

Registra anche le categorie senza risultato e richiami inline al source appendix: l'assenza deve
essere riproducibile, non una supposizione.

Dopo il secondo gate, riapri le URL decisive e registra `final_accessed_at` prima di `as_of`;
altrimenti il finding non è corrente-confermato.

## Doppio gate bmad-review

Dopo che esiste il report e il suo source appendix, esegui due gate separati, in contesto fresco e
in questa sequenza. Se `bmad_review=available`, sono due invocazioni separate di **`bmad-review`**;
altrimenti sono due passaggi manuali separati con le stesse lenti e checklist:

1. **Gate evidenza e vigenza.** Usa le lenti `adversarial,edge-case-hunter`. Chiedi di aprire ogni
   URL citato, verificare fonte primaria, date, giurisdizione e ogni arco della lineage: modifica,
   sostituzione, conversione, abrogazione, proroga, rettifica, attuazione ed efficacia. Deve
   cercare affermazioni senza fonte, fonti stale, duplicati, titoli che non sostengono il testo e
   risultati che mostrano una legge vecchia mentre esiste un testo successivo.
2. **Gate indipendente di completezza.** Dopo le correzioni, esegui il secondo passaggio in
   contesto fresco con le lenti `verification-gap,adversarial` e istruzione nuova: ricontrollare da
   zero ogni finding load-bearing, la matrice di copertura e l'atto contrario/successivo usando
   un editore diverso o una versione ufficiale successiva. Se `bmad_review=available` usa
   `bmad-review`; altrimenti applica la stessa checklist manualmente. Lo stesso URL non conta due
   volte. Verifica che `as_of` sia reale, che nulla fuori periodo sia diventato un risultato
   corrente e che ogni finding marcato `vigente-confermato` soddisfi tutti i requisiti del
   reference.

Non chiudere il workflow se un finding decisivo resta senza fonte primaria, senza seconda verifica
indipendente, con lineage incompleta, se la matrice è `partial`/`blocked`, se i due gate discordano
senza spiegazione o se una pagina non è accessibile. In questi casi il finding resta
`unverified`/`disputed`/`blocked` e il report dichiara il limite, la fonte o l'arco mancante e il
prossimo controllo necessario. L'assenza di `bmad-review` non è da sola un errore: applica i due
passaggi manuali previsti dal preflight e registrali. La data di accesso da sola non dimostra che
una pagina sia la versione più recente.

## Output

Conserva nella cartella di ricerca il report prodotto dalla modalità effettivamente usata
(`deep_recon`, `live_manual` o `materials_only`) e restituisci in conversazione un riepilogo breve. Il report deve
avere almeno:

- sintesi esecutiva e periodo/giurisdizione;
- `as_of`, criteri di inclusione e `coverage_status` (`complete_for_declared_scope`, `partial` o
  `blocked`);
- capability preflight, `collection_mode` (`deep_recon`, `live_manual` o `materials_only`), `review_mode` e motivazione di ogni eventuale blocco;
- tabella degli atti pubblicati, bollettini, prassi, sentenze e emendamenti;
- tabella di lineage/versione per ogni finding decisivo, inclusi atti sostitutivi o abrogativi;
- stato `vigente`, `efficace`, `approvato-non-efficace`, `proposto`, `scaduto`, `abrogato`,
  `unverified` o `disputed`;
- impatto pratico, soggetti coinvolti e prossima data da controllare;
- sezione separata per risultati esclusi o fuori periodo;
- registro dei due gate `bmad-review` oppure dei due gate `manual_review` di fallback, con esito e correzioni;
- fonti con ente, URL, data di pubblicazione, data di accesso, ruolo della fonte (primaria o
  indipendente) e confidenza;
- source matrix con fonti controllate senza risultato e query/filtri usati;
- staleness map o istruzione esplicita su quando ripetere la ricerca.

Invoca Aldo (`grl-agent-legal`) solo per tradurre l'effetto pratico dei finding confermati: Aldo
non può colmare una fonte mancante né cambiare lo stato ufficiale di un atto. Non presentare come
attuale una norma ricordata.

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
