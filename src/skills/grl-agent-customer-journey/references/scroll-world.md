---
name: scroll-world
description: "Conduce l'intervista e traduce storia, brand, journey, riferimenti e asset verificati in una specifica di landing scroll-driven statica con pattern curtain e regie gallery; un video fornito passa prima dalla rotta video-to-scroll."
code: SW
added: 2026-08-10
type: internal-capability
---

# Scroll-world statico

Agisci come regista di esperienza per una landing che si attraversa con lo scroll. Il consumatore
dell'output è il team che dovrà reperire gli asset, approvare la direzione e implementare la pagina:
deve poter capire perché esiste ogni scena, quale decisione accompagna e come il movimento derivi
dallo scroll. Non consegnare una galleria di immagini, una moodboard senza percorso o un prompt di
generazione; consegna un viaggio visuale verificabile.

Se il brief contiene un'idea-madre, conservala come `private_direction` nel pacchetto interno e
compilala in `public_effect`: fuoco, ordine delle scene, scelta degli asset, ritmo, spazio,
transizioni e comportamento allo scroll. Non riportarla nel testo della pagina, nei nomi delle
sezioni, nella CTA, nei claim o nelle caption; il visitatore deve percepirne la direzione senza
ricevere la spiegazione. L'alt text resta fattuale e il messaggio commerciale resta esplicito.

Questa rotta usa asset statici come default. Se il committente porta un video e chiede di
sincronizzarlo o scomporlo con lo scroll, la rotta cambia: è `video-to-scroll`, che la tabella delle
capacità instrada. `SW` consuma soltanto keyframe o asset derivati già approvati e registrati nel
manifest; non analizza, non estrae e non pubblica il video.

Quando la richiesta comprende aperture da destra/sinistra/alto/basso, tende che si aprono o effetti
su una gallery, serve anche la libreria cinematica, che la tabella delle capacità instrada. `SW` ne
usa i pattern nominati e consegna la scelta narrativa a `grl-web` senza trasformarla in codice.

## Inquadra il risultato

Il lavoro finisce quando esistono, con stato e responsabile:

- una storia breve del soggetto, dell'evento o del business;
- il pubblico prioritario, la decisione richiesta e una CTA concreta;
- un journey di scene ordinate, ciascuna con funzione, prova, copy provvisorio e criterio di uscita;
- una grammatica di camera applicabile ad asset statici: fuoco, scala, posizione, ingresso, uscita,
  profondità, transizione, pattern curtain/gallery e comportamento su desktop e mobile;
- un registro di asset già forniti, trovati online, derivati da asset approvati o eventualmente da
  generare, con provenienza e diritti separati;
- una scheda pronta per `grl-web`, con i gate aperti chiaramente visibili.

Se il committente chiede una pagina funzionante, questa rotta prepara il pacchetto e lo passa a
`grl-web`. Se chiede soltanto concept o regia, consegna il pacchetto senza simulare l'implementazione.

## Intervista: chiedi ciò che cambia la regia

Apri con una domanda ampia sul risultato desiderato e ascolta il vocabolario del committente. Poi
chiedi solo le lacune ad alto impatto, raggruppandole in una breve tornata invece di imporre un
questionario. Conserva la risposta in `dichiarato`; ciò che manca resta `non noto`.

Copri, quando pertinente:

1. **Soggetto e promessa:** che cosa stiamo attraversando, perché esiste, quale trasformazione o
   prova deve restare nella memoria del visitatore.
2. **Pubblico e decisione:** chi deve riconoscersi, quale dubbio porta, quale azione deve compiere e
   quale CTA è autorizzata. Una CTA non dichiarata non diventa automaticamente “Scopri di più”.
3. **Brand e riferimenti:** sito, logo, palette, font, canale proprietario, fotografie o
   illustrazioni già posseduti, esempi amati e rifiutati, tono, lingua e grado di realismo.
4. **Art direction:** materia, luce, punto di vista, rapporto fra figura e spazio, densità, ritmo,
   temperatura, presenza di mascotte o oggetti ricorrenti e ciò che non deve comparire.
5. **Viaggio e scene:** cosa il visitatore scopre per primo, quale prova arriva dopo, quale ostacolo
   viene sciolto, dove compare la CTA, che cosa deve restare sullo schermo mentre scorre e dove il
   viaggio termina.
6. **Forma e vincoli:** canvas desktop e mobile, orientamento, performance, preferenze di scroll,
   accessibilità del movimento, asset ammessi, budget, titolari dei diritti, approvatore e data di
   revisione.

Se manca il soggetto, la decisione o il vincolo che determina il primo piano, fermati su una bozza
di struttura e segnala `blocked`; non riempire il vuoto con un concept generico. Se esistono già
brief, profile, decisioni o asset, riusali e chiedi soltanto cosa è cambiato.

## Disegna il journey prima della camera

Per ogni scena compila questa scheda:

| Campo | Domanda |
| --- | --- |
| Ordine e nome | Quale momento del viaggio rappresenta? |
| Funzione | Attira, orienta, dimostra, rassicura, approfondisce o fa agire? |
| Decisione | Quale dubbio o scelta del visitatore cambia qui? |
| Prova | Quale dettaglio osservabile sostiene la promessa e da dove proviene? |
| Asset | Quale immagine, illustrazione, logo, texture, font o elemento UI serve? |
| Fuoco | Quale soggetto deve restare leggibile e quale spazio deve rimanere libero per il testo? |
| Camera | Da dove entra lo sguardo, cosa mette a fuoco, come attraversa la scena e dove esce? |
| Scroll mapping | Quale tratto di scroll attiva scala, traslazione, opacità, profondità o transizione? |
| Copy | Quale frase breve accompagna la scena; cosa è ancora da approvare? |
| Desktop/mobile | Quale composizione cambia senza perdere la stessa funzione? |
| Gate | Diritti, privacy, accessibilità, performance, approvazione e owner. |

Non imporre un numero fisso di scene. Accorpa quando due scene fanno la stessa cosa; separa quando
una nuova prova cambia davvero la decisione. La CTA deve arrivare quando la storia ha già tolto
l'obiezione principale, salvo una ragione dichiarata per anticiparla.

## Determina la grammatica cinematica

Scegli una grammatica che il team possa eseguire con asset statici e che renda più chiaro il viaggio:

- **Ingresso nel mondo:** campo largo o composizione isometrica; il fuoco è stabile mentre il
  visitatore capisce contesto e promessa.
- **Avvicinamento alla prova:** scala o traslazione lenta verso un dettaglio; il dettaglio deve
  dimostrare qualcosa, non soltanto essere “cinematico”.
- **Attraversamento:** movimento laterale, verticale o su più piani; usa la profondità soltanto se
  chiarisce una relazione fra elementi.
- **Cambio di stato:** dissolvenza, maschera, clip o sostituzione di asset quando cambia il momento
  narrativo; non animare ogni elemento allo stesso modo.
- **Curtain di bordo:** un pannello entra da destra, sinistra, alto o basso e rivela la scena solo
  quando il gesto corrisponde a un ingresso, un passaggio o una prova.
- **Apertura a tenda:** due ante verticali o orizzontali si separano dal centro per aprire un mondo,
  una trasformazione o un nuovo capitolo; la scena deve restare leggibile anche già rivelata.
- **Arrivo e azione:** rallenta, stabilizza il fuoco, lascia spazio e contrasto alla CTA; il climax
  non deve rendere il bottone difficile da trovare.

Per ogni scena descrivi `camera_in`, `camera_hold`, `camera_out` e il legame con il progresso dello
scroll. Un mapping utile è qualitativo (`0–25%`, `25–60%`, `60–100%`) finché il canvas e le misure
non sono approvati; non inventare coordinate precise quando l'asset non è ancora scelto.

### Gallery come sequenza

Una gallery entra nel journey con una funzione precisa: confronto, trasformazione, attraversamento
di un luogo o dettaglio di una prova. Scegli fra `gallery-curtain`, `gallery-track`,
`gallery-mosaic-reveal`, `gallery-focus`, `gallery-stagger` e `gallery-before-after`; registra ordine,
elemento focale, criterio di avanzamento, controllo touch/tastiera, progress, alt text e fallback.
La gallery deve restare una lista o griglia leggibile con `prefers-reduced-motion`, senza autoplay,
hover obbligatorio o scroll orizzontale che intrappola il percorso principale.

La resa predefinita è deterministica: `transform`, `opacity`, `clip-path`, livelli con parallax,
Intersection Observer, SVG o canvas possono realizzare il movimento. Mantieni una versione ridotta
per `prefers-reduced-motion`, un ordine leggibile senza animazione e un fallback per immagini che
non caricano. La specifica `SW` non autorizza analisi video, estrazione, rendering o encoding. Una
sequenza di frame già approvata da `VF` può entrare come asset statico solo con budget, provenienza,
diritti e fallback espliciti.

## Cerca e registra gli asset online

Parti sempre dagli asset forniti dall'utente e dalle sorgenti ufficiali del brand. Solo dopo cerca
online ciò che manca, usando fonti coerenti con il soggetto e con l'uso previsto. Per ogni candidato
registra almeno:

| Campo | Valore |
| --- | --- |
| `asset_id` | Identificatore stabile usato nelle scene |
| `kind` | Foto, illustrazione, SVG, logo, font, texture, icona o altro |
| `source_type` | `user_provided`, `official_online`, `licensed_online`, `derived`, `video_derived`, `codex_opt_in` |
| `source_url` | URL della pagina sorgente, non solo del file |
| `creator_or_owner` | Autore o titolare se disponibile |
| `license` | Licenza e condizioni dichiarate |
| `attribution` | Testo o link richiesto, se richiesto |
| `verified_at` | Data della verifica |
| `use_scope` | Canale, territorio, durata e uso commerciale noto |
| `status` | `candidate`, `needs_rights`, `approved`, `rejected`, `missing` |
| `scene_use` | Scena e funzione, non soltanto “hero” |
| `crop_and_focal_point` | Punto di interesse e composizione necessaria |

Non chiamare “free” un asset soltanto perché appare in un motore di ricerca. Non rimuovere watermark,
non aggirare paywall, non copiare un'immagine di riferimento e non riprodurre il volto di una persona
senza diritto e consenso documentabili. Un riferimento estetico può restare ispirazione, mentre la
sorgente pubblicabile deve essere trovata o approvata separatamente. Se diritti, attribuzione,
privacy o qualità non sono chiari, usa `needs_rights` e apri l'handoff ad Aldo o Vera.

“Prendere” un asset significa reperirlo o indicarlo soltanto entro l'autorizzazione disponibile:
non caricare file su servizi, non modificare account e non pubblicare. Se l'ambiente può scaricare
asset autorizzati, conserva il file locale insieme al manifest e verifica formato, dimensioni,
trasparenza, proporzioni, alt text e peso; altrimenti consegna URL e criteri di selezione senza
affermare che il download sia avvenuto.

## Generazione solo su richiesta esplicita

La prima scelta è sempre: asset dell'utente, asset ufficiale, equivalente con licenza, oppure asset
derivato da materiale approvato.

Se resta un buco e l'utente chiede esplicitamente le immagini mancanti, **l'esecutore di serie è
Elio** (`grl-agent-imaging`): passagli prompt, vincoli e scene scoperte. Marea genera lei stessa con
Codex solo quando Elio non è installato o non risponde, e in quel caso lo dichiara. Quando genera:

1. mostra quali scene restano scoperte e perché la ricerca online non basta;
2. separa il prompt visivo dai vincoli di brand, diritti, privacy e formato;
3. dichiara che la generazione può consumare la quota o l'account disponibile e chiede il gate
   previsto dall'ambiente;
4. usa soltanto la capacità Codex disponibile, marca gli output come `codex_opt_in` e aggiorna
   provenienza, prompt, data e stato di approvazione;
5. torna alla revisione della scena e non genera video.

Se mancano sia Elio sia `image_gen`, dichiara `missing_capability` e lascia il prompt e l'asset slot
da approvare. Non invocare Monid, Higgsfield, ffmpeg o ffprobe
come sostituti.

## Pacchetto e gate

Consegna un pacchetto nominato con slug, nella cartella di lavoro prevista dal progetto o in
conversazione se la richiesta è esplorativa, con questi artefatti logici:

```text
scroll-world/
├── interview.md          # dichiarato, non noto, decisioni e domande aperte
├── journey.md            # tappe, frizioni, prove, CTA e metriche
├── cinematic-plan.md     # scene, pattern, camera_in/hold/out e scroll mapping
├── asset-manifest.md     # sorgenti, diritti, focal point e stato
├── scroll-spec.md        # comportamento statico desktop/mobile e fallback
└── review.md             # gate, handoff, approvazioni e blocchi
```

Il pacchetto è `ready_for_review` solo se ogni scena ha una funzione, ogni asset ha una sorgente o un
blocco esplicito, la CTA è coerente con il journey, mobile e reduced motion sono previsti e non resta
un video implicito. Passa a `grl-web` per la pagina, a Iris per la direzione visiva, a Sally per
l'interazione, a Nora per findability/SEO, a Nils per accessibilità, ad Aldo per licenze, a Vera per
privacy e a Elio soltanto per la generazione immagine richiesta esplicitamente.

Chiudi con `ready_for_review`, `blocked` oppure `EVIDENZA_INSUFFICIENTE`, indicando il prossimo owner,
la domanda che sblocca il lavoro e l'osservazione che potrebbe falsificare la direzione.
