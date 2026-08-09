# Eval di grl-legal-updates

I casi verificano periodo inclusivo, distinzione fra stato dell'atto e data di efficacia, fonti
primarie, lineage di sostituzione e obbligo dei due gate `bmad-review`. Se Deep Recon non è
disponibile ma il web sì, il modo è `collection_mode: live_manual`; senza web è
`materials_only` e la verifica corrente resta `blocked`. I due gate diventano
`review_mode: manual_review` se `bmad-review` non è esposto. Il workflow deve degradare a
`unverified`, `partial` o `blocked` quando una fonte live o una parte della copertura non è
accessibile; non deve promettere completezza assoluta.
