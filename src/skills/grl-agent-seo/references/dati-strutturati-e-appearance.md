# Dati strutturati e search appearance

## Risultato

Una scelta sobria e verificabile: markup solo quando esiste un tipo che descrive davvero la pagina,
proprietà coerenti con ciò che vede l'utente, test eseguiti e monitoraggio dopo il deploy.

## Decisione

1. Identifica il contenuto principale della pagina e la feature di Search che potrebbe descriverlo.
2. Consulta la guida ufficiale della feature corrente: requisiti, proprietà, qualità e limiti.
3. Scrivi dati completi ma non inventati; non marcare contenuto nascosto, falso, irrilevante o più
   ricco di quello visibile.
4. Valida il markup con il test appropriato e controlla la pagina renderizzata, non solo una stringa
   nel sorgente.
5. Dopo il deploy, usa URL Inspection e i report disponibili in Search Console per cercare errori,
   cambiamenti di copertura e idoneità.

JSON-LD è spesso il formato più manutenibile, ma il formato non risolve un tipo sbagliato o dati non
veritieri. Schema.org può aiutare a capire il vocabolario; per il comportamento in Google Search la
fonte decisiva è Google Search Central.

## Cose da dire esplicitamente

- markup valido non garantisce visualizzazione come rich result;
- una proprietà consigliata non va riempita con un valore inventato solo per eliminare un warning;
- un tipo più specifico non è migliore se non corrisponde al contenuto principale;
- la feature, il nome delle proprietà e le linee guida possono cambiare: `as_of` è obbligatorio per
  una raccomandazione basata su documentazione corrente.

## I tipi dismessi non sono marcati: sono assenti

⚠️ La [gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
elenca i tipi supportati e **non segnala i dismessi**: semplicemente non ci sono. Per sapere se un
tipo è stato ritirato e quando, la fonte è il
[changelog](https://developers.google.com/search/updates), non la gallery.

Dismissioni verificate, `as_of` 2026-08-08:

| Tipo | Data | Nota |
| ---- | ---- | ---- |
| HowTo | 2023-05-14 | «no longer shown in search results, on both desktop and mobile devices» |
| Sitelinks search box | 2024-11-29 | feature non più disponibile, documentazione ritirata |
| ClaimReview, book actions, course info, estimated salary, learning video, vehicle listing | 2025-06-12 | sei tipi insieme, iniziativa «simplify search results» |
| Special announcement | 2025-07-31 | data propria |
| Practice problems | 2025-11-05 | rimosso da Search Console, Rich Result Test e API da gennaio 2026 |
| **FAQ** | **2026-05-07** | «This feature will no longer appear in Google Search starting May 7, 2026»; documentazione rimossa il 2026-06-15 |

Book, Fact check (ClaimReview) ed Estimated salary **sono esistiti e sono stati dismessi**, non «mai
esistiti»: se l'utente li nomina, non trattarlo come un errore di comprensione.

La fine di FAQ ha lasciato una traccia misurabile: calo delle impressions su Performance e Rich
result dal 7 maggio 2026, registrato fra le anomalie di Search Console. Un calo in quella data non
è necessariamente un problema del sito.

## Funzioni generative: il markup non serve

Google dichiara: «**Structured data isn't required for generative AI search**, and there's no special
schema.org markup you need to add» (`as_of` 2026-07-10). Non proporre markup come leva per comparire
nelle risposte generative. La fonte primaria è la [guida Google alle funzioni generative](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide),
`as_of` 2026-07-10.

Sulla stessa pagina, il controllo che esiste dal **3 giugno 2026**: un toggle in Search Console per
uscire dalle funzioni generative, con il costo dichiarato — chi esce non riceve traffico né
impression da quelle funzioni — e la dichiarazione che non è usato come segnale di ranking altrove.
**La documentazione tecnica non lo menziona**: chi cerca l'opt-out partendo da lì non lo trova.

## Consegna

Produci: tipo scelto e motivo, proprietà richieste/reali, esempio limitato al caso dell'utente,
strumento di validazione, stato del test, piano di monitoraggio e ciò che il markup non può garantire.
