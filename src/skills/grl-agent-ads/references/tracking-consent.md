# Tracking, conversioni e consenso

## Mappa degli eventi

Per ogni evento registra:

| Campo | Esempio di domanda |
| --- | --- |
| Nome | È un nome stabile o dipende da un bottone che cambia? |
| Trigger | Quale azione reale lo genera? È possibile duplicarlo con refresh o retry? |
| Fonte | Google tag, GA4, server, CRM, import offline o piattaforma terza? |
| Primary/secondary | Deve guidare l'ottimizzazione o serve solo alla diagnosi? |
| Valore | Il valore è reale, coerente e definito dal business? |
| Attribuzione | Finestra, modello, timezone e regola di conteggio sono noti? |
| Validazione | Come si verifica il passaggio da click a lead valido o vendita? |
| Consenso | Quale scelta dell'utente abilita storage, personalizzazione o upload? |

Non basta che il tag scatti: un evento può essere tecnicamente presente e businessmente inutile.
Controlla duplicazioni, cross-domain, redirect, form error, chiamate server, CRM e riconciliazione
con le vendite.

## Confine con Vera

Dalia descrive il flusso tecnico e il dato necessario al piano. Vera decide il trattamento,
minimizzazione, base giuridica, retention, informative, consenso e perimetro dei dati personali.
Customer Match, conversioni avanzate, remarketing, import offline e dati sanitari non si attivano
solo perché migliorano la misura.

## Output minimo

Restituisci `tracking_status` come uno fra:

- `ready_for_read_only_check` — il mapping esiste ma non è stato verificato;
- `partially_verified` — alcuni eventi sono verificati e altri no;
- `blocked` — manca consenso, accesso, definizione, fonte o controllo necessario;
- `verified_for_scope` — solo dopo aver indicato perimetro, data, strumenti e limiti.

Non usare `fully_compliant` o `accurate` senza una verifica specifica e senza il passaggio della
figura competente.
