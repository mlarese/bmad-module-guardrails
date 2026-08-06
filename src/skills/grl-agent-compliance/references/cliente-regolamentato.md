---
name: cliente-regolamentato
description: Anticipare i requisiti che un committente di settore regolamentato imporrà, prima che li imponga
code: CLR
added: 2026-08-06
type: prompt
---

# Vincoli del cliente regolamentato

## Cosa deve essere vero alla fine

Il team conosce in anticipo le richieste che arriveranno dal committente, sa quali di quelle sono **strutturali** — cioè costano una riscrittura se scoperte tardi — e quali si soddisfano a fine progetto con un documento. Chi vende sa cosa promettere; chi progetta sa cosa non può decidere da solo.

## Perché è una capacità a sé

Questi requisiti non sono obblighi di legge del fornitore: sono obblighi del cliente che scendono per contratto. La distinzione va detta esplicitamente, altrimenti il team crede di essere soggetto a DORA o a NIS2 e sovradimensiona.

Ciò che cambia è la trattabilità. Un obbligo di legge non si negozia; un requisito contrattuale sì — e sapere quali si possono ridurre, e in cambio di cosa, è metà del valore di questa consultazione.

## Come ci arrivi

Serve il settore del committente e cosa gli stai consegnando. Poi ricava, da quel settore, i requisiti tipici — carica `references/soglie-applicabilita.md` per la norma che li genera, e verifica sul web se il settore ha avuto novità recenti.

Le famiglie che ricorrono quasi sempre, quale che sia il settore:

| Famiglia | Cosa chiedono | Strutturale? |
| --- | --- | --- |
| Localizzazione dei dati | dove risiedono e dove transitano; spesso «solo UE» | sì — decide la scelta del cloud |
| Diritto di audit e ispezione | accesso a documentazione, log, ambienti; a volte visita in sede | in parte |
| Livelli di servizio e continuità | RTO, RPO, piani di continuità e di ripristino testati | sì |
| Uscita e reversibilità | export dei dati, assistenza alla migrazione, sopravvivenza del servizio alla fine del contratto | sì |
| Subappalto e catena di fornitura | elenco dei sub-fornitori, preavviso, diritto di veto | in parte |
| Sicurezza del ciclo di sviluppo | ambienti separati, revisione del codice, gestione delle vulnerabilità, a volte certificazioni | in parte |
| Segnalazione degli incidenti | tempi stretti verso il cliente, che a sua volta deve rispettarne di più stretti verso l'autorità | no, ma cambia i processi |
| Tracciabilità e conservazione | log immodificabili, tempi di conservazione fissati dal settore | sì |

## Cosa consegni

Un elenco corto ordinato per **costo del ritardo**: prima ciò che se non è deciso ora costa una riscrittura, poi ciò che si sistema alla fine. Per ognuno, una riga su cosa fare adesso.

Chiudi con la cosa che quasi nessuno chiede in tempo: farsi dare il capitolato o l'allegato tecnico del cliente prima di firmare, non dopo.

## Confini

Le clausole così come sono scritte, la trattativa, le penali e la ripartizione delle responsabilità sono di **Aldo**. Il DPA e i sub-responsabili del trattamento sono di **Aldo** e **Vera**. Tu dici quali requisiti arriveranno e perché; chi li negozia non sei tu.
