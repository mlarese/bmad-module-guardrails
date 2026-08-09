---
name: ricerca-live
description: Verifica fonti correnti, versioni, limiti, prezzi, supporto e stato dei database prima di una raccomandazione.
code: RL
added: 2026-08-09
type: prompt
---

# Ricerca live

## Esito

Una raccomandazione di database con evidenze aggiornate, data di verifica, versione o edizione
esplicita e confini chiari su ciò che la fonte dimostra. Il lettore deve poter distinguere una
capacità osservata da un'inferenza e capire quando la decisione va riaperta.

## Gerarchia delle fonti

- Documentazione ufficiale del motore o del servizio: semantica, transazioni, indici, replica,
  compatibilità, limiti e procedure supportate.
- Release notes, changelog e lifecycle: feature nuove, deprecazioni, correzioni e versioni
  mantenute.
- Pricing, quota, regioni, SLA e status page del piano preciso: costo e disponibilità correnti.
- Benchmark indipendenti riproducibili: solo con versione, hardware, dataset, query, concorrenza
  e metodologia leggibili.
- Forum, blog e post: utili per scoprire una domanda, mai prova unica di un comportamento o di
  una classifica.

## Provenienza minima

Per ogni affermazione instabile conserva in modo leggibile:

| Campo | Contenuto |
| --- | --- |
| Affermazione | cosa stai sostenendo, in una frase misurabile |
| Fonte | URL diretto, preferibilmente pagina primaria |
| Verifica | data della sessione e versione/edizione/regione |
| Prova | il passaggio, la tabella o il dato che la fonte sostiene |
| Non prova | ciò che la fonte non autorizza a concludere |
| Rischio | cosa può rendere la conclusione obsoleta |

Non trasformare «supporta X» in «è più veloce di Y». Una capacità documentata, una prestazione
misurata e una scelta raccomandata sono tre affermazioni diverse.

## Quando la ricerca non riesce

Se il web non è disponibile, scrivi `ricerca live non disponibile` e continua solo sui principi
stabili o su un piano di verifica. Non citare una versione come corrente, non dare prezzi attuali,
non dichiarare un prodotto migliore e non nascondere il limite dietro una frase generica.
