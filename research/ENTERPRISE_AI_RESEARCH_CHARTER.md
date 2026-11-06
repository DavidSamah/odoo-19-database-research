# Enterprise Accounting Intelligence — Strict Research Charter

**Branch:** `research/enterprise-ai-opportunities-2026`  
**Baseline:** `main` at `810f54f3f5a6d2546acc0b95e1e92fa3c56a730b`  
**Started:** 2026-11-06  
**Status:** Stage 0 — branch and method established; no product concept approved.

## 1. Objective and boundary

Identify, test, and prioritize an enterprise-grade opportunity for **native Odoo accounting intelligence**, informed by the verified ProofFlow/Odoo 19 architectural research. The eventual aspiration is meaningful global commercial value, but **market size, novelty, feasibility, sales traction, and company value are currently unverified**. Do not claim that nobody has attempted a feature until there is supporting evidence; even a thorough search cannot prove global firstness.

This is a **research branch**, not an implementation branch. Do not alter `main`, production accounting records, the preserved research database, Odoo's original source code, or the separately retained integrity-verified source archive.

## 2. User authority and pacing

- Research is collaborative and sequential. Work on **one numbered checkpoint at a time**.
- Ask only for essential missing data; use established evidence before requesting repetitions.
- Present evidence and uncertainty before recommending a design. No feature is approved merely because it appears here as a hypothesis.
- No code implementation, addon installation, database mutation, merge, deployment, external outreach, expense, or live financial action without an explicit next decision by the researcher.
- Keep all historical source observations and timestamps intact. Distinguish prior records from new research.
- Keep private business data, credentials, database dumps, unreleased models, sensitive transcripts and customer data out of this **public** Git repository.

## 3. Research stages (strict order)

| Stage | Question | Required evidence/output | Exit criterion |
|---|---|---|---|
| 0. Governance and scope | What are we studying and under what constraints? | This charter; branch provenance | Researcher agrees to scope |
| 1. Enterprise pain | Which accounting-control failures are costly, frequent and unsolved? | Problem register with independent evidence, affected roles, current workarounds and measurable consequences | At least three concrete problems verified; no unsupported global statistics |
| 2. Existing products | What do Odoo, SAP, Oracle and specialists already offer? | Dated competitor/capability matrix with primary citations and implementation caveats | Distinguish documented functionality from untested marketing |
| 3. Research and prior art | Have similar approaches appeared in papers, code, patents or product descriptions? | Search query log, source/date inventory, feature-by-feature comparison, novelty uncertainty | Avoid absolute novelty claims |
| 4. Technical feasibility | Can we build a safe Odoo-native addon and local model? | Exact model/method interfaces, permissions, dataset needs, resource requirements, integration and legal risks | Main dependencies and critical unknowns traced |
| 5. Economic test | Would a large enterprise buy and safely operate it? | Buyer, adoption blockers, competitive substitutes, bounded ROI scenarios and assumptions | Numbers are sourced or explicitly hypothetical |
| 6. Experiment design | What is the smallest falsifiable test? | Synthetic cases, baselines, acceptance criteria, false-positive costs, verification design | Researcher approves test design |
| 7. Decision | What should we build, postpone or reject? | Evidence-weighted decision memorandum, unresolved contradictions and next action | No development until explicitly approved |

Do not advance stages solely because a search returned useful-looking results. Record the outcome and approval at each stage.

## 4. Mandatory observation record

For each observation use this exact structure:

- **ID / date (UTC) / stage / research question**
- **Hypothesis** (if any; never a finding)
- **Why this method** and source selection rationale
- **Exact query, command, URL or source path**
- **Observed excerpt or terminal output** (faithful, dated, appropriately shortened)
- **Interpretation and business relevance**
- **Contradictions / negative results**
- **Limitations, source reliability and potential bias**
- **Classification:** VERIFIED SOURCE / DOCUMENTED CLAIM / DIRECT EXPERIMENT / INFERENCE / UNVERIFIED / CONTRADICTED
- **Decision and next single action**
- **Publication review:** public-safe or private evidence

## 5. Non-negotiable evaluation criteria

1. **Actual enterprise loss or friction:** measurable cost, delay, control failure or audit exposure.
2. **Existing alternative:** can Odoo or an incumbent already solve this adequately?
3. **Differentiation:** exact mechanism and evidence, not just the term "AI".
4. **Correctness:** accounting calculations remain rule-based and auditable.
5. **Safety and governance:** identity, company isolation, fiscal locks, human authority, transaction integrity and data residency.
6. **Model validity:** dataset provenance, reproducibility, calibration, false positives, false negatives and concept drift.
7. **Economic feasibility:** compute/storage expense, deployment complexity, sales cycles and customer maintenance.
8. **Verifiable outcomes:** what would count as a failed hypothesis?
9. **Defensibility:** proprietary data advantage, switching cost, network effects, integration depth or other evidenced advantage; not assumed.
10. **Scope discipline:** start with one well-defined use case, without inventing platform-wide success.

## 6. Initial research questions — not conclusions

1. Which enterprise accounting decisions remain expensive to **verify** even after automation?
2. Where do audit evidence, approvals, source transactions and financial consequences become disconnected?
3. What could a local inference model identify that deterministic Odoo checks cannot?
4. Could a model produce advice while a separate deterministic engine proves the proposed outcome?
5. What comparable capabilities already exist in products, research, or patents?
6. Why would a CFO, controller, AP manager or internal auditor purchase this instead of extending existing software?

## 7. Reuse of existing findings

The `main` branch contains the archived Odoo 19 framework map, purchase-to-receipt research, nine accounting-domain indexes, privacy boundaries and ProofFlow business logic. Treat these as the **current foundation**, with each claim retaining its original evidence classification. The separate 60,706-file source-and-schema reconstruction remains private and is not copied into this public branch.

## 8. Current log

| Checkpoint | Observation | Status |
|---|---|---|
| 0.1 | Created branch from observed current `main` SHA `810f54f3f5a6d2546acc0b95e1e92fa3c56a730b` | Verified by GitHub branch creation |
| 0.2 | Defined research stages, evidence rules, privacy and user approval boundaries | Recorded in this charter |
| 1.1 | Identify and source the first enterprise accounting pain point | NOT STARTED |

**Next checkpoint:** Stage 1.1, one enterprise pain-point hypothesis and its independently retrieved evidence. This document authorizes research only—not implementation.
