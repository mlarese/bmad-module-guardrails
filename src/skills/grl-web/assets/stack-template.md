# Stack e convenzioni — {nome del sito}

Compilato da `grl-web`, corretto dall'utente. `bmad-spec` lo adotta come companion e non lo riscrive: qui sta il **come**, che nel kernel della spec non può stare.

Questo file viene letto **fuori** da `grl-web`, da chi implementa le fette: ogni cosa fra graffe va sostituita con il valore concreto quando il file si scrive, percorsi e nomi di figure compresi.

## Lo stack

**Scelto:** {Astro, o l'alternativa scelta}

**Perché:** {le ragioni concrete su questo progetto, non le virtù generiche dello strumento}

Astro è il default della rotta: manda zero JavaScript quando non serve, ha le transizioni fra pagine integrate, e regge i contenuti sia da file sia da un CMS senza cambiare impianto. Se la scelta è caduta altrove, la ragione va scritta qui sopra.

**Contenuti:** {file dentro il progetto / CMS / database} — deriva dalla colonna «chi la cambia» della scheda del sito.

**Messa online:** {hosting, dominio} — la decide `grl-agent-ops`, non questa scheda.

## Come si sviluppa

**A fette verticali.** Ogni fetta è una pagina o una sezione che funziona da cima a fondo, non uno strato orizzontale. «Prima tutti i layout, poi tutti i contenuti» non è una fetta: è un cantiere che non si vede mai.

**Prima il frontend.** Ogni sezione nasce con dati finti della forma dichiarata nella scheda. Il backend arriva dopo, nelle ultime fette, e non cambia la forma. La prima fetta deve **vedersi nel browser**: se non produce una pagina guardabile, va unita alla prima pagina vera.

## I principi, con la loro misura

Attrezzi, non dogmi. Su un sito di contenuti non pesano uguale:

| Principio | Quanto conta qui |
| --- | --- |
| **DRY** | È il cuore. Header, footer e hero sono un componente solo con parametri, e la direzione visiva della scheda si legge invece di riscegliere i valori |
| **Separazione delle responsabilità** | Contenuto, struttura e stile separati. In Astro è la divisione naturale fra contenuti, layout e componenti |
| **KISS** | Nessun CMS finché la scheda non dice «lo cambiano altri, spesso». Nessun database prima di allora |
| **SOLID** | Quasi tutto fuori scala. Interfacce e iniezione di dipendenze su un sito di sei pagine sono il difetto, non la virtù |

Se una fetta comincia a produrre strati di astrazione che nessuna pagina usa, è il segnale di fermarsi: quello è `grl-agent-architecture`.

## Vincoli che valgono su tutto

Valgono su ogni fetta, non solo sulla prima.

- **Nessuna pagina è finita finché qualcuno non l'ha guardata.** Quando una fetta produce una pagina visibile, la si passa a `grl-board` — **prima la pagina a freddo**, poi, per il confronto, la riga di quella pagina nella scheda del sito (chi ci arriva, cosa deve far fare, hero, sezioni) e il brief di conversione del lavoro. Su questa rotta non esiste un brief per pagina: la scheda lo sostituisce. Il verdetto torna nella colonna *Gate* della scheda prima che parta la fetta successiva. Senza `grl-board`, le figure del modulo Guardrails: {elenco risolto dei revisori, Iris `grl-agent-ui-critic` compresa}.
- **Il pavimento statico si verifica, non si guarda a occhio.** Deve esserci, su ogni pagina: `lang`, `<title>`, meta description, canonical, le tre meta Open Graph, `alt` sulle immagini, `width`/`height`, un'etichetta per ogni campo, un `<main>`; e per il sito, sitemap e robots. La verifica meccanica è `check_static_site.py` della skill `grl-web` (percorso: {percorso risolto}), che dice per ogni pagina cosa manca. Se dalla fetta non è raggiungibile, il pavimento si verifica leggendo — la lista qui sopra è il vincolo, lo script è solo la via rapida. Lo script constata presenze: se il titolo dica davvero cosa c'è nella pagina resta giudizio.
- **`prefers-reduced-motion`** rispettato ovunque ci sia movimento: c'è chi sta fisicamente male, ed è materia di `grl-agent-compliance`.
- **Livello di accessibilità obbligatorio:** {quello che dice `grl-agent-compliance`} — dipende da settore e mercato, non dalle buone intenzioni
- **Font e immagini:** serviti dal sito, mai da un dominio terzo; licenze verificate da `grl-agent-legal`
- **Librerie di animazione:** licenza verificata al momento dell'adozione, non a memoria

## Cosa non si fa

{Le scelte tecniche escluse e il perché: un framework scartato, un CMS che non si vuole, una libreria evitata. Serve a chi implementa una fetta fra tre settimane e non era nella stanza.}
