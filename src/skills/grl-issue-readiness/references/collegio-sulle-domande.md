# Il collegio prima della domanda

Una domanda scritta in un commento costa a chi la riceve: deve leggerla, capirla, rispondere, e
intanto la issue è ferma. Molte di quelle domande, però, hanno già una risposta dentro il progetto
— nel codice, nei test, in una decisione presa il mese scorso, nel glossario di dominio. Chiederle
a una persona è farle rifare un lavoro che qualcun altro ha già fatto.

**Regola: prima di scrivere una domanda nel commento, convoca il collegio e vedi quante si
chiudono da sole.** Nel commento finisce solo ciò che resta.

Il collegio si convoca con `bmad-party-mode` se è installato — le figure discutono fra loro e i
dissensi si vedono — altrimenti con `grl-board`, che le fa guardare lo stesso artefatto e
restituisce un riepilogo unico.

## 1. Quali figure

Non tutte: quelle che il segnale della issue chiama.

| Nella issue compare | Chi convocare |
| --- | --- |
| dove si tocca, confini fra moduli, dove va una funzione nuova | Otto |
| schema, query, migrazione, dato che deve sopravvivere | Dario |
| un percorso che non torna indietro, un gate, uno stato bloccato | Vito |
| dati personali, consenso, retention | Vera |
| autenticazione, permessi, segreti, superficie esposta | Kai |
| dato clinico, reparto, prescrizione | Livia |
| una norma, una soglia, un obbligo | Nils |
| pagina, layout, testo che l'utente legge | Iris, Marea |
| un difetto da riprodurre prima di poterlo descrivere | `grl-bug-finder` |

Se nessuna figura è pertinente, non convocare: la domanda è di chi ha scritto la issue.

## 2. Che cosa chiude una domanda

**Solo l'evidenza.** Una risposta vale se porta con sé dove è stata trovata:

| Fonte | Esempio |
| --- | --- |
| il codice | «l'export mensile è `reports/export_csv.py:88`, gli altri due sono interni» |
| un test esistente | «`test_totale_iva` fissa già l'aliquota al 22%» |
| una decisione registrata | «`decisions.md`, 2026-06-02: i resi restano fuori dall'export» |
| il profilo di progetto o il glossario | «"ordine" nel glossario include gli storni» |
| la storia del repository | «quella colonna è stata tolta nel commit `a1b2c3` con questo motivo» |

Una figura che dice «di solito si fa così» **non chiude niente**: è un'opinione, e un'opinione al
posto di un requisito è esattamente l'errore che queste skill esistono per impedire.

## 3. Che cosa il collegio non può chiudere, mai

Le domande che non chiedono conoscenza ma **volontà**:

- quale comportamento vuole chi ha aperto la issue, quando il codice ne permette due;
- se una cosa va fatta adesso o dopo, e a scapito di cosa;
- quale aliquota, quale soglia, quale testo mostrare all'utente;
- se un caso limite si accetta o si copre;
- cosa il cliente ha chiesto davvero, quando la issue riporta un riassunto.

Nessuna figura ha accesso a queste risposte. Chiuderle «per non disturbare» significa scrivere il
requisito al posto dell'autore, e il codice che ne esce risolve un problema immaginato.

## 4. Esito, e come cambia il commento

Ogni domanda esce dal collegio con uno di tre esiti:

| Esito | Dove va |
| --- | --- |
| **chiusa con evidenza** | nel verdetto, con la fonte accanto; non nel commento |
| **ricostruita, da confermare** | nel commento, ma come domanda chiusa: «risulta X, confermi?» |
| **aperta** | nel commento come domanda vera, perché è una decisione |

La riga di mezzo è quella che fa la differenza. «Quale export?» costa all'autore un'indagine;
«risulta `reports/export_csv.py`, confermi?» costa un sì. La stessa issue si sblocca in un minuto
invece che in due giorni, e la ricostruzione resta verificabile perché porta la sua fonte.

Una ricostruzione senza fonte non è una ricostruzione: è un'ipotesi travestita, e torna a essere
una domanda aperta.

## 5. Quando non convocare

- **Zero domande aperte**: non c'è niente da chiudere.
- **La issue è `SOSPESA`**: prima si toglie il freno, poi si discute il contenuto.
- **Il collegio è già stato convocato sulla stessa issue** e da allora la issue non è cambiata: la
  discussione ripeterebbe se stessa. Cita l'esito precedente.
- **Un lotto di issue**: si convoca per issue, non per lotto, e solo su quelle con domande
  bloccanti. Su venti issue una convocazione ciascuna costa più di quanto valga.

## 6. Il costo, detto

La convocazione è la parte più lenta e più cara di questa skill: sono più figure che leggono lo
stesso materiale. Convocarla per una domanda che una persona chiuderebbe in dieci secondi è uno
spreco, e va contro lo scopo — che è togliere lavoro alle persone, non spostarne su di loro
l'attesa.

Dichiara sempre chi hai convocato e cosa ha chiuso. Se il collegio non chiude niente, dillo: è
un'informazione, e significa che le domande erano decisioni fin dall'inizio.
