---
name: ai-act-responsabilita-e-contratti
description: Chi risponde se il sistema AI sbaglia, con quale tetto, e quale clausola sposta il rischio sull'altro
code: AIR
added: 2026-08-07
type: prompt
---

# AI Act: responsabilità e contratti

**Verificato il 7 agosto 2026** su AI Act Service Desk ed EUR-Lex. Il Digital Omnibus (Reg. (UE) 2026/1744) è in vigore dal 27 luglio 2026 e ha spostato parte del calendario: prima di usare una data, ricontrollala e dichiara cosa hai riverificato.

## Il risultato

Tre risposte: **chi risponde** verso l'autorità, **fino a quanto**, **quale clausola** sposta il rischio.

Tutto discende dalla categoria di rischio, e la categoria la stabilisci tu: `references/ai-act-classificazione-e-obblighi.md`. Se l'utente non te l'ha data, non chiedergliela come un modulo — falla emergere dalle due domande che la decidono: *il sistema decide qualcosa su una persona?* e *di chi è il sistema?*

## Il ruolo, e come cambia senza volerlo

Il ruolo lo produce il fatto, non il contratto. L'art. 25 elenca i tre modi per diventare fornitore di un sistema che era di un altro:

| Fatto | Effetto |
| ----- | ------- |
| Chiami l'API di un modello di terzi dentro il tuo prodotto | resti utilizzatore |
| **Metti il tuo nome o marchio** su un sistema già immesso sul mercato | diventi fornitore |
| **Modifichi sostanzialmente** un sistema ad alto rischio che resta tale | diventi fornitore |
| **Cambi la finalità prevista** di un sistema non ad alto rischio, e così lo rendi alto rischio | diventi fornitore |
| Immetti sul mercato UE il sistema di un fornitore extra-UE | sei importatore: obblighi propri, più leggeri di quelli del fornitore |

**La clausola che conta è nell'art. 25(2).** Chi cede il ruolo deve cooperare col nuovo fornitore e dargli documentazione e accesso tecnico — **salvo** che abbia escluso espressamente che il sistema venga convertito ad alto rischio. Quell'esclusione si scrive nel contratto, e se manca la cooperazione è dovuta. È la leva da usare in entrambe le direzioni.

**Il fine-tuning non è di per sé modifica sostanziale.** Conta se il sistema resta ad alto rischio e se cambia la finalità prevista. Su cosa puoi dare in pasto al modello e su chi possiede il modello derivato, la risposta sta in `references/dati-e-modelli-ai.md`: le due capacità si leggono insieme.

## I massimali

Servono a una cosa: dimensionare il tetto di responsabilità e la manleva. Non si citano mai come cifra a effetto.

| Violazione | Massimale | Chi lo irroga |
| ---------- | --------- | ------------- |
| Pratiche vietate dell'art. 5 | 35 M€ **o** 7% del fatturato mondiale — **il maggiore** | autorità nazionale |
| Obblighi di fornitore, rappresentante, importatore, distributore, utilizzatore, organismi notificati, trasparenza dell'art. 50 (artt. 16, 22, 23, 24, 26, 31, 33, 34, 50) | 15 M€ o 3% — il maggiore | autorità nazionale |
| Informazioni inesatte, incomplete o fuorvianti alle autorità | 7,5 M€ o 1% — il maggiore | autorità nazionale |
| **Fornitori di modelli per finalità generali** (art. 101) | 15 M€ o 3% — il maggiore | **la Commissione**, non l'autorità nazionale |

**Tre cose che cambiano il numero.**

- **PMI e start-up, art. 99(6): si applica il minore** fra percentuale e importo fisso. È l'inverso della regola generale.
- **Autorità pubbliche, art. 99(8):** è lo Stato membro a decidere se e in che misura sanzionarle. Se il committente è pubblico, il tetto non si presume.
- **Gli obblighi sui dati dell'art. 10 stanno al secondo scaglione**, non al primo: ci arrivano attraverso gli obblighi del fornitore dell'art. 16. Il primo scaglione è solo l'art. 5.

Le sanzioni sulle pratiche vietate sono già applicabili; i poteri sanzionatori delle autorità nazionali sono a regime dal 2 agosto 2026.

## Cosa metti nel contratto

Due categorie diverse, e confonderle fa cedere sulla cosa sbagliata.

**Obblighi di legge riflessi** — il fornitore li ha comunque, tu li pretendi per poterti difendere:

- documentazione tecnica e **istruzioni d'uso**: senza, l'utilizzatore non può dimostrare l'uso conforme;
- per i modelli per finalità generali, la **sintesi sufficientemente dettagliata dei contenuti di addestramento** e la **policy sul diritto d'autore**. Non la pubblicazione del dataset: quell'obbligo non esiste, e chiederlo fa perdere credibilità in trattativa;
- cooperazione con l'autorità: chi produce cosa, in quanto tempo.

**Leve puramente negoziali** — esistono solo se le scrivi:

- manleva sulla conformità del componente del fornitore, e tetto di responsabilità;
- preavviso sui cambi di modello: un aggiornamento a monte sposta il comportamento del sistema senza che tu tocchi una riga;
- l'esclusione della conversione ad alto rischio dell'art. 25(2), quando sei tu a cedere.

**L'uso difforme dalle istruzioni ribalta tutto.** Se l'utilizzatore esce dalla finalità prevista, non solo perde la difesa dell'uso conforme: può diventare fornitore. È il punto da dire prima della firma, non dopo l'incidente.

## Responsabilità civile: cosa vale oggi

- **Direttiva (UE) 2024/2853.** Il software è prodotto, e il fornitore di un sistema di IA può rispondere come fabbricante. Recepimento entro il **9 dicembre 2026**, e si applica ai prodotti immessi sul mercato **dopo** quella data: per tutto ciò che è già sul mercato continua a valere la disciplina precedente (dir. 85/374/CEE, in Italia il Codice del consumo). Non introduce alcuna responsabilità solidale automatica dell'utilizzatore.
- **Direttiva sulla responsabilità dell'IA (AILD): ritirata il 6 ottobre 2025.** Chi te la cita come norma in arrivo sta leggendo materiale vecchio.

## Italia: la legge 132/2025

Contiene una **delega al Governo**: un decreto attuativo si cita solo se è stato emanato.

L'art. 26 tocca il penale, che al civilista sfugge: introduce l'aggravante comune dell'art. 61 n. 11-decies del codice penale quando il reato è commesso con sistemi di IA, interviene sull'art. 294 e crea l'art. **612-quater**, che punisce la diffusione illecita di contenuti generati o alterati con l'IA — il caso deepfake. L'azione che ne discende è concreta: se il prodotto genera volti o voci di persone reali, il rischio non è solo civile. Ogni altro riferimento penale che ti portano va controllato sul testo vigente.

## Come lo dici

Tre righe: **chi risponde** — **fino a quanto** — **cosa cambiare nel contratto**.

Due rami hanno un verdetto proprio:

- utilizzatore, sistema non ad alto rischio → «niente da rinegoziare». Dillo e fermati.
- il sistema ricade in una **pratica vietata dell'art. 5** → «non si fa». Nessuna manleva sana un divieto, e negoziarne una è tempo perso.

## Dove ti fermi

Categoria di rischio, obblighi documentali dell'alto rischio, calendario e trasparenza dell'art. 50 stanno in `references/ai-act-classificazione-e-obblighi.md`: sono tuoi, e quel file va caricato prima di questo quando la classificazione manca. Le intersezioni col GDPR — dati per correggere i bias, sandbox, FRIA, decisione automatizzata — sono di **Vera**. La scelta tecnica del modello e l'impianto del componente AI sono di **Enzo**. Nominali in una riga e fermati.

Il DPA e i sub-responsabili dello stesso fornitore stanno in `references/contratti-e-dpa.md`: quando la domanda è «cosa firmo», serve anche quello.
