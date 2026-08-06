---
name: accessibilita-senza-imbruttire
description: Come rispettare un requisito di accessibilità già stabilito senza appiattire il design, e cosa fare quando obbligo e direzione visiva confliggono davvero.
code: a11y-design
added: 2026-08-06
type: prompt
---

# Accessibilità senza imbruttire

**Il livello richiesto non lo stabilisci tu.** Lo stabilisce Nils (compliance): quale norma si
applica, quale livello, da quando. Se il livello non è stato stabilito, la risposta è «chiedilo a
Nils», non una stima tua. Tu entri dopo, su una domanda sola: **come lo rispettiamo senza che il
design diventi quello di tutti gli altri.**

## Il risultato

L'utente esce con i requisiti soddisfatti **e** la direzione visiva intatta, e sa quali due o tre
cose ha dovuto cedere davvero.

## Il perimetro vincolato è più piccolo di quanto si creda

È il punto che fa la differenza fra un design accessibile e un design appiattito. L'accessibilità
tocca cinque cose. Tutto il resto — carattere tipografico, palette, layout, densità, raggio,
immagini, tono — resta libero.

| Vincolo | Il numero che conta | La libertà che resta |
| --- | --- | --- |
| Contrasto del testo | 4.5:1 normale, **3:1 sopra i 24px** (o 18.7px in grassetto) | il testo grande può restare chiaro: la scala tipografica ampia è alleata dell'accessibilità, non nemica. `#6b7280` su bianco è ≈4.8:1 e passa; `#9ca3af` è ≈2.5:1 e non passa a nessuna dimensione da corpo |
| Contrasto non testuale | 3:1 per bordi di controlli, icone informative, indicatore di focus | il bordo `1px #e5e7eb` su bianco è ≈1.24:1: come unico segno del perimetro di un campo non esiste. Si risolve con uno sfondo diverso dal fondo pagina o con una linea sola sotto il campo — nessuna delle due imbruttisce |
| Focus visibile | deve esserci e avere 3:1 | la forma è tua: spessore, colore, offset, un riquadro invece dell'anello, uno spostamento. Vietato toglierlo. `:focus-visible` lo mostra solo a chi naviga da tastiera |
| Il colore non è l'unico canale | — | il colore resta, si aggiunge un secondo segno: forma, icona, posizione, parola. Un solo carattere in più su un badge, non un ridisegno |
| Bersagli e movimento | 24×24px (AA), 44×44 (AAA); `prefers-reduced-motion` | l'area cliccabile si allarga con padding trasparente senza ingrandire il bottone. La riduzione del moto non è togliere l'animazione: è sostituirla con una dissolvenza o con lo stato finale |

Da qui la cosa da dire per prima, quasi sempre: **il design non è il problema.** I punti che
cadono sono quasi sempre i grigi tenui del testo secondario, i bordi chiarissimi dei campi e il
focus rimosso — cioè tre tic del repertorio (T22, T38, T46). Rimuoverli migliora la pagina in
entrambe le direzioni.

## Quando il conflitto è vero

Capita, e va risolto con una scelta, non con un compromesso tiepido:

- **Il colore del brand non regge il contrasto sul testo.** Si tiene per le aree grandi e i fondi;
  per il testo si usa una variante più scura dello stesso colore, dichiarata come token separato
  (`brand` e `brand-text`). Il brand resta riconoscibile.
- **La tipografia scelta è illeggibile a dimensioni piccole.** Si tiene per i titoli e si accoppia
  a un carattere leggibile per il corpo. L'accoppiamento è anche una deviazione da T23: si guadagna
  due volte.
- **La direzione è ad alto contrasto e violenta.** Nessun problema: l'accessibilità non chiede
  gentilezza, chiede contrasto e chiarezza. Le direzioni severe passano più facilmente di quelle
  soffici.
- **La direzione è tenue e sussurrata.** Qui la cessione è reale: si concentra il contrasto dove il
  testo va letto e si tiene il sussurro dove è decorazione. Dillo esplicitamente, è la cosa che si
  perde.

## Come si consegna

- Solo i punti che riguardano **questo** design. Non l'elenco dei criteri WCAG.
- Per ciascuno: cosa cade, il valore che serve, la correzione concreta, e se il carattere della
  pagina ne risente.
- Alla fine, in una riga: cosa si è ceduto davvero. Se non si è ceduto niente, si dice.
