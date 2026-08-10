# Schema del catalogo e della configurazione

Il catalogo è la forma canonica in cui le regole di un prodotto diventano verificabili da una macchina. Qualunque sia l'origine — intervista, PDF, ERP — la destinazione è sempre questa.

Lo schema è deliberatamente povero: cinque costrutti. Un catalogo che ha bisogno di un sesto sta descrivendo un prodotto che vuole un motore di configurazione vero, e va detto invece di aggirato.

## Il catalogo

`{project-root}/_bmad/memory/grl-agent-product-config/catalog/<linea>.yaml`

```yaml
version: 1
line:
  code: infissi-pvc
  name: Serramenti in PVC
  as_of: 2026-08-10
  source: "listino 2026 rev.3, pagine 4-11, più intervista ufficio tecnico"
  reviewed_by: "Nome Cognome"      # senza questo campo il catalogo non è utilizzabile
  reviewed_on: 2026-08-10

options:
  - code: serie
    name: Serie del profilo
    type: enum                     # enum | number | boolean | text
    required: true
    values:
      - code: s70
        name: "Serie 70 mm"
      - code: s82
        name: "Serie 82 mm"

  - code: larghezza
    name: Larghezza foro
    type: number
    unit: mm
    required: true
    min: 400
    max: 2400

  - code: rinforzo
    name: Rinforzo in acciaio
    type: boolean
    required: false

  - code: colore_interno
    name: Colore interno
    type: enum
    required: false
    impact: pricing                # blocking | pricing | cosmetic
    values:
      - code: bianco
      - code: noce
      - code: ral

rules:
  - kind: requires                 # se la condizione vale, l'esito deve valere
    when: { option: serie, value: s82 }
    then: { option: rinforzo, value: true }
    because: "peso anta oltre 90 kg"

  - kind: excludes                 # se la condizione vale, l'esito non può valere
    when: { option: colore_interno, value: ral }
    then: { option: serie, value: s70 }
    because: "la verniciatura RAL non è disponibile sul profilo 70"

  - kind: required_if              # se la condizione vale, l'opzione va compilata
    when: { option: colore_interno, value: ral }
    then: { option: codice_ral }
    because: "senza codice non è ordinabile"
```

### I cinque costrutti

| Costrutto | Dove sta | Cosa dichiara |
| --- | --- | --- |
| `option` | `options[]` | una scelta configurabile, con tipo, unità e valori ammessi |
| vincolo di dominio | `min`, `max`, `values`, `required` sull'opzione | quali valori sono ammessi in assoluto |
| `requires` | `rules[]` | una combinazione ne impone un'altra |
| `excludes` | `rules[]` | due combinazioni non possono coesistere |
| `required_if` | `rules[]` | un'opzione diventa obbligatoria sotto condizione |

### Campi non facoltativi

- **`because`** su ogni regola. È la frase che Ines ripete al cliente quando chiede perché non può avere quella combinazione. Una regola senza ragione non si può difendere e non si può nemmeno verificare quando il prodotto cambia.
- **`reviewed_by` e `reviewed_on`**. Senza, lo script rifiuta il catalogo. Vale anche per un catalogo importato da ERP: importato non significa verificato.
- **`impact`** su ogni opzione non obbligatoria. Serve a ordinare le domande al cliente: `blocking` prima di `pricing`, `pricing` prima di `cosmetic`.

### Cosa il catalogo non contiene

- Prezzi e listini. Il prezzo è un lavoro a valle e cambia con una frequenza diversa dalle regole; tenerlo qui costringe a rivedere il catalogo a ogni ritocco commerciale.
- Formule di calcolo geometrico o strutturale. Se il prodotto le richiede, il catalogo dichiara i limiti (`min`, `max`) e il calcolo resta di chi lo fa oggi.
- Testi commerciali e descrizioni di vendita.

## La configurazione

`{output_folder}/product-config/{slug}/config.yaml`

```yaml
version: 1
line: infissi-pvc
catalog: "{project-root}/_bmad/memory/grl-agent-product-config/catalog/infissi-pvc.yaml"
source_document: "richieste/rfq-rossi-2026-08.pdf"

selections:
  serie: s82
  larghezza: 1800
  rinforzo: true

evidence:                          # perché quella scelta, una voce per selezione
  serie:
    origin: written                # written | imposed | assumed
    quote: "p. 2 riga 14 — «profilo maggiorato, serie 82»"
  larghezza:
    origin: written
    quote: "tabella allegato A, foro 1800×1400"
  rinforzo:
    origin: imposed
    rule: "requires: serie=s82 → rinforzo=true"

assumptions: []                    # origin: assumed, con la ragione dichiarata

missing:                           # ciò che blocca: obbligatorie e opzioni imposte da una regola
  - option: codice_ral
    impact: blocking
    question: "Qual è il codice RAL a campione?"

open_choices:                      # facoltative non ancora decise: visibili, ma non bloccano
  - option: colore_interno
    impact: pricing
    question: "Colore interno: bianco, noce o RAL a campione?"
```

Ogni chiave di `selections` deve comparire in `evidence`: una scelta senza origine è la cosa che lo script rifiuta per prima.

## Cosa verifica lo script

`uv run scripts/config_validator.py catalog <path>` controlla il catalogo:

- codici duplicati fra opzioni o fra valori della stessa opzione;
- regole che citano opzioni o valori inesistenti;
- `requires` in contraddizione con un `excludes` sulla stessa coppia;
- catene di `requires` che si chiudono su sé stesse;
- opzioni `required: true` rese impossibili da un `excludes`;
- regole senza `because`, catalogo senza `reviewed_by`.

`uv run scripts/config_validator.py config <path>` controlla la configurazione:

- selezioni fuori dai valori ammessi o fuori da `min`/`max`;
- opzioni obbligatorie mancanti, in assoluto o per `required_if`;
- `requires` non soddisfatti ed `excludes` violati;
- selezioni prive di voce in `evidence`.

L'esito è `valid`, `incomplete` o `invalid`, e le tre parole significano una cosa sola:

| Esito | Cosa dice | Cosa lo produce |
| --- | --- | --- |
| `valid` | è ordinabile | nessun conflitto e nessuna voce in `missing` |
| `incomplete` | manca qualcosa che blocca | almeno una voce in `missing` |
| `invalid` | c'è una contraddizione | almeno un errore |

`missing` e `open_choices` non sono la stessa cosa e non vanno mescolati. In `missing` finisce ciò che blocca l'ordine: le opzioni `required` del catalogo, quelle rese obbligatorie da un `required_if`, quelle imposte da un `requires`. In `open_choices` finiscono le facoltative non ancora decise, con il loro `impact`: restano visibili in ogni output, ma una configurazione ordinabile con il colore ancora da scegliere è `valid`, non `incomplete`.

`incomplete` non è un errore: è lo stato normale di una richiesta appena letta.
