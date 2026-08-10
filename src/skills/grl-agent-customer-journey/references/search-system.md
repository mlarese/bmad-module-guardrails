---
name: search-system
description: "Suggerisce un sistema di ricerca coerente con cliente, luogo, business e storia del percorso, distinguendo discovery, ricerca interna e retrieval AI."
code: SS
added: 2026-08-10
type: internal-capability
---

# Search system contestuale

Un search system è il modo in cui una persona esprime un bisogno, trova un insieme di possibilità,
capisce perché un risultato è pertinente e prosegue anche quando la prima ricerca non funziona.
Non è solo una casella di testo e non è automaticamente SEO, ricerca full-text o RAG.

## Prima identifica il sistema

Dichiara quale dei tre casi è in gioco — anche più di uno, se sono collegati:

1. **Discovery esterna:** il cliente deve trovare il business, la categoria o il contenuto fuori
   dal prodotto. Le domande e il contesto passano a Nora per SEO, Search Console e regole correnti.
2. **Ricerca interna:** il cliente cerca un'offerta, una sede, un prodotto, un servizio o una prova
   dentro sito, catalogo, portale o app. Marea definisce intenti, lessico, risultati e fallback; Dario
   decide dati, indice e prestazioni, Sally l'interazione.
3. **Retrieval semantico o RAG:** il sistema recupera documenti, conoscenza o fonti per una risposta
   generata. Marea definisce domanda, contesto e criterio di utilità; Enzo decide chunking, retrieval,
   eval, tool e modello.

Se il problema non richiede ricerca — bastano navigazione, categorie note o una regola — dillo. La
soluzione più semplice è una capacità, non una riduzione del valore del progetto.

## Modello minimo

Costruisci il modello in questo ordine concettuale:

| Elemento | Domanda da chiudere |
| --- | --- |
| Intento | Cosa vuole ottenere il cliente con parole proprie? Quale tappa del journey sta vivendo? |
| Lessico | Quali termini, sinonimi, errori, lingue o nomi locali usa? Quali sono dichiarati e quali da ricercare? |
| Contesto | Location, distanza, orario, stagione, disponibilità, accessibilità, canale e stato del cliente: quali servono davvero? |
| Entità | Cosa viene cercato: servizio, prodotto, sede, persona, evento, prova, documento o domanda? |
| Filtri | Quali filtri aiutano la decisione senza creare una tassonomia ingestibile? |
| Risultato | Quale prova deve mostrare una card o una risposta per essere scelta? Fonte e aggiornamento. |
| Ranking | Quali segnali di pertinenza sono ammessi e verificabili? Non usare popolarità come scorciatoia. |
| Fallback | Cosa succede con zero risultati, query ambigua, luogo non noto o disponibilità scaduta? |
| Misura | Successo, zero-result, riformulazione, click utile, contatto, conversione assistita e abbandono. |

## Cliente e luogo nel ranking

Usa location e collocazione del business solo quando hanno un legame osservabile con la decisione.
Preferisci segnali spiegabili — distanza dichiarata, area servita, orario, disponibilità, accesso,
lingua o categoria — a inferenze opache su identità, potere d'acquisto o preferenze personali.

Per un business locale distingui almeno:

- dove la persona si trova o si muove;
- dove si trova l'offerta e quanto è raggiungibile;
- quale contesto rende pertinente il risultato: tempo, occasione, servizio, urgenza o prova;
- cosa resta vero quando la persona cambia zona o usa il canale digitale.

Non chiedere la posizione precisa per default. Spiega l'uso, raccogli solo il necessario e passa
geolocalizzazione, consenso e profilazione a Vera.

## Output della proposta

Consegna una scheda con:

```text
Tipo: discovery esterna | ricerca interna | retrieval semantico/RAG
Utente e momento del journey:
Domande reali da coprire:
Entità e vocabolario:
Contesto usato e motivo:
Filtri e segnali di ranking spiegabili:
Risultato minimo utile:
Zero-result, ambiguità e fallback:
Fonti, freschezza e owner:
Metriche, finestra e criterio di successo:
Rischi privacy/accessibilità/diritti:
Handoff tecnico:
```

Proponi da una a tre ipotesi testabili, non una piattaforma per inerzia. Per ogni ipotesi indica
baseline, campione o fonte, metrica, finestra, soglia e criterio di stop. Se non ci sono dati,
scrivi `non noto` e il piano minimo per ottenerli.

## Confini

Nora presidia le regole SEO live, il crawl, l'indicizzazione e Search Console. Dario presidia
schema, indice, query, prestazioni, affidabilità e migrazione. Enzo presidia retrieval AI, RAG,
embedding, tool e valutazione del modello. Marea non dichiara un risultato tecnico o commerciale
senza l'evidenza e l'handoff corretto.
