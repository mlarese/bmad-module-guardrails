# Guardrails (`grl`)

Guardrails è un modulo [BMad](https://github.com/bmad-code-org/BMAD-METHOD) con **quattordici agenti**
che affiancano il team nello sviluppo software: privacy e GDPR, sicurezza, legale, compliance,
fisco, design, architettura, operations, sanità, AI, WordPress, SEO, revenue management e paid media.

Gli agenti fanno emergere vincoli e rischi mentre cambiare è ancora economico; le decisioni restano
al team. Parlano in modo operativo, non producono documenti formali né sostituiscono professionisti
abilitati. I workflow coordinano invece il percorso, dall'analisi alla consegna.

## Agenti

Gli agenti sono interattivi: si convoca la competenza decisiva per la domanda concreta. Per una
revisione multidisciplinare dello stesso artefatto si usa `grl-board`.

| Agente | Ambito | Cosa porta |
| --- | --- | --- |
| 🛡️ **Vera** — Data Protection Officer | Dati personali, GDPR, DPIA, retention, analytics, log e dati nei prompt | Mappa dati, base giuridica, minimizzazione e rischi privacy; distingue l'obbligo reale dalla prassi. |
| 🔐 **Kai** — Application Security Engineer | API, autenticazione, autorizzazione, segreti, dipendenze, CVE e superfici LLM | Ordina gli attacchi realistici e propone la contromisura minima con il relativo costo. |
| ⚖️ **Aldo** — Tech Lawyer | Licenze, contratti, DPA, titolarità, output AI e AI Act | Traduce il vincolo legale in una decisione su uso, distribuzione, accordi e obblighi. |
| 📐 **Nils** — Regulatory Compliance | NIS2, DORA, EAA/WCAG, eIDAS, CRA, MDR e obblighi settoriali | Stabilisce se una norma si applica, quale soglia la attiva e quali obblighi ne derivano. |
| 🧾 **Marta** — Fiscalista e Finanza Agevolata | Imposte, IVA, bandi, incentivi, credito d'imposta e rendicontazione | Verifica fonti primarie, requisiti, scadenze e spese ammissibili in un pre-screening operativo. |
| 👁️ **Iris** — Design Critic | UI, landing, markup, CSS, tipografia, palette, densità e layout | Riconosce i pattern generici e propone una deviazione visiva concreta e utilizzabile. |
| 🧱 **Otto** — Code Architect | Confini, cartelle, dipendenze, interfacce, factory e strati architetturali | Indica il punto giusto in cui collocare una responsabilità e pesa il costo delle alternative. |
| 🖥️ **Bruno** — Infrastructure & Ops Engineer | Server, VPS, Docker, CI/CD, deploy, TLS, backup, log e incidenti | Propone l'impianto operativo più semplice che regge il carico e una via di ritorno verificabile. |
| 🩺 **Livia** — Clinical Informatics | Dati clinici, codifiche, HL7/FHIR/DICOM, workflow di reparto e sicurezza del paziente | Verifica modello dati, interoperabilità e uso reale; indirizza a `grl-mdsw` quando emerge il MDR. |
| 🧠 **Enzo** — AI Engineer | LLM, prompt, RAG, embedding, tool calling, eval, costi e latenza | Progetta l'impianto minimo che regge quando il modello sbaglia e valuta se serve davvero. |
| 🧩 **Milo** — WordPress Component Architect | Gutenberg, Elementor, ACF, post type, template parts e Media Library | Progetta contenuti e componenti riusabili, con Gutenberg come default e confini chiari. |
| 🔎 **Nora** — SEO Strategist & Search Systems Auditor | Intento, crawling, indicizzazione, contenuti, dati strutturati e Search Console | Verifica le regole e lo stato osservato, distingue fatti da ipotesi e non promette ranking. |
| 📣 **Dalia** — Media Manager & Paid Advertising Strategist | Google Ads, ADV, audience, creatività, tracking, consenso, budget e policy | Traduce l'obiettivo in un piano misurabile e prepara change set con dry-run e rollback. |
| 📈 **Rhea** — Revenue Management Strategist | Occupazione, ADR, RevPAR, TRevPAR, NRevPAR, GopPAR, MUP, MOL, pickup, forecast, pricing, PMS e Channel Manager | Collega costi, domanda, inventario e canale; mostra formule e assunzioni, separa floor economico, prezzo consigliato e prezzo pubblicato e blocca l'invio senza un gate verificato. |

## Workflow

I workflow impongono un percorso ripetibile e producono artefatti o verdetti leggibili. Gli agenti
entrano solo sui segnali e sulle competenze necessarie.

| Workflow | Quando usarlo | Cosa fa e cosa lascia |
| --- | --- | --- |
| `grl-profile` | All'inizio del progetto o quando il contesto è cambiato | Raccoglie il profilo di progetto e lo scrive in `_bmad/memory/grl-shared/project-profile.md`. |
| `grl-board` | Quando lo stesso artefatto richiede più assi di revisione o un release gate | Convoca le figure pertinenti, rende esplicite le esclusioni e restituisce riepilogo, conflitti e verdetto. |
| `grl-mdsw` | Quando una funzione software potrebbe rientrare nel perimetro dei dispositivi medici | Classifica il software rispetto al MDR e indica conseguenze e non-conseguenze per il piano. |
| `grl-legal-updates` | Per aggiornamenti legali, atti, vigenza e novità in un periodo definito | Cerca fonti primarie e produce un digest con copertura, `as_of`, verifiche e obsolescenza. |
| `grl-fiscal-updates` | Per novità fiscali, bandi, incentivi, emendamenti e scadenze | Applica lo stesso percorso verificabile a requisiti, spese, soggetti e date fiscali. |
| `grl-web` | Per creare landing e siti, riprendere mockup o diagnosticare una pagina | Parte dal brief di conversione e porta il risultato verso review, accessibilità, SEO e consegna. |
| `grl-wordpress-delivery` | Per creare, riprendere, migrare o verificare una consegna WordPress | Coordina Milo e conduce la consegna fino al release gate di `grl-board`. |
| `grl-ads` | Per audit, piano, tracking, ottimizzazione e preflight Google Ads/ADV | Prepara change set controllabili e applica solo con scope, approvazione, limite e rollback. |
| `grl-revenue-audit` | Per verificare export, qualità dati, KPI e decisioni revenue | Produce un audit read-only con formule, fonti, blocker e dati mancanti. |
| `grl-revenue-plan` | Per costruire scenari di pricing, domanda e profitto | Separa floor, mercato e domanda, con trigger di monitoraggio senza pubblicare tariffe. |
| `grl-revenue-preflight` | Prima di inviare prezzi a PMS o Channel Manager | Verifica contratto, mapping, dry-run, response, riconciliazione, idempotenza e rollback. |
| `grl-automation` | Per processi ripetitivi fra sviluppo, legale, fisco, design, medicina, paid media e revenue management | Instrada il lavoro da read-only a dry-run ed esecuzione osservabile, separando approvazioni e rollback. |

Il repository contiene il bundle completo; i moduli tematici derivati condividono gli stessi agenti
e workflow nel perimetro dell'area. Per architettura, build e decisioni di progetto si vedano
`CLAUDE.md` e `docs/module-plan.md`.
