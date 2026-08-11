# Eval di `grl-issues`

I casi proteggono il contratto del registro: dire con quale account e su quale repository si è
letto, dichiarare una lettura parziale, non risincronizzare tutto quando basta il delta, e non
scrivere mai su GitHub.

| Caso | Cosa protegge |
| --- | --- |
| `account-dichiarato` | due identità nel keychain non producono letture silenziose sull'account sbagliato |
| `registro-parziale` | il tetto raggiunto si dichiara, non si nasconde |
| `sync-incrementale` | il delta invece della rilettura completa, con i `checked_at` conservati |
| `sessione-e-chiusure` | la chiusura dichiarata a voce si verifica prima di scriverla |
| `nessuna-scrittura-remota` | la skill resta read-only verso GitHub |
| `decisione-ricordata` | quello che è stato deciso non torna in discussione da solo |
| `decisione-senza-autore` | una decisione senza chi e perché non si scrive |
| `stati-derivati` | uno stato solo per issue, con l'ordine di precedenza rispettato |
| `stato-dichiarato-contraddetto` | il fatto letto da GitHub vince sulla dichiarazione a mano |
| `cache-fuori-da-git` | il registro non finisce in un commit per distrazione |

I trigger separano il registro dal verdetto di chiarezza (`grl-issue-readiness`), dalla diagnosi
(`grl-bug-finder`) e dalla configurazione della macchina (Bruno).
