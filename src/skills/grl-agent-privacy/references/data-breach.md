---
name: data-breach
description: Prepara la procedura essenziale di reazione a una violazione di dati, prima che serva
code: DB
added: 2026-08-06
type: prompt
---

# Cosa fare se succede

L'esito è una procedura essenziale che sta in mezza pagina e che qualcuno potrà davvero seguire alle tre di notte: chi decide, entro quando, cosa si comunica e a chi. Il consumatore è un team nel panico, non un auditor.

La procedura resta **in conversazione**: Vera non la scrive su disco. Il team la copia dove la troverà davvero quella notte — il runbook, la pagina interna, il canale di reperibilità — e quella scelta è sua.

Le tre cose che valgono più di tutto il resto:

- **Chi decide.** Un nome, non un ruolo vacante. E chi decide se quella persona non risponde.
- **L'orologio, e di chi è.** Se chi legge è **titolare**, la notifica all'autorità corre da quando si accorge della violazione, non da quando ha capito cosa è successo: 72 ore. Se è **responsabile** — il caso più comune per una software house — l'orologio che lo riguarda è un altro: avvisare il titolare **senza ingiustificato ritardo**, e sarà il titolare a notificare. Un'informazione parziale nei termini vale più di una completa in ritardo. Se il rischio per le persone è alto, vanno avvisate anche loro, senza aspettare la ricostruzione completa.
- **Cosa serve avere già pronto.** Come si capisce quali utenti sono coinvolti (una query, non un'indagine), come si revocano sessioni, token e chiavi, e dove si annota cosa succede mentre succede.

Non ogni incidente è una violazione notificabile, e non ogni violazione va comunicata agli interessati. Dì dove cade la soglia usando un esempio preso dal progetto che hai davanti — altrimenti il team notificherà tutto o niente.

Scrivi la procedura come istruzioni brevi in ordine di esecuzione, non come policy. Se il progetto è un prototipo senza utenti veri, la procedura giusta è di due righe: dillo e chiudi.
