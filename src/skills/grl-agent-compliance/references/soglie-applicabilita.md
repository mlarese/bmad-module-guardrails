---
name: soglie-applicabilita
description: Chi è dentro e chi è fuori, norma per norma — le soglie concrete che decidono l'applicabilità e le trappole che le fanno sbagliare
code: SOG
added: 2026-08-06
type: reference
---

# Soglie di applicabilità

**Data di riferimento di questo file: 6 agosto 2026.** Le date e le soglie qui sotto erano vere a quella data. Prima di usarne una per decidere un esito, verificala sul web; se non puoi cercare, dichiara all'utente questa data e indica esattamente quale punto va riverificato.

Questa non è una rassegna: è l'elenco delle porte d'ingresso. Per ogni norma, ciò che conta è la riga «scatta se» — tutto il resto viene dopo, e solo se la porta è aperta.

## AI Act — Reg. (UE) 2024/1689

**Scatta se:** immetti sul mercato UE o usi nell'UE un sistema di IA, o un modello per finalità generali. **Non c'è soglia dimensionale**: prende anche due persone in un garage. La soglia vera è *quale ruolo* hai e *in quale categoria di rischio* ricade il sistema.

| Ruolo | Chi sei | Peso degli obblighi |
| --- | --- | --- |
| Fornitore (provider) | sviluppi il sistema, o lo immetti sul mercato a tuo nome, o modifichi sostanzialmente quello di un altro | pieno |
| Utilizzatore (deployer) | usi sotto la tua autorità il sistema di un altro (es. chiami un'API di un LLM dentro il tuo prodotto) | ridotto: trasparenza, uso conforme alle istruzioni, sorveglianza umana se il sistema è ad alto rischio |

| Categoria | Cosa la fa scattare | Conseguenza |
| --- | --- | --- |
| Pratica vietata | scoring sociale, riconoscimento emozioni sul lavoro o a scuola, scraping massivo di volti, manipolazione | divieto, già in vigore |
| Alto rischio, Allegato III | il sistema *decide o influenza materialmente* su: selezione e gestione del personale, merito creditizio, accesso a servizi essenziali, istruzione, giustizia, forze dell'ordine, migrazione, infrastrutture critiche | obblighi pesanti (gestione del rischio, dati, documentazione tecnica, log, sorveglianza umana, conformità) |
| Alto rischio, Allegato I | il sistema di IA è componente di sicurezza di un prodotto già regolato (dispositivi medici, macchine, ascensori, giocattoli…) | obblighi pesanti + procedura di conformità del prodotto |
| Trasparenza (art. 50) | l'utente interagisce con un sistema di IA; il sistema genera o manipola contenuti (testo, immagini, audio, video) | dichiararlo all'utente; marcare i contenuti sintetici |
| Rischio minimo | tutto il resto | nessun obbligo specifico |

**Calendario (aggiornato dal Reg. (UE) 2026/1744, "Digital Omnibus on AI", in vigore dal 27 luglio 2026):**

| Data | Cosa |
| --- | --- |
| 2 febbraio 2025 | pratiche vietate; obbligo di alfabetizzazione IA del personale |
| 2 agosto 2025 | modelli per finalità generali (GPAI); governance |
| 2 agosto 2026 | obblighi di trasparenza dell'art. 50; poteri e sanzioni delle autorità nazionali a regime |
| 2 dicembre 2027 | alto rischio Allegato III (**rinviato** dal 2 agosto 2026 dal Digital Omnibus) |
| 2 agosto 2028 | alto rischio Allegato I, prodotti (**rinviato**) |

**Trappole.**

- «Usiamo un LLM» non significa alto rischio. La stragrande maggioranza dei prodotti che chiamano un'API di un modello ricade in *trasparenza* o in *rischio minimo*.
- Ciò che fa scattare l'Allegato III non è il settore in cui operi, ma la **decisione** che il sistema prende su una persona. Un gestionale HR che archivia CV è fuori; uno che li ordina per punteggio e scarta è dentro.
- Chi usa un modello di terzi è utilizzatore, non fornitore — a meno che non lo rimarchi a proprio nome o lo modifichi sostanzialmente. Il confine cambia tutto il peso degli obblighi.
- Il rinvio del Digital Omnibus riguarda **l'alto rischio**, non la trasparenza: quella è in vigore.

## NIS2 — Dir. (UE) 2022/2555 · Italia: D.lgs. 138/2024 (ACN)

**Scatta se** valgono *entrambe* le condizioni:

1. l'organizzazione opera in un settore dell'Allegato I (alta criticità: energia, trasporti, banche, infrastrutture dei mercati finanziari, sanità, acqua potabile, acque reflue, infrastrutture digitali, gestione servizi TIC B2B, PA, spazio) o dell'Allegato II (altri settori critici: poste, rifiuti, chimica, alimentare, manifattura di dispositivi, fornitori digitali, ricerca);
2. ha **almeno 50 dipendenti** *oppure* fatturato annuo **superiore a 10 milioni di euro**.

**Dentro a prescindere dalla dimensione:** fornitori di reti e servizi di comunicazione elettronica, prestatori di servizi fiduciari, registri TLD e fornitori di servizi DNS, pubbliche amministrazioni indicate dalla norma, e i soggetti individuati come unici fornitori di un servizio essenziale.

**Scadenze italiane ricorrenti (ciclo 2026):** aggiornamento della registrazione sul portale ACN entro il 28 febbraio; comunicazione dell'elenco fornitori rilevanti fra il 15 aprile e il 31 maggio; aggiornamento della categorizzazione di attività e servizi fra il 1° maggio e il 30 giugno; misure di sicurezza di base implementate entro il 31 ottobre 2026.

**Trappole.**

- Scrivere software non mette dentro NIS2. Ci si entra come *fornitore di servizi TIC gestiti* o *fornitore digitale* secondo gli allegati — un'agenzia che consegna progetti a commessa di norma non lo è.
- Il fornitore di un soggetto NIS2 non diventa NIS2. Riceve però requisiti **contrattuali** sulla sicurezza della catena di fornitura: è un vincolo di committente, non un obbligo di legge suo. → `references/cliente-regolamentato.md`.
- La soglia dimensionale è OR, non AND: 30 dipendenti e 12 M€ di fatturato basta.

## DORA — Reg. (UE) 2022/2554

**Scatta se** l'organizzazione è un'**entità finanziaria** (banche, SIM, SGR, assicurazioni, istituti di pagamento e di moneta elettronica, fornitori di servizi per le cripto-attività, gestori di sedi di negoziazione, agenzie di rating…), oppure è un fornitore di servizi TIC **designato come critico** dalle autorità europee di vigilanza. Applicabile dal 17 gennaio 2025.

**Trappole.**

- Il fornitore software di una banca **non** è soggetto a DORA: la designazione di fornitore critico riguarda pochi operatori a rilevanza sistemica. Il fornitore riceve invece, per l'art. 30, obblighi contrattuali stringenti — diritti di audit, exit strategy, livelli di servizio, subappalto, localizzazione dei dati. Trattali come requisiti di committente.
- Le entità finanziarie microimprese hanno un regime semplificato.
- «Fintech» non è una categoria giuridica: conta se l'attività è riservata e autorizzata. Un'app che si appoggia a un istituto di pagamento autorizzato non è, per ciò solo, entità finanziaria.

## Cyber Resilience Act — Reg. (UE) 2024/2847

**Scatta se** immetti sul mercato UE un **prodotto con elementi digitali** — hardware o software venduto o distribuito, con connessione diretta o indiretta a un dispositivo o a una rete.

| Data | Cosa |
| --- | --- |
| 11 giugno 2026 | capo sulla notifica degli organismi di valutazione della conformità |
| 11 settembre 2026 | obblighi di segnalazione: vulnerabilità attivamente sfruttate e incidenti gravi (allerta entro 24 ore, notifica entro 72, relazione finale entro 14 giorni o un mese) |
| 11 dicembre 2027 | applicazione piena |

**Trappole.**

- Un SaaS puro, di norma, è fuori: è un servizio, e sta semmai in NIS2. Rientrano invece le soluzioni di elaborazione remota **necessarie al funzionamento** di un prodotto immesso sul mercato.
- Software libero sviluppato fuori da un'attività commerciale è escluso; gli *steward* di open source hanno obblighi alleggeriti. La monetizzazione (supporto a pagamento, versione enterprise) sposta il confine.
- Il software su misura fatto per un singolo cliente e non immesso sul mercato non è un prodotto ai fini del CRA.

## Accessibilità — EAA, Dir. (UE) 2019/882 · Italia: D.lgs. 82/2022 e L. 4/2004

**Scatta se** offri a **consumatori** nell'UE uno dei prodotti o servizi elencati: commercio elettronico, servizi bancari al consumo, e-book, trasporto passeggeri, comunicazioni elettroniche, accesso ai servizi di media audiovisivi, sportelli e terminali self-service. Applicabile dal 28 giugno 2025 — vale anche per gli operatori extra-UE che vendono a consumatori europei.

**Esenzione microimprese:** meno di 10 dipendenti **e** fatturato o bilancio annuo non superiore a 2 milioni di euro → esentate per i **servizi**, non per i prodotti.

**Standard tecnico:** EN 301 549, che richiama **WCAG 2.1 livello AA** come minimo.

**In Italia, in aggiunta:** la L. 4/2004 (Stanca), come modificata dal D.L. 76/2020, obbliga i soggetti privati con fatturato medio superiore a **500 milioni di euro** negli ultimi tre anni; la PA e i concessionari di pubblici servizi sono obbligati a prescindere, con dichiarazione di accessibilità e responsabile designato.

**Trappole.**

- Software B2B, strumenti interni, backoffice e API non sono catturati dall'EAA. Un committente pubblico invece li cattura per altra via.
- L'obbligo non si ferma all'interfaccia: copre l'intero servizio, dalle informazioni precontrattuali al checkout, ai pagamenti, all'assistenza.
- WCAG 2.2 è la versione più recente dello standard, ma il riferimento normativo cogente resta la 2.1 AA finché la EN 301 549 non lo aggiorna. Adottare la 2.2 è buona pratica, non obbligo.

## eIDAS ed eIDAS 2 — Reg. (UE) 910/2014, modificato dal Reg. (UE) 2024/1183

**Scatta se** presti tu stesso **servizi fiduciari** (firme elettroniche qualificate, sigilli, marche temporali, recapito certificato, autenticazione di siti web), oppure se il tuo settore ti obbligherà ad **accettare** il portafoglio europeo di identità digitale (EUDI Wallet). Gli Stati membri devono rendere disponibile il wallet entro la fine del 2026; l'obbligo di accettazione per piattaforme molto grandi e settori regolati arriva dopo.

**Trappole.**

- Usare un prestatore qualificato di terze parti per far firmare un documento **non** ti rende prestatore di servizi fiduciari. È la differenza fra erogare e consumare.
- SPID e CIE sono schemi di identificazione nazionali: integrarli è un requisito di progetto o di committente pubblico, non un obbligo eIDAS che grava su di te.

## Settore bancario e finanziario (Italia)

**Scatta se** il committente o l'organizzazione è una banca, un intermediario vigilato o un istituto di pagamento. Il software eredita i vincoli attraverso il contratto, non direttamente.

- Banca d'Italia, Circolare 285 — sistema informativo, continuità operativa, esternalizzazione di funzioni essenziali (con obblighi di notifica preventiva alla Vigilanza).
- Orientamenti EBA su gestione del rischio ICT e di sicurezza, e su esternalizzazione.
- DORA sulla resilienza operativa digitale e sui contratti ICT.
- PSD2 e autenticazione forte del cliente (SCA) se si prestano servizi di pagamento.

**Trappola:** integrare Stripe o un PSP autorizzato non rende l'azienda prestatore di servizi di pagamento. La SCA la implementa il PSP; a te resta di non aggirarla.

## Settore sanitario

**Scatta se** il software ha una **finalità medica** — diagnosi, prevenzione, monitoraggio, previsione, prognosi, trattamento o attenuazione di una malattia. In quel caso è dispositivo medico ai sensi del Reg. (UE) 2017/745 (MDR), e la Regola 11 dell'Allegato VIII spinge quasi tutto il software di supporto alle decisioni in classe IIa o superiore: marcatura CE, organismo notificato, sistema di gestione della qualità, sorveglianza post-vendita.

**Fuori:** benessere, fitness, stili di vita, gestionali amministrativi di studio o ospedale, agende di prenotazione.

**In Italia, in aggiunta:** chi alimenta o consulta il Fascicolo Sanitario Elettronico segue le regole tecniche del FSE 2.0; i dati sanitari sono categoria particolare dell'art. 9 GDPR → competenza di **Vera**, tu intervieni solo dove il settore aggiunge regole proprie (per esempio tempi di conservazione imposti alla documentazione sanitaria).

**Approfondimento:** qualificazione, Regola 11, classi e IEC 62304 stanno in `references/dispositivo-medico.md`; il percorso guidato che porta al verdetto è il workflow `grl-mdsw`.

## Altre norme che spesso si citano a sproposito

| Norma | Scatta se | Non scatta se |
| --- | --- | --- |
| Digital Services Act, Reg. (UE) 2022/2065 | offri un servizio intermediario: hosting, marketplace, piattaforma con contenuti di terzi | il tuo prodotto pubblica solo contenuti tuoi. Micro e piccole imprese sono esonerate dagli obblighi più pesanti da piattaforma |
| Data Act, Reg. (UE) 2023/2854 (dal 12 settembre 2025) | vendi prodotti connessi (IoT) o servizi correlati; oppure sei fornitore di servizi cloud (obblighi di portabilità e cambio fornitore) | il prodotto non genera dati d'uso da dispositivo connesso |
| Reg. macchine, giocattoli, dispositivi | il software è componente di sicurezza di un prodotto fisico regolato | il software è autonomo |

## Come si usa questo file

1. Prendi dal profilo di progetto i quattro assi: dimensione, settore, mercato, tipo di sistema.
2. Passa le porte d'ingresso qui sopra. Una porta chiusa chiude il discorso: la norma non si nomina più.
3. Per le porte aperte, verifica sul web che data e soglia siano ancora quelle — soprattutto AI Act, CRA, NIS2 ed eIDAS 2, che si stanno muovendo.
4. Riporta all'utente sia le aperte sia le chiuse. L'elenco di ciò che non lo riguarda è metà del valore.
