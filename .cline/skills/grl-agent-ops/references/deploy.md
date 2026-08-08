---
name: deploy
description: Si rilascia senza paura perché la via di ritorno è nota, provata e alla portata di chi è di turno
code: DEP
added: 2026-08-06
type: prompt
---

# Deploy, rollback e CI/CD

## Cosa vuol dire riuscirci

Chiunque nel team può rilasciare, e **chiunque può tornare indietro** senza chiedere aiuto. Il consumatore è la persona che rilascia alle 18 di venerdì e vede il sito bianco: se in quel momento non sa cosa digitare, la procedura è fallita, per quanto elegante sia la pipeline.

Il rollback non è un capitolo del deploy: è **la prima cosa da definire**. Un deploy senza via di ritorno non è un deploy, è una scommessa.

## Le domande che decidono tutto

1. **Come si torna indietro, in quanti minuti, con che perdita?** Se la risposta è «rifacciamo il deploy della versione vecchia» va bene, purché sia stato provato.
2. **Cosa succede al database?** È qui che il rollback si rompe: il codice torna indietro, lo schema no. Una migrazione che rinomina o elimina una colonna rende il rollback impossibile.
3. **Chi può rilasciare?** Se è una persona sola, quella persona è il punto di guasto.

## Migrazioni: la regola che salva i rollback

Le modifiche di schema si fanno **compatibili all'indietro** e in due passi separati nel tempo:

- aggiungere una colonna → sì, sempre sicuro;
- rinominare → aggiungi la nuova, scrivi su entrambe, migra, e **solo dopo** un rilascio stabile elimina la vecchia;
- eliminare → mai nello stesso rilascio che smette di usarla.

Così il codice vecchio gira sullo schema nuovo, e il rollback resta possibile. Ogni migrazione distruttiva rientra nel protocollo dei comandi distruttivi.

## La pipeline minima

Per la maggior parte dei progetti: **build → test → artefatto versionato → rilascio → verifica**. In ordine di valore reale:

- **artefatto identificabile** (tag, SHA del commit, immagine con tag immutabile): senza, non si sa cosa c'è in produzione né a cosa tornare;
- **un test che blocca il rilascio** — anche uno solo, purché fallisca davvero;
- **verifica dopo il rilascio**: una chiamata all'endpoint di salute. Un deploy «riuscito» su un servizio che non risponde è il caso peggiore;
- **rilascio senza interruzione** (nuovo su, vecchio giù dopo la verifica) solo se l'interruzione costa. Su un progetto interno, dieci secondi di disservizio non giustificano la complessità.

Se il deploy oggi è uno script `deploy.sh` lanciato a mano e funziona, **la risposta può essere «va bene così»**. La CI si aggiunge quando rilasciare a mano fa perdere tempo o produce errori, non per completezza.

## Forma dell'output

La procedura in passi numerati con i comandi, **e in cima la via di ritorno**, non in fondo. Poi cosa manca oggi, ordinato per quanto fa male: di solito il primo punto è che nessuno ha mai provato il rollback.

## Trappole

- **`git push --force` su un branch di deploy**: protocollo dei comandi distruttivi.
- **Il rollback teorico.** Se non è mai stato eseguito, non esiste. Provalo una volta, in orario tranquillo.
- **Segreti nella pipeline** stampati nei log di build. Dove iniettarli è competenza di Bruno; il rischio di esposizione è di **Kai**.
- **La pipeline che fa venti cose** su un progetto che rilascia una volta al mese: è manutenzione senza contropartita.
- **Il deploy che dipende dal portatile di una persona**: chiavi, tunnel o script che stanno solo lì.
