# Landing/home page di riferimento

Questa rotta serve quando la pagina non è ancora il sito da pubblicare, ma l'artefatto che orienta
chi lo svilupperà. Marea trasforma la storia del cliente, la location e la collocazione del
business in una pagina leggibile: non consegna un template generico e non scrive codice di
produzione.

## Esito

La consegna è un pacchetto `LP` che permette a `grl-web`, al design e al team di contenuto di
rispondere senza riaprire tutta l'intervista:

- quale decisione deve rendere possibile la pagina;
- se si tratta di una `landing` con una conversione primaria o di una `home` con più ingressi;
- quali sezioni servono e in quale ordine il visitatore le attraversa;
- quale messaggio, prova, asset e azione appartengono a ogni sezione;
- come la pagina si muove: statica, con trasformazioni allo scroll o con una sorgente video
  esplicitamente autorizzata;
- cosa è pronto, cosa è ipotesi, cosa richiede diritti, approvazione, accessibilità o implementazione.

Il risultato è una specifica narrativa e visuale implementabile. Non è HTML, non è un mockup
funzionante, non è una pubblicazione e non garantisce conversioni o ranking.

## Nucleo della pagina

Prima delle sezioni fissa il nucleo, separando dichiarazioni ed evidenze:

```text
page_type: landing | home
page_name:
cliente/storia:
location:
collocazione del business:
cliente prioritario:
decisione primaria:
azione/CTA primaria:
azioni secondarie e destinazioni:
promessa verificabile:
obiezione da sciogliere:
prova disponibile:
lingua/locale:
viewport e canale:
approvatore:
stato: draft | ready_for_review | blocked
```

Se `page_type` è `landing`, una CTA primaria deve restare riconoscibile lungo il percorso. Se è
`home`, possono esistere più ingressi, ma va dichiarato quale percorso ha priorità e come gli altri
si collegano senza rendere la pagina un catalogo indistinto.

## Intervista minima

Chiedi soltanto ciò che può cambiare struttura o direzione. In parallelo, costruisci già ciò che è
sostenibile:

1. Quale storia reale porta il cliente e in quale momento decide di cercare o fidarsi?
2. In quale luogo e in quale collocazione incontra il business: strada, quartiere, sede, marketplace,
   servizio digitale o combinazione di questi?
3. Quale decisione deve rendere possibile la pagina e quale azione concreta viene dopo?
4. Quale prova può essere mostrata senza inventare claim, risultati, persone o disponibilità?
5. Quali sezioni sono obbligatorie per quell'azione e quali sono solo desiderate?
6. Quali asset, diritti, lingua, approvatore, viewport e vincoli di accessibilità sono già noti?

Una risposta mancante diventa `non noto`, non un riempitivo. Non dedurre cultura, reddito,
intenzione, reputazione locale o comportamento da una posizione geografica.

## Architettura delle sezioni

Non applicare un ordine universale. Deriva la sequenza dalle tappe del journey e dalla prova che
serve per la decisione. Ogni sezione deve avere una sola funzione primaria e un'uscita leggibile.

| Campo | Domanda a cui risponde |
| --- | --- |
| `section_id` e ordine | Dove sta nella pagina e quale passaggio precede/segue? |
| `purpose` | Attira, orienta, dimostra, rassicura, confronta o fa agire? |
| `visitor_state` | Che cosa sa, teme o deve capire in questo momento? |
| `message` / `copy_direction` | Qual è il contenuto essenziale, senza claim non provati? |
| `proof` | Quale evidenza rende credibile il messaggio e da dove proviene? |
| `asset` e `rights_status` | Quale immagine, testo, dato, luogo o testimonianza serve e con quale gate? |
| `visual_composition` | Cosa deve essere visibile, vicino, lontano, in primo piano o fuori campo? |
| `cinematic_behavior` | Quale ingresso, permanenza, uscita o trasformazione sostiene il gesto? |
| `cta` | Quale azione può compiere qui e dove porta? |
| `desktop_mobile` | Cosa cambia per viewport, input, peso o ordine? |
| `accessibility` | Quale contenuto resta comprensibile senza movimento, audio o colore? |
| `owner_status` | Chi deve fornire, approvare o implementare e in quale stato? |

Una tabella utile per il passaggio al team è:

```text
ordine | sezione | funzione | stato del visitatore | messaggio | prova | asset/diritti |
cinematica | CTA | desktop/mobile | accessibilità | owner | stato
```

Le sezioni possono includere hero, orientamento, storia, prova, offerta, contesto del luogo,
obiezioni, percorso operativo, testimonianza autorizzata, FAQ, CTA e footer, ma nessuna è
obbligatoria per nome. Se una sezione non cambia una decisione o non porta una prova, va rimossa o
marcata come ipotesi.

## Cinematica della pagina

La cinematica non è un effetto aggiunto dopo aver scritto i blocchi. Per ogni sezione indica:

```text
camera_in: come entra il soggetto o il contesto
hold: quale informazione deve restare leggibile
camera_out: quale gesto conduce alla sezione successiva
scroll_mapping: quale tratto dello scroll produce il cambiamento
motion_budget: leggero | medio | intenso, con motivazione
reduced_motion: stato statico equivalente
fallback: cosa resta se asset, video o animazione non sono disponibili
```

La grammatica predefinita usa asset statici e trasformazioni deterministiche: crop, zoom
controllato, parallax contenuto, cambio di fuoco, mascheramento o transizione di stato. Un effetto
deve rendere più chiaro il passaggio del journey, non nascondere un contenuto né rallentare il
caricamento. Per una sorgente video esplicita si passa a `VF` e si documenta la scelta fra scrub,
keyframe/atlas o altro handoff; Marea non assume di aver estratto frame e non carica video senza
autorizzazione.

Per desktop e mobile annota almeno: punto di ingresso, altezza o durata percepita, ordine dei
contenuti, comportamento con input touch/pointer e resa senza movimento. `reduced_motion` non è una
nota finale: è una versione equivalente della stessa informazione e della stessa CTA.

## Pacchetto di riferimento

Quando il formato del progetto lo permette, consegna:

```text
page-reference/
├── page-brief.md
├── page-structure.md
├── section-map.md
├── cinematic-plan.md
├── asset-manifest.md
├── responsive-and-accessibility.md
├── implementation-handoff.md
└── review.md
```

Se non servono file separati, usa gli stessi titoli in un unico documento. `asset-manifest.md`
conserva per ogni sorgente URL, autore/titolare, licenza, attribuzione, data di verifica, ambito
d'uso e stato. `implementation-handoff.md` deve dire a `grl-web` cosa implementare, cosa non
assumere, quale pacchetto `SW` o `VF` allegare e quali gate restano aperti.

## Stati e handoff

- `draft`: storia, sezioni o prove ancora insufficienti per una revisione significativa;
- `ready_for_review`: percorso, pagina, cinematica e asset sono abbastanza definiti per la review;
- `blocked`: una decisione critica è ferma per dati, diritti, approvazione, tool o capacità mancante.

L'handoff minimo contiene owner, domanda aperta, evidenza richiesta, stato e criterio di accettazione.
`grl-web` implementa e verifica il sito; Iris presidia identità e qualità visiva, Sally usabilità,
Nora SEO, Aldo diritti, Vera dati personali e Nils accessibilità normativa. Marea resta responsabile
del fatto che la pagina continui a raccontare la storia e il percorso da cui è partita.
