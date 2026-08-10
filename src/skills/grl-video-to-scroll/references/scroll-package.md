# Pacchetto scroll-driven

Il pacchetto deve poter essere consegnato a chi implementa la pagina senza ricostruire la storia dalla chat.

## Artefatti

- `interview.md`: risposte del cliente, `non noto`, vincoli e autorizzazioni dichiarate.
- `tool-preflight.json`: capability locali, versioni rilevate, strumenti mancanti e stato del gate.
- `journey.md`: fasi del visitatore, tensione, prova, scena, transizione, CTA e criterio di successo.
- `source-search.md`: query, fonti consultate, data `as_of` e limiti della ricerca.
- `video-candidates.md`: matrice diritti/qualità/fit narrativo e candidato selezionato o bloccato.
- `frame-plan.md`: sorgente, timecode, sampling, motivo di ogni scena, formato, budget e fallback.
- `frames/`: output locale prodotto solo dopo il gate `local_extract`.
- `frame-manifest.json`: manifest generato dallo script; non modificare a mano per far passare un controllo.
- `scroll-spec.md`: contratto di implementazione per `grl-web`.
- `review.md`: verdetti, evidenze, reviewer, blocchi e stato.

## Piano dei frame

Ogni riga del piano contiene `scene_id`, fase del journey, scopo, `source_start`, `source_end` o timestamp, numero massimo di frame, formato/qualità, dimensione massima, budget byte, caption/alt, mobile crop, poster e fallback. Il piano esplicita se il tempo è esatto o approssimativo. Il numero di frame deve essere motivato dalla percezione della scena, non dalla dimensione totale del video.

La sequenza deve avere un inizio e una fine leggibili. Con frame statici associa il progresso normalizzato `0..1` all'indice del frame; per una scena senza movimento significativo preferisci meno frame e una transizione più lunga. Con scrub associa il progresso alla posizione temporale ma conserva sempre un poster e una versione statica per rete lenta, mobile e movimento ridotto.

## Contratto per la pagina

`scroll-spec.md` descrive almeno:

```yaml
mode: frames
source_manifest: frame-manifest.json
progress_mapping: normalized-0-to-1
poster: frames/frame-00000.webp
preload: first-frame-plus-nearby-chunk
lazy_loading: true
mobile_variant: <file o regola dichiarata>
reduced_motion: poster-or-tap-to-advance
semantic_fallback: <testo, immagini o video controllabile>
captions: <testo o none motivato>
alt_strategy: <descrizione del significato, non della tecnica>
status: ready_for_review
```

Il codice che consuma il manifest non deve assumere che ogni frame sia già in memoria: deve caricare per chunk, prevedere un errore di rete e non bloccare il testo o la CTA. `prefers-reduced-motion` non può essere un dettaglio cosmetico: deve offrire poster, avanzamento discreto o contenuto equivalente. Un frame con volto, targa, indirizzo o musica riconoscibile conserva il relativo esito privacy/diritti nel review file.

## Gate finale

Il pacchetto è `ready_for_implementation` solo quando il manifest passa la validazione, il budget è compatibile con il target, il journey è specifico del cliente e la licenza copre l'ambito dichiarato. `ready_for_review` indica che manca ancora un verdetto umano. `blocked` indica il motivo concreto e il reviewer a cui è stato inviato. `published` non è uno stato di questo workflow.
