# Audit e piano di un account paid

## Prima del giudizio

Raccogli, oppure marca `non noto`:

- obiettivo commerciale, mercato, lingua, offerta e destinatario;
- account, canale, fuso orario, valuta, intervallo e data di estrazione;
- campagne, stato, budget, targeting, strategia d'offerta, asset e destinazioni;
- conversioni primarie e secondarie, definizione dell'evento, valore, finestra e fonte;
- spesa, impression, clic, CTR, CPC, conversioni, tasso di conversione, CPA/ROAS e qualità
  del lead, senza trattare le metriche come confrontabili se la definizione è diversa;
- capacità commerciale: tempi di risposta, qualificazione, margine e valore della vendita.

## Inventario minimo

| Livello | Domande |
| --- | --- |
| Business | Quale risultato deve cambiare? Qual è l'unità economica? Chi decide che un lead è valido? |
| Account | Chi ha accesso? Quali modifiche sono già in corso? Esistono limiti di budget o brand safety? |
| Campagna | Il nome e la struttura descrivono obiettivo, mercato, lingua e prodotto? Ci sono duplicati o sovrapposizioni? |
| Pubblico | La segmentazione è motivata da domanda o solo dalla disponibilità della piattaforma? |
| Creatività | Claim, asset, diritti, destinazione e messaggio sono coerenti? |
| Misura | L'evento è quello di business o solo un segnale facile da contare? |
| Operatività | Chi approva, chi applica, chi monitora e come si torna indietro? |

## Priorità

Ordina i finding così:

1. blocchi: tracking assente o duplicato, destinazione non raggiungibile, policy o claim ad alto
   rischio, budget non autorizzato, dati caricati senza perimetro;
2. distorsioni: conversione sbagliata, finestra incoerente, attribuzione non confrontabile,
   campagne sovrapposte, query o placement non pertinenti;
3. opportunità: struttura, creatività, keyword, audience, test, budget e automazioni;
4. cosmetica: naming, colonne e ordinamento che non cambiano la decisione.

Ogni finding ha `severity`, evidenza, ipotesi, azione, costo, owner, verifica e stato. Un
optimization score o una raccomandazione di piattaforma può essere evidenza della proposta della
piattaforma, non prova dell'impatto sul business.

## Piano media

Un piano leggibile contiene:

- una riga di obiettivo e una conversione primaria;
- una matrice `segmento → bisogno → messaggio → offerta → destinazione → evento`;
- struttura delle campagne e motivazione della separazione;
- asset necessari, proprietario e stato: `mancante`, `da approvare`, `pronto`;
- budget come scenario, con ipotesi esplicite e limite massimo;
- piano di test con una sola variabile principale per volta quando il traffico non consente altro;
- misurazione prima del lancio e criteri di stop;
- passaggi a Vera, Aldo, Iris, Nora, `grl-web`, Marta o Bruno quando il tema esce da Dalia.

## Change set

Non scrivere solo «ottimizzare». Per ogni modifica usa:

```text
id: CS-001
scope: account/campagna/ad group/asset
action: create | update | pause | move-budget | no-change
before: stato osservato o non noto
after: stato proposto
reason: evidenza + ipotesi
budget_delta: importo e periodo, oppure none
risk: policy/privacy/tracking/business/operational
approval: ruolo e stato
validate: controllo read-only o validate_only
observe_for: finestra e segmenti
rollback: azione e owner
```

Se `before` non è osservato, il change set resta `blocked`: non si applica una supposizione.
