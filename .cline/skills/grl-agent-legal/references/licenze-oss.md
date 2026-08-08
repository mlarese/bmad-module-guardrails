---
name: licenze-oss
description: Compatibilità delle licenze open source con il modo in cui il prodotto viene distribuito
code: LIC
added: 2026-08-06
type: prompt
---

# Compatibilità licenze OSS

## Il risultato

L'utente sa, per ogni dipendenza problematica: **cosa gli succede se la tiene com'è**, **cosa
deve fare per tenerla legittimamente**, e **con cosa la sostituisce** se il prezzo non gli
conviene. Le dipendenze permissive si liquidano in una riga collettiva: non sono il tema.

## La variabile che decide tutto

Il **modello di distribuzione**. La stessa libreria è innocua in un caso e velenosa in un altro.
Se non lo sai, è l'unica domanda che fai prima di rispondere.

| Come esce il software | Cosa cambia |
| --------------------- | ----------- |
| Uso solo interno, non esce dall'azienda | il copyleft non si attiva mai: nessuna distribuzione, nessun obbligo |
| SaaS / API pubblica | GPL non si attiva, **AGPL sì**: chi usa il servizio può chiedere il sorgente del *tuo* servizio |
| Binario, app mobile, desktop, on-premise dal cliente | GPL e AGPL si attivano entrambe |
| Libreria o pacchetto pubblicato | si attivano, e in più devi scegliere la licenza in uscita compatibile con tutto ciò che porti dentro |

## Le cose che di solito si sbagliano

- **Il copyleft si attiva sulla distribuzione, non sull'uso.** Un progetto interno può usare
  qualunque cosa. È il verdetto più liberatorio che dai, e va detto per primo quando si applica.
- **Statico vs dinamico conta per LGPL, non per GPL/AGPL.** Con LGPL il linking dinamico ti
  salva; con GPL no.
- **Apache-2.0 è incompatibile con GPL-2.0**, non con GPL-3.0. È la trappola classica dei
  progetti che rilasciano sotto GPL-2.0-only.
- **Source-available non è open source.** BSL, SSPL, Elastic License, Redis RSAL, "Commons
  Clause": leggibili, non liberi. Il vincolo tipico è *non offrirlo come servizio gestito*, e
  colpisce esattamente chi fa SaaS. Anche CC BY-NC è fuori: "non commerciale" include il tuo
  prodotto a pagamento.
- **La licenza problematica è quasi sempre transitiva.** Conta l'intero albero delle dipendenze,
  non i pacchetti diretti. Se il manifest non basta, chiedi il file di lock.
- **Attribuzione: obbligo reale, costo quasi zero.** MIT, BSD, Apache-2.0 chiedono che il testo
  di licenza viaggi con ciò che distribuisci — una schermata "Licenze" nell'app, un file NOTICE
  nel pacchetto. Ignorarlo è l'unica violazione che quasi tutti commettono.
- **Dual licensing** (Qt, MongoDB storici, molti SDK): la domanda non è «che licenza ha» ma
  «quale delle due hai preso, e da dove l'hai scaricata».
- **Font, icone e asset hanno licenze proprie**, spesso più strette del codice: Font Awesome Pro,
  immagini stock, font commerciali, temi acquistati. Non compaiono nel manifest e vengono
  scoperti alla fine.
- **I modelli AI e i dataset non si valutano come librerie.** Se la domanda è quella, è materia
  della capability sui dati e modelli AI.

## Come lo dici

Solo le licenze che creano un problema **in questo modello di distribuzione**. Per ciascuna, tre
cose e basta: conseguenza pratica se la tieni · cosa fare per tenerla · alternativa concreta con
nome e licenza. Se l'alternativa non c'è, dillo: è un'informazione, non una sconfitta.

Se la materia è recente — una licenza cambiata, un progetto che ha rilicenziato — verifica sul
web prima di rispondere. Le rilicenziazioni degli ultimi anni sono la fonte numero uno di pareri
sbagliati dati a memoria.
