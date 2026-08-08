---
name: auth
description: Se il modello di chi-può-fare-cosa regge, dove si rompe per primo e come si corregge
code: AUTH
added: 2026-08-06
type: prompt
---

# Autenticazione e autorizzazione

## Cosa vuol dire riuscirci

L'utente sa **dove il suo modello di accesso si rompe per primo** e cosa cambiare per ripararlo — senza rifare il sistema di login.

Il consumatore è chi ha già scritto (o sta per scrivere) i controlli di accesso. Vuole sapere quale riga è sbagliata, non un trattato su OAuth.

## Dove si rompe davvero

L'autenticazione (*chi sei*) è quasi sempre delegata a qualcosa di decente. **L'autorizzazione (*cosa puoi fare*) è dove si rompe.** Guarda lì per primo.

Le rotture ricorrenti, in ordine di frequenza reale:

- **Il controllo sta solo nella UI.** Il bottone è nascosto, l'endpoint no. È il primo posto da guardare in qualunque SPA.
- **ID prevedibile senza verifica del proprietario** (IDOR — accedere alla risorsa di un altro cambiando un numero nell'URL). `GET /api/ordini/1042` risponde a chiunque sia loggato.
- **Il ruolo arriva dal client.** Un campo `role` nel token, nel body o in un cookie che il server crede.
- **Il controllo è ripetuto endpoint per endpoint**, quindi prima o poi ne manca uno. Il difetto non è il singolo buco: è che ogni nuovo endpoint è un'altra occasione di sbagliare.
- **Multi-tenant senza filtro sul tenant** nella query. Funziona finché c'è un solo cliente.
- **Sessione che non muore**: nessuna scadenza, nessuna invalidazione al cambio password, token di lunga durata senza revoca.
- **Reset password** che conferma l'esistenza dell'account e non ha limiti di tentativi.

## Come si risponde

Nomina il punto rotto sul codice o sul flusso che hai davanti, poi la correzione minima. Se il difetto è strutturale (controlli sparsi), la correzione è strutturale — un punto unico di verifica — e va detto che costa più di una patch, ma una volta sola.

Dove il modello di ruoli è più complicato di quanto il prodotto richieda, dillo: i permessi che nessuno capisce diventano permessi che nessuno verifica.

## Trappole

- **Proporre un rifacimento del login.** Quasi mai è la risposta. La domanda giusta è cosa può fare un utente autenticato che non dovrebbe.
- **La MFA come risposta a tutto.** Ha un costo di attrito reale; proponila dove il valore dell'account la giustifica, non per riflesso.
- **Il rollout completo di un framework di policy** su un'app con tre ruoli.
