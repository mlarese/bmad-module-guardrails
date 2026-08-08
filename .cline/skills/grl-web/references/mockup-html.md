# Mockup a file singolo

La rotta di `grl-web` per costruire una landing come mockup, a valle del brief di conversione. L'esito è **un solo file `.html`** nella cartella di lavoro della pagina, accanto al suo brief.

## Il vincolo del file singolo

CSS in un `<style>` inline, nessun asset esterno, nessuna chiamata di rete. Font: stack di sistema, oppure un font incorporato in base64 se l'identità visiva lo richiede. Immagini: SVG scritto a mano, oppure un blocco segnaposto che dichiara cosa ci andrà e in che proporzione — mai un URL remoto, mai un servizio di placeholder.

Il motivo è che il mockup si apre col doppio click e deve funzionare offline, su una macchina qualsiasi, fra sei mesi. Un file che chiede la rete non è un mockup: è un sito senza server. Niente Tailwind da CDN — Tailwind stessa lo esclude dalla produzione, e qui aggiunge una dipendenza di rete per risparmiare CSS che sai già scrivere.

Il vincolo si verifica, non si guarda a occhio: `uv run scripts/check_mockup.py <file.html>` restituisce le violazioni in JSON — risorse remote, `@import` e `@font-face` che escono, chiamate di rete nel JavaScript, marcatori segnaposto letterali. Lo script constata presenze; se una testimonianza o un numero siano inventati lo sai solo tu, che hai letto il brief. Se Python non è disponibile, dillo in una riga e verifica leggendo.

## Dal brief alla pagina

Ogni blocco esiste per rispondere a **una** domanda che il visitatore ha in testa in quel momento. Un blocco che non risponde a nessuna domanda è riempimento e si toglie.

| La domanda in testa | Il blocco | Da quale campo del brief |
| --- | --- | --- |
| «Dove sono finito, e mi riguarda?» | apertura: la promessa, per chi è, l'azione | Promessa + Destinatario + Azione |
| «Ci credo?» | la prova, subito dopo la promessa e non in fondo | Prova |
| «Sì ma nel mio caso…» | l'obiezione affrontata per nome, non aggirata | Obiezione |
| «Come funziona, concretamente?» | il meccanismo in tre passi, o una demo | Promessa |
| «Cosa devo fare adesso?» | la stessa azione di sopra, ripetuta identica | Azione |

L'ordine non è sacro, la logica sì: la promessa prima della prova, la prova prima dell'obiezione, l'obiezione prima della richiesta. Chiedere l'azione prima di aver smontato l'obiezione è il modo più comune in cui una landing perde.

Una landing ha **una** azione. Se l'utente ne vuole due, la seconda è un link discreto, non un bottone della stessa dimensione: due bottoni pari fanno scegliere fra loro invece che fra agire e andarsene.

## Il copy

Il difetto per default è la prosa da brochure. Ogni riga passa questi test:

- **Il test del concorrente.** Se la frase funziona anche sul sito di un concorrente, non dice niente. «Soluzioni innovative per la tua azienda» supera indenne qualsiasi cambio di logo.
- **Il test del numero.** Un'affermazione senza un numero, un nome o una data è un'opinione. «Veloce» → «esporta 10.000 righe in 4 secondi».
- **Il test dell'aggettivo.** Togli l'aggettivo: se la frase perde significato, l'aggettivo stava facendo il lavoro del fatto che manca.
- **Le parole sue, non le tue.** L'obiezione e la promessa si scrivono con le parole che ha usato l'utente nel brief. Tradurle in gergo di marketing le rende irriconoscibili al destinatario.

## La direzione visiva e il gate

**Prima del CSS:** chiedi a `grl-agent-ui-critic` la direzione visiva — tipografia, palette, densità, ritmo — con valori concreti. Non inventarla qui: il repertorio dei tic dell'estetica generata e le direzioni visive vivono dentro quella skill. Sui rapporti di contrasto della palette che ti consegna, `uv run scripts/contrast.py "#1a1a1a,#ffffff" …` dà i numeri invece di una stima a occhio; quale livello sia obbligatorio lo dice `grl-agent-compliance`. Se Python non è disponibile i rapporti **non si stimano**: si dichiara che il contrasto non è stato verificato e finisce fra le cose che mancano nel brief — un numero inventato qui diventa un'affermazione di accessibilità falsa su una pagina che va online.

**A pagina pronta, prima di consegnare:** passa a `grl-board` **il percorso della pagina e quello del suo brief**, dicendo che il brief va aperto solo *dopo* aver letto la pagina — chi rilegge l'asse del contenuto deve vederla come la vede un visitatore freddo, e serve poi il brief per dire dove diverge. `grl-board` sceglie le figure pertinenti, risolve la severità dal profilo, filtra ciò che è già in `accepted-risks.md` e lascia aperti i conflitti fra figure invece di appianarli. Se `grl-board` non è installato, convoca `{workflow.finalize_reviewers}` — in parallelo con i subagenti disponibili, uno per figura, altrimenti in sequenza. Se nemmeno Iris è installata, giudica tu la pagina sulla direzione visiva definita qui sopra — tipografia, palette, densità, ritmo, con valori concreti — e dillo in una riga.

È un gate, non un parere: se il verdetto è che la pagina è indistinguibile dal template, si interviene prima di mostrarla all'utente come finita. Scatta alla prima consegna e ogni volta che si tocca il sistema visivo; una correzione di solo testo si consegna senza ri-convocare.

Se il form raccoglie dati di persone, `grl-agent-privacy` entra prima del gate, non dopo.

## La consegna

Mostra il percorso del file e di' all'utente di aprirlo. Poi, in poche righe: cosa hai deciso e perché, cosa manca ancora, e la direzione visiva adottata con i suoi valori.

Aggiorna il brief nello stesso momento: lo stato del gate diventa `passato il AAAA-MM-GG da <figure>`, il percorso della pagina viene compilato, e ciò che l'attrito ha scartato finisce nella sua sezione. Se la pagina appartiene a un sito, il verdetto su sistema visivo e navigazione va **anche** in `brief-sito.md`, che è il campo che autorizza la promozione dell'intero sito. La rotta di promozione a progetto legge proprio quel campo per sapere se il gate è stato fatto.

Le decisioni che vincolano il resto del progetto — direzione visiva, font, dove arrivano i contatti — vanno in append in `{project-root}/_bmad/memory/grl-shared/decisions.md` come `[AAAA-MM-GG] [web] decisione — vincolo che l'ha imposta`, mostrandole prima all'utente. Poi esegui `{workflow.on_complete}` se non è vuoto.
