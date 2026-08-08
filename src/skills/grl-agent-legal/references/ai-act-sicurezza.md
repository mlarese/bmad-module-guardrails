---
name: ai-act-sicurezza
description: Sicurezza dei sistemi AI — art. 15, uso sicuro da parte del personale, incidenti da notificare e a chi
code: AIS
added: 2026-08-07
type: prompt
---

# Sicurezza

**Data di riferimento: 7 agosto 2026.** Termini e finestre di notifica cambiano: verificali sul web prima di indicarne uno.

Tre domande diverse arrivano con la stessa parola. Riconoscere quale ti è stata fatta è metà della risposta.

| Domanda | Dove va |
| ------- | ------- |
| «Il sistema è abbastanza robusto?» | art. 15 — obbligo del fornitore, sotto |
| «Cosa può fare o non fare chi lo usa?» | uso sicuro del personale, sotto |
| «È successo qualcosa: chi devo avvisare?» | incidenti, sotto |

## Art. 15: accuratezza, robustezza, cybersecurity

Obbligo del fornitore di un sistema ad alto rischio. Tre requisiti distinti, spesso confusi in uno.

| Requisito | Cosa vuole |
| --------- | ---------- |
| Accuratezza | un livello **dichiarato nelle istruzioni d'uso**, con le metriche usate per misurarlo |
| Robustezza | il sistema regge errori, guasti e input imprevisti; ridondanza o piani di ripiego dove serve. I sistemi che continuano ad apprendere in esercizio non devono produrre loop di retroazione |
| Cybersecurity | resistenza ai tentativi di alterare l'uso o il comportamento del sistema **sfruttando le sue proprietà di modello**: avvelenamento dei dati di addestramento o dei pesi, input costruiti per ingannarlo, attacchi che estraggono il modello o i dati |

La cybersecurity dell'art. 15 non è quella dell'infrastruttura. Un cluster blindato con un modello avvelenato è conforme sul perimetro e non conforme qui: sono due controlli separati, e vanno documentati separatamente.

**Cosa ne fai in pratica.** L'accuratezza dichiarata è la cosa più utile del pacchetto, in due direzioni: se sei fornitore, è il tetto che ti protegge — un sistema usato oltre le prestazioni dichiarate è usato in modo difforme, e la responsabilità si sposta; se sei utilizzatore, è il numero che devi pretendere prima di firmare, perché senza non puoi dimostrare l'uso conforme né dimensionare la sorveglianza umana. Il fornitore che non la dichiara ti sta lasciando la sua parte di rischio.

Le clausole che ne discendono — livelli minimi, preavviso sui cambi di modello, manleva — stanno in `references/ai-act-responsabilita-e-contratti.md`.

## Uso sicuro da parte del personale

È il contenuto d'aula dell'art. 4 e la sostanza della AI policy. Non è materia di legge: è la parte che evita i danni che si verificano davvero.

**Cosa non entra in un prompt.** Dati personali di clienti e dipendenti, segreti industriali, codice proprietario, documenti coperti da NDA, contratti, listini. La ragione da dire in aula non è la sanzione: è che l'informazione uscita non rientra, e che il segreto commerciale perde tutela proprio perché ha smesso di essere segreto.

**L'output non è una fonte.** Un modello produce testo plausibile, non testo vero. Numeri, norme, citazioni e riferimenti si verificano prima di usarli. Chi manda l'output al cliente risponde dell'output: lo strumento non è mai un soggetto responsabile, e questa frase in aula vale mezz'ora di teoria.

**La sorveglianza umana è una persona che può dire di no.** Se chi rivede non ha tempo, competenza o autorità per fermare la decisione, il presidio non esiste — esiste il modulo che dice che esiste, e in ispezione è peggio di niente.

**Strumenti autorizzati.** L'elenco per nome, e una via rapida per aggiungerne uno. Il divieto senza alternativa produce uso nascosto, che è la condizione peggiore: rischio identico, nessuna visibilità.

## Incidenti: chi si avvisa, e quando

Regimi diversi con finestre diverse. Il rischio è applicare la finestra sbagliata: si guarda **cosa** è successo, non chi sei.

| Cosa è successo | Regime | Chi si avvisa |
| --------------- | ------ | ------------- |
| Un sistema di IA ad alto rischio ha causato un danno grave a salute, diritti fondamentali, beni o infrastrutture | AI Act art. 73 — obbligo del fornitore, con termini brevi e più stringenti in caso di decesso o violazione diffusa | autorità di vigilanza del mercato (in Italia ACN) |
| Sono stati esposti dati personali | GDPR, 72 ore | Garante, e gli interessati se il rischio è elevato → **Vera** |
| Vulnerabilità sfruttata o incidente grave su un prodotto con elementi digitali | Cyber Resilience Act, dal 11 settembre 2026 | ENISA e CSIRT nazionale |
| Incidente significativo in un soggetto NIS2 | NIS2 | CSIRT Italia via portale ACN |

I regimi si cumulano: lo stesso evento può far scattare due notifiche a due autorità con due termini. Chi ne fa una sola e pensa di aver chiuso, non ha chiuso.

**La cosa da fissare prima dell'incidente** è chi decide che è un incidente. Le finestre sono corte e partono dal momento in cui si è venuti a conoscenza del fatto: se la decisione risale una catena gerarchica, il termine è già scaduto quando arriva in cima. Una persona con nome e un canale, scritti nella policy.

## Quando ti chiedono di sicurezza informatica in generale

Capita in consulenza e in aula: dall'AI Act si scivola su NIS2, backup, password, ransomware. Rispondi su cosa l'azienda deve fare e di cosa risponde, senza rimbalzare.

Due confini restano:

- **se NIS2 o il CRA si applichino** a quell'azienda è una domanda di soglie, ed è di **Nils**. Rispondere «probabilmente sì» a una soglia è l'errore che non si recupera;
- **come si mette in sicurezza un sistema** — prompt injection, filtraggio degli output, superficie d'attacco dell'integrazione, vulnerabilità nelle dipendenze, gestione dei segreti — è di **Kai**. Tu dici cosa è dovuto, lui dice come si fa.

Su tutto il resto — obblighi, doveri di chi decide, catena contrattuale, incidenti — parli tu.
