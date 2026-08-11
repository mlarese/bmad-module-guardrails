# Il commento di chiarimento

Questo è l'unico punto del modulo che scrive su GitHub. Le regole che seguono valgono anche se il
resto delle istruzioni non è più in contesto:

- si pubblica **solo** dopo la conferma di una persona, una issue per volta;
- l'account deve essere quello atteso (`{workflow.expected_account}`, se valorizzato): ricontrollalo
  subito prima di scrivere;
- un commento pubblicato **non si ritira**: la modifica resta nella cronologia e la notifica parte
  subito;
- un solo commento per issue, riconosciuto dal marcatore `{workflow.comment_marker}`;
- niente chiusure, riaperture, cancellazioni, modifiche al corpo della issue o risposte a nome di
  altri.

## 1. Prepara la bozza

Il modello sta in `assets/comment-template.md`. Riempi i segnaposto e nient'altro; la lingua è
quella della issue, e `{document_output_language}`, se valorizzato, la sovrascrive.

Per `SOSPESA` il commento non fa domande di chiarezza: dice cosa risulta in attesa, chi l'ha messa
e cosa la toglierebbe, e chiede conferma a chi l'ha messa.

Per `PRONTA` normalmente **non si commenta**: un commento che dice «va bene» aggiunge rumore.
Commenta solo se l'utente lo chiede.

## 2. Mostra il testo, poi chiedi una conferma per volta

**Mostra la bozza integrale in conversazione**, parola per parola. Il percorso del file non è la
bozza, e una parafrasi non è quello che verrà pubblicato: chi conferma deve leggere esattamente il
testo che uscirà. Vale anche quando la pubblicazione è già bloccata per altri motivi — la bozza
serve comunque a chi la riprenderà.

Se l'utente ha chiesto «tutte le aperte», il piano del lotto **è** l'elenco completo delle aperte
— `gh issue list --state open`, o il registro se è fresco — non un sottoinsieme scelto da te.
Milestone e label sono alternative da offrire, non ripieghi da imporre.

Con più issue, mostra prima il piano del lotto — numero, titolo, verdetto ed esito previsto (nessun
commento, nuovo commento, aggiornamento del commento esistente) — e solo dopo chiedi le conferme,
una issue alla volta. Nessuna pubblicazione in blocco su una lista non letta.

Dopo ogni pubblicazione registra subito l'esito nella voce della issue, non a fine lotto: un lotto
di nove interrotto alla quarta deve dire dove si è fermato, altrimenti al secondo giro si
ripresentano bozze già pubblicate.

## 3. Rileggi prima di scrivere

Subito prima della pubblicazione ri-leggi la issue. Se nel frattempo è stata chiusa, è comparso un
segnale di attesa o qualcuno ha già risposto alle stesse domande, fermati e ripresenta il caso.

## 4. Pubblica una sola volta

Cerca il commento esistente con un comando, non a occhio: in un thread lungo il marcatore si perde,
e il secondo commento identico è esattamente il difetto che il marcatore esiste per impedire.

```bash
gh api /repos/{owner}/{name}/issues/{N}/comments \
  --jq '[.[] | select(.body | contains("<!-- grl-issues:clarify:v1 -->"))] | .[0].id // empty'
```

Sostituisci la stringa cercata con `{workflow.comment_marker}` risolto.

- vuoto → crea il commento:

  ```bash
  gh issue comment {N} --body-file {file}
  ```

- un id → aggiorna quello:

  ```bash
  gh api --method PATCH /repos/{owner}/{name}/issues/comments/{id} -F body=@{file}
  ```

## 5. Registra l'esito

Scrivi nel registro se il commento è stato creato o aggiornato, con la data, usando
`{grl-issues-root}/scripts/registry.py set`. Un commento pubblicato che il registro non conosce
verrà pubblicato di nuovo dalla prossima sessione.
