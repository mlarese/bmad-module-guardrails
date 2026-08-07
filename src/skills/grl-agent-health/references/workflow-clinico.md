---
name: workflow-clinico
description: Chi usa ogni schermata, quando, con quanto tempo — e dove il software verrà aggirato
code: WC
added: 2026-08-07
type: prompt
---

# Workflow clinico reale

## Cosa vuol dire riuscirci

L'utente sa **dove il suo software verrà aggirato**, e perché. L'aggiramento è la modalità di fallimento tipica del software sanitario: non un crash, ma un infermiere che compila tutto a fine turno a memoria, un medico che tiene la lista vera su un foglio, un amministrativo che usa un unico account condiviso.

Il consumatore è chi decide cosa rendere obbligatorio e cosa no.

## Il principio da cui discende tutto

**Il tempo è la risorsa scarsa, non l'attenzione.** Una schermata che richiede trenta secondi in un compito che ne dura sessanta non viene usata: viene falsificata.

Le tre domande, in quest'ordine:

> **Chi apre questa schermata? Cosa stava facendo un secondo prima? Quanti secondi ha?**

## Le figure e i loro vincoli

Non sono ruoli di un diagramma: sono condizioni d'uso diverse, e cambiano il progetto.

| Chi | Come lavora davvero | Cosa rompe il software |
| --- | ------------------- | ---------------------- |
| Medico in ambulatorio | visite a slot fissi, il paziente è davanti e guarda | ogni campo obbligatorio che non serve alla visita; la ricerca lenta; il login che scade a metà |
| Medico di reparto | giro visite, in piedi, spesso su tablet o su un carrello | schermate progettate per un monitor grande; qualsiasi cosa richieda due mani |
| Infermiere | attività a cadenza fissa su molti pazienti, interruzioni continue | perdere il contesto quando si viene interrotti; dover ripetere l'identificazione a ogni azione |
| Tecnico di laboratorio o radiologia | flusso di lavoro guidato dalla macchina, non dal software gestionale | doppio inserimento fra strumento e sistema |
| Amministrativo / front office | telefono e sportello, paziente in attesa fisica o in linea | tutto ciò che richiede più di pochi secondi mentre qualcuno aspetta |
| Paziente | usa il sistema poche volte l'anno, da telefono, spesso in condizioni non ideali | qualsiasi cosa presupponga che ricordi come funzionava l'anno scorso |

Chiedi quale di queste figure userà la cosa di cui state parlando. Se la risposta è «tutti», il progetto ha un problema di scopo, non di interfaccia.

## Le rotture ricorrenti

- **La sessione contro il turno.** Una sessione che scade in quindici minuti su una postazione condivisa produce un account condiviso e sempre aperto. Il rimedio non è allungare la scadenza, è separare autenticazione della postazione e identificazione dell'operatore.
- **L'obbligatorietà che produce dati falsi.** Ogni campo obbligatorio che non è disponibile nel momento in cui la schermata si compila genera un valore di comodo. La domanda da fare è: *questo dato esiste già, quando l'utente arriva qui?*
- **Il flusso lineare su un lavoro non lineare.** Le visite si interrompono, i pazienti tornano indietro, i risultati arrivano dopo. Un wizard a passi obbligati su un processo clinico è quasi sempre sbagliato: serve poter salvare incompleto.
- **Il lavoro fuori orario e fuori rete.** Guardie notturne, domiciliari, ambulanze, strutture con connessione instabile. Se il software non funziona senza rete, chiedi cosa fanno in quel caso — la risposta è di solito «carta», e la carta poi va reinserita da qualcuno.
- **Chi corregge.** Ogni sistema clinico ha bisogno di una via per correggere un errore commesso in buona fede: paziente sbagliato, referto scambiato, terapia inserita due volte. Se non c'è, gli utenti ne inventano una peggiore.
- **Le consegne fra turni.** Il passaggio di informazioni fra chi smonta e chi monta è il momento in cui le cose si perdono. Quasi nessun software lo copre, e quasi tutti i reparti lo fanno su carta o a voce.
- **Il paziente che non esiste ancora.** Urgenza, neonato non ancora registrato, persona senza documenti. Se il sistema pretende un'anagrafica completa prima di poter registrare qualsiasi cosa, in urgenza viene aggirato.

## Come si conduce

Non chiedere di descrivere il processo: chiedi di raccontare **l'ultima volta**. «L'ultima volta che è arrivato un paziente senza appuntamento, cosa è successo, in che ordine?» I processi raccontati sono quelli scritti nelle procedure; i racconti sono quelli veri.

Se non c'è accesso a nessun clinico, dillo esplicitamente e marca le tue ipotesi come ipotesi: il rischio di questa capacità è inventare un reparto plausibile.

## Forma dell'output

Per ogni punto: **chi** · **quando** · **cosa farà invece di usare il software** · **la modifica minima** che lo evita. Massimo cinque punti, ordinati per quanto spesso capita.

## Trappole

- **Progettare per il caso normale.** In sanità il caso limite — urgenza, paziente non identificato, sistema offline — non è raro: è quotidiano.
- **Chiamarlo problema di formazione.** Se serve formazione perché il flusso è innaturale, il difetto è nel flusso.
- **Sconfinare sull'aspetto.** Densità, tipografia, gerarchia visiva sono di Iris: tu dici quale informazione deve essere raggiungibile in quanti secondi, non come si disegna.
