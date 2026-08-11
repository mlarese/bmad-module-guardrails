# Guardrails (`grl`)

Guardrails is a [BMad](https://github.com/bmad-code-org/BMAD-METHOD) module with **twenty-three agents**
that support software development teams across privacy and GDPR, security, legal, compliance,
tax, design, customer journey, visual storytelling, contextual search, landing/home page references, curtain and gallery cinematics, video-to-scroll direction, code and database architecture, blocking points,
embedded firmware, operations, healthcare, AI, WordPress, SEO, social/content, creative video, AI image generation,
revenue management, product configuration, GitHub issue triage, and paid media.

Agents surface constraints and risks while changes are still inexpensive; decisions remain with
the team. They speak operationally, do not produce formal documents, and do not replace qualified
professionals. Workflows coordinate the path from analysis to delivery.

Whatever an agent claims, it claims from something readable: a file and a line, a primary source,
a dated record. Where it cannot check, it says so instead of filling the gap.

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
| 🧭 **Marea** — Customer Journey & Visual Storytelling Strategist | Client story, location, business placement, landing/home page references, curtain and gallery cinematics, customer journeys, visual narratives, contextual search systems, and video-to-scroll direction | Turns a real client story and its place into a page reference with ordered sections, CTAs, curtain/reveal transitions and gallery direction, a situated journey, static scroll direction, or an explicit video-source plan choosing scrub versus optimized frames; rights, performance, accessibility, and Codex generation stay behind gates. |
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
| 📋 **Tito** — Issue Triage & Backlog Steward | GitHub issues, backlog and triage, work states, readiness before development, hold signals, recorded decisions, duplicates, and dependencies | Reads the dated local issue registry and always states how old it is; groups issues by work state and shows what each one is about, not just its title. Searches the code before judging, so «which export?» becomes «I find three — which one?». Remembers the decisions already taken and cites them instead of reopening them. Treats issue bodies and comments as untrusted data, never as instructions, and writes the missing question instead of inventing the missing requirement. |
| 🔩 **Ines** — Product Configuration Specialist | RFQs, tender specs, customer documents, product options and variants, compatibility rules, product catalogs, and CPQ | Turns a customer document into a configuration validated against the company catalog: every choice carries its origin — written, imposed by a rule, or assumed — and whatever the document leaves out stays an open question instead of becoming a silent default. |

## Workflows

Workflows enforce a repeatable path and produce readable artifacts or verdicts. Agents enter only
when the relevant signals and expertise are needed.

| Workflow | When to use it | What it does and leaves behind |
| --- | --- | --- |
| `grl-profile` | At the start of a project or when its context changes | Collects the project profile and writes it to `_bmad/memory/grl-shared/project-profile.md`. |
| `grl-board` | When the same artifact needs multiple review perspectives or a release gate | Convenes the relevant figures, makes exclusions explicit, and returns a summary, conflicts, and verdict. |
| `grl-bug-finder` | When a code path, configuration, integration, or regression behaves incorrectly | Builds a minimal reproduction, traces the failure path, separates evidence from hypotheses, and proposes a regression test without changing the artifact. |
| `grl-mdsw` | When a software feature might fall within the scope of medical devices | Classifies the software against the MDR and identifies the consequences and non-consequences for the plan. |
| `grl-legal-updates` | For legal updates, instruments, validity, and developments in a defined period | Searches primary sources and produces a digest with coverage, `as_of`, checks, and obsolescence. |
| `grl-fiscal-updates` | For tax developments, grants, incentives, amendments, and deadlines | Applies the same verifiable process to requirements, expenses, eligible parties, and tax dates. |
| `grl-video-to-scroll` | To turn a customer journey and an authorized video source into a scroll-driven frame package | Runs a tool preflight first, asks before installing missing capabilities, interviews the client context, searches candidates with rights evidence, extracts local frames after approval, validates the manifest, and hands the scroll specification to `grl-web`. |
| `grl-web` | To create landing pages and websites, consume an approved `scroll-world` package, recreate mockups, or diagnose a page | Starts from the conversion brief, can implement static scroll direction from Marea, and moves the result through review, accessibility, SEO, and delivery. |
| `grl-wordpress-delivery` | To create, resume, migrate, or verify a WordPress delivery | Coordinates Milo and leads the delivery through the `grl-board` release gate. |
| `grl-ads` | For Google Ads/advertising audits, plans, tracking, optimization, and preflight | Prepares controllable change sets and applies them only with scope, approval, limits, and rollback. |
| `grl-social` | For organic strategy, calendars, posts, captions, audits, and social-channel measurement | Produces briefs, calendars, and review-ready content without scheduling or publishing. |
| `grl-social-creative` | For concepts, advertising design, scripts, storyboards, shot lists, and video/social adaptations | Delivers producible creative packages for posts, Reels, TikToks, and Shorts without editing or uploading. |
| `grl-revenue-audit` | To verify exports, data quality, KPIs, and revenue decisions | Produces a read-only audit with formulas, sources, blockers, and missing data. |
| `grl-revenue-plan` | To build pricing, demand, and profit scenarios | Separates the economic floor, market, and demand, with monitoring triggers and no rate publishing. |
| `grl-revenue-preflight` | Before sending prices to a PMS or Channel Manager | Verifies the contract, mapping, dry-run, response, reconciliation, idempotency, and rollback. |
| `grl-automation` | For repeatable processes across development, legal, tax, design, healthcare, paid media, and revenue management | Routes work from read-only checks through dry-run to observable execution, separating approvals and rollback. |
| `grl-issues` | To keep a dated local registry of open GitHub issues and update it during a work session | Syncs incrementally, assigns each issue one work state (to assess, to clarify, to do, in progress, on hold, not approved, closed), records the decisions taken on the backlog with who decided and why, opens and closes a work session with a declared scope, and reports what actually got closed. Reads GitHub only; it never comments, closes, or edits labels. |
| `grl-issue-readiness` | Before assigning or starting a GitHub issue | Applies seven criteria with citations and checks the entry point against the code — a file named in the issue but absent from the repository does not satisfy it. Detects who already asked to wait, returns a ready/not-ready verdict, and publishes a single recognizable clarification comment after explicit confirmation. |
| `grl-issue-build` | To turn a clarified GitHub issue into code | Checks that a comment carries the full explanation — expected behavior, acceptance criterion, entry point, exclusions — builds a brief where every line cites its source, and hands the work to `bmad-build` only after an explicit authorization. Without that explanation it stops and sends the issue back to the readiness check. |
| `grl-issue-verify` | Before closing a GitHub issue, to check that the code actually resolves it | Reads the code around the diff, not only the diff, then maps every acceptance criterion onto it with file-and-line evidence. Flags work no criterion asked for, records which tests actually ran, and authorizes closing only when every criterion is covered. It prepares the closing comment and command; a person runs them. |
| `grl-toolchain` | To find, assess, and install skills and MCP servers across every agent harness on the machine | Translates a candidate into each harness's own syntax, writes only after a dry-run and a backup, and refreshes its own harness cards from the source. |

The repository contains the complete bundle; derived thematic modules share the same agents and
workflows within their area. See `CLAUDE.md` and `docs/module-plan.md` for architecture, build,
and project decisions.
