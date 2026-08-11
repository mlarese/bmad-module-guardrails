---
name: cinematic-library
description: "Sceglie transizioni curtain, aperture a tenda e regie per gallery in base alla storia della pagina, allo scroll e alla prova che ogni scena deve rendere leggibile."
code: CM
added: 2026-08-10
type: internal-capability
---

# Libreria cinematica per pagine e gallery

Questa rotta amplia la regia di Marea senza trasformarla in una libreria di effetti da applicare
ovunque. Il consumatore è il team che deve costruire la pagina: riceve pattern nominati, motivazione
narrativa, mappatura allo scroll, fallback e gate abbastanza chiari da poterli implementare e
verificare con `grl-web`.

Un effetto è riuscito quando rende visibile un passaggio della storia: apre un luogo, accompagna un
ingresso, separa due momenti, porta una prova in primo piano o fa percepire il cambio di stato. Se
serve soltanto a rendere la pagina più “cinematica”, è decorazione e va scartato o marcato come
ipotesi.

Un'idea-madre del committente può guidare la scelta del pattern, ma resta una direzione privata:
curtain, doppia tenda e gallery devono farne percepire ritmo, soglia o trasformazione senza
nominarla nel contenuto pubblico. I nomi dei pattern sono strumenti per il brief e per il handoff a
`grl-web`, non copy da mostrare al visitatore.

## Curtain dai bordi

I pattern `curtain-*` usano una superficie di copertura — colore, texture, immagine o pannello —
che entra dal bordo, mantiene leggibile il contesto necessario e poi rivela la scena sottostante.
La superficie non deve diventare un contenuto obbligatorio: il messaggio, la prova e la CTA devono
esistere anche nello stato senza movimento.

| Pattern | Movimento | Funzione narrativa adatta |
| --- | --- | --- |
| `curtain-right` | Un pannello entra da destra e scorre via o si apre verso destra | Far entrare il visitatore nel mondo del business o passare dalla promessa alla prova |
| `curtain-left` | Un pannello entra da sinistra e scorre via o si apre verso sinistra | Riportare una traccia del percorso, un contesto precedente o una scena già incontrata |
| `curtain-top` | Una superficie scende dall'alto e libera il contenuto | Svelare un luogo, un titolo o un punto di vista che prima era fuori campo |
| `curtain-bottom` | Una superficie sale dal basso e libera il contenuto | Portare in primo piano un gesto, un prodotto, una prova o una CTA |
| `curtain-split-vertical` | Due ante si incontrano al centro e si aprono verso destra e sinistra | Aprire le “tende” su una scena principale, un luogo o una trasformazione |
| `curtain-split-horizontal` | Due ante si incontrano al centro e si aprono verso alto e basso | Separare prima/dopo, dettaglio/contesto o due stati della stessa storia |

Destra e sinistra non sono varianti casuali: il lato scelto deve seguire la direzione del viaggio,
del gesto o della composizione. Alto e basso devono rispettare il fuoco e lo spazio del contenuto.
Le ante possono aprirsi all'ingresso, richiudersi per segnare un cambio di capitolo o restare come
cornice; non moltiplicare entrata e uscita se una sola trasformazione basta.

## Regie per gallery

Una gallery non è una fila di immagini decorative. È una sequenza di prove, dettagli o punti di vista
che deve avere ordine, soggetto prioritario e un criterio di avanzamento. Scegli il pattern in base a
ciò che la sequenza deve far capire:

| Pattern | Regia | Quando usarlo |
| --- | --- | --- |
| `gallery-curtain` | Ogni cambio di immagine avviene dietro una tenda laterale o una doppia apertura breve | Quando ogni immagine è un nuovo capitolo e il passaggio deve essere percepito |
| `gallery-track` | Le immagini scorrono su una rotaia orizzontale o verticale legata al progresso dello scroll | Quando la relazione fra luoghi, passaggi o varianti è più importante del singolo dettaglio |
| `gallery-mosaic-reveal` | Tessere o colonne rivelano una composizione e poi portano un elemento in primo piano | Quando più prove compongono un luogo, un processo o una trasformazione |
| `gallery-focus` | Un'immagine principale resta leggibile mentre le successive entrano come variazioni o dettagli | Quando serve una prova dominante con approfondimenti secondari |
| `gallery-stagger` | Gli elementi compaiono in sequenza breve e controllata, con un ordine già comprensibile senza animazione | Quando il ritmo dei gesti o dei passaggi è parte della storia |
| `gallery-before-after` | Due stati della stessa prova si separano con una tenda o un divisore controllato | Solo quando i due stati sono comparabili e la fonte della prova è chiara |

Per ogni gallery dichiara: numero e ordine degli elementi, immagine o prova focale, criterio di
selezione, direzione di scorrimento, indicatore di avanzamento, input previsto, testo alternativo,
focal point, sorgente e diritti. Non nascondere l'unica informazione importante dentro un gesto di
scroll o in un cambio automatico che l'utente non può riprendere.

## Scheda del pattern

Ogni transizione o gallery entra nel `cinematic-plan.md` con una scheda compatta:

```text
pattern_id: curtain-right | curtain-left | curtain-top | curtain-bottom |
            curtain-split-vertical | curtain-split-horizontal |
            gallery-curtain | gallery-track | gallery-mosaic-reveal |
            gallery-focus | gallery-stagger | gallery-before-after
story_function:
source_scene:
target_scene:
trigger: section-entry | scroll-range | item-change | explicit-action
cover_or_layer:
direction:
camera_in:
hold:
reveal_or_change:
camera_out:
scroll_mapping:
desktop:
mobile:
reduced_motion:
static_fallback:
motion_budget:
performance_gate:
asset_and_rights_gate:
owner:
status: draft | ready_for_review | blocked
```

Per una gallery aggiungi `item_order`, `focal_item`, `progress_model`, `keyboard_and_touch_model`,
`alt_text_strategy` e `empty_or_failed_asset_fallback`. Per una tenda aggiungi quale contenuto sta
sopra e sotto la copertura, cosa resta leggibile durante l'apertura e quale stato si vede se il
movimento è disabilitato.

## Scroll, movimento e accessibilità

Mappa l'effetto su un intervallo qualitativo dello scroll e non su coordinate inventate. Il gesto
può avere ingresso, apertura, permanenza e uscita, ma la CTA e la prova devono avere un punto di
lettura stabile. Un pattern può essere attivato dall'ingresso della sezione, da una porzione dello
scroll, dal cambio di elemento della gallery o da un'azione esplicita: dichiara quale.

La versione `prefers-reduced-motion` mostra subito lo stato rivelato o una transizione minima,
mantiene ordine, testo, alt text, controlli e CTA e non richiede di “capire” l'animazione. Touch,
tastiera e puntatore devono avere un comportamento riprendibile; una gallery non deve dipendere da
un hover né intrappolare lo scroll verticale.

Il fallback statico può essere un'immagine composta, una griglia ordinata, il primo elemento focale
con gli altri disponibili in modo lineare o una scena già rivelata. Registra peso cumulativo,
numero di asset, lazy loading, dimensioni, cache e soglia di qualità nel gate per `grl-web`; Marea
non dichiara superati i vincoli runtime senza evidenza.

## Handoff

Marea consegna la grammatica e il motivo per cui il pattern esiste. `grl-web` decide la tecnica di
implementazione e verifica comportamento, performance e compatibilità; Iris verifica identità e
composizione, Sally l'interazione, Nils l'accessibilità, Aldo diritti e Vera dati personali.

Stato `ready_for_review` richiede una funzione narrativa, una sorgente o un blocco esplicito per
ogni asset, una versione senza movimento, un comportamento mobile e un owner. La presenza di
`curtain-*` o di una gallery non autorizza HTML, CSS, JavaScript, caricamento o pubblicazione.
