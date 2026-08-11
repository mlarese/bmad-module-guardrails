# {nome del sito}

**Cartella:** {slug} · **Gate collegio:** `non ancora`, oppure `passato il AAAA-MM-GG da <figure>` · **Aggiornato:** AAAA-MM-GG

Compilato da `grl-web`, corretto dall'utente. `bmad-spec` lo adotta come companion e non lo riscrive.

## A chi parla e per fare cosa

Dal brief di conversione: il destinatario, la promessa in una riga, l'azione che il sito deve far compiere. Sono i campi che diventano il «perché» e il «segnale di successo» della spec.

## Le pagine

| Pagina | Chi ci arriva, da dove | Cosa deve far fare | Hero | Gate |
| --- | --- | --- | --- | --- |
| | | | | `non ancora` |

Una pagina esiste se qualcuno ci arriva da fuori, o se toglierla fa perdere una decisione. Le pagine legali stanno qui per obbligo, non per conversione.

La colonna **Gate** è lo stato del controllo su quella pagina: `non ancora` finché nessuno l'ha guardata, poi `passato il AAAA-MM-GG da <figure>`. Si aggiorna quando la fetta che produce la pagina è finita, prima che parta la successiva, e a ogni ripresa del lavoro si riparte da qui. È l'unico posto in cui quello stato sopravvive: la conversazione in cui il gate è avvenuto può non esserci più.

Il documento contro cui si confronta la pagina è **la riga qui sopra più il brief di conversione del lavoro**: su questa rotta non esiste un brief per pagina.

## Direzione visiva

Decisa una volta per tutto il sito, **con i suoi valori** — è quello che Iris giudica prima che diventi codice, ed è quello che ogni fetta legge per non reinventare la precedente.

- **Tipografia:** famiglie e pesi
- **Palette:** esadecimali, con il ruolo di ciascuno
- **Spaziature:** la scala
- **Raggi e bordi**
- **Contrasti verificati:** sì / no, con la data

Il verdetto su questi valori arriva dalla convocazione del collegio e sta nel campo *Gate collegio* in testa al file, insieme al resto.

## Le parti condivise

**Header:** cosa contiene, quali voci, cosa cambia da una pagina all'altra.
**Footer:** cosa contiene, cosa è uguale ovunque.
**Hero:** la struttura è una sola; ogni pagina passa titolo, testo, immagine, eventuale colore.

Ciò che non è scritto qui verrà reinventato dalla seconda pagina in poi.

## Le sezioni

Una riga per sezione, in ordine di apparizione nella pagina.

| Pagina | Sezione | Forma del contenuto | Chi la cambia, ogni quanto | Da dove arriva |
| --- | --- | --- | --- | --- |
| | | `{ campo, campo, campo? }` | mai / ogni tanto solo io / spesso anche altri | file / CMS / database |

La **forma** si dichiara adesso e non cambia più: i dati finti della prima fetta devono avere la stessa struttura di quelli veri, altrimenti la sezione va rifatta quando arriva il backend.

## Le animazioni

Vuoto significa nessuna animazione, ed è una risposta legittima.

| Pagina | Sezione | Effetto | Con cosa |
| --- | --- | --- | --- |
| | | | |

## Il backend

Da compilare solo se una sezione ha detto «spesso, anche altri».

- **Chi amministra i contenuti**, e se serve una password
- **Quali dati si raccolgono**, e se riguardano persone
- **Dove vivono i dati**, e chi li salva
- **Serve cercare o filtrare?**
- **Quanto traffico**, e quanto si può stare giù

## Quello che il sito non farà

L'elenco esplicito di ciò che resta fuori. Diventa i «non-obiettivi» della spec, e senza di esso qualcuno più a valle riempirà il vuoto da solo.

## Verdetti del collegio

Cosa è emerso dalla convocazione, una riga per punto, con la figura che l'ha sollevato. I vincoli diventano vincoli della spec; i disaccordi restano aperti finché non decide l'utente.

| Figura | Punto | Cosa comporta |
| --- | --- | --- |
| | | |

## Manca ancora

Contenuti veri, immagini, prove, decisioni sospese: cosa serve prima che si possa cominciare.

## Scartato

Pagine proposte e non fatte, sezioni tolte, animazioni scartate — con il perché. Serve a non rifare la stessa discussione fra sei mesi.

| Cosa | Perché |
| --- | --- |
| | |
