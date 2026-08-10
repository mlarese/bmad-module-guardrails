# Scansione completa

L'esito è **una lista sola**, nella forma della tabella del `SKILL.md`, che copre tutti e quattro
gli assi e sta sotto gli otto punti. Chi la legge deve poter decidere cosa sistemare per primo
senza riaprire il codice.

Gli assi sono quattro perché trovano cose diverse, e un repo può essere pulitissimo su tre e
bloccato sul quarto:

| Asse | Rotta |
| ---- | ----- |
| Percorsi obbligatori senza uscita | `references/percorsi-senza-uscita.md` |
| Rigidità cablata nel codice | `references/rigidita-cablata.md` |
| Blocchi a runtime | `references/blocchi-runtime.md` |
| Procedure di repo e pipeline | `references/procedure-di-repo.md` |

## Da dove si entra

Il codice che nessuno esegue non blocca nessuno, quindi la scansione parte da dove il software
viene usato davvero: gli entry point (rotte HTTP, comandi CLI, handler di coda, job schedulati) e
i percorsi che il profilo di progetto dice essere il mestiere principale. Da lì si scende.

Due sorgenti valgono più di qualunque lettura sistematica, e vanno cercate per prime perché sono
prove già scritte:

- **gli script fuori procedura** — `scripts/fix_*`, `manage.py shell`, i notebook, le query di
  correzione a mano: ognuno è la controprova di un blocco che qualcuno ha già colpito;
- **i commenti che si scusano** — `TODO`, `HACK`, `per ora`, `temporaneo`, `non toccare`: chi li
  ha scritti stava aggirando qualcosa.

Se il repository ha una cronologia leggibile, i file toccati sempre insieme a un fix urgente
raccontano dove il sistema costringe.

## Come si chiude

Ordina per chi ci sbatte oggi, non per gravità teorica: quante volte capita e chi ne paga il
costo. Un blocco quotidiano su una persona sta sopra a un blocco catastrofico che nessuno ha mai
raggiunto.

Poi taglia. Oltre i sette-otto punti la lista smette di essere una priorità: consegna i primi e
liquida gli altri in **una riga sola**, con il conteggio per asse — «restano 12: 4 di rigidità
cablata, 3 di percorso, 3 di runtime, 2 di repo». Non rienumerarli, nemmeno raggruppati per tipo:
un elenco delle voci escluse è la lista lunga rimessa in campo dalla porta di servizio.

Chiudi sempre dichiarando **cosa non è stato guardato** — le cartelle saltate, gli assi non
percorsi, il codice che non si è potuto leggere. Una lista senza il suo perimetro si legge come
se fosse completa, e non lo è quasi mai.

Se dopo la scansione non è rimasta nessuna voce, l'esito è «nessun blocco» e si consegna con la
stessa sicurezza di una lista lunga, insieme al perimetro guardato.
