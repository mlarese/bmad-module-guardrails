---
name: deep-module-design
description: Valutare se un confine nasconde complessità reale e se il suo seam è verificabile senza accoppiare i test all'implementazione.
code: DM
added: 2026-08-09
type: prompt
---

# Deep-module design

## Vocabolario operativo

- **Modulo**: una responsabilità che il team può nominare e cambiare senza aprire tutto il
  sistema.
- **Interfaccia**: ciò che il resto del codice deve conoscere; è anche la superficie su cui si
  prova il comportamento.
- **Implementazione**: il lavoro nascosto dietro l'interfaccia — policy, query, parsing, retry,
  transazioni o integrazioni — non il suo nome.
- **Profondità**: valore del lavoro nascosto meno il costo di imparare e attraversare il confine.
- **Seam**: punto osservabile in cui una prova può sostituire o esercitare il modulo senza
  conoscere i dettagli interni.
- **Adapter**: traduzione fra due contratti già reali; non un contenitore preventivo per una
  seconda implementazione che non esiste.

## Domande di revisione

1. Quale decisione costosa o volatile nasconde questo confine?
2. Quale chiamata pubblica dimostra il valore senza ispezionare l'interno?
3. Il test prova il contratto o ripete l'implementazione passo per passo?
4. Se cancelliamo l'interfaccia o l'adapter, quale comportamento diventa impossibile da
   mantenere o da verificare?
5. Esistono due implementazioni reali, team/deploy separati o un profilo di carico indipendente?

Un confine che non supera queste domande non va “migliorato” aggiungendo pattern: va semplificato
oppure lasciato com'è se il suo costo futuro è trascurabile.
