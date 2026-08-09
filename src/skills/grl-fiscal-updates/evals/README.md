# Eval di grl-fiscal-updates

I casi verificano la finestra di un mese, l'uso di fonti fiscali live, la distinzione fra atto
ufficiale e commento professionale, la lineage di sostituzione/proroga e i due gate `bmad-review`
prima di dichiarare una misura attuale o applicabile. Se le capability non sono disponibili, il
fallback è esplicito: `collection_mode: live_manual` con web disponibile, `materials_only` senza
web, e `review_mode: manual_review` per i due gate. La completezza è sempre riferita al perimetro
dichiarato e a una data `as_of` oppure `pending` se il run è bloccato.
