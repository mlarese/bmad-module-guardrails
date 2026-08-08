# Fonti live per gli aggiornamenti legali

Questi URL sono punti di ingresso, non una cache. A ogni run apri la pagina corrente e registra
la data di accesso. Un risultato è “ufficiale” solo se proviene dall'ente che pubblica l'atto o
dal registro che ne dichiara lo stato.

| Ambito | Fonte live | Uso | Regola |
| --- | --- | --- | --- |
| Pubblicazione italiana | [Gazzetta Ufficiale](https://www.gazzettaufficiale.it/) | leggi, decreti, atti pubblicati e serie | prevale per il testo ufficiale in caso di discordanza |
| Testo vigente italiano | [Normattiva](https://www.normattiva.it/) | versioni vigenti e multivigenti | utile per il consolidato, da confrontare con la Gazzetta |
| Iter parlamentare | [Parlamento](https://www.parlamento.it/), [Camera](https://www.camera.it/), [Senato](https://www.senato.it/) | disegni di legge, emendamenti, votazioni, testi approvati | “presentato” non significa approvato né vigente |
| Unione europea | [EUR-Lex](https://eur-lex.europa.eu/), [CURIA](https://curia.europa.eu/site/) | regolamenti, direttive, decisioni e sentenze UE | distinguere pubblicazione, entrata in vigore e termine di recepimento |
| Giurisprudenza italiana | [ItalgiureWeb](https://www.italgiure.giustizia.it/index_it.asp?lang=it) | sentenze e massime disponibili | citare numero, data e organo; non confondere massima e motivazione |
| Giurisprudenza pubblica | [Corte costituzionale](https://www.cortecostituzionale.it/), [Giustizia amministrativa](https://www.giustizia-amministrativa.it/) | decisioni e comunicazioni degli organi competenti | aprire sempre il provvedimento, non solo la notizia |
| Autorità e ministeri | sito ufficiale dell'ente competente | circolari, provvedimenti, bollettini, FAQ e scadenze | l'ente emittente è la fonte primaria |
| Territorio o settore | portale istituzionale regionale, comunale o dell'autorità di settore | atti locali e regole speciali | chiedere territorio/settore se cambiano l'applicabilità |

I portali professionali possono fornire lead o interpretazioni, ma non chiudono il verdetto:
in caso di conflitto si torna all'atto ufficiale, alla pubblicazione e alla versione vigente.
Non citare snippet, risultati di motori di ricerca o aggregatori come prova.

## Controllo della versione

Per ogni atto trovato, apri sia la pubblicazione originale sia il testo vigente/multivigente o
l'archivio dell'ente competente. Cerca l'identificativo e il titolo insieme a `modifica`,
`sostituisce`, `abroga`, `proroga`, `rettifica`, `conversione`, `attuazione`, `entrata in vigore`
e `decorrenza`. Registra nel source appendix `published_at`, `effective_at`, `last_modified` (se
esposto), `accessed_at`, la fonte primaria, la fonte indipendente e l'eventuale atto successivo.

Una pagina ufficiale priva di testo corrente, stato o data non certifica da sola che la regola sia
ancora vigente. Se la pagina è inaccessibile o la successione non è ricostruibile, il finding deve
restare `unverified`/`supersession_risk` e la copertura del run deve rifletterlo.
