---
name: ai-act-e-gdpr
description: I punti in cui l'AI Act tocca i dati personali, e cosa cambia davvero nel trattamento
code: AIG
added: 2026-08-07
type: prompt
---

# AI Act e GDPR

**Verificato il 7 agosto 2026** su AI Act Service Desk e Garante. Se il punto è recente o di confine, ricontrolla e dichiara cosa hai riverificato.

## Il risultato

L'utente sa se l'AI Act cambia qualcosa nel **suo** trattamento. Quasi sempre non cambia niente e il GDPR resta quello di prima: è l'esito più frequente e si dice per primo.

**L'AI Act non deroga al GDPR.** Nessuno degli articoli qui sotto è una base giuridica. Se una risposta suona come «l'AI Act me lo consente», è sbagliata.

## I punti di contatto

| Punto | Chi riguarda e cosa dice davvero | L'errore da smontare |
| ----- | -------------------------------- | -------------------- |
| **Art. 10(5) AI Act** — dati per correggere i bias | solo i **fornitori** di sistemi ad alto rischio, e solo se strettamente necessario, con garanzie: limiti di accesso, pseudonimizzazione, cancellazione, divieto di trasmissione a terzi | «per misurare il bias posso raccogliere etnia e religione». Non se sei utilizzatore, e comunque non prima di aver dimostrato che senza non si può fare |
| **Art. 59 AI Act** — sandbox | casi ristretti, dentro una sandbox nazionale autorizzata, per finalità di interesse pubblico rilevante. Per un prodotto commerciale ordinario è irrilevante | «in sandbox il GDPR non si applica» |
| **Art. 27 AI Act** — FRIA | **organismi di diritto pubblico**, privati che **erogano servizi pubblici**, e utilizzatori dei sistemi dell'Allegato III punti **5(b)** (merito creditizio) e **5(c)** (assicurazioni vita e salute). Escluso il punto 2 | «è la nuova DPIA per chiunque usi l'AI» |
| **Art. 86 AI Act** — spiegazione | la persona colpita da una decisione presa dall'utilizzatore **sulla base dell'output** di un sistema ad alto rischio dell'Allegato III (escluso il punto 2), che produce effetti giuridici o incide significativamente **in modo negativo** su salute, sicurezza o diritti fondamentali. Dà diritto a spiegazioni chiare sul **ruolo del sistema** nella decisione e sugli elementi principali di questa | «l'utente può chiedermi i criteri del modello». Il diritto non arriva all'algoritmo |
| **Art. 22 GDPR** — decisione automatizzata | non è un divieto assoluto: contratto, consenso esplicito e legge lo permettono, con garanzie fra cui l'intervento umano | «le decisioni automatiche sono vietate» |
| **Art. 15(1)(h) GDPR** — accesso | dà le informazioni sulla logica del trattamento nei casi dell'art. 22. È la via che di solito si applica davvero, prima di scomodare l'art. 86 | «non c'è nessun diritto alla spiegazione» |
| **Art. 73 AI Act** — incidenti gravi | obbligo del **fornitore** del sistema ad alto rischio, non tuo se sei utilizzatore | «ogni anomalia va notificata» |

## FRIA e DPIA

Due obblighi distinti. La DPIA (art. 35 GDPR) dipende dal rischio per gli interessati → `references/pre-dpia.md`. La FRIA dipende dal ruolo e dal sistema, secondo l'elenco qui sopra.

Il regolamento è esplicito: la FRIA **completa** la DPIA, non la sostituisce. Dove entrambe sono dovute, la DPIA già fatta copre parte del lavoro; dove la FRIA non è dovuta, non si fa «per sicurezza».

## Le due notifiche che si confondono

| | Data breach — art. 33 GDPR | Incidente grave — art. 73 AI Act |
| --- | --- | --- |
| Presupposto | violazione di sicurezza sui dati personali | incidente grave come definito dal regolamento |
| Chi notifica | il titolare | il **fornitore** del sistema ad alto rischio |
| A chi | autorità di controllo — in Italia il Garante | autorità di vigilanza del mercato |
| Termine | 72 ore | 15 giorni; **2 giorni** per violazione diffusa o lesione di diritti fondamentali; **10 giorni** in caso di decesso |

**Se sei utilizzatore, l'art. 73 non ti fa notificare: ti fa avvisare il fornitore**, ed è quell'avviso a far partire i suoi termini. Non farlo lo espone e ti lascia scoperto sul contratto.

Sullo stesso fatto le due notifiche possono scattare insieme, e resta a parte l'informazione agli interessati dell'art. 34 GDPR.

## Chi è l'autorità

La legge 132/2025 assegna ruoli ad AgID e ACN per l'AI Act, **senza togliere al Garante la competenza sui dati personali** né alle autorità di settore la loro. Se la questione è un trattamento, l'interlocutore resta il Garante — anche quando il sistema è un sistema di IA.

## I precedenti del Garante, citati bene

Mai «il Garante ha vietato ChatGPT». Con data, oggetto e stato:

- **31 marzo 2023** — limitazione provvisoria del trattamento verso OpenAI; il servizio è tornato disponibile dopo le misure.
- **Provvedimento n. 755 del 2 novembre 2024**, reso noto il 20 dicembre 2024 — 15 milioni di euro e una campagna informativa di sei mesi, per mancata notifica di una violazione, assenza di base giuridica per l'addestramento, difetto di trasparenza e mancata verifica dell'età. **Il Tribunale di Roma ne ha sospeso l'esecuzione con ordinanza del 21 marzo 2025**: la sanzione non è definitiva, e citarla come tale è un errore.
- **8 marzo 2024** — richiesta di informazioni su Sora: atto istruttorio, non decisione.

## Come lo dici

Una riga per punto toccato, verdetto in testa. Quattro rami ricorrenti:

- **utilizzatore, sistema non ad alto rischio, nessun dato personale nell'addestramento** → il GDPR resta quello di prima, l'AI Act non aggiunge obblighi sul tuo trattamento. In una riga.
- **fine-tuning su dati propri** — il caso più frequente: l'AI Act non c'entra, il GDPR sì. La domanda è la base giuridica del riuso per addestramento e la compatibilità con la finalità originaria → `references/base-giuridica.md`. Che dati possano entrare nel prompt e nei log sta in `references/dati-fuori-posto.md`.
- **fornitore e utilizzatore coincidono** — chi sviluppa e usa in casa il proprio sistema cumula gli obblighi di entrambi i ruoli: la FRIA, se dovuta, non si annulla perché il sistema è tuo.
- **il bias si misura su dati sintetici o anonimi** → non ci sono dati personali, e l'art. 10(5) non entra nemmeno in gioco. È la strada più economica: proponila prima dell'eccezione.

Il capo V resta tuo: log, sorveglianza umana e assistenza di un fornitore extra-UE sono trasferimenti da valutare, e l'AI Act non li tocca.

## Dove ti fermi

Categoria di rischio, ruolo ai fini del regolamento, calendario, obblighi documentali dell'alto rischio, trasparenza dell'art. 50, manleve, massimali dell'art. 99 e responsabilità civile sono di **Aldo**: sull'AI Act è lui il riferimento unico. Nominalo in una riga e fermati.
