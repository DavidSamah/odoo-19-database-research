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

Our research first reconstructs the **evolution of AI over time**, because each breakthrough changed not only what a model could do but what engineers had to build around it. We will compare contemporaneous problems, methods, resources, software integration interfaces, adoption constraints, failures, and the next technology that responded. Later stages identify persistent friction and attempt original contributions. No technological progress is assumed to be linear or inevitable.

| Stage | Research question | Required evidence/output | Exit criterion |
|---|---|---|---|
| 0. Scope and governance | What counts as trustworthy, time-aware AI history and a serious innovation claim? | Revised charter; historical-study protocol and source register | Scope recorded; researcher sets next checkpoint |
| 1. Historical evolution of AI | How did AI's theory, architectures, compute, data, interfaces and integration approaches change from foundations through 2026? | Chronological primary-source register, dated milestone analyses, causes and limits, parallel traditions, contested narratives | Chronology and mechanisms corroborated; separate observations vs historical inferences |
| 2. Persistent integration friction | Which hard integration problems persisted, disappeared or emerged through successive AI eras? | Cross-era bottleneck matrix, developer tasks, failure mechanisms, measurable baseline hypotheses | At least three independently grounded integration bottlenecks |
| 3. Existing approaches | What do inference runtimes, ML frameworks, agent stacks, model serving, ERP integrations and observability already solve? | Dated capability matrix and primary citations | Existing techniques accounted for |
| 4. Scientific and technical prior art | Which analogous techniques appear in papers, patents, standards and open-source systems? | Reproducible search logs, similarities, exclusions, uncertainty | No unsupported world-first claims |
| 5. Candidate technical mechanism | Can a new abstraction, algorithm or architecture remove a historical or present bottleneck? | Multiple falsifiable hypotheses, invariants, technical design alternatives | Researcher selects an experiment |
| 6. Odoo and broader feasibility | Can the idea work with Odoo 19's ORM, permissions, local model execution and an independent second host? | Dependency map, threat model, test requirements, generality limits | Critical unknowns exposed |
| 7. Comparative experiments | Does it materially outperform rigorous baselines? | Replicable tests of developer time, complexity, correctness, security and performance | Evidence supports, limits or rejects hypothesis |
| 8. Research decision | Is it distinctive, reproducible and worth pursuing academically or commercially? | Evidence-weighted paper-style report, risks and opportunities | Researcher decides iterate / develop / publish / reject |

**Chronological evidence rule:** Record the date of invention, preprint, peer-reviewed publication, first deployment and broad adoption *separately*, wherever known. Avoid attributing a development to a single person or date without reviewing earlier work. Measure trends at several time scales and watch for cyclical or parallel developments (e.g., symbolic, statistical, neural and hybrid AI).

One numbered checkpoint at a time. Do not move from an historical milestone to a new invention merely because an idea seems exciting.

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

1. Historically, what did AI systems require from host software, domain experts, data and computing hardware at each major transition?
2. Which assumptions and limitations of earlier generations of AI reappeared with new techniques?
3. Why is running a model generally easier than integrating its behavior **correctly** with transactional business software?
2. What bespoke integration "glue" repeats across applications: data types, permission boundaries, contextual state, verification and schema changes?
3. Could a reusable mechanism derive safe constraints from an application's model metadata, workflows and invariants?
4. How could local inference, model updates and continuous evaluation be integrated without compromising auditable business state?
5. Which existing frameworks, papers, patent claims and repositories already approach these questions?
6. Which integration tasks can be quantified in Odoo 19 and replicated against a second independent system?
7. What empirical outcome would falsify the claim of significantly easier AI integration?

## 7. Reuse of existing findings

The `main` branch contains the archived Odoo 19 framework map, purchase-to-receipt research, nine accounting-domain indexes, privacy boundaries and ProofFlow business logic. Treat these as the **current foundation**, with each claim retaining its original evidence classification. The separate 60,706-file source-and-schema reconstruction remains private and is not copied into this public branch.

## 9. Current log

| Checkpoint | Observation | Status |
|---|---|---|
| 0.1 | Created branch at `main` SHA `810f54f3f5a6d2546acc0b95e1e92fa3c56a730b` | Verified |
| 0.2 | Scope first established for enterprise accounting AI | Historic record; subsequently revised |
| 0.3 | Scope revised to investigate original methods for easier, actual AI integration | Recorded |
| 0.4 | User added deep, chronological research on AI's evolution as a **foundational prerequisite** | Recorded and charter updated |
| 1.0 | Chronological research protocol and initial dated source register | Source selection complete; not a full literature review |
| 1.1 | Historical foundations and causal turning points, beginning with early formal and symbolic AI | NOT STARTED IN DEPTH |

**Next checkpoint:** Stage 1.1, investigate AI's early foundations using original primary sources, including contemporaneous technical constraints and integration consequences. No invention or product implementation is approved.
