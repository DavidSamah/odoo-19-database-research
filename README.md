# Odoo 19 — Database & Architecture Research

**An independent, evidence-driven investigation of Odoo 19's accounting, procurement, inventory, and ORM architecture.**

**Research status:** Active — Source-code analysis and relationship mapping  
**Development approach:** Research → Verify → Design → Implement → Test → Deploy

## 1. About This Project

I began this project to understand Odoo's internal architecture before developing an application that integrates with its business workflows.

As a self-taught software developer, I approach complex systems by breaking them down into their underlying components, studying their relationships, testing assumptions, and documenting findings before implementation.

Rather than immediately writing a new Odoo application, I chose to investigate how Odoo already manages accounting records, purchase orders, inventory movements, and vendor bills.

This repository documents that investigation and the reproducible tooling developed along the way.

## 2. Research Completed So Far

### Environment and Version Control

- Established a local research environment using Python 3.11.9, Git, and Docker Desktop.
- Verified Docker Engine 29.7.2 and identified an existing PostgreSQL 17 staging environment.
- Kept the existing PostgreSQL database volume separate from the Odoo research.
- Pinned the Odoo 19 source investigation to commit `7c45959e02b2d8abc52913184237b72f7bae93a2`.
- Created Git checkpoints to preserve reproducible research progress.

### Odoo ORM Model Analysis

Developed a Python AST-based analyzer to examine Odoo model declarations.

**Initial extraction results:**

| Metric | Result |
|---|---:|
| Source files analyzed | 4 |
| Field declarations extracted | 353 |
| Many2one relationships | 82 |
| One2many relationships | 15 |
| Many2many relationships | 21 |
| Total relational declarations | 118 |

The initial investigation focused on:

- `account.move` — Journal entries and vendor bills
- `account.move.line` — Accounting line items
- `purchase.order` — Purchase orders
- `stock.move` — Inventory movements

The analyzer produces a CSV inventory containing field names, field types, model declarations, source locations, and selected field attributes.

These results represent static source-code declarations, not the complete runtime PostgreSQL schema.

### Accounting and Purchasing Relationships

Traced relationships connecting purchase order lines, vendor bill lines, and their parent accounting records.

Verified that Odoo links purchase order lines to accounting lines through `purchase_line_id`, and uses related record traversal to derive purchase order billing relationships.

This investigation also established that invoice lines are a filtered subset of accounting move lines, rather than a completely separate underlying model.

### Inventory and Receipt Calculations

Examined Odoo's `purchase_stock` module to understand how received quantities are derived from stock movements.

The source investigation covered:

- Completed stock movements
- Supplier returns
- Receipt eligibility
- Unit-of-measure conversions
- Manual receipt quantities
- Special dropshipping conditions

An important finding was that Odoo's receipt calculations involve business rules beyond simply summing stock quantities.

### Vendor Billing and Credit Notes

Investigated how Odoo computes invoiced quantities and determines quantities remaining to be billed.

Verified that vendor bills contribute positively to invoiced quantities, while qualifying supplier credit notes reduce those quantities.

Also examined how product billing policies affect whether invoiceable quantities are calculated from ordered or received quantities.

### Existing Bill-Matching Functionality

Studied Odoo's `purchase.bill.line.match` implementation.

The investigation identified:

- A SQL-backed matching view
- Purchase-order-line and vendor-bill-line selection
- Product-based matching behavior
- Creation of draft vendor bills
- Updates to purchase-line relationships
- Potential deletion of unmatched selected bill lines
- An action that opens the `bill.to.po.wizard`

These findings are important because matching operations can modify existing financial records. Any future integration must distinguish read-only investigation from authorized corrective actions.

## 3. Research Methodology

My investigation follows a reproducible process:

1. Identify the relevant Odoo model or business workflow.
2. Retrieve the source from a pinned Odoo revision.
3. Extract field definitions and relationships programmatically.
4. Inspect the methods responsible for business behavior.
5. Trace dependencies across related addons.
6. Separate verified findings from unresolved questions.
7. Preserve research tooling and selected results in Git.

The objective is to understand existing behavior before implementing new functionality.

## 4. Repository Contents

```text
odoo-19-database-research/
├── README.md
├── LICENSE
├── scripts/
│   └── extract_odoo_models.py
└── models/
    └── odoo19_field_inventory.csv
```

The repository contains original research tooling and an extracted model inventory. The analysis references the official Odoo 19 source code.

## 5. Current Limitations

This is an ongoing investigation, not a completed Odoo application or full database audit.

At the present stage:

- Static source-code relationships have been investigated.
- The complete installed Odoo database schema has not been verified.
- Runtime behavior still requires testing in an isolated Odoo environment.
- Database constraints, access rights, record rules, and multi-company protections require further investigation.
- The proposed ProofFlow application has not yet completed implementation or deployment.

These limitations are documented deliberately to keep the research reproducible and technically accurate.

## 6. What Comes Next

The next research and development stages will focus on:

- Completing the investigation of Odoo's bill-to-purchase-order wizard
- Studying PostgreSQL constraints and ORM inheritance
- Examining accounting permissions and multi-company security
- Testing invoice, receipt, return, and pricing edge cases
- Building an isolated Odoo 19 development environment
- Designing and implementing ProofFlow's accounting-exception workflow
- Validating the application through automated tests before deployment

### ProofFlow — Planned Application

The longer-term objective is to develop **ProofFlow**, an accounting workflow solution focused on investigating and resolving exceptions between purchasing, inventory, and vendor billing records.

The intended workflow includes discrepancy detection, supporting evidence, review and approval, authorized corrections, and verification of resolution outcomes.

ProofFlow is currently a development objective informed by this research—not a completed integration demonstrated by this repository.

## 7. Motivation and Professional Development

I am sharing this project as evidence of how I approach software engineering: through independent learning, source-code investigation, structured experimentation, and progressively verified implementation.

My interest in Odoo extends beyond using its applications. I want to understand how its internal systems operate, why particular business rules exist, and how to develop reliable extensions that respect those rules.

Following my application for an Odoo Software Developer position, I recognized the importance of presenting concrete, independently inspectable evidence of my technical abilities.

This repository is part of that effort.

I respect the recruitment decision, while remaining committed to improving my engineering skills and demonstrating them through practical work.

My goal is to continue developing this research into a carefully tested, useful application and to remain open to future opportunities where these skills may contribute value.

---

## 8. Source and Attribution

Official Odoo source code: https://github.com/odoo/odoo

Research baseline: `7c45959e02b2d8abc52913184237b72f7bae93a2`

Odoo and its source code remain the intellectual property of their respective owners and contributors. This project is an independent investigation and is not affiliated with or endorsed by Odoo S.A.

**Author:** David Samah  
**Project:** Odoo 19 Database & Architecture Research  
**Status:** Research ongoing
