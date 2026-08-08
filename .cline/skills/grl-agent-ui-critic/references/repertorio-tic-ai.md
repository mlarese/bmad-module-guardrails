# Repertorio dei tic dell'estetica generata

L'occhio addestrato di Iris, scritto. È un **strumento di riconoscimento**, non una lista da recitare:
serve a dare un nome preciso a «questa l'ho già vista mille volte» e a proporre subito la deviazione.

I codici (T01, T02…) servono solo qui dentro, per riferimento incrociato. **Non compaiono mai in
output**: all'utente si parla del suo hero, della sua card, del suo `#8b5cf6`.

---

## Perché succede

Un modello che genera una pagina produce la **mediana del suo addestramento**. La mediana delle
landing page sul web è: Tailwind UI, i template più venduti sui marketplace, e i cloni delle cinque
o sei aziende che tutti copiano. Non è cattivo gusto — è statistica.

Due conseguenze operative:

- **Si devia dove la mediana è più spessa.** Font, palette, raggio dei bordi, ritmo verticale: lì
  ogni pagina generata converge, e lì la deviazione si vede subito.
- **Non si devia da tutto.** Una pagina che contraddice ogni convenzione è illeggibile, non
  originale. Tre-quattro deviazioni forti battono trenta deviazioni tiepide.

## Tic o convenzione utile?

La distinzione che tiene Iris lontana dal contrarianismo. Prima di segnalare, si passa questo filtro:

| Domanda | Se sì |
| --- | --- |
| Serve a farsi leggere in fretta da un utente che ha già visto quel pattern altrove? | **convenzione** — si tiene (pricing a colonne confrontabili, nav in alto, footer di servizio, campo email prima del bottone) |
| Sparisce senza che nessuno se ne accorga tranne il designer? | **tic** — si toglie |
| È lì perché era il default del kit e nessuno l'ha guardato? | **tic**, sempre |
| Rende quella pagina riconoscibile fra mille? | non è né l'uno né l'altro: è **identità**, si difende |

Il pricing a tre colonne è una convenzione. Il pricing a tre colonne **con quella centrale scalata
del 5% e il badge "Most popular" in gradiente** è un tic.

## Costo della deviazione

Ogni proposta si presenta con il suo costo, e si parte dalle gratuite. Ordine di attacco:

| Costo | Leve | Effetto |
| --- | --- | --- |
| **Zero** (cambio di valore) | famiglia tipografica, pesi, scala, palette, raggio, ritmo verticale, colore di sfondo | altissimo — è qui che si gioca il 70% dell'anonimato |
| **Basso** (mezza giornata) | un layout asimmetrico, densità differenziata, un trattamento immagine, un dettaglio ricorrente proprio | alto |
| **Medio** (giorni) | illustrazione o fotografia su misura, componente interattivo proprio, tipografia a pagamento | alto, ma non prima dei precedenti |
| **Alto** (settimane) | sistema visivo completo, motion design proprio, 3D | da proporre solo se il progetto lo giustifica |

Una critica che parte dal costo alto e ignora quello zero è mal tarata.

---

## A · Layout e struttura di pagina

| # | Segno concreto | Origine | Deviazione concreta |
| --- | --- | --- | --- |
| T01 | Hero centrato: eyebrow + H1 su due righe + sottotitolo grigio + due bottoni (pieno / ghost), tutto in `max-w-3xl mx-auto text-center` | il pattern più rappresentato in assoluto nei dataset di landing | allineamento a sinistra su griglia a due terzi, con lo spazio a destra occupato da una cosa sola e grande; oppure H1 a tutta larghezza con il resto rientrato di una colonna |
| T02 | Fascia "trusted by" subito sotto l'hero: 5-6 loghi grigi al 40% di opacità | i template la mettono sempre, anche quando i clienti sono due | se i clienti veri sono pochi: un nome solo, scritto per esteso e grande, con una riga di cosa ha fatto. Se non ce ne sono, si toglie |
| T03 | Tre card affiancate con icona in alto, titolo, due righe. **Sempre tre** | la griglia a 3 colonne è il default di ogni sistema | quattro voci in due righe asimmetriche, o una lista verticale con numeri grandi, o una card sola grande più due piccole |
| T04 | Sezioni alternate bianco / `#f9fafb` fino in fondo | il modo più economico di separare senza pensarci | separatori diversi per natura diversa: una sezione in colore pieno, una con una regola sottile, due unite senza stacco |
| T05 | Ogni sezione ha lo stesso incipit: eyebrow maiuscoletto colorato + H2 centrato + sottotitolo + griglia | struttura da template, replicata a ogni blocco | solo la prima sezione ha il titolo centrato; le altre entrano direttamente nel contenuto, o hanno il titolo laterale sticky |
| T06 | Feature rows a zig-zag: testo sinistra / immagine destra, invertito, ripetuto tre volte | pattern da presentazione prodotto | rompere alla seconda: una feature a tutta larghezza, una in griglia densa, una sola riga di testo |
| T07 | `max-w-7xl mx-auto px-4` su tutto — nessun elemento tocca mai il bordo | il container di default | almeno un elemento a sanguinare fino al bordo (immagine, banda di colore, tabella orizzontale) |
| T08 | Padding verticale identico per ogni sezione (`py-20` / `py-24`) | la scala di spaziatura applicata uniformemente | ritmo variabile: sezioni compresse e sezioni ariose, con lo stacco più grande dove cambia l'argomento |
| T09 | CTA finale: banda a tutta larghezza in gradiente, titolo bianco centrato, bottone bianco | il blocco di chiusura di ogni template | chiusura sobria e breve, o CTA che riprende un elemento specifico della pagina invece di un blocco autonomo |
| T10 | Footer a 4 colonne (Product / Company / Resources / Legal), logo a sinistra, spesso con link morti | wireframe di default | footer proporzionato al sito reale: se le pagine sono cinque, si elencano cinque link su una riga |
| T11 | Stats row: 4 numeri grandi con etichetta sotto (`10k+`, `99.9%`, `24/7`, `4.9★`) | numeri inventati che riempiono uno spazio | un numero solo, vero, verificabile, con la fonte. Oppure niente |
| T12 | Griglia sempre simmetrica: 3 o 4 colonne uguali, mai una asimmetria | il default della griglia | griglia 2/3 + 1/3, o colonne di larghezza diversa in base al peso del contenuto |
| T13 | Nav sticky con `backdrop-blur`, logo a sinistra, 4 voci al centro, bottone accento a destra | il pattern di ogni header generato | nav non sticky, o allineata tutta a sinistra, o senza bottone (se la CTA vera è nell'hero) |
| T14 | Nessuna zona compatta: tutto respira nello stesso modo, dall'hero al footer | spaziature applicate come costante e non come strumento | almeno un blocco deliberatamente denso (una tabella, una lista fitta, una specifica tecnica) che faccia da contrasto |
| T15 | Bento grid: rettangoli di dimensioni diverse in una griglia arrotondata | nato come fuga dalla griglia a 3, diventato esso stesso il default 2024-2026 | se serve mostrare cose eterogenee, una pagina in scorrimento con blocchi a piena larghezza dice la stessa cosa senza l'etichetta "bento" |
| T16 | La pagina è una sequenza di blocchi intercambiabili: si può riordinare senza che cambi nulla | assenza di un argomento | un ordine che è una tesi: la seconda sezione deve esistere *perché* c'è stata la prima |

## B · Tipografia

| # | Segno concreto | Origine | Deviazione concreta |
| --- | --- | --- | --- |
| T17 | Inter. In alternativa Geist, Manrope, Plus Jakarta Sans, Poppins, DM Sans | i grotteschi neutri che ogni starter kit installa | grotteschi con un carattere: Söhne, Suisse Int'l, ABC Diatype, Neue Haas. Gratuiti con personalità: Instrument Sans, Bricolage Grotesque, Public Sans, Space Grotesk. Oppure la scelta che nessuno fa: un serif per i titoli (Instrument Serif, Newsreader, Fraunces) |
| T18 | Titoli a peso 600, corpo a 400. Mai un 300, mai un 800, mai un corsivo | il default `font-semibold` | contrasto di peso vero: 300 grande contro 700 piccolo. O un solo peso in tutta la pagina, con la gerarchia fatta solo dalla dimensione |
| T19 | `tracking-tight` su ogni titolo | un tic copiato dai siti che lo usano per la loro tipografia specifica | crenatura decisa in base al font reale: molti display vogliono `tracking` normale o aperto |
| T20 | Scala timida: H1 48-60px, H2 36px, corpo 16px, rapporto ~1.25 | la scala di default di ogni sistema | un salto vero: H1 a 96-120px e corpo a 16px, e niente in mezzo. La gerarchia si vede a occhi socchiusi o non esiste |
| T21 | Una parola del titolo in gradiente o in colore accento («Build **faster**») | il modo più veloce di far sembrare un titolo progettato | se serve enfasi: cambio di famiglia (una parola in corsivo serif), o dimensione, o una linea sotto. Il gradiente sul testo è la firma più riconoscibile di tutte |
| T22 | Corpo in grigio `#6b7280` invece che nero | «il grigio sembra più elegante» | nero pieno o quasi (`#111`), grigio riservato ai soli metadati. Il testo grigio su bianco è anche il primo problema di contrasto |
| T23 | Un solo font per tutto, nessun accoppiamento | il modello non rischia | due famiglie con un contrasto netto (serif/grottesco, o grottesco/mono). Il mono per numeri, codice, etichette è una firma a costo zero |
| T24 | Interlinea uniforme 1.5-1.6 anche sui titoli grandi | valore unico applicato a tutto | titoli grandi a 0.95-1.1, corpo a 1.5-1.7 |
| T25 | Nessuna cifra tabellare nelle tabelle e nei prezzi, nessun maiuscoletto vero, nessun numero oldstyle | funzionalità OpenType mai attivate | `font-variant-numeric: tabular-nums` su prezzi e dati, `small-caps` reale al posto di `text-transform: uppercase` |
| T26 | Paragrafi lunghi centrati | centratura ereditata dall'hero | testo lungo allineato a sinistra, misura 60-75 caratteri |
| T27 | Nessun testo mai più grande di quanto serva né più piccolo: tutto in una fascia 14-60px | assenza di rischio tipografico | una cosa sola enorme in tutta la pagina, e le note davvero piccole (12px) dove il contesto lo permette |

## C · Colore

| # | Segno concreto | Origine | Deviazione concreta |
| --- | --- | --- | --- |
| T28 | Blu → viola (`#3b82f6` → `#8b5cf6`), o indaco → fucsia | la palette più rappresentata nelle landing tech dal 2020 | un accento solo e sporco: ruggine, verde oliva, ocra, bordeaux, ciano acido. Se il blu è obbligato per il brand, si desatura e si cambia la temperatura del neutro |
| T29 | Gradiente a 135° su hero, bottone e testo del titolo | il gradiente come sostituto della decisione cromatica | tinte piatte. Se un gradiente serve davvero: due toni della stessa famiglia, molto ravvicinati, su un'area sola |
| T30 | Grigi presi tali e quali dalla scala `gray`/`slate`/`zinc` | il default del kit | neutri con una tinta propria: grigio caldo verso il beige, o freddo verso il verde. Basta ruotare la tonalità di 8-12° per uscire dall'anonimato |
| T31 | Un solo accento usato per bottone, link, icone, eyebrow e badge — tutto dello stesso colore | il token `primary` applicato ovunque | l'accento riservato a **una** funzione (l'azione). Tutto il resto in neutro. Un accento che compare due volte in una pagina pesa più di uno che compare venti |
| T32 | Nessun colore «sbagliato»: mai un ocra, un ruggine, un verde oliva, un rosa polveroso | i modelli evitano il rischio cromatico | un colore che a prima vista sembra un errore e a guardarlo bene è la cosa che si ricorda |
| T33 | Verde=successo, rosso=errore, ambra=warning, nelle tinte di default | semantica mai ripensata | mantenere la semantica, cambiare le tinte: un verde più cupo, un rosso più caldo, coerenti con la palette invece che importati |
| T34 | Sfondo `#ffffff` puro | il default | carta calda (`#faf8f5`), o grigio molto chiaro con tinta, o fondo scuro se il contenuto lo regge |
| T35 | Mesh gradient / aurora blur sfocato dietro l'hero | l'effetto «prodotto AI» del 2023-2026 | fondo pieno. Se serve profondità: una texture leggera, una foto molto sgranata, o una singola forma geometrica netta |
| T36 | Saturazione media uniforme: niente di quasi-neutro, niente di violentemente saturo | la mediana | quasi tutta la pagina in neutri, con un unico punto ad alta saturazione |

## D · Superfici, bordi, ombre, raggi

| # | Segno concreto | Origine | Deviazione concreta |
| --- | --- | --- | --- |
| T37 | `border-radius: 12px` (o 8, o 16) su tutto: card, bottoni, input, immagini, avatar | un token applicato a ogni superficie | spigolo vivo ovunque (durissimo, molto riconoscibile), oppure raggio differenziato per gerarchia: contenitori squadrati, controlli molto arrotondati (pillola). Il raggio uniforme è il segno più diffuso e il più economico da togliere |
| T38 | Bordo `1px solid #e5e7eb` su ogni superficie | il modo di default di dire «questa è una cosa» | separare per contrasto di sfondo o per spazio. Se il bordo serve, che sia visibile: 2px scuro, o una regola a tutta larghezza invece di un contorno |
| T39 | Ombra grande e morbida (`shadow-lg`/`shadow-xl`) su card che non si sollevano da niente | l'ombra come decorazione, non come piano | nessuna ombra; l'elevazione riservata a ciò che è davvero sopra (menu, modale, toast) |
| T40 | Glassmorphism: `backdrop-blur` + bianco al 60% su elementi che non hanno nulla sotto | l'effetto vetro applicato senza il presupposto | vetro solo dove qualcosa scorre sotto, quindi quasi mai. Altrimenti superficie piena |
| T41 | Card ovunque: ogni contenuto è dentro un rettangolo, anche quando non serve | il contenitore come riflesso | contenuto sul fondo di pagina, separato solo da spazio e tipografia. Meno scatole, più ritmo |
| T42 | Bottone primario con ombra colorata (`shadow-blue-500/25`) | dettaglio da template | nessuna ombra colorata; il bottone si distingue per forma, peso e posizione |
| T43 | Hover uguale su tutto: `-translate-y-1` + ombra maggiore | un'unica micro-interazione replicata | hover che comunica qualcosa di specifico (cambio di colore del bordo, comparsa di un dettaglio, spostamento di un solo elemento interno). O nessun hover sulle card non cliccabili |
| T44 | Badge/pill con sfondo tenue e testo accento (`bg-blue-50 text-blue-700`) per ogni etichetta | il componente Badge di default | etichette tipografiche: maiuscoletto piccolo, o mono, senza contenitore |
| T45 | Nessuno spigolo vivo, nessuna regola piena, nessuna linea spessa in tutta la pagina | morbidezza uniforme | una linea spessa (4-8px) usata una volta come elemento strutturale |
| T46 | Focus ring identico ovunque: anello accento 2px con offset 2px | default di shadcn/Tailwind | anello coerente con il sistema visivo (colore proprio, spessore proprio) — resta obbligatorio che sia **visibile**, cambia solo che sia riconoscibile |

## E · Icone, illustrazioni, immagini

| # | Segno concreto | Origine | Deviazione concreta |
| --- | --- | --- | --- |
| T47 | Lucide/Heroicons stroke 2px, una per card. Sparkles=AI, Zap=veloce, Shield=sicuro, Rocket=lancio, Users=team, BarChart=analytics | la mappatura concetto→icona più ovvia possibile | niente icone: numeri grandi, o iniziali, o una singola immagine per sezione. Se le icone servono, che siano tutte insolite (pittogrammi propri, o una famiglia con carattere: Phosphor duotone, Iconoir, Radix) |
| T48 | Icona dentro un quadrato colorato tenue arrotondato (`bg-blue-50 rounded-lg p-3`) | il pattern «feature card» | icona nuda alla dimensione del testo, o molto grande e monocroma sullo sfondo |
| T49 | Emoji al posto delle icone (🚀 ⚡ ✨ 🎯 🔒 💡) | ripiego quando manca la libreria | mai emoji come icone di sistema. Rendono la pagina istantaneamente riconoscibile come generata |
| T50 | Illustrazioni isometriche o piatte con persone senza volto, arti lunghi, colori pastello (Corporate Memphis / Alegria) | l'illustrazione stock più diffusa 2018-2023 | fotografia reale (anche imperfetta), diagrammi tecnici veri, screenshot ritagliati stretti, o disegno a tratto con una mano riconoscibile |
| T51 | Blob SVG organici colorati dietro il contenuto | riempitivo decorativo | nessun riempitivo. Se lo spazio sembra vuoto, il problema è il ritmo, non la mancanza di forme |
| T52 | Screenshot del prodotto in un finto browser con tre pallini, ruotato di 3° in prospettiva | il mockup di default | screenshot a schermo intero senza cornice, tagliato sul dettaglio che conta, o ingrandito su un solo elemento dell'interfaccia |
| T53 | Foto stock: ufficio luminoso, mani su laptop, team che ride, grattacieli | banca immagini generica | nessuna foto è meglio di una foto stock. In alternativa: foto vere del prodotto, del luogo, delle persone reali |
| T54 | Avatar delle testimonianze da `pravatar`/`randomuser`, o volti generati | segnaposto mai sostituiti | testimonianze senza volto: nome, ruolo, azienda in tipografia. Se il volto non è vero, non ci va |
| T55 | Loghi «trusted by» inventati o segnaposto mai sostituiti | riempimento del blocco | vedi T02. Un logo finto è anche un problema legale, non solo estetico |
| T56 | Immagini tutte trattate allo stesso modo: stesso raggio, stessa ombra, stesso ritaglio | trattamento come costante | un trattamento riconoscibile e coerente: duotone, bianco e nero con un solo elemento a colori, grana, ritaglio fuori griglia |
| T57 | Pattern a puntini o griglia tenue di sfondo | decorazione di default | niente, o un pattern che significhi qualcosa nel dominio del prodotto |

## F · Movimento

| # | Segno concreto | Origine | Deviazione concreta |
| --- | --- | --- | --- |
| T58 | Fade-in + slide-up di 20px allo scroll, stagger 100ms, su ogni sezione | l'animazione d'ingresso di default | animare **una** cosa in tutta la pagina, quella che conta. Il resto compare e basta |
| T59 | `ease-out 300ms` su ogni transizione, sempre la stessa curva | il default | curve distinte per natura del movimento; uno spring dove c'è manipolazione diretta; durate diverse per entrata e uscita |
| T60 | Numeri che contano fino al valore quando entrano in viewport | effetto da template | il numero c'è e si legge. Se il numero non è interessante fermo, non lo è nemmeno in movimento |
| T61 | Testo che si digita da solo alternando tre parole | «Build faster / smarter / better» | una frase sola, ferma, scelta bene |
| T62 | Gradiente di sfondo che ruota lentamente | animazione decorativa infinita | fondo fermo |
| T63 | Nessun movimento che dica qualcosa di specifico su questo prodotto | il moto come guarnizione | un'animazione sola che mostri il meccanismo del prodotto: cosa entra, cosa esce |

## G · Testo e microcopy (come suona la pagina)

Confine: il **contenuto** e il tono di voce del prodotto non sono di Iris. Qui si guardano solo gli
schemi verbali che rendono la pagina riconoscibile come generata, allo stesso titolo del gradiente.

| # | Segno concreto | Origine | Deviazione concreta |
| --- | --- | --- | --- |
| T64 | H1 a formula: imperativo + oggetto + promessa («Ship faster with AI-powered X» / «Crea di più, in meno tempo») | la struttura di titolo più frequente | dire cosa fa il prodotto in modo letterale e specifico, con un sostantivo concreto del dominio |
| T65 | Triplette retoriche («Veloce, semplice, sicuro») | ritmo da slogan generato | due cose, o una. La tripletta è il ritmo che tradisce l'origine |
| T66 | Trattini em usati come punteggiatura generale, spesso mal spaziati in italiano | tic di scrittura del modello | punto, virgola, due punti. Il trattino em resta per gli incisi veri, non come pausa universale |
| T67 | «Non è solo X — è Y», «X, ripensato», «X, ma per Y» | costruzioni antitetiche da copy generato | frase affermativa senza contrasto costruito |
| T68 | Il sottotitolo ripete l'H1 con altre parole | riempimento di uno slot | il sottotitolo aggiunge l'informazione che l'H1 non poteva contenere, oppure sparisce |
| T69 | CTA «Inizia gratis» / «Get started free» con sotto «Nessuna carta di credito richiesta» | coppia da template | verbo dell'azione reale: «Prova su un tuo file», «Guarda una demo di 2 minuti» |
| T70 | Nomi di feature in Title Case e vaghi: Smart Insights, Seamless Workflow, Powerful Analytics | etichettatura generica | il nome che il prodotto usa davvero, o nessun nome: la descrizione basta |
| T71 | Eyebrow maiuscoletto sopra ogni titolo: FEATURES, HOW IT WORKS, PRICING | la struttura del template esplicitata all'utente | via. Se il lettore ha bisogno di sapere che sta guardando le funzionalità, il problema è il titolo |
| T72 | Testimonianze tutte con la stessa struttura: problema, prodotto, risultato numerico, tre righe | forma di default | citazioni di lunghezza diversa, una lunga e specifica invece di tre corte e simmetriche |

## H · Componenti ricorrenti

| # | Segno concreto | Origine | Deviazione concreta |
| --- | --- | --- | --- |
| T73 | Pricing a 3 colonne, quella centrale scalata e bordata in accento, badge «Most popular» | il blocco pricing di ogni template | le colonne restano (è convenzione), sparisce la messa in scena: stessa dimensione, differenza segnata dalla tipografia o da una nota |
| T74 | Toggle mensile/annuale con badge «Risparmia il 20%» | idem | se c'è un solo piano che ha senso, si mostra quello e si spiega il resto a parole |
| T75 | «Come funziona» in 3 step numerati con linea tratteggiata fra i cerchi | schema di processo di default | i passi reali, che raramente sono tre, mostrati con lo stato dell'interfaccia a ogni passo |
| T76 | FAQ ad accordion con 5-6 domande e chevron che ruota | riempitivo di fine pagina | domande vere, aperte, leggibili senza click. Un accordion nasconde ciò che dovrebbe convincere |
| T77 | Box newsletter in fondo: input + bottone + «Niente spam, disiscriviti quando vuoi» | blocco standard | se la newsletter non esiste davvero, si toglie |
| T78 | Toast in alto a destra, modale centrata con overlay nero al 50%, sheet da destra | i default della libreria di componenti | posizione e forma coerenti con dove sta l'attenzione: inline dove è successa la cosa |
| T79 | Tabella comparativa con spunte verdi e croci rosse contro concorrenti anonimi | blocco competitor da template | confronto onesto e specifico, o niente |

## I · Modalità scura

| # | Segno concreto | Origine | Deviazione concreta |
| --- | --- | --- | --- |
| T80 | Dark mode = viola scuro (`#0f0a1f`) con accento fucsia e alone luminoso | l'estetica «AI / cyber» 2023-2026 | scuro neutro o caldo (`#111`, `#1a1815`), accento sobrio |
| T81 | Inversione meccanica: `#111827` di fondo, `#e5e7eb` di testo, ombre rimaste identiche | il tema scuro derivato per calcolo | tema scuro ridisegnato: le ombre non funzionano, l'elevazione si fa con la luminosità della superficie; i colori accento vanno rischiarati per reggere il contrasto |
| T82 | Bordi bianchi al 10% su ogni superficie | il sostituto del bordo grigio | superfici distinte per livello di grigio, non per contorno |
| T83 | Alone (`glow`) al posto dell'ombra su tutto | decorazione | alone solo su ciò che emette luce nella finzione della pagina (uno stato attivo), altrimenti niente |

## J · Kit non digerito

Il segnale più chiaro di tutti: **il template si riconosce prima del prodotto**.

| # | Segno concreto | Origine | Deviazione concreta |
| --- | --- | --- | --- |
| T84 | shadcn/ui intatto: `zinc`/`neutral`, `--radius: 0.5rem`, bottoni `h-10 px-4`, `CardHeader/CardTitle/CardDescription` mai toccati | ottimo punto di partenza, pessimo punto di arrivo | i token si cambiano in un file: raggio, neutri, altezza dei controlli, tipografia. È mezz'ora di lavoro e cambia tutto |
| T85 | Solo classi Tailwind di default, nessun token di tema proprio | nessuna configurazione | definire nel tema: due-tre colori propri, una scala tipografica propria, una scala di spaziatura propria. Poi usare solo quelli |
| T86 | Bootstrap 5 o Material Design riconoscibili al primo sguardo, senza una sola personalizzazione | framework installato e usato così com'è | come sopra: variabili di tema, non `!important` sparsi |
| T87 | `container mx-auto` come unico sistema di layout in tutta la pagina | assenza di sistema | una griglia dichiarata (colonne, gutter, punti di rottura) usata anche per rompere la simmetria |
| T88 | Tutti i componenti provengono dallo stesso kit e nessuno è stato modificato | costruzione per assemblaggio | scegliere **un** componente ad alta visibilità (il bottone primario, la card principale, l'input) e ridisegnarlo davvero. Un solo elemento proprio ricalibra la percezione dell'intera pagina |

---

## Le famiglie riconoscibili

I tic arrivano in gruppo. Nominare la famiglia è più utile che elencare i pezzi, perché dice
all'utente **da dove viene** la sua pagina — che è la domanda «dove l'ho già vista?» con una risposta.

| Famiglia | Combinazione tipica | Cosa la rompe per prima |
| --- | --- | --- |
| **SaaS Tailwind** (2020-2024) | T01+T03+T04+T09+T10+T17+T28+T37 | palette e tipografia insieme, in un pomeriggio |
| **Clone Linear/Vercel** (2023-2026) | fondo quasi nero, grigi freddi, T82, T80, Inter `tracking-tight`, T35, T52 | il neutro caldo e una tipografia non-grottesca |
| **Stripe-like** | gradiente fluido multicolore diagonale, sezioni chiare, illustrazione a linee, accoppiamento serif+sans | togliere il gradiente: sotto resta un impianto solido |
| **Corporate Memphis** | T50+T51 con pastelli e blob | sostituire l'immagine, non il layout |
| **shadcn crudo** | T84+T85+T37+T46, `zinc` ovunque | i token del tema |
| **AI-native** (2025-2026) | nero + un accento acido, Sparkles ovunque, T80, finta barra di prompt nell'hero, T61, badge «Powered by …» | togliere Sparkles e la barra di prompt finta: sono la firma |
| **Notion-like soft** | bianco caldo, T49, tipografia media, molta aria, disegni a matita | le emoji-icona e il contrasto tipografico |

## Come si usa questo repertorio in una diagnosi

- Si nominano **3-5 tic**, non trenta. Quelli che, tolti, cambiano davvero la faccia della pagina.
- Ognuno con l'elemento concreto («il tuo H1 in gradiente blu-viola»), non con il codice né con il
  nome della categoria.
- Ognuno con la deviazione, il costo e cosa si guadagna.
- Se la pagina appartiene a una famiglia riconoscibile, si dice quale: è l'informazione più utile
  che l'utente riceve.
- Ciò che nella pagina **funziona** si dice: una pagina in cui tutto è sbagliato non è credibile, e
  l'utente smette di ascoltare.
- Quando la pagina non ha nessuno di questi problemi, il verdetto è che non ne ha. Detto con la
  stessa sicurezza di una stroncatura.
