# AI Integration Systems — Strict Research Charter

**Branch:** `research/enterprise-ai-opportunities-2026`  
**Baseline:** `main` at `810f54f3f5a6d2546acc0b95e1e92fa3c56a730b`  
**Started:** 2026-11-06  
**Status:** Stage 0 scope revised — generalizable AI-integration research; no invention or application approved.


## 1. Objective and boundary

**Primary research aim:** Discover, rigorously characterize, and experimentally validate a **potentially original technical mechanism that makes actual AI integration substantially easier** for engineers working with complex, stateful software systems. The intended intellectual depth is that of a publishable computer-science or software-engineering contribution capable of sustaining serious review by advanced AI researchers and engineers (including researchers at institutions such as Harvard). This is an **ambition, not a claim of novelty, institutional interest, endorsement, or future commercial success**.

**"Actual AI integration" includes:** Model execution and lifecycle—model choice or training, inference, data interfaces, access controls, evaluation, observability, updates, debugging, and reproducibility. We are **not** limiting this effort to an external AI API, prompt wrapper, or chatbot feature. Local/self-hosted models are an important target; alternatives must still be compared fairly.

**"Easier" means measurable improvement:** Less time to integrate a model correctly, less bespoke glue code, lower debugging and upgrade effort, simpler deployment and model substitution, **without unacceptable losses** in security, correctness, latency, cost, or auditability. Establish baselines and conditions for failure before making improvement claims.

**Relation to existing Odoo research:** Odoo 19—its modular addons, registry/ORM, PostgreSQL transactions, permissions, and accounting workflows—is our **primary engineering testbed**. A strong research contribution might generalize to other business applications, but applicability beyond Odoo must be demonstrated, not presumed.

**Secondary aim:** Investigate whether a validated mechanism can underpin ProofFlow, a native Odoo addon, or a broader developer platform. Enterprise revenue potential is a later test, not a substitute for technical novelty.

**Boundary:** This is a public research branch, not an implementation or deployment branch. Nothing here authorizes changing `main`, production records, Odoo's original source, or the preserved source archive. No feature design is approved in advance; global originality and Harvard researchers' interest are not claims we can currently verify.

## 2. User authority and pacing

- Research is collaborative and sequential. Work on **one numbered checkpoint at a time**.
- Ask only for essential missing data; use established evidence before requesting repetitions.
- Present evidence and uncertainty before recommending a design. No feature is approved merely because it appears here as a hypothesis.
- No code implementation, addon installation, database mutation, merge, deployment, external outreach, expense, or live financial action without an explicit next decision by the researcher.
- Keep all historical source observations and timestamps intact. Distinguish prior records from new research.
- Keep private business data, credentials, database dumps, unreleased models, sensitive transcripts and customer data out of this **public** Git repository.


## 3. Research stages (strict order)

| Stage | Research question | Required evidence/output | Exit criterion |
|---|---|---|---|
| 0. Scope and governance | What constitutes new AI-integration technology and credible research? | Updated charter and branch provenance | Researcher approves revised scope |
| 1. Integration friction | Which engineering tasks make integrating real AI models into complex systems difficult? | Independent primary evidence, developer workflows, failure mechanisms and quantitative friction hypotheses | At least three distinct, grounded integration bottlenecks |
| 2. Existing approaches | What do inference runtimes, ML frameworks, agent stacks, model-serving tools, ERP integrations and observability systems already solve? | Dated capability matrix with source citations and verified-vs-marketed distinctions | Existing solutions mapped without omission |
| 3. Scientific prior art | What similar mechanisms exist in papers, standards, patents and open-source implementations? | Reproducible search log, overlaps and limitations | No unqualified "world first" claims |
| 4. Candidate technical mechanism | Could a new abstraction or algorithm remove a documented bottleneck? | Multiple hypotheses, falsifiable predictions, interface sketch, correctness and safety invariants | Researcher selects one hypothesis |
| 5. Technical feasibility | Can we safely test it with Odoo's ORM, permissions and local AI execution? | Dependency map, threat model, system constraints, test plan | All critical assumptions and access boundaries identified |
| 6. Comparative experiments | Does it outperform credible existing integration methods? | Reproducible baselines, measured developer effort, performance, correctness, failure cases and ablations | Transparent acceptance or rejection of hypothesis |
| 7. Research decision | Is it technically distinct, useful, reproducible, and worth building or publishing? | Evidence-weighted technical report and market implications | Researcher decides to iterate, develop, publish or reject |

One numbered checkpoint at a time. Never advance merely because an idea sounds exciting.

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

1. **Engineering friction:** Specify the integration task, affected developers, and measurable difficulty.
2. **Existing solutions:** Compare to current model-serving, training, orchestration and application-integration systems.
3. **Technical distinctiveness:** Describe the exact mechanism, prior-art overlaps and uncertain novelty.
4. **Actual AI functionality:** Address the model lifecycle, not merely a hosted API call.
5. **State and correctness:** Respect ORM invariants, transaction boundaries and deterministic accounting rules.
6. **Safety and privacy:** Permissions, company isolation, secrets, data boundaries, privileged tools and attack surfaces.
7. **Developer experience:** Time-to-correct-inference, lines of glue code, setup steps, fault diagnosis and upgrade friction.
8. **Model reliability:** Evaluation design, calibration, reproducibility, false positives, regressions, drift.
9. **Systems feasibility:** Latency, throughput, CPU/GPU/RAM usage, deployment and maintenance burden.
10. **Generality:** Test a second independent host application rather than assume transferability from Odoo.
11. **Research rigor:** Control/baseline, falsifiable hypothesis, reproducible procedure, failure cases and limitations.
12. **Commercial impact (secondary):** Independently assess actual enterprise adoption barriers and willingness to pay.


## 6. Initial research questions — not conclusions

1. Why is running a model generally easier than integrating its behavior **correctly** with transactional business software?
2. What bespoke integration "glue" repeats across applications: data types, permission boundaries, contextual state, verification and schema changes?
3. Could a reusable mechanism derive safe constraints from an application's model metadata, workflows and invariants?
4. How could local inference, model updates and continuous evaluation be integrated without compromising auditable business state?
5. Which existing frameworks, papers, patent claims and repositories already approach these questions?
6. Which integration tasks can be quantified in Odoo 19 and replicated against a second independent system?
7. What empirical outcome would falsify the claim of significantly easier AI integration?

## 7. Reuse of existing findings

The `main` branch contains the archived Odoo 19 framework map, purchase-to-receipt research, nine accounting-domain indexes, privacy boundaries and ProofFlow business logic. Treat these as the **current foundation**, with each claim retaining its original evidence classification. The separate 60,706-file source-and-schema reconstruction remains private and is not copied into this public branch.

## 8. Current log

| Checkpoint | Observation | Status |
|---|---|---|
| 0.1 | Created branch at `main` SHA `810f54f3f5a6d2546acc0b95e1e92fa3c56a730b` | GitHub creation verified |
| 0.2 | Original scope: enterprise accounting AI opportunity, research-first | Historically recorded; superseded |
| 0.3 | User revised aim: generate a genuinely new and scientifically interesting mechanism that makes real AI integration easier | Scope revision recorded; no research hypothesis selected |
| 1.1 | Identify and document a measurable AI-integration bottleneck, with current tools and credible independent evidence | NOT STARTED |

**Next checkpoint:** Stage 1.1, integration-friction discovery. Start with one concrete engineering bottleneck and compare what existing systems do. No candidate technology is presumed, and this document does not authorize implementation.
