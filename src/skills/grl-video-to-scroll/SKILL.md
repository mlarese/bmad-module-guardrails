---
name: grl-video-to-scroll
description: "Prepara pacchetti video-to-scroll verificati. Use when l'utente dice \"cerca video per una landing\", \"crea frame durante lo scroll\" o chiede una pagina che mostri fotogrammi mentre si scorre."
---

# grl-video-to-scroll

## Panoramica

Questo workflow trasforma la storia di un cliente e una sorgente video autorizzata in un pacchetto pronto per una pagina scroll-driven: intervista, customer journey, ricerca delle sorgenti, piano dei frame, manifest tecnico e specifica per `grl-web`. Agisci come facilitatore di regia e produzione: l'utente conosce cliente e business, tu fai emergere le decisioni, rendi verificabili i diritti e non confondi una ricerca con un'autorizzazione.

## Convenzioni

- I percorsi nudi (`references/source-search.md`, `scripts/extract_frames.py`) si risolvono dalla cartella installata di questa skill; `{project-root}` è la cartella del progetto.
- Il lavoro vive in `{workflow.output_path}/{workflow.run_folder_pattern}/`, con `{slug}` in kebab-case. Riusa lo stesso slug quando il lavoro rientra.
- La resa predefinita è una sequenza di frame statici. Il video scrub-driven è un'alternativa esplicita, da scegliere solo se il budget di rete, il comportamento mobile e il fallback sono sostenibili.
- Non scaricare, caricare, pubblicare o distribuire automaticamente un video. La ricerca produce candidati; l'estrazione richiede un file locale e un'autorizzazione esplicita.

## In attivazione

1. Risolvi la configurazione con `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core`; se non è disponibile, usa i default ragionevoli e dichiaralo.
2. Risolvi la personalizzazione con `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow`. Applica `{workflow.activation_steps_prepend}`, carica `{workflow.persistent_facts}` e poi `{workflow.activation_steps_append}`. Se il resolver fallisce, fondi base, override di team e override personali in quell'ordine.
3. Elenca i lavori esistenti sotto `{workflow.output_path}` e risolvi lo slug. Se trovi il lavoro, riusa la cartella; altrimenti creala.
4. Esegui il preflight obbligatorio prima dell'intervista o della ricerca: `uv run scripts/check_tools.py {project-root} --output <run>/tool-preflight.json`. Controlla `uv`, `ffmpeg`, `ffprobe` e gli script runtime BMad (`resolve_config.py`, `resolve_customization.py`, `memlog.py`). Se `uv` manca, esegui il controllo con il Python disponibile per poterlo dichiarare come capability mancante.
5. Se il report è `missing`, fermati e mostra strumenti mancanti, versione rilevata, comando d'installazione per il sistema operativo e cosa rimane bloccato. Chiedi esplicitamente: «Vuoi che proceda con l'installazione?». Non installare nulla senza un sì; dopo l'installazione riesegui il preflight e prosegui solo con `status: pass`. Se l'utente sceglie di non installare, lascia `blocked` e conserva il report; non fingere di poter estrarre frame.
6. Ricava l'intento dalla richiesta: `create` prepara un pacchetto nuovo, `update` riprende un pacchetto, `validate` lo controlla in sola lettura. Se l'intento è ambiguo, chiedi una sola domanda che lo separi. Dopo il preflight, leggi una sola volta `.memlog.md` e gli artefatti esistenti oppure inizializza il memlog con `uv run {project-root}/_bmad/scripts/memlog.py init --path <run>/.memlog.md`.

Il preflight copre gli strumenti locali indispensabili; ricerca web, skill BMad di handoff e revisori sono capability dell'harness. Se una di queste non è installata o disponibile, registrala come `missing_capability`, chiedi di abilitarla/installarla e mantieni il relativo gate `blocked` senza inventare il loro verdetto. Le istruzioni per i package manager sono in `references/tool-preflight.md`.

## Scoperta della storia

In `create` fai un'intervista compatta, non un questionario infinito. Chiedi e salva in `interview.md` ciò che l'utente sa, lasciando `non noto` dove manca:

- chi è il cliente/persona, quale storia porta, quale cambiamento cerca e quale prova lo rende credibile;
- segmento e situazione del visitatore, lingua, luogo e cultura rilevanti;
- dove si trova il business, come è collocato nel territorio e quali dettagli locali devono apparire o restare fuori;
- azione unica della pagina, obiezione da superare e momento in cui va mostrata la CTA;
- tono, brand, canali e viewport, durata/peso massimo, numero indicativo di frame, formato e fallback;
- persone riconoscibili, musica, marchi, indirizzi, interni privati o altri dati/diritti presenti nel materiale.

Poi convoca Marea (`grl-agent-customer-journey`) per legare ogni scena alla storia, al luogo e alla collocazione del business. Il pacchetto — `frame-plan.md`, `asset-manifest.md`, `scroll-spec.md`, `review.md` — resta di questo workflow: Marea entra come consulente narrativa e non lo riscrive. Scrivi `journey.md` come sequenza di fasi: stato del visitatore, tensione, prova visiva, messaggio, transizione, CTA e criterio per cui la scena non è intercambiabile con una generica.

In `update` rileggi prima memlog e artefatti, mostra ogni conflitto con una decisione già approvata e non cancellare candidati accettati o scartati: una nuova ricerca deve colmare un gap dichiarato. Appendi decisioni e override al memlog; non riscriverlo.

## Ricerca delle sorgenti

Se manca un video, chiedi il perimetro di ricerca se non è già chiaro: archivio del cliente, fonte ufficiale, stock con licenza, dominio pubblico/open licence, territorio e motivo visuale. Cerca con le fonti dichiarate in `{workflow.external_sources}` e registra in `source-search.md` le query, la data `as_of`, i risultati consultati e i limiti della ricerca. La matrice `video-candidates.md` deve contenere per ogni candidato URL della pagina sorgente e dell'asset, autore/titolare, licenza e testo applicabile, attribuzione, territorio/canali/durata d'uso, persone e musica, risoluzione/durata, stato `verified`, `needs_rights`, `rejected` o `unknown` e motivo della scelta.

Un risultato di ricerca, la parola «free» o un'anteprima non provano il diritto d'uso. Senza licenza verificabile non si scarica e non si estrae: passa il candidato alla figura competente fra quelle di `{workflow.external_handoffs}` — di serie Aldo (`grl-agent-legal`) per i diritti; volti, targhe, indirizzi o altri dati personali passano anche a Vera (`grl-agent-privacy`). Nora (`grl-agent-seo`) entra quando la ricerca deve diventare un sistema di domanda, intento e contenuto locale.

## Piano e produzione

In `frame-plan.md` fai corrispondere journey e sorgente: timecode (esatto o dichiarato approssimativo), scopo della scena, numero di frame, sampling, dimensione massima, formato, qualità, budget in byte, poster, mobile, caption/alt e fallback. Distribuisci i frame sul progresso `0..1`; non inventare un timecode che la sorgente non consente di verificare.

Prima di estrarre verifica che il candidato sia `verified` o esplicitamente approvato, che il file sia locale e che l'autorizzazione includa `local_extract`. Poi esegui dalla radice della skill:

```text
uv run scripts/extract_frames.py <video-locale> --output <run>/frames --timestamps <run>/timestamps.txt --width 1600 --format webp --quality 80 --manifest <run>/frame-manifest.json
uv run scripts/validate_manifest.py <run>/frame-manifest.json --root <run> --max-frames 48 --max-bytes <budget>
```

Per un campionamento uniforme usa `--fps` al posto di `--timestamps`. Gli script usano solo `ffprobe`/`ffmpeg` locali, non hanno dipendenze di rete, emettono JSON e non pubblicano nulla. Se mancano, restituisci `missing_capability`, conserva piano e handoff a Bruno (`grl-agent-ops`) o a `grl-web`; non simulare un manifest riuscito. Se la sorgente non è locale/autorizzata, fermati al piano.

La specifica `scroll-spec.md`, consumata da `grl-web`, descrive la mappa `scroll progress → frame`, poster, preload/lazy loading, chunk, dimensioni mobile, captions/alt, `prefers-reduced-motion`, pausa/salto e alternativa semantica. Per scrub descrive durata, sincronizzazione, seek, fallback statico e condizioni di abbandono; il percorso statico resta quello di riferimento.

## Validazione e consegna

`validate` è read-only: controlla diritti e fonti, esistenza/hash/byte dei file, ordine dei timestamp e del progresso, budget, mapping, accessibilità, privacy, performance e fallback. Non correggere o rigenerare senza passare a `update`.

Prima del verdetto, passa il pacchetto a `{workflow.finalize_reviewers}` o, se `grl-board` non è installato, ai revisori pertinenti: Marea per la coerenza narrativa, Iris per la qualità visuale, Aldo per diritti, Vera per dati personali, Nils per accessibilità applicabile, Nora per ricerca e Bruno per runtime. `review.md` registra evidenze, blocchi, approvazioni, reviewer, `as_of` e stato. Gli stati ammessi sono `draft`, `blocked`, `ready_for_review` e `ready_for_implementation`; non usare `published`.

Alla consegna distilla il memlog, verifica che ogni decisione rilevante sia nell'artefatto o marcata come accantonata, esegui `{workflow.on_complete}` se valorizzato e passa `scroll-spec.md`, `frame-manifest.json`, la cartella `frames/` e `review.md` a `grl-web`. Il risultato è pronto per implementazione, non una pubblicazione automatica.

## Rotte di riferimento

| Necessità | Riferimento |
| --- | --- |
| Cercare sorgenti e verificare diritti | `references/source-search.md` |
| Definire frame, manifest e comportamento dello scroll | `references/scroll-package.md` |
| Controllare gli strumenti prima di partire | `scripts/check_tools.py`, `references/tool-preflight.md` |
| Estrarre e validare localmente | `scripts/extract_frames.py`, `scripts/validate_manifest.py` |

## Chiusura

I passaggi di consegne ammessi sono quelli di `{workflow.external_handoffs}`: nominane uno quando
la materia è suo, e dichiara il passaggio all'utente.

## Revisione editoriale finale

Prima della consegna rileggi la prosa destinata alle persone e correggi chiarezza, grammatica, coesione, tono e terminologia. Non cambiare fatti, stati, numeri, fonti, URL, identificatori, comandi, JSON, YAML, frontmatter o testo fornito dall'utente. Se `bmad-review` è disponibile usa `lenses=prose`, la lingua dell'output e `reader_type=humans`; altrimenti esegui lo stesso controllo manualmente.
