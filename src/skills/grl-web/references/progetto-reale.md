# Dal mockup al progetto

La rotta di `grl-web` quando un mockup approvato deve diventare un sito vero, che sta online e che si mantiene.

**Prima di tutto, leggi lo stato del gate.** Su una pagina singola sta nel `brief.md` del lavoro; su un sito i campi sono due — il gate di sito in `brief-sito.md` e quello di ogni pagina nel proprio `brief.md`. Se un campo dice `non ancora`, quella cosa non è mai stata guardata dalle figure: proponi il gate **per quel livello soltanto** — l'intero sito se manca il gate di sito, la singola pagina se manca il suo — e fallo prima di promuovere, con le meccaniche descritte in `references/mockup-html.md`: a `grl-board` vanno il percorso della pagina e quello del suo brief, la pagina si legge a freddo prima del brief, e senza `grl-board` si convoca `{workflow.finalize_reviewers}`. Non assumere che sia stato fatto perché l'utente lo dà per scontato: l'approvazione vive nel brief proprio perché la conversazione in cui è avvenuta può non esserci più.

## Lo stack

HTML statico più Tailwind, **senza toolchain npm**. Tailwind arriva dal suo CLI standalone: un binario singolo, nessun `node_modules`, nessun `package.json` da tenere aggiornato per anni.

Il progetto vive nella stessa cartella di lavoro del mockup, `{workflow.output_path}/{workflow.run_folder_pattern}/`:

```
{workflow.output_path}/{workflow.run_folder_pattern}/
├── brief.md             # resta: è lo stato del lavoro
├── tailwindcss          # il binario, scaricato una volta (non va in git)
├── src/input.css        # le direttive Tailwind più i propri stili
├── src/*.html           # le pagine
├── dist/site.css        # generato, mai modificato a mano
└── assets/              # immagini e font propri
```

**Se il lavoro è un sito**, i brief restano dove sono — `brief-sito.md` alla radice e il `brief.md` dentro la cartella di ogni pagina: sono lo stato del lavoro e non diventano artefatti del progetto. Si sposta solo l'HTML, dalle cartelle di pagina a `src/`, e le cartelle di pagina restano con il solo brief. Non lasciare l'`.html` anche al posto vecchio: due copie della stessa pagina, di cui una che nessuno ricompila, sono il modo più rapido per pubblicare quella sbagliata.

Il build è un comando solo: il binario legge il CSS di ingresso, scandisce l'HTML e scrive in `dist/` il CSS effettivamente usato, con una modalità di sorveglianza mentre si lavora. Prendi la forma esatta — nome del binario, flag, direttive del CSS di ingresso — dalla release corrente di Tailwind: le versioni maggiori hanno cambiato sia la configurazione sia le direttive, e un comando ricordato a memoria costa un giro inutile.

Il CDN di Tailwind resta escluso: è pensato per prototipare in una pagina, blocca il rendering e dipende da un terzo per una cosa che un file statico risolve.

**La conversione dal mockup** riscrive il `<style>` inline in classi Tailwind e sposta in `src/input.css` solo ciò che le utility non esprimono. I valori della direzione visiva — font, esadecimali, scala tipografica, raggi — diventano token nel tema, non numeri sparsi nel markup: è quello che permette di cambiare la palette in un punto solo.

## Cosa il mockup non aveva

Un file che si apriva col doppio click non doveva farsi trovare, non doveva raccogliere nulla e non doveva essere veloce. Ora sì: applica il pavimento standard di un sito statico — `lang`, titoli e meta description per pagina, canonical, Open Graph con un'immagine 1200×630 vera, sitemap e robots, immagini dimensionate e lazy sotto la piega, elementi semantici, `alt`, `label`, focus visibile — e verificalo con `uv run scripts/check_static_site.py src/`, che restituisce per ogni pagina cosa manca. Lo script constata presenze: se il `<title>` dica davvero cosa c'è in quella pagina, e se l'`alt` descriva la funzione dell'immagine, resta giudizio tuo. I dati strutturati si aggiungono solo se esiste un tipo che corrisponde davvero — prodotto, evento, organizzazione, articolo — perché marcarli a caso non produce nessun effetto.

Quello che invece non è default:

- **I contatti.** Un sito statico non ha un backend. Se l'hosting scelto gestisce i form si usa quello — è una riga nel markup e i dati restano dove sta già il sito; altrimenti un servizio di form dedicato. `mailto:` non è una soluzione: espone l'indirizzo ai raccoglitori e perde il contatto ogni volta che chi legge non ha un client di posta configurato.
- **I font propri si servono dal sito, mai da un dominio terzo.** È una dipendenza di rete e un trasferimento di dati verso l'estero che qualcuno dovrà giustificare.
- **Un form che raccoglie dati di persone passa da `grl-agent-privacy` prima di andare online**: quali campi sono legittimi, cosa deve stare accanto al bottone, dove finiscono i dati e per quanto restano. Il campo raccolto «perché magari serve» è il difetto più comune e il più facile da togliere prima che esista.
- **Quale livello di accessibilità sia obbligatorio, e da quando, lo dice `grl-agent-compliance`** — dipende dal settore e dal mercato, non dalle buone intenzioni. Come rispettarlo senza appiattire il design è materia di `grl-agent-ui-critic`. Sui contrasti della palette, `uv run scripts/contrast.py "#fg,#bg" …` dà i rapporti invece di una stima; senza Python non si stimano — si dichiara che il contrasto non è verificato invece di dare un numero inventato.

Senza framework e senza JavaScript non c'è quasi nient'altro da ottimizzare, e mantenerlo così è la scelta di performance più efficace disponibile.

## Prima di mettere online

Font a pagamento, immagini di stock, loghi «trusted by» di clienti: la licenza per l'uso web e il diritto di mostrare quei marchi sono di `grl-agent-legal`. Un logo altrui in home senza autorizzazione è il tipo di problema che arriva dopo il lancio.

Hosting, dominio, certificato, rilascio e ripristino vanno instradati a `{workflow.external_handoffs}` — il modulo manda a Bruno. Passa il progetto e i suoi vincoli invece di improvvisare una procedura di deploy.

**Aggiorna i brief prima di chiudere.** L'HTML si è spostato in `src/`, quindi in ogni brief il campo `Pagina` va riscritto col nuovo percorso e `Aggiornato` con la data: un brief che nomina un file che non esiste più rende inutile il rientro. E se il gate lo hai tenuto qui, scrivine il verdetto nel campo che autorizzava la promozione — `Gate di sito` in `brief-sito.md`, `Gate revisori` nel `brief.md` della pagina — nella forma `passato il AAAA-MM-GG da <figure>`, altrimenti alla prossima ripresa si ripropone un gate già fatto.

Registra in append in `{project-root}/_bmad/memory/grl-shared/decisions.md`, mostrando prima le righe all'utente: `[AAAA-MM-GG] [web] decisione — vincolo che l'ha imposta`. Meritano una riga le cose che qualcun altro dovrà rispettare — dove arrivano i contatti, quale servizio di form, quale hosting, quale font e con quale licenza. Poi esegui `{workflow.on_complete}` se non è vuoto.
