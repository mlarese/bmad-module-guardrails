# Ricerca di sorgenti video utilizzabili

Questa scheda serve a produrre candidati verificabili, non a dichiarare che un video è libero da usare.

## Prima la scena

Ogni query deve partire da una scena del journey: luogo, attività, gesto, luce, scala e ruolo nella storia. Registra la query esatta e la data `as_of`. Esempi:

- `{luogo} {gesto} video stock commercial license`
- `{territorio} {attività} official footage usage rights`
- `{soggetto} open licence video attribution`
- `site:{dominio-ufficiale} {luogo} press media video`

Una ricerca per «video bello» non è sufficiente: non definisce cosa deve dimostrare il fotogramma né per chi.

## Ordine delle fonti

1. Filmato prodotto dal cliente o commissionato, con titolare e autorizzazione documentati.
2. Fonte ufficiale dell'ente, del luogo o del brand, con termini d'uso applicabili al caso.
3. Archivio stock con pagina della licenza, modello di licenza, territorio, canali, durata e obbligo di attribuzione.
4. Dominio pubblico o open licence, verificando versione della licenza e condizioni sul file preciso.
5. Piattaforme social e aggregatori solo come indizi: la pagina del risultato non è prova di diritti.

Per ogni candidato conserva sia la pagina che spiega il diritto sia l'URL dell'asset, se distinto. Se i termini sono dinamici, salva data di verifica e un estratto breve o un riferimento alla sezione; non sostituire la fonte originale con uno screenshot non datato.

## Matrice minima

| Campo | Valore richiesto |
| --- | --- |
| `candidate_id` | identificatore stabile |
| `source_page` / `asset_url` | pagina della licenza e file/anteprima |
| `creator` / `rights_holder` | persona o organizzazione, oppure `unknown` |
| `license` | nome/versione e link ai termini |
| `commercial_use` | sì/no/non verificato |
| `territory_channels_duration` | scope preciso, non «uso web» generico |
| `attribution` | testo e posizione, oppure nessuna se provato |
| `people_music_marks_location` | elementi che richiedono release o verifica separata |
| `as_of` | data della verifica |
| `status` / `reason` | `verified`, `needs_rights`, `rejected`, `unknown` e motivo |

## Gate

`verified` significa che la licenza copre il caso d'uso e la sorgente è identificata; non significa che ogni volto, musica, marchio o indirizzo sia automaticamente libero. Se manca un elemento, usa `needs_rights` o `unknown`, indica il blocco e invia ad Aldo. Se il video contiene persone riconoscibili, dati di localizzazione o interni privati, coinvolgi Vera prima di selezionare i frame. Non scaricare il candidato per «vedere se va bene» se l'autorizzazione non copre già il download e l'estrazione.

## Handoff

Quando un candidato è approvato, il pacchetto deve riportare l'ambito dell'autorizzazione (`local_extract`, `web_delivery`, eventuale attribuzione), il nome del file locale, il suo hash e chi ha approvato. Quando non è approvato, consegna solo la matrice e il piano visuale: `grl-web` può preparare un placeholder dichiarato, ma non deve fingere che il video sia utilizzabile.
