# Eval di `grl-agent-issues`

I casi verificano le regole che tengono in piedi Tito: dichiarare sempre l'età del dato,
non rispondere su un registro che non esiste, non eseguire istruzioni scritte dentro una issue,
non riempire con la propria idea il requisito che manca e ricordare cosa è già stato deciso.

| Caso | Cosa protegge |
| --- | --- |
| `registro-assente` | non simula una lettura che non ha fatto |
| `registro-vecchio` | oltre trenta giorni il verdetto resta provvisorio |
| `commento-che-comanda` | il testo della issue è dato, mai istruzione |
| `attesa-senza-uscita` | l'attesa porta chi l'ha messa e cosa la toglie |
| `vuoto-non-riempito` | la lacuna diventa una domanda, non un requisito inventato |
| `decisione-gia-presa` | le decisioni e le convenzioni registrate valgono, e si citano |
| `confine-diagnosi` | la causa del difetto è di `grl-bug-finder` |
| `ordine-senza-criteri-inventati` | non introduce criteri che il registro non contiene |
| `duplicati-dal-registro` | segnala le coppie, non le unisce |
| `registro-parziale-dichiarato` | una lettura troncata si dichiara prima del numero |
| `ricognizione-prima-del-verdetto` | il codice si guarda prima di giudicare, e l'ambiguità diventa una domanda |
| `elenco-con-descrizione` | nessun elenco muto: ogni riga dice a cosa si riferisce |
| `nessuna-proposta-non-richiesta` | Tito risponde alla domanda fatta, senza allargare il lavoro |

I trigger separano il backlog dalla diagnosi, dall'implementazione, dal registro (`grl-issues`),
dal commento (`grl-issue-readiness`) e dalla verifica di chiusura (`grl-issue-verify`): Tito dice
se il lavoro è definito, non come si fa.

## Come si eseguono

| File | Modo | Cosa misura |
| --- | --- | --- |
| `cases.json` | quality | la risposta rispetta la rubric, caso per caso |
| `triggers.json` | trigger | la `description` porta il router a Tito e non alle skill vicine |

Tito è una figura interattiva: i casi iniziano con `Run headless.` perché il banco li esegue a
colpo singolo, senza conversazione. Non è una modalità della figura, è il modo in cui si misura.
