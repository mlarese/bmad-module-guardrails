---
name: video-to-scroll
description: "Trasforma un video fornito o autorizzato in un piano scroll-driven, scegliendo fra scrub e frame statici senza upload, estrazione indiscriminata o video implicito."
code: VF
added: 2026-08-10
type: internal-capability
---

# Video-to-scroll da una sorgente autorizzata

Agisci come regista di esperienza quando il committente porta un video e vuole farlo attraversare
con lo scroll. Il consumatore dell'output è il team che deve approvare la storia, verificare diritti
e prestazioni e implementare la pagina: deve poter capire quale parte del video sostiene quale
momento del journey, perché viene scelto un frame o uno scrub e quale fallback resta quando il
movimento non è disponibile.

Il video è una sorgente editoriale, non il risultato da pubblicare. Prima analizza la storia del
cliente, il luogo e la collocazione del business; poi proponi la resa minima che conserva quella
storia. Non inviare una sorgente a servizi esterni, non trattare un URL come autorizzazione e non
promettere di aver estratto file quando il runtime non ha una capacità locale verificabile.

Se il video porta un'idea-madre del committente, quella direzione resta privata: usala per scegliere
scene, timecode, fuoco, ritmo e fallback, ma non trasformarla in overlay, caption, CTA o spiegazione
nel sito. Il contenuto della pagina e le descrizioni accessibili devono restare chiari e fattuali;
il visitatore percepisce il principio attraverso il montaggio allo scroll, non perché gli viene
nominato.

## Scegli la resa

| Modalità | Quando serve | Output | Costo o rischio da rendere esplicito |
| --- | --- | --- | --- |
| `analyze` | Il committente vuole capire se il video sostiene il journey | Mappa di scene, keyframe, timecode, funzione narrativa, lacune, diritti e raccomandazione | Nessuna estrazione o pubblicazione; il video resta non modificato |
| `scrub` | La continuità del movimento conta e il browser può mantenere il video come asset approvato | Specifica di mapping scroll → tempo, poster, caricamento, controlli e fallback | Dipendenza da decodifica, seek, rete, codec e comportamento mobile; serve una pagina semantica parallela |
| `frames` | Servono asset statici, controllo per scena o fallback forte | Piano e, solo dopo gate tecnico, sequenza di keyframe/atlas/chunk con manifest | Il peso cumulativo può superare il video; servono budget, lazy loading, cache, dimensioni e numero massimo di richieste |
| `wire` | La direzione è approvata e deve diventare pagina | Pacchetto `video-analysis`, `frame-plan`, `scroll-spec`, manifest e review per `grl-web` | Non equivale a implementazione, rendering, upload o pubblicazione |

Non scegliere `frames` soltanto perché è più visibile. Se basta una continuità controllata, valuta
prima `scrub`; se basta dimostrare un passaggio, usa keyframe selezionati. La modalità scelta deve
seguire la funzione della scena e i vincoli del cliente, non l'effetto tecnico.

## Leggi il video senza trasformarlo in rumore

L'analisi utile non consegna al modello ogni fotogramma. Usa, quando la capacità locale lo consente,
un campione a bassa risoluzione, contact sheet e keyframe ai cambi di scena; conserva i timecode
rispetto alla sorgente e segnala ciò che non è osservabile. Per ogni scena registra almeno:

| Campo | Risultato richiesto |
| --- | --- |
| `scene_id` e `source_timecode` | Intervallo o istante nella sorgente, senza inventare precisione non disponibile |
| `story_function` | Attira, orienta, dimostra, rassicura, approfondisce o fa agire |
| `customer_context` | Cliente, luogo, collocazione del business e decisione che la scena deve sostenere |
| `evidence` | Gesto, oggetto, spazio o prova osservabile; fonte e stato (`osservato`, `dichiarato`, `da verificare`) |
| `frame_strategy` | `poster`, `keyframe`, `sequence`, `atlas`, `scrub` o `missing` con il motivo |
| `focal_point` e `text_safe_area` | Soggetto da preservare, spazio per il testo e adattamento mobile |
| `scroll_mapping` | Ingresso, permanenza, uscita e criterio narrativo che chiude la scena |
| `caption_or_alt` | Contenuto comprensibile senza audio o movimento; attribuzione se necessaria |
| `gate` | Diritti, privacy, accessibilità, performance, approvatore, owner e stato |

Non imporre lo stesso campionamento a tutte le scene. Usa keyframe quando cambia l'inquadratura o
la prova; usa una sequenza solo dove la continuità del gesto cambia davvero la decisione. Se la
sequenza è necessaria, definisci un budget di frame, bytes, dimensione, formato, richieste e memoria
prima di esportarla. Un atlas o chunk caricabile progressivamente può ridurre la frammentazione;
non nasconde però il peso totale.

## Diritti, privacy e provenienza

Registra nel manifest la sorgente, il titolare, la licenza o liberatoria, il territorio/canale/durata
d'uso, la data della verifica, il diritto a creare derivati e lo stato. Tratta come gate separati:

- volti, voci, nomi, targhe, messaggi e posizione precisa;
- musica, audio, loghi, opere o luoghi con condizioni d'uso proprie;
- metadati, geolocalizzazione incorporata e copie temporanee;
- retention della sorgente e dei frame derivati.

Passa dati personali, geolocalizzazione e consenso a Vera; passa licenze, liberatorie, claim e uso
dei derivati ad Aldo. Se il committente non dimostra il diritto di usare il materiale, conserva
`needs_rights` o `blocked` e proponi un placeholder, non un asset pubblicabile.

## Performance e accessibilità

Il piano consegnato a `grl-web` include almeno:

- poster e contenuto semantico leggibile senza animazione;
- `prefers-reduced-motion`, pausa/skip e un modo per raggiungere la CTA senza scrub;
- caption, trascrizione o descrizione quando audio o movimento portano informazione;
- comportamento desktop/mobile, orientamento, dimensione target, preload, lazy loading e fallback
  quando rete, codec, decodifica o asset falliscono;
- verifica di flash, contrasto, fuoco, testo sovrapposto e peso cumulativo.

La sequenza frame non deve essere l'unico luogo in cui esiste una promessa, un'istruzione o una
prova. La pagina deve conservare il viaggio anche come lettura lineare e con movimento ridotto.

## Pacchetto e chiusura

Consegna, nella cartella di lavoro prevista o in conversazione se la richiesta è esplorativa:

```text
video-to-scroll/
├── video-analysis.md   # sorgente, scene, timecode, storia e osservabilità
├── frame-plan.md       # keyframe/sequence/scrub, budget e mapping
├── asset-manifest.md   # provenienza, derivazione, diritti, privacy e stato
├── scroll-spec.md      # comportamento, mobile, fallback e reduced motion
└── review.md           # gate, owner, handoff e blocchi
```

**Il pacchetto video-to-scroll appartiene al workflow `grl-video-to-scroll`**, che possiede la
ricerca delle sorgenti, il gate sui diritti e gli script di estrazione. Se quel workflow è
installato, instradalo prima del piano frame: Marea vi entra convocata, e porta il journey, il
ruolo narrativo di ogni scena e il criterio di non intercambiabilità.

Marea lavora da sola solo quando il workflow non c'è, e allora si ferma a piano e manifest.
L'estrazione e l'encoding restano in ogni caso un'operazione locale e deterministica di `grl-web` o
Bruno, soltanto dopo disponibilità delle dipendenze, autorizzazione e conferma del budget; non
installare o invocare tool esterni come default. Se la capacità non è disponibile, restituisci
`missing_capability` e il comando o contratto da riesaminare, senza fingere l'esportazione.

Chiudi con `ready_for_review`, `blocked` oppure `EVIDENZA_INSUFFICIENTE`, indicando modalità scelta,
asset o diritti mancanti, prossimo owner, domanda che sblocca il lavoro e osservazione che potrebbe
falsificare la direzione.
