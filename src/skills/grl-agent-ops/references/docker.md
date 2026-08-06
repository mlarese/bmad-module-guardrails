---
name: docker
description: Immagini piccole e riproducibili, container che non girano da root, compose che si capisce a colpo d'occhio
code: DOCK
added: 2026-08-06
type: prompt
---

# Docker

## Cosa vuol dire riuscirci

L'immagine si ricostruisce uguale domani, la build non aspetta minuti per una virgola cambiata, e il container non gira con più privilegi di quanti gliene servano. Il consumatore è chi farà `docker compose up` fra sei mesi su una macchina nuova e si aspetta che funzioni.

## Cosa si guarda in un `Dockerfile`, in ordine di resa

1. **Ordine dei layer.** I file di dipendenze (`package.json` + lock, `requirements.txt`, `go.mod`) si copiano e si installano **prima** del codice. Se si copia tutto e poi si installa, ogni modifica al codice ributta via l'intera cache dei pacchetti. È l'errore più comune e quello che si paga a ogni singola build.
2. **Build multi-stage.** Toolchain, compilatori e dipendenze di sviluppo restano nello stage di build; nell'immagine finale va solo l'artefatto. È dove si tolgono le centinaia di megabyte.
3. **Immagine base pinnata.** `node:22.11-slim`, non `node:latest`. `latest` significa che la build di domani non è quella di oggi, e la differenza si scopre in produzione.
4. **Utente non privilegiato.** `USER` esplicito prima del `CMD`. Il default è root, e root nel container su un volume montato è root sui file dell'host.
5. **`.dockerignore`.** Senza, il contesto di build si porta dentro `node_modules`, `.git` e — occasionalmente — il `.env`. Un segreto che entra in un layer ci resta anche se un layer successivo lo cancella.
6. **`HEALTHCHECK`** quando qualcosa deve sapere se il servizio è vivo davvero e non solo avviato.

## Cosa si guarda in un `compose`

- **Volumi**: cosa è dato persistente (deve stare su volume nominato) e cosa è cache rigenerabile. Un database su bind mount di una directory temporanea è una perdita di dati che aspetta.
- **Reti**: solo i servizi che devono essere raggiunti dall'esterno pubblicano porte. Il database parla con l'app sulla rete interna e **non** espone `5432` sull'host.
- **Segreti**: variabili d'ambiente da file `.env` non versionato, o secret del gestore. Mai valori in chiaro nel compose committato. Dove e come iniettarli è competenza di Bruno; il rischio dell'esposizione è di **Kai**.
- **`restart: unless-stopped`** sui servizi che devono tornare su dopo un riavvio.
- **Limiti di memoria** sui servizi che possono gonfiarsi, se la macchina è piccola: un container senza limiti che satura la RAM porta giù anche gli altri.
- **Log**: senza `max-size` il file di log cresce finché riempie il disco. È una delle cause più banali di macchina ferma.

## Forma dell'output

Correzioni concrete sul file che ha davanti, ordinate per quanto rendono: la prima è quella che cambia la vita, non la più formalmente corretta. Per ciascuna: la riga da cambiare e cosa si guadagna.

Se il file va già bene, dillo e fermati.

## Trappole

- **`docker system prune`** suggerito con leggerezza: cancella volumi e immagini non referenziate. Rientra nel protocollo dei comandi distruttivi, senza eccezioni.
- **Ottimizzare i megabyte quando il problema sono i minuti.** Chiedi cosa fa male prima di ottimizzare.
- **Aggiungere `HEALTHCHECK` e limiti ovunque** su un progetto da una persona: è la checklist recitata a memoria.
- **Il container come macchina virtuale**: `apt install` a mano dentro un container vivo, che sparisce al prossimo `up`. Se succede, il problema è il `Dockerfile`.
