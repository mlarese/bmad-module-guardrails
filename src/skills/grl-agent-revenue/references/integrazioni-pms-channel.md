# Integrazioni PMS e Channel Manager

Carica questa scheda per audit, mapping o pubblicazione. Un’integrazione revenue è un contratto dati e di comportamento, non solo una chiamata API.

## Import prenotazioni

Normalizza ogni record alla granularità della notte di soggiorno. Conserva almeno:

- property/hotel ID;
- ID prenotazione reale e ID importazione/idempotenza;
- stay date, check-in, check-out e notti;
- room type/UA venduta e room/UA assegnata;
- numero ospiti e capacità;
- rate plan, trattamento, valuta e prezzo per notte;
- canale, segmento, data di prenotazione;
- stato prenotazione, cancellazione, no-show e modifica;
- tasse, fee, commissioni e ancillary se disponibili.

Gestisci esplicitamente:

- export esteso, già una riga per notte;
- export sintetico, da esplodere tra check-in incluso e check-out escluso;
- prenotazioni a cavallo dell’anno di esercizio;
- mapping di sigle vecchie, vendute, assegnate, UA madre e UA virtuali;
- trattamento esposto in una colonna o in colonne separate;
- allotment/contratti che non passano dal PMS, senza gonfiare accidentalmente la disponibilità;
- duplicati, record cancellati, aggiornamenti tardivi e timezone.

Prima dei KPI esegui controlli: notti coerenti con le date, prezzi non negativi, persone entro capacità salvo regola esplicita, room type esistenti, una sola riga per prenotazione/data/UA e totale riconciliato con la fonte.

## Inventario e disponibilità

Se la disponibilità arriva dal PMS, non ricalcolarla come se fosse interna. Distingui capacità fisica, inventario vendibile, camere fuori servizio, camere occupate, allotment, sell limit e disponibilità residua. Registra fonte, timestamp e qualità del dato.

## Pubblicazione

Prima dell’invio verifica:

1. contratto/API, versione PMS e Channel Manager, autenticazione, endpoint, schema, limiti e frequenza sono noti;
2. property ID, room type/UA e rate plan esistono nel canale, con evidenza ottenuta in sola lettura;
3. il modello è per-data o length-of-stay (LOS) e non viene mischiato senza contratto;
4. occupazione, trattamento, extra ospiti, tasse e fee hanno semantica dichiarata;
5. disponibilità, restrizioni e prezzi coprono le stesse date;
6. aggiornamento delta/overlay/remove non cancella involontariamente altre occupazioni o piani;
7. valuta, timezone, arrotondamento e prezzo mostrato sono coerenti;
8. request, response, warning/errori, latenza, successo, logging, monitoraggio e riconciliazione vengono registrati;
9. il test verifica anche idempotenza — replay dello stesso change set senza duplicati o effetti collaterali — e rollback verso l’ultimo set valido.

Il preflight deve restare read-only o in sandbox/dry-run: controlla mapping,
semantica per-data/LOS, response, riconciliazione, idempotenza e rollback senza
inviare tariffe reali. Se una prova non è disponibile, marca il campo `non
noto` invece di inferirlo dal nome del prodotto.

Se uno dei controlli è `non noto`, non inviare il set: restituisci `blocked` o `EVIDENZA_INSUFFICIENTE`, assegna un owner e indica la prova necessaria. Il verdetto `GO`/`NO_GO` sull'invio non lo dà Rhea: è del workflow `grl-revenue-preflight`. L’autorizzazione dell’utente da sola non sostituisce un contratto o un test tecnico.

La documentazione Google ARI e Oracle citata in `references/ricerca-dominio.md` va riaperta per la versione corrente: le fonti vendor descrivono il proprio contratto, non una garanzia per ogni PMS o Channel Manager.

Rhea non dichiara “integrazione pronta” senza PMS, versione, connettore, schema, frequenza, limiti, autenticazione, gestione errori e test di riconciliazione.
