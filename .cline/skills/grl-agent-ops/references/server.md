---
name: server
description: Una macchina configurata in modo prevedibile e ripetibile — utenti, firewall, reverse proxy, certificati, aggiornamenti
code: SRV
added: 2026-08-06
type: prompt
---

# Configurazione server

## Cosa vuol dire riuscirci

La macchina fa quello che deve, **si sa perché**, e se sparisse si potrebbe rifare uguale. Il consumatore è chi ci tornerà sopra fra sei mesi senza ricordarsi nulla — spesso l'utente stesso.

Il criterio non è «configurata bene» in astratto: è **ripetibile**. Una macchina toccata a mano in venti punti diversi e non annotata da nessuna parte è un pezzo unico, e i pezzi unici si rompono nel modo peggiore.

## L'ordine che conta

Non è una checklist da recitare: è la sequenza in cui gli errori fanno più male se si sbaglia l'ordine.

1. **Accesso prima di tutto.** Utente non-root con `sudo`, chiave SSH, e la sessione di controllo aperta (vedi `references/ssh.md`). Chiudersi fuori da una macchina appena creata è l'incidente più comune e più stupido.
2. **Firewall.** Chiuso di default, aperto solo su ciò che serve: 22 (o la porta scelta), 80, 443. Il resto no — soprattutto le porte di database e di amministrazione, che non devono mai vedere internet.
3. **Reverse proxy davanti.** nginx o Caddy: unico punto d'ingresso HTTP, TLS terminato lì, l'applicazione ascolta solo su localhost. Caddy prende i certificati da solo; con nginx si usa certbot con rinnovo automatico — e il rinnovo va **verificato** una volta, non dato per scontato.
4. **I servizi.** Container o `systemd`, con riavvio automatico e log che vanno da qualche parte.
5. **Aggiornamenti.** Almeno quelli di sicurezza in automatico (`unattended-upgrades` o equivalente). Un server che nessuno aggiorna per un anno è una superficie che si allarga da sola.
6. **Backup.** Non è il passo finale opzionale: vedi `references/backup.md`.

## Ripetibilità

Chiedi dove sta scritto com'è fatta la macchina. Le risposte accettabili, in ordine di preferenza: un `docker-compose.yml` versionato · uno script di provisioning · un file di note nel repository. La risposta non accettabile è «me lo ricordo».

Non serve Ansible per una macchina. Serve che i venti comandi dati a mano stiano in un file dentro la repo.

## Forma dell'output

Passi concreti sulla macchina che ha davanti, ciascuno con **il comando e cosa fa**, mai il comando da solo. Segna quali passi sono reversibili e quali no — firewall e `sshd` rientrano nel protocollo dei comandi distruttivi, perché sbagliarli chiude fuori.

Chiudi con **cosa non serve**: quello che il progetto non ha bisogno di configurare, detto esplicitamente, così non lo configura.

## Trappole

- **Il firewall applicato prima di aver verificato la regola SSH.** Sempre una seconda sessione aperta.
- **L'applicazione in ascolto su `0.0.0.0`** con il reverse proxy davanti: la porta resta raggiungibile e scavalca il proxy. Deve ascoltare su `127.0.0.1`.
- **Il rinnovo dei certificati mai provato.** Si scopre a novanta giorni, di sabato.
- **Il servizio avviato a mano** che non riparte dopo un riavvio della macchina.
- **Hardening a tappeto** copiato da una guida: ogni riga di `sshd_config` o di `sysctl` che l'utente non capisce è debito, non sicurezza. Se serve sapere *quale* rischio vale la pena chiudere e con che priorità, è **Kai**.
