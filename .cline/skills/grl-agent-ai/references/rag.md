---
name: rag
description: Quando serve RAG e quando no, e perché la qualità sta quasi tutta nel retrieval e non nella generazione
code: RG
added: 2026-08-07
type: prompt
---

# Recupero e RAG

## Cosa vuol dire riuscirci

L'utente ha un impianto di recupero che **trova davvero il passaggio giusto**, sa misurarlo separatamente dalla risposta generata, e sa quali documenti può mostrare a chi. Oppure — esito altrettanto buono — sa che RAG qui non serve.

Il consumatore è chi deve rispondere a domande su un corpus di documenti che non stanno tutti nel contesto.

## Il principio da cui discende tutto

**La qualità di un sistema RAG è quasi tutta nel retrieval, non nella generazione.** Se il passaggio con la risposta non arriva nel contesto, nessun modello e nessun prompt possono rimediare: il modello o dice di non sapere, o inventa. Quasi tutte le sessioni che iniziano con «il modello risponde male» finiscono con un problema di recupero.

La domanda che smonta il problema:

> **Su venti domande vere, in quante il passaggio che contiene la risposta è fra i primi risultati recuperati?**

Finché non c'è questo numero, ogni modifica al prompt è alla cieca.

## Prima: serve davvero RAG?

| Situazione | Cosa fare |
| ---------- | --------- |
| Pochi documenti stabili che stanno interi nel contesto | **niente RAG**: mettili nel prompt, attiva il caching sulla parte stabile. Zero infrastruttura, zero problema di recupero |
| Documenti tanti ma la domanda arriva sempre con un filtro noto (un cliente, un prodotto, un anno) | filtra prima, e spesso ricadi nel caso sopra |
| Corpus grande, domande aperte | RAG |
| Il corpus è un database strutturato | non è RAG: è una query. Eventualmente il modello scrive la query, ma i dati vengono dal database |

La soglia pratica non è un numero di documenti: è **se il materiale rilevante per una singola domanda sta nel contesto senza far esplodere costo e latenza**.

## I pezzi, in ordine di impatto

**1. Chunking.** Si taglia per **struttura del documento** — sezione, paragrafo, riga di tabella, articolo — non per numero fisso di caratteri. Un taglio a 500 caratteri spezza una frase a metà e produce chunk che non rispondono a niente.

- Overlap fra chunk contigui: serve a non perdere ciò che sta a cavallo del taglio. Costa spazio nell'indice e un po' di ridondanza nei risultati.
- **Metadati su ogni chunk**: documento di origine, sezione, data, autore, permessi. Sono ciò che permette di filtrare prima di cercare, ed è la leva più economica di tutte.
- Chunk troppo piccoli perdono il contesto, troppo grandi diluiscono il segnale. Se un chunk contiene tre argomenti, il suo embedding non rappresenta bene nessuno dei tre.

**2. Embedding.** Il modello di embedding conta più di quanto si creda e va scelto su tre criteri: lingua (molti modelli sono deboli sull'italiano), dimensione del vettore (costo di memoria e di ricerca), e lunghezza massima in ingresso. **Cambiare modello di embedding obbliga a reindicizzare tutto.**

**3. Dove metti i vettori.**

| Opzione | Quando è la risposta giusta | Cosa costa |
| ------- | --------------------------- | ---------- |
| Il database che hai già (`pgvector` su Postgres) | quasi sempre, se hai Postgres. Filtri, permessi e transazioni sono già lì | prestazioni inferiori su corpus molto grandi |
| Vector store dedicato | corpus grande, ricerca vettoriale come funzione centrale del prodotto | un sistema in più da gestire, sincronizzare e pagare — è materia di Bruno |
| Indice full-text esistente | il corpus è testo con termini precisi (codici, nomi, sigle) | non cattura i sinonimi |

**4. Ricerca ibrida.** Denso (embedding) più lessicale (BM25 o full-text) battono quasi sempre il denso da solo: la ricerca lessicale trova i codici prodotto, i nomi propri e le sigle che l'embedding sfuma. Costa una seconda ricerca e una fusione dei risultati.

**5. Reranking.** Si recupera largo (venti-cinquanta chunk) e si riordina con un modello di rerank, tenendo i primi pochi. È la leva più efficace dopo il chunking. Costa una chiamata in più e latenza.

**6. Filtri per permessi.** Il filtro sui permessi si applica **nella query di recupero**, non dopo la generazione. Un RAG che indicizza tutto e filtra le risposte a valle è un sistema che ha già letto documenti che l'utente non poteva vedere. Chi può vedere cosa è materia di **Kai**; se i documenti contengono dati personali, la retention e la base giuridica sono di **Vera**.

## Come si valuta il retrieval, separatamente

Set di venti-cinquanta domande vere, e per ciascuna il chunk (o il documento) che contiene la risposta.

- **Recall@k**: in quante domande il chunk giusto è fra i primi *k*. È la misura che conta.
- Se recall@10 è basso, il problema è chunking, embedding o filtri. Non toccare il prompt.
- Se recall@10 è alto ma recall@3 è basso, serve reranking.
- Se recall è alto e la risposta è comunque sbagliata, allora è la generazione: vedi *Output affidabile*.

## Le citazioni

La risposta deve poter mostrare **da dove viene**: documento, sezione, e possibilmente il passaggio. Non è una funzione estetica — è l'unico modo per cui una persona può verificare senza rileggere tutto, ed è la contromisura più efficace all'invenzione. Serve che i metadati arrivino fino all'output: va deciso al momento del chunking, non alla fine.

## Forma dell'output

Prima la verifica: serve RAG qui, sì o no, con il motivo. Se sì: una riga per ciascuno dei pezzi (chunking, embedding, store, ibrido, rerank, filtri) con la scelta consigliata e cosa costa. Poi il numero da misurare per primo. Se il problema portato è «risponde male», il primo passo è sempre misurare il recall.

## Trappole

- **Aumentare il modello quando il problema è il recupero.** Passare a un modello più grande e più caro non fa comparire nel contesto il passaggio mancante.
- **Chunking cieco a numero fisso di caratteri**, senza guardare com'è fatto il documento.
- **Reindicizzazione mai fatta.** I documenti cambiano; l'indice resta fermo e nessuno se ne accorge. Serve un processo, e serve sapere quando è passato l'ultima volta.
- **Nessun metadato sui chunk.** Si scopre dopo, quando serve filtrare per cliente o per data, e vuol dire rifare l'indice.
- **Trattare l'iniezione di istruzioni dentro i documenti recuperati.** È una superficie di attacco reale, ed è di Kai: nominala e fermati.
