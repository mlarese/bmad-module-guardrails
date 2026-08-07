# Sito su più pagine

La rotta di `grl-web` quando l'esito non è una pagina sola. Qui si decide **quali pagine esistono e cosa fa ciascuna**; nel modo mockup ogni pagina si costruisce poi con `references/brief-di-conversione.md` e `references/mockup-html.md`, perché ognuna ha un proprio destinatario e una propria azione.

## Cosa vale in quale modo

Questo file serve due modi. **Il test di esistenza di una pagina**, **Una pagina un compito**, **Navigazione** e la regola del sistema visivo deciso una volta sola valgono in entrambi.

**Come sta in cartella**, **I due livelli del gate** e il confronto della coerenza valgono solo per il **modo mockup**, dove ogni pagina è un file autosufficiente da far validare. Se il sito nasce già come progetto — o ci viene promosso — struttura, gate e stato del lavoro stanno in `references/configura.md`.

## Come sta in cartella

Nel modo mockup un sito ha un brief suo e N brief di pagina, quindi la cartella del lavoro si annida:

```
{workflow.output_path}/{workflow.run_folder_pattern}/
├── brief-sito.md        # le pagine che esistono, la navigazione, il sistema visivo
├── prezzi/
│   ├── brief.md
│   └── prezzi.html
└── contatti/
    ├── brief.md
    └── contatti.html
```

`brief-sito.md` tiene ciò che vale per tutte: l'elenco delle pagine con il motivo per cui esistono, il menu, la direzione visiva decisa una volta sola, e lo stato del gate di sito. La sua forma sta in `{workflow.site_brief_template}`. Riprendendo un lavoro si legge prima quello, poi il brief della pagina che si tocca.

## I due livelli del gate

Su un sito il collegio non si convoca per intero a ogni pagina — sarebbe la cerimonia che fa smettere di farlo girare — ma nemmeno una volta sola per tutte.

| Livello | Cosa guarda | Quando | Dove si registra |
| --- | --- | --- | --- |
| **Gate di sito** | il sistema visivo e la navigazione | una volta, sulla prima pagina costruita, e di nuovo se si tocca tipografia, palette, spaziature, layout o menu | `brief-sito.md` |
| **Gate di pagina** | solo l'asse nuovo: cosa dice quella pagina, in che ordine, e privacy se ha un form | a ogni pagina nuova, giro corto | il `brief.md` della pagina |

Al gate di pagina passa a `grl-board` il percorso della pagina e quello del **suo** `brief.md`, con lo stesso ordine di lettura: prima la pagina a freddo, il brief dopo, per il confronto.

Sulla **prima** pagina i due gate girano insieme, e il verdetto si spacca in due campi: sistema visivo e navigazione in `brief-sito.md`, asse del contenuto nel `brief.md` di quella pagina. Un gate, due campi — scriverne uno solo lascia l'altro a `non ancora`, e la promozione a progetto rifarebbe un gate già tenuto.

Una pagina che riusa il sistema visivo già approvato non riapre il gate di sito: il verdetto di Iris riguarda ciò che quella pagina non cambia. Una correzione di solo testo non riapre nessuno dei due.

## Il test di esistenza di una pagina

Il riflesso da evitare è la mappa d'ufficio — Home, Chi siamo, Servizi, Blog, Contatti — che nasce dall'organigramma dell'azienda e non da nessun bisogno di chi legge.

Una pagina esiste se supera almeno uno di questi:

- **Qualcuno ci arriva da fuori.** C'è una ricerca, un link, una campagna, un QR che porta lì e non in home. Una pagina raggiungibile solo dal menu è una sezione, non una pagina.
- **Toglierla fa perdere una decisione.** Chi la legge decide qualcosa che altrove non deciderebbe: comprare, candidarsi, fidarsi del prezzo, capire se il prodotto fa la cosa che gli serve.
- **Il contenuto invecchia con un ritmo suo.** I prezzi cambiano ogni trimestre, il team ogni assunzione: separarli evita di riaprire tutto per una riga.

Tutto il resto è una sezione di una pagina esistente. Un sito di quattro pagine vere batte un sito di dodici pagine di cui otto rimandano altrove. Il test vale anche per ogni pagina aggiunta dopo, non solo alla prima stesura.

## Una pagina, un compito

Ogni pagina dichiara nel suo brief chi la legge e cosa deve fargli fare. Due compiti sulla stessa pagina significano che nessuno dei due viene svolto: si divide, o se ne abbandona uno.

Le pagine legali — privacy, termini, cookie — esistono per obbligo, non per conversione: si scrivono, non si progettano, e il loro contenuto è materia di `grl-agent-privacy` e `grl-agent-legal`, non tua.

## Navigazione

Il menu è la promessa di cosa c'è dentro, e si legge in due secondi. Cinque voci sono tante; sette sono un indice. Le etichette dicono cosa trovi («Prezzi»), non come si chiama il reparto («Soluzioni»).

Ogni pagina risponde in alto a «dove sono» e in basso a «dove vado adesso»: un fondo pagina che non propone il passo successivo scarica il visitatore proprio quando era convinto. Il passo successivo di ogni pagina è dichiarato nel suo brief, non improvvisato.

## Coerenza fra le pagine

Il sistema visivo si decide **una volta sola**, con `grl-agent-ui-critic`, prima della prima pagina: tipografia, palette, spaziature, componenti ricorrenti. Deciderlo pagina per pagina produce un sito che sembra fatto da tre persone che non si parlano — ed è il difetto che si nota per primo e si corregge per ultimo.

Nel modo mockup ogni pagina resta un file `.html` autosufficiente — CSS inline, nessun asset esterno, nessuna chiamata di rete — quindi il CSS condiviso è duplicato in ciascuno: è accettabile per validare la forma, ed è esattamente il motivo per cui un sito di più pagine finisce in un progetto vero invece di restare mockup — e con parti condivise quel progetto è `references/configura.md`, non la promozione statica.

Finché resta duplicato, la deriva fra le copie si verifica invece di cercarla a occhio su N file: `uv run scripts/check_coerenza.py <cartella-del-lavoro>` dice quale pagina non ha quale token — custom property, font, esadecimali — e se lo stile è ancora identico ovunque. Se una divergenza è voluta, come una pagina legale senza il CSS dell'hero, si tiene: lo script constata, il giudizio è tuo.

