---
name: minimizzazione-retention
description: Decide cosa smettere di raccogliere e per quanto tenere il resto, con un meccanismo che lo faccia rispettare
code: MR
added: 2026-08-06
type: prompt
---

# Minimizzazione e retention

L'esito è duplice: cosa smettere di raccogliere, e per quanto tenere il resto. Il consumatore deve poterlo implementare, quindi la retention si esprime come un numero e un meccanismo — «12 mesi, job notturno che cancella» — mai come «per il tempo necessario».

**Parti dal togliere.** Per ogni dato raccolto chiedi a cosa serve *oggi*, in quale schermata o in quale processo. «Per analisi future» non è una finalità: è un dato da non raccogliere. Il campo che nessuno ha mai letto è il candidato numero uno.

**Poi i tempi.** Cose che i team dimenticano sistematicamente e che devi nominare:

- **Backup e repliche.** Una cancellazione che non li tocca non è una cancellazione. Se scadono da soli, dì entro quanto.
- **Log e code.** Conservano spesso più a lungo del database che dovrebbero servire.
- **Account cancellati.** Cosa resta dopo la cancellazione, e perché resta.
- **I dati che vanno tenuti per obbligo** (fatturazione, contabilità). Vanno separati dal resto, non usati come scusa per tenere tutto.
- **Export e fogli di calcolo** usciti dal sistema. Se esistono, la retention non esiste.

Proponi tempi brevi e difendibili, e un meccanismo che li faccia rispettare da solo: una scadenza applicata dal database, un job, una policy di lifecycle sullo storage. Un tempo scritto in un documento e in nessun altro posto non è una retention.

Se il team decide di tenere di più, va bene: è un rischio accettato, e si registra in `accepted-risks.md` solo dopo conferma esplicita dell'utente.
