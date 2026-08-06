---
name: owasp-design
description: Quali pattern insicuri noti si applicano a questo progetto, intercettati prima che il codice li fissi
code: OWASP
added: 2026-08-06
type: prompt
---

# Revisione del design contro i pattern insicuri noti

## Cosa vuol dire riuscirci

Il pattern insicuro viene intercettato **prima** di essere scritto, e l'utente riceve solo i punti che riguardano *questo* progetto. Non i dieci di default.

Il consumatore è chi sta per implementare la story o ha appena scritto il design. Vuole sapere cosa cambiare adesso, mentre cambiare costa poco.

## Come si usa la lista, e come no

La OWASP Top 10 è un promemoria per te, non un formato di output. **Non nominarla, non numerarla, non recitarla.** Il metodo è: leggi il design, riconosci il pattern, dillo con le parole del progetto.

I punti si tengono o si scartano in base a cosa il progetto ha davvero:

| Se il progetto ha… | guarda |
| ------------------ | ------ |
| ruoli, permessi, risorse per utente | controllo di accesso rotto — il tema più frequente in assoluto, e materia della capacità `AUTH` se merita di essere approfondito |
| query su database costruite da input | injection: query concatenate, ORM usato in modo grezzo, filtri dinamici |
| upload di file | tipo e dimensione non verificati, percorso costruito dal nome del file, servizio del file caricato dallo stesso dominio |
| URL o webhook forniti dall'utente | SSRF (il server chiama un indirizzo scelto da altri, incluso l'interno della rete) |
| deserializzazione, template dinamici, `eval` | esecuzione di codice per input |
| password gestite in proprio | hashing debole, assenza di limiti sui tentativi, reset che rivela l'esistenza dell'account |
| dati sensibili in transito o a riposo | trasporto in chiaro, cifratura assente dove serve (il *che serve* lo decide Vera, il *come* tu) |
| configurazioni di deploy | default non cambiati, pannelli di amministrazione esposti, CORS permissivo, debug attivo in produzione |
| logging e monitoraggio | nessuna traccia di chi ha fatto cosa sulle azioni che contano |

Se il progetto non ha upload, l'upload non si nomina. Se non c'è un database, l'injection non si nomina.

## Forma dell'output

Per ogni punto trovato: **dove** (file, endpoint, passaggio del design) · **cosa va storto in pratica** · **la correzione minima**. Ordinati per probabilità, come sempre.

Se il design è pulito, dillo in una riga e indica l'unico punto su cui stare attenti in implementazione. Un design senza problemi è un esito frequente e legittimo.

## Trappole

- **La checklist recitata.** Dieci voci di cui otto «non applicabile» è rumore travestito da completezza.
- **La revisione di un design che non esiste ancora.** Se l'input è troppo vago, fai una domanda invece di elencare rischi generici.
- **Ricadere nel threat model.** Qui si guarda il pattern dentro il design; da dove arriverebbe l'attacco è la capacità `TM`.
