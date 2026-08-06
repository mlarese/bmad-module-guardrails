---
name: perimetro-normativo
description: Stabilire quali norme toccano davvero il progetto e quali no, con la soglia che lo determina
code: PER
added: 2026-08-06
type: prompt
---

# Perimetro normativo

## Cosa deve essere vero alla fine

L'utente ha in mano due elenchi: le norme che lo riguardano, e quelle che non lo riguardano con la ragione per cui sono escluse. Il secondo elenco è quello che smette di costargli attenzione, e va consegnato con la stessa serietà del primo.

Ogni riga porta la **soglia** che ha deciso l'esito, non un giudizio. «Fuori» senza numero non chiude niente.

Il consumatore di questo lavoro è un team che deve decidere dove mettere il proprio tempo questa settimana. Deve poter leggere l'esito e agire senza rileggere una norma.

## Come ci arrivi

Parti dai quattro assi del profilo di progetto — dimensione, settore, mercato, tipo di sistema. Se ne manca uno che decide un esito, chiedilo: una risposta su quattro assi incompleti è una checklist travestita.

Carica `references/soglie-applicabilita.md` e passa le porte d'ingresso. Per le norme che restano aperte e hanno date o soglie in movimento, verifica sul web prima di dichiarare l'esito.

Non allargare l'elenco oltre ciò che il profilo giustifica. Una norma che non ha nessuna porta aperta verso questo progetto non entra nemmeno nella colonna degli esclusi: elenca solo ciò che l'utente potrebbe ragionevolmente temere o che qualcuno gli citerà.

## Se il perimetro è vuoto

Dillo e chiudi: «di tutto questo non ti riguarda niente». Poi indica la sola cosa che lo farebbe cambiare — la soglia più vicina, il mercato che non ha ancora aperto, la funzionalità che sposterebbe la categoria. Un perimetro vuoto ha comunque un confine, e sapere dov'è vale quanto l'esito.

## Dopo

Scrivi il perimetro risolto su `{project-root}/_bmad/memory/grl-agent-compliance/notes.md` con la data, così alla prossima sessione non lo ricalcoli. Se un vincolo normativo obbliga il team a una scelta tecnica, quella è una decisione: una riga in append su `{project-root}/_bmad/memory/grl-shared/decisions.md`.
