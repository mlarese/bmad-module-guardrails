---
name: vettoriale-e-ibrido
description: Decide se usare il database principale o un motore vector/hybrid e definisce indice, filtri, aggiornamenti e valutazione.
code: VH
added: 2026-08-09
type: prompt
---

# Vector e ricerca ibrida

## Esito

Una scelta di retrieval che tiene insieme embedding, metadati, filtri, keyword search, precisione,
recall, latenza, aggiornamenti, durabilità, multi-tenancy, costo e operabilità. Un vector store
non è automaticamente un buon sistema documentale e una pipeline RAG non è automaticamente un
motivo per introdurne uno.

## Prima decisione

Chiedi se il dato vettoriale vive insieme a quello transazionale e se volume, p95, concorrenza,
filtri e frequenza di aggiornamento giustificano un servizio separato. Se PostgreSQL con pgvector,
MongoDB, Redis, Elasticsearch o OpenSearch copre il target e riduce sincronizzazione, partire da
lì è una scelta valida. Qdrant, Milvus, Weaviate, Pinecone, Vespa, Chroma e LanceDB entrano quando
il workload, la scala, la modalità gestita o le primitive di ricerca pagano il confine.

## Cosa verificare live e misurare

- metrica e normalizzazione: cosine, inner product o L2, dimensione e modello di embedding;
- indice ANN disponibile, memoria/storage, build e aggiornamento, delete e compaction;
- filtri booleani e numerici, full-text/BM25, sparse+dense, reranking e fusione dei risultati;
- recall@k, nDCG/precisione, p50/p95/p99, concorrenza, cold start e costi di query/indexing;
- replica, backup/restore, multi-tenancy, isolamento, regioni, SLA, lock-in e import/export;
- comportamento quando il documento sorgente cambia o viene cancellato.

Distingui il benchmark del motore dal risultato applicativo: la qualità del retrieval dipende anche
da chunking, filtri, embedding, query rewrite e reranker. La scelta del modello e la valutazione
della pipeline RAG sono di Enzo; Dario decide la persistenza e il failure mode dello store.
