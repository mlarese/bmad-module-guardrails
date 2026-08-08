---
name: dispositivo-medico
description: Quando un software è dispositivo medico, in che classe cade per la Regola 11 e cosa cambia nel progetto da quella classe in su
code: DM
added: 2026-08-07
type: reference
---

# Software come dispositivo medico

**Data di riferimento di questo file: 7 agosto 2026.** Prima di usare una classe o una data per decidere un esito, verificala sul web.

Il percorso guidato che porta al verdetto è il workflow **`grl-mdsw`**: finalità dichiarata → Regola 11 → classe → conseguenze. Questo file è la materia che serve quando la domanda arriva a te direttamente, senza passare dal workflow.

## Qualificazione: decide la finalità, non la tecnologia

Qualifica ciò che il **fabbricante dichiara** come destinazione d'uso del software — nella documentazione, nel materiale commerciale, nell'interfaccia. Non la sofisticazione tecnica, non la presenza di un modello, non il linguaggio. Riferimento: **MDCG 2019-11**, guida sulla qualificazione e classificazione del software ai sensi di MDR e IVDR.

Il crinale operativo è uno solo:

| Cosa fa il software sui dati | Qualifica? |
| --- | --- |
| Archivia, trasmette, comprime senza perdita, mostra tali e quali | **no** |
| Interpreta, calcola, correla, suggerisce, allerta su un **singolo paziente** | **sì** |

Resta fuori, salvo che la finalità dichiarata dica altro:

- benessere, fitness, stili di vita;
- gestionali amministrativi di studio, poliambulatorio, ospedale;
- agende e prenotazioni, CUP;
- cartelle cliniche usate come archivio, senza elaborazione del contenuto;
- motori di ricerca su letteratura scientifica;
- software di gestione della struttura (magazzino, turni, fatturazione).

## Classificazione: Regola 11, Allegato VIII, Reg. (UE) 2017/745

| Cosa fa il software | Classe |
| --- | --- |
| Fornisce informazioni usate per decisioni diagnostiche o terapeutiche | **IIa** almeno |
| …e la decisione può causare deterioramento grave della salute o un intervento chirurgico | **IIb** |
| …e la decisione può causare la morte o un deterioramento irreversibile | **III** |
| Monitora processi o parametri fisiologici | **IIa** |
| …e la variazione del parametro può portare a pericolo immediato per il paziente | **IIb** |
| Tutto il resto del software che qualifica | I |

**La Regola 11 spinge quasi tutto il supporto alle decisioni fuori dalla classe I.** È la sorpresa più costosa del settore: un team che ha progettato per la classe I si trova con un percorso di conformità che cambia il piano di progetto.

## Cosa cambia dalla classe I in su

Classe I: autocertificazione, il fabbricante dichiara la conformità da solo. Da **IIa** in su serve un **organismo notificato**, con tempi e costi che vanno messi nel piano prima di scrivere codice, non dopo.

| Cosa | Norma | Cosa comporta nel progetto |
| --- | --- | --- |
| Sistema di gestione della qualità | ISO 13485 | procedure scritte e applicate su progettazione, rilascio, assistenza; audit periodici |
| Ciclo di vita del software | **IEC 62304** | classe di sicurezza A/B/C in base al danno possibile; tracciabilità requisito → progettazione → test; gestione dei componenti **SOUP** |
| Gestione del rischio | ISO 14971 | analisi dei rischi mantenuta viva, non un documento iniziale |
| Usabilità | IEC 62366 | l'errore d'uso è un rischio: va valutato e testato con utenti reali |
| Dopo il rilascio | MDR, artt. 83-92 | sorveglianza post-vendita, raccolta dei reclami, vigilanza e segnalazione degli incidenti |

**SOUP** = *software of unknown provenance*: componente di terzi non sviluppato per quell'uso. Riguarda direttamente le dipendenze open source: ognuna va elencata, giustificata, versionata, e i suoi difetti noti vanno valutati come rischi. È il punto che sorprende chi ha una lista di dipendenze lunga.

## La domanda dell'aggiornamento

Una modifica al software può richiedere una **nuova valutazione di conformità**. Vale quando la modifica tocca la destinazione d'uso, la sicurezza, le prestazioni, o l'architettura in modo sostanziale; correzioni di difetti e modifiche senza impatto sul rischio di norma no, ma la distinzione va documentata ogni volta.

Conseguenza sul modo di lavorare: il rilascio continuo non è più gratuito. Va detto **prima** di scegliere il modello di rilascio, non quando la pipeline è già in produzione.

## AI Act × MDR

Un sistema di IA che è **componente di sicurezza** di un dispositivo medico soggetto a valutazione da parte di un organismo notificato ricade nell'**alto rischio dell'Allegato I** dell'AI Act. Gli obblighi si **integrano** con quelli MDR — documentazione tecnica, gestione del rischio, sorveglianza umana confluiscono nel fascicolo già previsto dal MDR — invece di sommarsi meccanicamente come due percorsi paralleli.

Il MDR resta tuo; ruolo, categoria, obblighi e calendario del lato AI Act sono di **Aldo**. Qui dici che i due regimi si incontrano e su cosa, non cosa impone l'AI Act.

**L'integrazione fra i due regimi è in evoluzione — verificare sul web** prima di dichiarare quali obblighi confluiscono e quali restano distinti.

## Altri regimi vicini

| Regime | Quando tocca |
| --- | --- |
| **IVDR**, Reg. (UE) 2017/746 | il software è associato a diagnostica in vitro: interpreta o refertisce risultati di esami di laboratorio |
| **NIS2** | le strutture sanitarie sono settore ad alta criticità; sul fornitore ricade per via **contrattuale**, non diretta → `references/cliente-regolamentato.md` |
| **Conservazione della documentazione sanitaria** | il settore impone tempi di conservazione lunghi: ribalta il ragionamento sulla minimizzazione e sulla cancellazione di **Vera** |

## Trappole

- **Marcare tutto il prodotto quando qualifica solo un modulo.** Il perimetro del dispositivo si delimita: si marca la parte con finalità medica, il resto resta fuori se è separabile e documentato come tale.
- **«Lo usa solo un medico» non esclude la qualificazione.** È il contrario: il supporto alla decisione clinica rivolto a un professionista è proprio il caso della Regola 11.
- **Riformulare la finalità dichiarata mentre il software continua a fare la stessa cosa non regge.** Se il prodotto calcola e suggerisce, scrivere «solo a scopo informativo» nell'interfaccia non lo toglie dal MDR. Va detto all'utente invece di lasciarlo credere.
- **Dare la classe come definitiva.** Quando l'esito dipende da un parere di un organismo notificato, si consegna l'**esito più probabile con il motivo**, non una certificazione.

## Confini

| Questione | Chi |
| --- | --- |
| Dati sanitari, art. 9 GDPR, basi giuridiche, DPIA | **Vera** (`grl-agent-privacy`) |
| Contenuto clinico, codifiche, interoperabilità HL7/FHIR/DICOM, FSE 2.0, workflow di reparto | **Livia** (`grl-agent-health`) |
| Percorso guidato per arrivare al verdetto di qualificazione e classe | workflow **`grl-mdsw`** |
| Impianto tecnico di un componente AI: RAG, orchestrazione, eval, costi | **Enzo** (`grl-agent-ai`) |
