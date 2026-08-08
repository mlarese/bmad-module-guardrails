---
name: grl-fiscal-updates
description: Monitora novità fiscali e finanziarie recenti. Use when l'utente chiede «ultime novità fiscali», «aggiornamenti del commercialista», «circolari», «bollettini», «bandi», «incentivi» o emendamenti per periodo.
---

## Revisione editoriale finale

Ogni output destinato a una persona — risposta in conversazione, riepilogo, digest, profilo o testo
visibile di una pagina — passa da un controllo di prosa prima della consegna.

- Invoca `bmad-review` con `lenses=prose` se disponibile, impostando la lingua dell'output, la
  guida di stile del progetto e `reader_type=humans`; se l'output contiene più lingue, revisiona ogni lingua
  separatamente.
- Applica solo correzioni di chiarezza, grammatica, coesione, tono e terminologia. Non cambiare
  fatti, conclusioni, severità, fonti, citazioni, riferimenti normativi o clinici, decisioni o testo
  fornito dall'utente.
- Lascia invariati codice, comandi, YAML/JSON/TOML/CSV, frontmatter, URL, identificatori, date,
  formule, dati strutturati e righe di memoria. Nei file HTML/Markdown revisiona solo la prosa
  leggibile, non markup e struttura.
- La review è interna: consegna il testo già migliorato, non la tabella del revisore. Se la skill
  non è installata, esegui un controllo manuale equivalente e prosegui; non installare Freya per
  questo passaggio.

# grl-fiscal-updates 🧾

## Overview

Questo workflow produce un digest verificabile delle novità fiscali, contabili, previdenziali e
di finanza agevolata pubblicate nel periodo richiesto. Il destinatario deve poter distinguere
una norma applicabile da una prassi, un bando aperto da un annuncio e un emendamento da una regola
già efficace.

Act as a fiscal research coordinator. Parti dalla fonte dell'ente che emette o gestisce la
misura, usa fonti professionali solo per trovare piste o spiegare il contesto e non sostituire
mai la verifica live con una risposta ricordata.

## Resolution rules

- I percorsi nudi come `references/fonti-live.md` si risolvono dalla radice di questa skill.
- `{project-root}` è la directory del progetto.
- `{date}` è la data corrente risolta dalla configurazione BMad.

## On Activation

Registra `run_started_at`; fissa `as_of` solo dopo il secondo gate e la sweep conclusiva. Leggi il
report eventuale dello stesso argomento e
instrada la richiesta:
nuova finestra → raccolta; stessa finestra già presente → `Refresh` di Deep Recon; sola richiesta
di controllo → i due gate `bmad-review` sul report esistente. Se mancano territorio o periodo
esplicito, applica i default qui sotto e chiedi solo il dato economico che cambia il verdetto.

## Periodo e dati minimi

Il periodo è inclusivo e termina oggi, salvo un termine esplicito. Senza `dal`, usa **un mese di
calendario prima di oggi**; se il giorno corrispondente non esiste, usa l'ultimo giorno del mese
precedente. Accetta `dal YYYY-MM-DD`, `dal DD/MM/YYYY` e `al ...`, poi mostra le date normalizzate
in ISO. Rifiuta date malformate, `dal > al` e una finestra futura senza correggere l'input in
silenzio; in headless segnala `blocked/invalid_scope` e non produrre un verdetto corrente. Se
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

Leggi `references/assurance-controls.md` e apri il run con `scope` e `as_of`: “completo” significa
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

Carica `references/fonti-live.md` e `references/assurance-controls.md` e invoca
**`bmad-deep-recon` direttamente**, con tipo `domain`.
Non usare `bmad-domain-research`: è deprecato e inoltra alla stessa skill. Nel brief indica
periodo, territorio, temi fiscali e questo obiettivo: costruire un registro corrente di norme,
circolari, risoluzioni, bollettini, emendamenti e misure agevolative, potando le dimensioni del
pack domain a “regole del gioco” e “cambiamenti pendenti”.

Usa il preset `standard`, `validation = max`, ricerca web live e `red_team = on`: per materia
fiscale e incentivi il controllo massimo è il default, anche se aumenta tempi e consumo. Gli
assistenti possono dividersi per Agenzia/ente, previdenza e incentivi, ma il lead deve eliminare
duplicati e comunicati che rinviano allo stesso atto e compilare la matrice di copertura.

Ogni finding deve avere fonte primaria aperta, ente, atto o misura, data, stato, destinatari,
condizioni economiche e URL diretto, oltre alla versione/lineage e alla data di ultima verifica.
Per un incentivo controlla almeno beneficiari, territorio,
ATECO o attività, spese, intensità, cumulo/de minimis, risorse, apertura, chiusura, erogazione e
rendicontazione. La verifica interna di Deep Recon non sostituisce i due gate `bmad-review`.
Registra anche le categorie di fonti consultate senza risultato e usa richiami inline che
risolvono a una riga del source appendix: un elenco vuoto non dimostra che non esistano novità.
Dopo il secondo gate, riapri le URL decisive e registra `final_accessed_at` prima di `as_of`;
altrimenti il finding non è corrente-confermato.

## Doppio gate bmad-review

Quando report e source appendix sono completi, esegui due invocazioni separate di
**`bmad-review`**, in contesto fresco:

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

Un finding decisivo senza fonte primaria, senza seconda verifica indipendente, con lineage
incompleta, matrice `partial`/`blocked`, gate discordanti, pagina non accessibile o
`bmad-review` non disponibile resta `unverified`/`disputed`/`blocked`; il workflow lo dichiara con
il passaggio mancante. Non si risolve scegliendo la fonte più ottimistica. Se una fonte
professionale (CNDCEC/FNC, Eutekne, IPSOA o Contributi Europa) anticipa un dato, usala come lead e
poi sostituiscila con l'atto dell'ente competente. La data di accesso non prova da sola che la
pagina sia la versione più recente.

## Output

Conserva il report prodotto da Deep Recon nella sua cartella e restituisci un riepilogo breve.
Includi:

- periodo, territorio e criteri di ricerca;
- `as_of` e `coverage_status` (`complete_for_declared_scope`, `partial` o `blocked`);
- tabella di norme, prassi, bollettini, emendamenti, bandi e incentivi;
- tabella di lineage/versione con atti sostitutivi, modificativi, abrogativi, proroghe e stato
  corrente;
- per ogni misura: chi, cosa, quanto solo se verificato, quando, vincoli, liquidità e
  rendicontazione;
- stato `vigente`, `efficace`, `aperto`, `chiuso`, `prorogato`, `esaurito`, `proposto`,
  `unverified` o `disputed`;
- risultati esclusi o fuori periodo;
- registro dei due gate `bmad-review` e delle correzioni;
- fonti con ente, URL, data di pubblicazione, data di accesso, ruolo della fonte (primaria o
  indipendente) e confidenza;
- source matrix con fonti controllate senza risultato e query/filtri usati;
- prossima data di ricontrollo/staleness map.

Invoca Marta (`grl-agent-fiscal`) per tradurre i finding confermati in impatto pratico o
pre-screening: non può completare dati mancanti, promettere la concessione di un incentivo o
firmare una dichiarazione. Se Deep Recon non è disponibile, usa una ricerca web live diretta con
lo stesso brief e la stessa mappa delle fonti; se manca anche il web, separa chiaramente ciò che è
nei materiali forniti da ciò che richiede verifica. Non dichiarare attuali aliquote, soglie o
scadenze a memoria.
