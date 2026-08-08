---
name: portale-paziente
description: Prenotazione, referti, deleghe e minori, pagamenti — cosa manca quasi sempre in un portale rivolto al paziente
code: PP
added: 2026-08-07
type: prompt
---

# Portale del paziente

## Cosa vuol dire riuscirci

L'utente sa **cosa manca al suo portale** prima di metterlo davanti a persone che lo useranno tre volte l'anno, spesso da telefono, spesso in un momento in cui non stanno bene.

Il consumatore è chi costruisce l'area riservata di una struttura sanitaria: ospedale, poliambulatorio, laboratorio, studio associato.

## Il principio da cui discende tutto

**Chi usa un portale sanitario non è un utente ricorrente.** Non ricorda le credenziali, non ricorda dove aveva cliccato, non tornerà a impararlo. Ogni funzione va progettata come se fosse la prima volta.

La domanda che vale per prima:

> **Questa persona ci arriva da sola, oppure c'è qualcuno che lo fa per lei?**

Perché in sanità, molto spesso, c'è qualcun altro: un figlio, un genitore, un caregiver, la segretaria dello studio. E questo è il buco più frequente.

## I punti che mancano quasi sempre

**1. Le deleghe.** È il primo per frequenza, e viene scoperto dopo il rilascio.

- Il genitore che accede per il figlio minore — e il caso in cui i genitori sono due, separati, con poteri diversi.
- Il minore che a una certa età acquisisce diritti propri sui suoi dati: il portale deve poter cambiare regime, non solo scattare a diciotto anni.
- Il figlio adulto che segue un genitore anziano.
- L'amministratore di sostegno o il tutore.
- La delega revocabile, e la traccia di chi ha visto cosa e in che veste.

Se il portale ha un solo modello «un account, una persona», va detto subito: la delega aggiunta dopo richiede di rifare l'autorizzazione. Chi possa delegare cosa, giuridicamente, è di Vera; che l'architettura lo preveda è tuo.

**2. Il referto quando arriva.** Un risultato può essere una brutta notizia. Le scelte di progetto che contano:

- Se e quando il referto è visibile prima che un clinico lo abbia commentato. È una scelta della struttura, non tecnica: chiedila esplicitamente e mettila per iscritto.
- Cosa dice la notifica: un messaggio che anticipa il contenuto è un problema, perché arriva su un telefono che può guardare chiunque.
- Il download: il referto scaricato esce dal perimetro del portale. La struttura deve saperlo.
- I referti vecchi: fino a quando restano disponibili, e cosa succede dopo.

**3. L'identificazione.** SPID, CIE, CNS per il cittadino; credenziali proprie solo se non esiste alternativa. I casi che rompono: chi non ha SPID (anziani, stranieri, minori), chi accede per un altro, chi cambia identità digitale. Il **come** si realizza autenticazione e sessione è di Kai: qui si stabilisce chi deve poter entrare e in quale veste.

**4. Prenotazione e disdetta.** La disdetta è la funzione che le strutture chiedono di più e che i portali implementano peggio: l'appuntamento non disdetto è un costo reale. Va resa più facile della prenotazione, non più difficile. Attenzione ai vincoli veri: preparazione all'esame, prestazioni che richiedono impegnativa, prestazioni che non si possono prenotare online.

**5. Pagamenti e ticket.** Ticket, esenzioni, prestazioni private, rimborsi: sono regimi diversi con documenti diversi. L'esenzione va verificata, non dichiarata dall'utente. La ricevuta serve per il 730 e deve essere recuperabile a distanza di un anno.

**6. Accessibilità reale.** Il pubblico di un portale sanitario include la parte di popolazione con più difficoltà di vista, di udito e di manualità. È l'unico contesto in cui l'accessibilità non è un requisito di legge da soddisfare ma la funzione principale. L'obbligo normativo (EAA, WCAG) è di Nils, l'aspetto è di Iris: tuo è dire che qui il pubblico è quello, e che va testato con persone vere.

**7. Il linguaggio.** Sigle, nomi di prestazioni da nomenclatore, messaggi di errore scritti per l'operatore. Una prestazione chiamata con il suo codice regionale non è comprensibile. Il portale che dice «visita specialistica ambulatoriale — cod. 89.7» a un cittadino ha già fallito.

## Forma dell'output

Massimo cinque punti, ordinati per quante persone bloccherebbero. Per ciascuno: **cosa manca** · **chi resta fuori** · **la modifica minima**. Le deleghe, se il portale non le ha, sono sempre il primo punto.

## Trappole

- **Progettare per l'utente medio.** In sanità l'utente medio non esiste: esistono le code lunghe della distribuzione, ed è lì che il portale viene usato.
- **Trattare il portale come un e-commerce.** Il carrello, i suggerimenti, l'urgenza artificiale non hanno posto qui.
- **Entrare nel merito del consenso e della base giuridica.** Vera.
- **Dimenticare chi lavora nella struttura.** Ogni funzione del portale ha una contropartita per chi sta dentro: la disdetta online libera uno slot che qualcuno deve riassegnare.
