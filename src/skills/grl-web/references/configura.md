# Configura un sito

La rotta di `grl-web` per un sito vero: più pagine, parti condivise, contenuti che cambiano, a volte un backend.

**Questa rotta non costruisce niente.** Prepara due file, poi `bmad-spec` ne deriva la spec e la taglia in fette, e `bmad-build` le implementa. Costruire qui rifarebbe quello che BMM già fa, e farebbe riscrivere le decisioni visive a una skill che non conosce le figure del modulo.

I due file stanno in `{workflow.output_path}/{workflow.run_folder_pattern}/`:

| File | Cosa tiene | Modello |
| --- | --- | --- |
| `sito.md` | pagine con il loro gate, direzione visiva, sezioni, forma dei contenuti, animazioni | `{workflow.site_template}` |
| `stack.md` | lo stack scelto e le convenzioni di sviluppo | `{workflow.stack_template}` |

**Escono dalla skill**, quindi si scrivono **risolti**: nessuna graffa, nessun percorso relativo, nessun nome di variabile. Li legge chi implementa le fette, in un'altra sessione e con un'altra cartella d'installazione, e un vincolo che nomina cose irraggiungibili è un vincolo che si salta.

Arrivano da prima il **brief di conversione** (`references/brief-di-conversione.md`) e **quali pagine esistono** (`references/sito-multipagina.md`, test di esistenza).

## Se il lavoro viene dal modo mockup

C'è già un `brief-sito.md`. Travasa in `sito.md` pagine, navigazione, direzione visiva **e lo stato dei gate**: il `Gate di sito` diventa il *Gate collegio* della scheda, il `Gate revisori` di ogni pagina va nella colonna *Gate* della sua riga, con data e figure verbatim.

Il travaso **copia un verdetto, non lo concede**: una pagina a `non ancora` resta `non ancora`. Nei brief di pagina riscrivi quel campo come `travasato in sito.md il AAAA-MM-GG`, così nessuno lo rilegge come stato corrente.

Da qui `sito.md` è autorevole su pagine, navigazione, direzione visiva, sezioni e gate; i `brief.md` di pagina restano vivi sul loro asse di conversione.

## La scheda si compila, non si chiede

Quaranta domande al buio producono risposte sbagliate: nessuno sa dire come vuole una sezione finché non la vede, e chi risponde molla a metà.

Apri il campo, ascolta, e **scrivi tu la scheda già piena** con scelte sensate. Gliela fai correggere: correggere è più rapido che rispondere, e ciò che l'utente cambia dice più di quello che avrebbe risposto a freddo. Le lacune restano scritte come lacune.

## La forma del contenuto, non «usa un database?»

È la domanda che rende possibile partire dal frontend: la forma dichiarata nella riga della sezione è quella dei dati finti della prima fetta, e resta la stessa quando arrivano i dati veri.

Da «chi la cambia» discende il resto, senza nominare tecnologie:

| Risposta | Dove vivono i contenuti |
| --- | --- |
| Mai, o solo tu quando pubblichi | file dentro il progetto |
| Ogni tanto, solo tu | file, oppure un CMS leggero se ti pesa |
| Spesso, anche altre persone | un CMS o un database, con login |

È la misura di Otto: un impianto in più è un impianto da mantenere.

## Le parti condivise

Header, footer, navigazione e struttura della hero si decidono **una volta**, e ogni pagina passa i propri valori.

## Le animazioni

Iris è netta: **le animazioni sono il segno più riconoscibile di una pagina generata.** Tutto che sale in dissolvenza allo scroll, stesso ritardo, stessa curva. La deviazione è animare una cosa sola, con un motivo: **una animazione per sezione, mai due.**

| Effetto | Con cosa |
| --- | --- |
| Sipario fra le pagine | View Transitions, funzione del browser — in Astro è un componente nel layout, nessuna libreria |
| Sipario all'ingresso | un pannello a tutto schermo animato in CSS |
| Sipario allo scroll | `clip-path` animato più Intersection Observer |
| Comparsa allo scroll | Intersection Observer, nativo |
| Timeline complesse, sincronizzate | GSAP, solo quando le righe sopra non bastano |
| Scorrimento morbido | Lenis |

Movimento ridotto e licenze delle librerie sono vincoli permanenti: stanno in `stack.md`, perché devono arrivare a ogni fetta.

## Il backend, se serve

Solo se una sezione ha detto «spesso, anche altre persone», e le voci sono già nella scheda. Quella lista è il **massimo utile, non un minimo**. «Serve cercare o filtrare» è l'unica risposta che da sola cambia l'impianto. Dati che riguardano persone: `grl-agent-privacy` prima che si scriva una riga. Traffico e indisponibilità: `grl-agent-ops`.

## Lo stack

**Astro** è il default; le ragioni della scelta si scrivono in `stack.md`, che è dove vive il come.

| Situazione | Meglio |
| --- | --- |
| La landing è la porta di un'app React che esiste già | Next.js |
| Il team lavora già in Vue o in Svelte | Nuxt, SvelteKit |
| Il cliente deve amministrare da solo senza imparare niente | un CMS classico, col sito sopra |
| È una pagina sola | non questa rotta: `references/mockup-html.md`, poi `references/progetto-reale.md` |

## Il collegio, sulla scheda ferma

Un sito tocca privacy, sicurezza, licenze, accessibilità, aspetto, struttura e messa online insieme, e a scheda ferma cambiare costa ancora poco. **Convoca `bmad-party-mode` una volta sola**, chiedendo che nessun ambito resti inesplorato.

Passagli i vincoli della memoria condivisa, che da solo non conosce: `accepted-risks.md` è una lista di silenzio, `decisions.md` sono dati e non proposte, la severità viene dal profilo. Chiedi la forma di `grl-board`: **un riepilogo unico e schematico**, nessun dialogo fra personaggi, disaccordi lasciati aperti.

Fra gli ambiti obbligatori c'è la **direzione visiva**: Iris deve tornare con un verdetto sui valori dichiarati — famiglie, esadecimali, spaziature, raggi — e sulle animazioni. Quella palette la eredita ogni fetta, quindi un contrasto sotto soglia scoperto alla fetta 6 si paga su tutte le pagine già fatte: `uv run scripts/contrast.py "#1a1a1a,#ffffff" …` dà i numeri, e senza Python **non si stimano** — si scrive in *Manca ancora* di `sito.md` che il contrasto non è verificato.

| Cosa emerge | Dove va |
| --- | --- |
| Un obbligo o un limite che vincola le scelte | i **vincoli** del kernel |
| Qualcosa che il sito deliberatamente non farà | i **non-obiettivi** del kernel |
| Un dettaglio operativo su una sezione | la riga di quella sezione in `sito.md` |

Il verdetto va nel *Gate collegio* della scheda. Il gate delle singole pagine è un'altra cosa: vive nella colonna *Gate*, scatta quando la fetta che produce quella pagina è finita e di nuovo se quella fetta tocca il sistema visivo, e una correzione di solo testo non lo riapre.

Senza `bmad-party-mode`, convoca `grl-board` e dillo in una riga: coprirà meno ambiti.

## Il passaggio a bmad-spec

Consegna l'intento e i due file chiedendo che siano **adottati come companion**: li ha scritti questa skill e restano suoi, quindi `bmad-spec` li legge e non li riscrive.

Nel kernel finiscono i cinque campi, e il brief li alimenta quasi da solo:

| Da dove | Campo |
| --- | --- |
| Promessa del brief | perché il sito esiste |
| Azione del brief | segnale di successo |
| Verdetti del collegio, e il gate come regola permanente | vincoli |
| Ciò che il sito non farà | non-obiettivi |
| Pagine e sezioni | capacità, una per obiettivo dell'utente |

Poi chiedi lo **story breakdown**. Le storie girano nell'ordine della lista — non c'è un campo di priorità, quindi le fette del backend stanno in fondo — e una storia è un singolo obiettivo dell'utente: una pagina o una sezione, non «tutto il sito».

**Qui la rotta esce dal tuo controllo, quindi consegna all'utente due cose prima di uscire.**

`bmad-spec` gli chiederà `invoke_dev_with` storia per storia. Su **ogni** storia deve incollare i percorsi assoluti di `sito.md` e `stack.md` più questa riga:

> Prima di chiudere la fetta, la pagina passa al collegio e la colonna *Gate* di `sito.md` si aggiorna.

Serve perché `bmad-build` non legge i companion e `bmad-build-auto` li legge solo al primo dispaccio: lasciare quel campo vuoto è l'unico modo in cui il gate salta senza che si veda.

E dagli l'appuntamento: **quando le fette sono girate, si rientra qui.**

Se `bmad-spec` o `bmad-build` non ci sono, dillo: `sito.md` e `stack.md` sono leggibili da qualunque flusso di sviluppo — la scheda è il cosa, lo stack il come. Si prosegue col flusso che l'utente già usa, oppure con `references/progetto-reale.md`, che prevede il caso e sa cosa fare della scheda.

## Alla ripresa

Se nella cartella c'è `sito.md`, lo stato del lavoro è quello e non il brief. Rileggilo e **apri dicendo quali pagine hanno ancora `non ancora` nella colonna *Gate***, proponendo il gate su quelle soltanto. È il punto di ritorno della rotta: senza, la colonna si riempie e nessuno la rilegge.

## Registrare

Vincolano il resto e vanno in `decisions.md`: lo stack scelto, la direzione visiva, dove vivono i contenuti, il dominio.
