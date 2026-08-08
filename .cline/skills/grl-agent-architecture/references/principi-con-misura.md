---
name: principi-con-misura
description: SOLID, KISS, DRY e separazione delle responsabilità applicati dove producono un danno reale, e lasciati stare dove non ne producono
code: PM
---

# Principi applicati con misura

## Com'è fatto un buon esito

L'utente sa **dove un principio è violato con danno** — e dove invece la violazione va lasciata dov'è. Il secondo elenco è spesso più lungo del primo, e va detto.

## Il test del danno

Prima di nominare un principio, rispondi a tre domande su **questo** codice:

1. **Chi paga?** Chi apre quel file, e quante persone sono.
2. **Quando?** Alla prossima feature, fra sei mesi, mai.
3. **Quanto?** File da aprire in più, conflitti di merge, test che non si isolano, bug che tornano.

Se non sai rispondere a tutte e tre, **non è una violazione che conta**: non nominarla. Un principio invocato senza conseguenza concreta è dogma.

## Quando ciascun principio conta davvero

| Principio | Conta quando | «Qui non serve» quando |
| --------- | ------------ | ---------------------- |
| **SRP** — una sola responsabilità | due motivi di cambiamento diversi vivono nello stesso file e due persone ci si pestano | il file è lungo ma coeso e cambia sempre per lo stesso motivo. La lunghezza non è una violazione |
| **OCP** — aperto/chiuso | ogni caso nuovo obbliga a modificare lo stesso `switch` in più punti sparsi | i casi sono due, chiusi, e non se ne aggiungeranno |
| **LSP** — sostituibilità | esiste una vera gerarchia polimorfica e qualcuno sostituisce davvero il tipo base | non c'è ereditarietà, o c'è una sola sottoclasse. Nel codice a composizione è quasi sempre inapplicabile |
| **ISP** — interfacce segregate | chi implementa è costretto a scrivere metodi che non userà mai | le interfacce sono piccole, o non ci sono interfacce ma funzioni |
| **DIP** — inversione delle dipendenze | al confine con l'esterno: database, rete, orologio, filesystem, servizi a pagamento | fra due moduli interni entrambi tuoi, che cambi insieme e distribuisci insieme |
| **DRY** | i due punti duplicati **cambiano sempre insieme** perché rappresentano la stessa regola | si somigliano per caso. Fattorizzarli non risparmia codice: crea un accoppiamento fra due parti destinate a divergere |
| **KISS** | hai in mano l'alternativa più semplice, concreta e scrivibile | è solo un giudizio estetico. «Semplifica» senza la versione semplice accanto non è un'osservazione |
| **Separazione delle responsabilità** | si giudica sui **motivi di cambiamento**, non sui sostantivi. Due cose che cambiano per motivi diversi vanno separate | la separazione seguirebbe solo il vocabolario del dominio (`Manager`, `Service`, `Handler`) senza che nulla cambi separatamente |

Regola pratica su DRY: **alla terza volta**, non alla seconda. Due occorrenze sono un caso, tre sono una regola.

## Cosa consegni

Per ogni punto che supera il test del danno, una riga sola:

> `percorso/file.ext` — cosa succede oggi · **costo se resta** · rimedio minimo

Il rimedio minimo è quasi sempre spostare, rinominare o eliminare. Se il rimedio che ti viene in mente introduce uno strato nuovo, fermati e verifica di non stare risolvendo un problema di stile con un costo strutturale.

## Cosa non consegni mai

- L'elenco dei principi **rispettati**. Non è informazione, è un compito scolastico.
- Il nome del principio senza il file. Se non c'è un file, non c'è osservazione.
- Più di quattro-cinque punti. Un elenco lungo viene ignorato per intero, e allora tanto valeva tacere.
