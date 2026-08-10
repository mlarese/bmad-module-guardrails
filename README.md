# Guardrails (`grl`)

Guardrails is a [BMad](https://github.com/bmad-code-org/BMAD-METHOD) module with **twenty-one agents**
that support software development teams across privacy and GDPR, security, legal, compliance,
tax, design, code and database architecture, blocking points, embedded firmware, operations, healthcare, AI, WordPress, SEO,
social/content, creative video, AI image generation, revenue management, product configuration, and paid media.

Agents surface constraints and risks while changes are still inexpensive; decisions remain with
the team. They speak operationally, do not produce formal documents, and do not replace qualified
professionals. Workflows coordinate the path from analysis to delivery.

## Agents

Agents are interactive: summon the expertise that decides the concrete question. For a
multidisciplinary review of the same artifact, use `grl-board`.

| Agent | Scope | What it contributes |
| --- | --- | --- |
| 🛡️ **Vera** — Data Protection Officer | Personal data, GDPR, DPIAs, retention, analytics, logs, and data in prompts | Maps data, legal bases, minimization, and privacy risks; distinguishes actual obligations from common practice. |
| 🔐 **Kai** — Application Security Engineer | APIs, authentication, authorization, secrets, dependencies, CVEs, and LLM attack surfaces | Prioritizes realistic attacks and proposes the smallest countermeasure with its associated cost. |
| ⚖️ **Aldo** — Tech Lawyer | Licenses, contracts, DPAs, ownership, AI outputs, and the AI Act | Translates legal constraints into decisions about use, distribution, agreements, and obligations. |
| 📐 **Nils** — Regulatory Compliance | NIS2, DORA, EAA/WCAG, eIDAS, CRA, MDR, and sector-specific obligations | Determines whether a rule applies, what threshold activates it, and which obligations follow. |
| 🧾 **Marta** — Tax and Incentives Specialist | Taxes, VAT, grants, incentives, tax credits, and reporting | Checks primary sources, requirements, deadlines, and eligible expenses in an operational pre-screening. |
| 👁️ **Iris** — Design Critic | UI, landing pages, markup, CSS, typography, palettes, density, and layout | Recognizes generic patterns and proposes a concrete, usable visual departure. |
| 🧱 **Otto** — Code Architect | Boundaries, folders, dependencies, interfaces, factories, architectural layers, and the architectural constraints of a story or spec | Identifies the right place for a responsibility and weighs the cost of alternatives; on a story still being written, delivers constraints that are verifiable at review time. |
| 🚧 **Vito** — Blocking Points Analyst | Mandatory paths, state machines, gates and approvals, hardcoded rigidity, runtime stalls, and repo or pipeline gates | Reads the code as someone stuck inside it and returns a list of possible blocking points, ordered by who hits them today, with the file, who gets stuck, the workaround already in use, and the exit that is missing. Reads only; never asks to remove a deliberate control. |
| 🗄️ **Dario** — Database Architect & Designer | Data models, PostgreSQL, Oracle, MongoDB, Redis/Valkey, distributed SQL, NoSQL, search, analytics, time-series, graph, vector and hybrid search | Chooses persistence from workload and invariants, verifies current solutions live, and carries the decision through schema, performance, reliability, benchmark, and migration. |
| ⚙️ **Ada** — Firmware Engineer | MCU/SoC firmware, startup, drivers, registers, interrupts/DMA, RTOS, timing, memory, testing, debugging, and secure updates | Turns embedded changes into compilable, measurable, recoverable firmware and refuses to invent a target-specific contract. |
| 🖥️ **Bruno** — Infrastructure & Ops Engineer | Servers, VPS, Docker, CI/CD, deployment, TLS, backups, logs, and incidents | Proposes the simplest operational setup that can handle the load and a verifiable way back. |
| 🩺 **Livia** — Clinical Informatics | Clinical data, codes, HL7/FHIR/DICOM, clinical workflows, and patient safety | Checks the data model, interoperability, and real-world use; routes to `grl-mdsw` when MDR becomes relevant. |
| 🧠 **Enzo** — AI Engineer | LLMs, prompts, RAG, embeddings, tool calling, evaluations, costs, and latency | Designs the minimum setup that remains reliable when the model is wrong and assesses whether it is actually needed. |
| 🧩 **Milo** — WordPress Component Architect | Gutenberg, Elementor, ACF, post types, template parts, and the Media Library | Designs reusable content and components, with Gutenberg as the default and clear boundaries. |
| 🔎 **Nora** — SEO Strategist & Search Systems Auditor | Intent, crawling, indexing, content, structured data, and Search Console | Verifies the rules and observed state, distinguishes facts from hypotheses, and makes no ranking promises. |
| 📣 **Dalia** — Media Manager & Paid Advertising Strategist | Google Ads, advertising, audiences, creative, tracking, consent, budgets, and policies | Turns the objective into a measurable plan and prepares change sets with dry-run and rollback. |
| 📱 **Sofia** — Social Media & Content Strategist | Organic strategy, content pillars, calendars, posts, captions, community, and metrics | Turns objectives and audiences into producible, approvable, measurable social content without promising reach. |
| 🎬 **Marco** — Advertising Creative Director & Short-form Video Producer | Advertising concepts, design, scripts, storyboards, shot lists, Reels, TikToks, and Shorts | Takes an idea from brief to a producible creative package, with variants and gates for claims, rights, and privacy. |
| 🖼️ **Elio** — AI Image Generation & Post-production Specialist | Nano Banana, Imagen, GPT Image, Photoshop, prompts, masks, subject consistency, provenance, and export | Picks the tool the task actually needs, writes the prompt that drives it, generates the files on request behind a dry-run and an explicit confirmation, and separates generative work from deterministic post-production. |
| 📈 **Rhea** — Revenue Management Strategist | Occupancy, ADR, RevPAR, TRevPAR, NRevPAR, GOPPAR, MUP, MOL, pickup, forecasting, pricing, PMS, and Channel Manager | Connects costs, demand, inventory, and channel; shows formulas and assumptions, separates the economic floor, recommended price, and published price, and blocks transmission without a verified gate. |
| 🔩 **Ines** — Product Configuration Specialist | RFQs, tender specs, customer documents, product options and variants, compatibility rules, product catalogs, and CPQ | Turns a customer document into a configuration validated against the company catalog: every choice carries its origin — written, imposed by a rule, or assumed — and whatever the document leaves out stays an open question instead of becoming a silent default. |

## Workflows

Workflows enforce a repeatable path and produce readable artifacts or verdicts. Agents enter only
when the relevant signals and expertise are needed.

| Workflow | When to use it | What it does and leaves behind |
| --- | --- | --- |
| `grl-profile` | At the start of a project or when its context changes | Collects the project profile and writes it to `_bmad/memory/grl-shared/project-profile.md`. |
| `grl-board` | When the same artifact needs multiple review perspectives or a release gate | Convenes the relevant figures, makes exclusions explicit, and returns a summary, conflicts, and verdict. |
| `grl-mdsw` | When a software feature might fall within the scope of medical devices | Classifies the software against the MDR and identifies the consequences and non-consequences for the plan. |
| `grl-legal-updates` | For legal updates, instruments, validity, and developments in a defined period | Searches primary sources and produces a digest with coverage, `as_of`, checks, and obsolescence. |
| `grl-fiscal-updates` | For tax developments, grants, incentives, amendments, and deadlines | Applies the same verifiable process to requirements, expenses, eligible parties, and tax dates. |
| `grl-web` | To create landing pages and websites, recreate mockups, or diagnose a page | Starts from the conversion brief and moves the result through review, accessibility, SEO, and delivery. |
| `grl-wordpress-delivery` | To create, resume, migrate, or verify a WordPress delivery | Coordinates Milo and leads the delivery through the `grl-board` release gate. |
| `grl-ads` | For Google Ads/advertising audits, plans, tracking, optimization, and preflight | Prepares controllable change sets and applies them only with scope, approval, limits, and rollback. |
| `grl-social` | For organic strategy, calendars, posts, captions, audits, and social-channel measurement | Produces briefs, calendars, and review-ready content without scheduling or publishing. |
| `grl-social-creative` | For concepts, advertising design, scripts, storyboards, shot lists, and video/social adaptations | Delivers producible creative packages for posts, Reels, TikToks, and Shorts without editing or uploading. |
| `grl-revenue-audit` | To verify exports, data quality, KPIs, and revenue decisions | Produces a read-only audit with formulas, sources, blockers, and missing data. |
| `grl-revenue-plan` | To build pricing, demand, and profit scenarios | Separates the economic floor, market, and demand, with monitoring triggers and no rate publishing. |
| `grl-revenue-preflight` | Before sending prices to a PMS or Channel Manager | Verifies the contract, mapping, dry-run, response, reconciliation, idempotency, and rollback. |
| `grl-automation` | For repeatable processes across development, legal, tax, design, healthcare, paid media, and revenue management | Routes work from read-only checks through dry-run to observable execution, separating approvals and rollback. |
| `grl-toolchain` | To find, assess, and install skills and MCP servers across every agent harness on the machine | Translates a candidate into each harness's own syntax, writes only after a dry-run and a backup, and refreshes its own harness cards from the source. |

The repository contains the complete bundle; derived thematic modules share the same agents and
workflows within their area. See `CLAUDE.md` and `docs/module-plan.md` for architecture, build,
and project decisions.
