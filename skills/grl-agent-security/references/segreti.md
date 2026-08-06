---
name: segreti
description: Chiavi e credenziali esposte o gestite male, con il rimedio giusto per ciascuna
code: SEC
added: 2026-08-06
type: prompt
---

# Gestione dei segreti

## Cosa vuol dire riuscirci

Nessuna chiave del progetto sta dove chiunque può leggerla, e per ognuna di quelle già esposte l'utente sa che **rimuoverla non basta**.

Il consumatore è chi ha le mani sul repository adesso. Vuole percorsi di file e nomi di variabile, non principi.

## Dove guardare, in quest'ordine

1. **File tracciati da git**: `.env`, `.env.local`, `config.json`, `settings.py`, `application.properties`, notebook, file di seed. Controlla che `.env` sia davvero in `.gitignore` — e che non ci sia finito *dopo* essere stato committato.
2. **Storia di git.** Un segreto tolto in un commit successivo è ancora nella storia. `git log -p -S "<frammento>"` o `git log --all --diff-filter=A -- .env`.
3. **Codice sorgente**: stringhe che sembrano chiavi (`sk-`, `AKIA`, `ghp_`, `xoxb-`, JWT, URL di connessione con password dentro), incluse quelle nei test e nei commenti.
4. **Bundle client.** Una chiave in un'app front-end è pubblica per definizione, anche se il file si chiama `.env.local`: tutto ciò che il bundler inlinea (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`) finisce nel browser. Verifica se quella specifica chiave è pensata per essere pubblica (chiave anon, publishable) o no.
5. **Pipeline CI**: segreti scritti nel workflow invece che nei secret del runner, `echo` di variabili, log di build che stampano l'ambiente.
6. **Log e messaggi d'errore**: header `Authorization` loggati, dump di configurazione al boot, stack trace con la stringa di connessione.
7. **Immagini container**: `ARG`/`ENV` con credenziali, file copiati e poi cancellati in un layer successivo (restano nel layer precedente).

## Il rimedio corretto

Per un segreto **già esposto**, l'ordine è sempre questo e va detto per intero:

1. **Ruota la chiave.** Un segreto pubblicato è compromesso, punto. Se è finito su un repository pubblico, considerarlo già raccolto è realismo, non allarmismo: gli scanner automatici passano in minuti.
2. Rimuovilo dal codice e dalla configurazione.
3. Ripulire la storia di git è opzionale e costoso (riscrittura, coordinamento sul team): serve solo se il repository è pubblico o passa di mano. La rotazione ha già chiuso il rischio.

Per un segreto **gestito male ma non esposto**, proponi lo spostamento più economico che il progetto già supporta — variabili d'ambiente della piattaforma di deploy, secret del CI — non l'adozione di un vault.

## Trappole

- **Proporre un secret manager** a un progetto con tre chiavi su Vercel. Il costo supera il beneficio.
- **Fermarsi alla rimozione senza la rotazione.** È l'errore più comune e vanifica tutto il resto.
- **Trattare come segreto ciò che non lo è**: chiavi anon di Supabase, publishable key di Stripe, ID pubblici. Segnalarle brucia credibilità.
