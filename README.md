# Odoo 19 — Accounting, Purchase & Inventory Research

**An evidence-driven examination of Odoo 19's business logic and the technical foundation for ProofFlow.**

> **Project status — 6 November 2026:** The source-research investigation and source/schema archive-preservation workflow have substantial documented evidence. A reconstructable **source-and-schema archive was verified locally**. This repository is **not** a deployed or production-validated Odoo system, and ProofFlow is **not** presented here as a completed Odoo integration.

## Why this repository exists

Accounting exceptions are difficult to resolve when a purchase order, receipt, vendor invoice, journal entry, and payment each contain different values. Those differences are not automatically errors: they may reflect legitimate deliveries, purchase policies, supplier credits, taxes, rounding, currency conversion, or partial payment.

The purpose of this research is to identify **what Odoo actually does**, where each rule resides, what data supports it, and what remains uncertain. ProofFlow is the intended downstream application: a system for detecting, investigating, reviewing, correcting and independently verifying accounting exceptions. That product objective is kept separate from proven Odoo behavior.

Our rule: **question → exact source/command → observed output → interpretation → limitation → next investigation**.

## Navigate the research

| Document | Purpose |
|---|---|
| [Odoo 19 framework architecture](docs/architecture/ODOO19_FRAMEWORK_MAP.md) | Entry points, registry, ORM, modules, security, business logic and PostgreSQL |
| [ProofFlow business logic derived from research](docs/PROOFFLOW_BUSINESS_LOGIC.md) | Purchase-to-pay evidence chain, exception cases, corrective-action boundaries and review gates |
| [Chronological commit research](docs/research/CHRONOLOGICAL_RESEARCH.md) | Historical Git patch order and recorded methodological progression |
| [Integrated observations](docs/research/INTEGRATED_OBSERVATION_INDEX.md) | Phase 1, procurement and nine-domain crosswalk |
| [Nine accounting domains](docs/research/NINE_DOMAIN_EVIDENCE_INDEX.md) | Domain-by-domain source/database findings and evidence status |
| [Source grouping by module](docs/research/SOURCE_GROUPING_BY_MODULE.md) | Original installed paths vs historical snapshots |
| [Reconstruction method](docs/research/RECONSTRUCTION_METHOD.md) | What an archive can—and cannot—reconstruct |
| [Source validation results](docs/research/VALIDATION_RESULTS.md) | Historical source and syntax integrity checks |
| [Local archive milestones](docs/RECONSTRUCTION_CHECKPOINTS.md) | Observed source, dependency, schema and ZIP checks |
| [Methodological evidence standard](docs/RESEARCH_METHODOLOGY.md) | Individual command record template and verification levels |
| [Publication and privacy policy](docs/PUBLICATION_BOUNDARY.md) | What belongs in a public repository vs a private capture |
| [Original temporary notebook](ProofFlow_Odoo19_Temporary_Research_Notebook.md) | Early Phase 1 and procurement investigation |
| [Original purchase/receipt workflow](docs/ProofFlow_Odoo19_Purchase_Receipt_Workflow.md) | Historical purchase-stock method tracing |
| [Field inventory](models/odoo19_field_inventory.csv) | Static Odoo model-field extraction |
| [Model extraction script](scripts/extract_odoo_models.py) | AST-based research tooling |
| [Historical source snapshots](models/source/) | Selected Odoo source copies previously committed |

**Historical evidence caveat:** Some research indexes were authored for an offline archive; relative references to its original terminal files or commit patches may not resolve on GitHub. Those records have not been silently regenerated or invented.

## End-to-end system logic

\`\`\`mermaid
flowchart LR
    A["Purchase order + line\nordered quantity / policy"] --> B["Stock picking + stock.move\ncompleted receipt / return"]
    A --> C["Vendor bill / credit note\naccount.move"]
    B --> D["Receipt-derived quantity"]
    D --> E{"Reconcile evidence\nagainst billing policy"}
    C --> E
    E --> F["Invoice / tax lines\naccount.move.line"]
    F --> G["Posting checks\nbalance + permissions + fiscal date"]
    G --> H["Journal / ledger"]
    H --> I["Payment + partial/full reconciliation"]
    E -. "possible discrepancy" .-> J["ProofFlow candidate exception"]
    J --> K["Evidence + review"]
    K --> L["Authorized correction"]
    L --> M["Independent outcome verification"]
\`\`\`

This diagram is a **conceptual dependency map**. Receipt, bill and payment processing do not necessarily occur in a fixed order, and an accounting difference is not necessarily an exception.

### 1. Purchase commitment

A purchase order, represented by \`purchase.order\` and \`purchase.order.line\`, records the commercial agreement. The source investigation located \`button_confirm()\`, approval conditions, ordered quantity (\`product_qty\`), unit price, discount, tax configuration and invoice policy.

**Key source:** \`purchase/models/purchase_order.py\`, \`purchase/models/purchase_order_line.py\`.

### 2. Physical receipt

The installed \`purchase_stock\` addon extends purchase models. Its purchase approval path invokes \`_create_picking()\`; stock movements and receipts are represented by \`stock.move\` and \`stock.picking\`.

Receiving quantity involves qualifying completed stock moves, returns and unit-of-measure conversion, with exceptional handling for manual receipt quantities and dropshipping. **It is not safe to infer receipt solely from ordered quantity or a picking existing.**

**Key source:** \`purchase_stock/models/purchase_order.py\`, \`purchase_stock/models/purchase_order_line.py\`, \`stock/models/stock_move.py\`.

### 3. Vendor billing and credit notes

Vendor bills are accounting documents (\`account.move\`), while bill lines are journal-line records (\`account.move.line\`). The purchase-line relationship may be represented by \`purchase_line_id\`. Invoiced quantity reflects qualifying bill lines and supplier credits/refunds under Odoo's rules.

**Key source:** \`account/models/account_move.py\`, \`account/models/account_move_line.py\`, \`purchase/models/purchase_order_line.py\`.

### 4. Pricing, tax and currency

\`account.move.line._compute_totals()\` delegates to tax-base preparation and \`account.tax\` calculations and rounding. Discounts, UoM normalization, tax inclusivity, fiscal positions and currency conversion can affect the apparent difference between PO, receipt and invoice.

**Key source:** \`account/models/account_move_line.py\` and related tax/currency models. Detailed trace: [framework map](docs/architecture/ODOO19_FRAMEWORK_MAP.md).

### 5. Posting and ledger entries

Posting through \`account.move.action_post()\` and \`_post()\` is subject to model and explicit access checks, balancing and fiscal-period restrictions. A database row or draft vendor bill does **not** prove a posted financial obligation.

Journal lines carry \`debit\`, \`credit\`, \`balance\` and \`amount_currency\` values, while receivable/payable obligations introduce maturity and residual calculations.

### 6. Payments and reconciliation

Payment registration, payment posting and matching are separate operations. Partial and full reconciliation change which obligations remain outstanding. **Ledger balance is not equivalent to invoice residual**, and posting is not equivalent to settlement.

### 7. System-wide controls

- **Security:** \`ir.model.access\`, \`ir.rule\`, groups, company checks, \`sudo()\`, \`with_company()\` and explicit posting checks.
- **Fiscal controls:** fiscal-year, tax, sale, purchase and hard lock dates, with configured exceptions.
- **Reporting:** base \`account.report\` definitions were found even though separately named reporting addons were absent from inspected paths.
- **Assets:** asset-type account classifications were present, but the dedicated depreciation addon was not available in the inspected installation.

These are **installation-scoped observations**, not statements about all Odoo editions or configurations.

## Source architecture and data paths

\`\`\`text
Odoo request / job / CLI / integration
   |
   +-- HTTP, actions and scheduling
   +-- per-database registry + ORM environment
   +-- installed modules and inherited models
   |   +-- purchase
   |   +-- purchase_stock
   |   +-- stock
   |   +-- account
   +-- access rights, record rules, fiscal and company constraints
   +-- PostgreSQL transaction, tables, relations and constraints
\`\`\`

Important inspected models and database mappings:

| Business object | Model | Physical table |
|---|---|---|
| Purchase order | \`purchase.order\` | \`purchase_order\` |
| Purchase line | \`purchase.order.line\` | \`purchase_order_line\` |
| Stock movement | \`stock.move\` | \`stock_move\` |
| Vendor bill / journal entry | \`account.move\` | \`account_move\` |
| Invoice / journal line | \`account.move.line\` | \`account_move_line\` |
| Payment | \`account.payment\` | \`account_payment\` |
| Accounting security | \`ir.model.access\`, \`ir.rule\` | \`ir_model_access\`, \`ir_rule\` |
| Company settings | \`res.company\` | \`res_company\` |

Model declarations, computed fields, ORM SQL views and relation tables do not always map one-to-one. See the [full architecture map](docs/architecture/ODOO19_FRAMEWORK_MAP.md).

## Research chronology and scope

| Phase | Scope | Key outcome |
|---|---|---|
| Oct 29–30 | Repository setup, source field inventory, early DB-031/DB-036 findings | Structured model/schema evidence |
| Nov 2 — Phase 1 | Invoice-line pricing, tax, discount, UoM and currency source tracing | Dependency-based source review recorded complete; runtime tests deferred |
| Nov 2–3 | Purchase receipt, procurement dispatch, stock rules, pull/push, lead time | Source paths and observed limitations preserved |
| Nov 4–5 | Nine accounting domains | Journal posting through company isolation investigated |
| Nov 5 | Domain 9 commands 6–10 | **New** source/database observations; not retroactively historical |
| Nov 5–6 | Source/schema capture | Complete installed-source TAR, dependency inventory, schema-only dump and ZIP reconstruction |

The original earliest workspace-creation command history remains incomplete. Later re-executed commands are explicitly tagged as **new evidence**.

## Verified reconstruction checkpoints (reported from local execution)

| Measure | Observed output |
|---|---|
| Live vs TAR source-path inventory | **71,801 vs 71,801; zero differences** |
| Archived regular source files | **60,706** |
| Symlinks | **19** |
| Byte-for-byte TAR ↔ ZIP comparisons | **60,706 / 60,706 passed** |
| Link-target comparisons | **19 / 19 passed** |
| Supporting file hashes | **35 / 35 passed** |
| Corrected missing-source inventory | **58 / 58 copied** |
| PostgreSQL schema-only table definitions | **458** |
| Local ZIP integrity | **PASS** |

These measurements come from the user's local commands. The large framework TAR and final ZIP are **not in this GitHub repository**. The research database then contained zero journal entries/journal lines, so the schema and source analysis must not be presented as an end-to-end runtime accounting test.

## ProofFlow: evidence-driven exception handling

**Intended workflow—not a claim of a deployed feature:**

1. Ingest the purchase order line, qualifying receipts/returns and linked vendor bill/credit-note lines.
2. Normalize quantity units, currencies and applicable tax/discount treatment.
3. Evaluate the relevant purchase billing policy and compare justified quantities and amounts.
4. Create an exception only when the discrepancy is meaningful under the policy and supported evidence.
5. Preserve provenance: Odoo model, record IDs, source timestamps, calculations, supporting documents and version of the rule.
6. Assign review; require independent approval where material or privileged corrections are involved.
7. Perform correction only through authorized, auditable operations.
8. Re-read authoritative records and independently verify the outcome; mark stale evidence and unresolved conditions.

Detailed specification and examples: [ProofFlow business logic](docs/PROOFFLOW_BUSINESS_LOGIC.md).

## Research methodology and evidence levels

Each command record should contain: **question, why this method, exact command, actual terminal output, explanation, interpretation, uncertainty, decision, next action, source paths and evidence classification**.

We distinguish source inspection, read-only database observation, runtime execution, architectural inference and proposed business rules. Blocked source searches remain recorded as blocked; negative results are not silently translated into claims of absence.

See [research methodology](docs/RESEARCH_METHODOLOGY.md).

## Public-repository safety and attribution

This is a **public** repository. Do not commit credentials, private database dumps, local capture paths containing personal data, Odoo filestore contents, production configurations, or the large reconstructed framework/ZIP. Preserve those privately with checksums. The full installed Odoo code is better obtained from its upstream sources under the applicable licenses; this repository preserves selected historical snapshots and independent analysis.

Upstream: https://github.com/odoo/odoo  
Research source baseline recorded: \`7c45959e02b2d8abc52913184237b72f7bae93a2\` (per-file/local-image revision equivalence has not been independently established).

**Independent research — not affiliated with or endorsed by Odoo S.A.** This repository is a research foundation, not a certification of Odoo security or ProofFlow production readiness.
