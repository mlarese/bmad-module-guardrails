---
name: ssh
description: Ci si collega in modo sicuro, si sa chi ha accesso a cosa, e si può revocare
code: SSH
added: 2026-08-06
type: prompt
---

# Accesso remoto SSH

## Cosa vuol dire riuscirci

Si sa **chi può entrare su cosa**, l'accesso si revoca in un minuto, e nessuno si chiude fuori nel farlo. Il consumatore è chi domani deve togliere l'accesso a una persona che ha lasciato il progetto: se non sa da dove cominciare, il lavoro è fallito.

## La regola d'oro

**Prima di ogni modifica a `sshd_config`, al firewall o alle chiavi autorizzate: apri una seconda sessione SSH e tienila aperta.** Modifichi nella prima, controlli con `sshd -t`, ricarichi il servizio, e provi a entrare da una **terza**. Se hai sbagliato, la seconda sessione è ancora dentro ed è la via di ritorno. Senza quella, un errore di battitura costa la macchina.

Questo non è un consiglio: è il passo 1 del protocollo in *Comandi distruttivi*, applicato a SSH.

## Cosa conta davvero

- **Chiavi, non password.** `PasswordAuthentication no` — ma solo dopo aver verificato che la propria chiave funzioni. Toglie in un colpo tutti i tentativi automatici, che sono la quasi totalità del traffico ostile su un server esposto.
- **Niente login diretto di root.** `PermitRootLogin no`, e utenti nominali con `sudo`. Serve per sapere *chi* ha fatto cosa.
- **Un accesso per persona.** Una chiave condivisa fra tre persone non si revoca: si revoca a tutti e tre. È la ragione principale per cui gli accessi restano aperti anni dopo.
- **Sapere cosa c'è dentro `authorized_keys`.** Chiedilo. Su una macchina ereditata è quasi sempre pieno di chiavi di cui nessuno sa più il proprietario. Il commento in fondo alla chiave dice a chi appartiene: se manca, è già un problema.
- **Cambiare la porta** riduce il rumore nei log, non il rischio. Va detto per quello che è, non venduto come sicurezza.
- **Bastion / jump host** solo quando le macchine sono più di poche e non devono stare su internet. Su una macchina sola è complessità che non paga.

## Revoca

La domanda che chiude ogni consultazione su SSH: **come si toglie l'accesso a una persona, oggi, in quanto tempo?** Se la risposta richiede di ricordarsi su quali macchine si era messa la chiave, l'inventario degli accessi va scritto in `notes.md` — nomi di macchine e di persone, mai chiavi.

## Forma dell'output

Lo stato attuale letto dal `sshd_config` o dalla descrizione, poi le due o tre modifiche che contano davvero, ciascuna con il comando, cosa fa e cosa succede se va storto. Non l'hardening completo: quello che serve **a questa macchina**.

## Trappole

- **Disattivare le password senza aver provato la chiave.** Fuori dalla macchina, immediatamente.
- **`chmod` sbagliati.** La directory `.ssh` dell'utente a 700 e il suo `authorized_keys` a 600, altrimenti `sshd` ignora la chiave in silenzio e sembra un problema di rete.
- **`fail2ban` come risposta a tutto.** Con le password disattivate aggiunge poco e va manutenuto.
- **Chiavi senza passphrase sul portatile** — accettabile, ma va detto ad alta voce che chi prende il portatile prende i server.
- **Copiare un `sshd_config` intero da internet.** Ogni direttiva non capita è debito.
