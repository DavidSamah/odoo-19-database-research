# Odoo 19 research observations — in the exact order of the Git patch

**Source:** `evidence/00_git_patch/commit_changes.patch` (original uploaded bytes). There are **32** commit records in the supplied patch.

This is the order recorded by `git log --all --reverse`; it is not a guarantee of a single linear development branch. Merge commits may contain no file patch. For exact added/deleted lines, open each commit's `COMMIT_PATCH.txt`. The documented Phase 1 source review and later nine accounting domains are **separate numbered sequences**.

## Original patch sequence

1. **`27bd54373` — docs: initialize Odoo research audit** (Thu Oct 29 23:48:24 2026 +0300). [Commit record](research/01_commit_order/01_27bd54373/README.md) · [Exact patch](research/01_commit_order/01_27bd54373/COMMIT_PATCH.txt)
2. **`ec7d1267e` — research: checkpoint Odoo 19 model investigation through DB-031** (Fri Oct 30 11:48:18 2026 +0300). [Commit record](research/01_commit_order/02_ec7d1267e/README.md) · [Exact patch](research/01_commit_order/02_ec7d1267e/COMMIT_PATCH.txt)
3. **`67d7b17ef` — research: preserve Odoo 19 source and matching analysis through DB-036** (Fri Oct 30 15:44:49 2026 +0300). [Commit record](research/01_commit_order/03_67d7b17ef/README.md) · [Exact patch](research/01_commit_order/03_67d7b17ef/COMMIT_PATCH.txt)
4. **`7bfd7e424` — Initial commit** (Fri Oct 30 15:54:21 2026 +0300). [Commit record](research/01_commit_order/04_7bfd7e424/README.md) · [Exact patch](research/01_commit_order/04_7bfd7e424/COMMIT_PATCH.txt)
5. **`e3aa7e1d3` — Merge GitHub repository initialization** (Fri Oct 30 15:58:09 2026 +0300). [Commit record](research/01_commit_order/05_e3aa7e1d3/README.md) · [Exact patch](research/01_commit_order/05_e3aa7e1d3/COMMIT_PATCH.txt)
6. **`47b0499e2` — Revise README for clarity and project updates** (Fri Oct 30 16:00:45 2026 +0300). [Commit record](research/01_commit_order/06_47b0499e2/README.md) · [Exact patch](research/01_commit_order/06_47b0499e2/COMMIT_PATCH.txt)  
   Recorded headings: 1. About This Project; 2. Research Completed So Far; 3. Research Methodology; 4. Repository Contents; 5. Current Limitations; 6. What Comes Next; 7. Motivation and Professional Development; 8. Source and Attribution
7. **`b31110964` — research: map Odoo 19 purchase and accounting security rules** (Sat Oct 31 12:16:33 2026 +0300). [Commit record](research/01_commit_order/07_b31110964/README.md) · [Exact patch](research/01_commit_order/07_b31110964/COMMIT_PATCH.txt)
8. **`3f2c1431e` — Merge remote-tracking branch 'origin/main'** (Mon Nov 2 03:23:09 2026 +0300). [Commit record](research/01_commit_order/08_3f2c1431e/README.md) · [Exact patch](research/01_commit_order/08_3f2c1431e/COMMIT_PATCH.txt)
9. **`238cb1a02` — docs: preserve Odoo 19 purchase and stock lifecycle research notebook** (Mon Nov 2 22:42:29 2026 +0300). [Commit record](research/01_commit_order/09_238cb1a02/README.md) · [Exact patch](research/01_commit_order/09_238cb1a02/COMMIT_PATCH.txt)  
   Recorded headings: Research tracker; Evidence received — task 1.1; Next command — trace tax-base preparation; Prior verified checkpoints (summarized from conversation); Recording convention for further steps; Phase 1 — Dependency-location checkpoint (2026-11-02); Phase 1 — Invoice tax-base preparation inspected (2026-11-02); Phase 1 — Shared account.tax preparation method located (2026-11-02) (+23 more)
10. **`a8ecda28b` — docs: record stock procurement dispatcher location** (Mon Nov 2 23:03:14 2026 +0300). [Commit record](research/01_commit_order/10_a8ecda28b/README.md) · [Exact patch](research/01_commit_order/10_a8ecda28b/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.15 procurement dispatcher location (2026-11-02)
11. **`4967ae43f` — docs: record procurement dispatch and stock rule selection** (Mon Nov 2 23:08:45 2026 +0300). [Commit record](research/01_commit_order/11_4967ae43f/README.md) · [Exact patch](research/01_commit_order/11_4967ae43f/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.16 procurement dispatch and rule selection (2026-11-02)
12. **`d4ee581d3` — docs: save complete Odoo purchase receipt workflow** (Mon Nov 2 23:11:29 2026 +0300). [Commit record](research/01_commit_order/12_d4ee581d3/README.md) · [Exact patch](research/01_commit_order/12_d4ee581d3/COMMIT_PATCH.txt)  
   Recorded headings: Evidence boundary; Workflow map; 1. Purchase order confirmation; 2. Approval decision; 3. Receipt preparation and reuse; 4. Purchase-line stock-move preparation; 5. Stock-move confirmation; 6. Procurement dispatch (+6 more)
13. **`b197403f6` — docs: record stock rule precedence and intercompany routing** (Mon Nov 2 23:21:06 2026 +0300). [Commit record](research/01_commit_order/13_b197403f6/README.md) · [Exact patch](research/01_commit_order/13_b197403f6/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.18 rule precedence, hierarchy fallback, and inter-company routing (2026-11-02)
14. **`b23c88052` — docs: add stock rule hierarchy and intercompany routing** (Mon Nov 2 23:21:08 2026 +0300). [Commit record](research/01_commit_order/14_b23c88052/README.md) · [Exact patch](research/01_commit_order/14_b23c88052/COMMIT_PATCH.txt)  
   Recorded headings: Procurement rule resolution and inter-company routing
15. **`d181be8a4` — docs: record scheduler and push-rule behavior** (Mon Nov 2 23:23:15 2026 +0300). [Commit record](research/01_commit_order/15_d181be8a4/README.md) · [Exact patch](research/01_commit_order/15_d181be8a4/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.19 rule-domain restrictions, push fallback, and scheduler (2026-11-02)
16. **`07ca37b55` — docs: add push fallback and scheduler behavior** (Mon Nov 2 23:23:17 2026 +0300). [Commit record](research/01_commit_order/16_07ca37b55/README.md) · [Exact patch](research/01_commit_order/16_07ca37b55/COMMIT_PATCH.txt)  
   Recorded headings: Push fallback and scheduler behavior
17. **`0d7a8822e` — docs: locate stock rule pull action** (Mon Nov 2 23:25:10 2026 +0300). [Commit record](research/01_commit_order/17_0d7a8822e/README.md) · [Exact patch](research/01_commit_order/17_0d7a8822e/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.20 pull-action method location (2026-11-02)
18. **`f44784e4b` — docs: locate pull action implementation** (Mon Nov 2 23:25:12 2026 +0300). [Commit record](research/01_commit_order/18_f44784e4b/README.md) · [Exact patch](research/01_commit_order/18_f44784e4b/COMMIT_PATCH.txt)  
   Recorded headings: Pull-action implementation
19. **`106fa3f70` — docs: record pull action and move construction** (Mon Nov 2 23:28:10 2026 +0300). [Commit record](research/01_commit_order/19_106fa3f70/README.md) · [Exact patch](research/01_commit_order/19_106fa3f70/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.21 pull action and procurement-to-move construction (2026-11-02)
20. **`81bba6fb9` — docs: add pull action and move construction** (Mon Nov 2 23:28:20 2026 +0300). [Commit record](research/01_commit_order/20_81bba6fb9/README.md) · [Exact patch](research/01_commit_order/20_81bba6fb9/COMMIT_PATCH.txt)  
   Recorded headings: Pull action and move construction
21. **`df6e7d693` — docs: record procurement serialization and lead times** (Mon Nov 2 23:33:43 2026 +0300). [Commit record](research/01_commit_order/21_df6e7d693/README.md) · [Exact patch](research/01_commit_order/21_df6e7d693/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.22 procurement serialization and lead-time calculation (2026-11-02)
22. **`56a893303` — docs: add procurement serialization and lead time** (Mon Nov 2 23:33:45 2026 +0300). [Commit record](research/01_commit_order/22_56a893303/README.md) · [Exact patch](research/01_commit_order/22_56a893303/COMMIT_PATCH.txt)  
   Recorded headings: Procurement serialization and lead time
23. **`c33692246` — docs: record unavailable procurement caller search** (Mon Nov 2 23:35:49 2026 +0300). [Commit record](research/01_commit_order/23_c33692246/README.md) · [Exact patch](research/01_commit_order/23_c33692246/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.23 caller search unavailable in current shell (2026-11-02)
24. **`9fab505a4` — docs: record caller search environment limitation** (Mon Nov 2 23:36:03 2026 +0300). [Commit record](research/01_commit_order/24_9fab505a4/README.md) · [Exact patch](research/01_commit_order/24_9fab505a4/COMMIT_PATCH.txt)  
   Recorded headings: Caller search environment note
25. **`502456b79` — docs: record lead time caller locations** (Mon Nov 2 23:39:12 2026 +0300). [Commit record](research/01_commit_order/25_502456b79/README.md) · [Exact patch](research/01_commit_order/25_502456b79/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.24 serialization and lead-time caller locations (2026-11-02)
26. **`a75b17666` — docs: summarize lead time caller evidence** (Mon Nov 2 23:39:22 2026 +0300). [Commit record](research/01_commit_order/26_a75b17666/README.md) · [Exact patch](research/01_commit_order/26_a75b17666/COMMIT_PATCH.txt)  
   Recorded headings: Lead-time caller evidence
27. **`2b631a01a` — docs: record blocked lead time consumer inspection** (Tue Nov 3 09:19:54 2026 +0300). [Commit record](research/01_commit_order/27_2b631a01a/README.md) · [Exact patch](research/01_commit_order/27_2b631a01a/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.25 surrounding lead-time callers unavailable in current shell (2026-11-03)
28. **`6b5f6908e` — docs: note blocked lead time consumer inspection** (Tue Nov 3 09:20:14 2026 +0300). [Commit record](research/01_commit_order/28_6b5f6908e/README.md) · [Exact patch](research/01_commit_order/28_6b5f6908e/COMMIT_PATCH.txt)  
   Recorded headings: Lead-time consumer inspection status
29. **`2c5f2cee3` — docs: record lead time consumer calculations** (Tue Nov 3 09:30:07 2026 +0300). [Commit record](research/01_commit_order/29_2c5f2cee3/README.md) · [Exact patch](research/01_commit_order/29_2c5f2cee3/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.26 lead-time consumption, rule recursion, and orderpoint dates (2026-11-03)
30. **`634e3e274` — docs: summarize lead time calculations** (Tue Nov 3 09:30:23 2026 +0300). [Commit record](research/01_commit_order/30_634e3e274/README.md) · [Exact patch](research/01_commit_order/30_634e3e274/COMMIT_PATCH.txt)  
   Recorded headings: Lead-time calculation evidence
31. **`05af84360` — docs: record unavailable purchase delay search** (Tue Nov 3 09:33:08 2026 +0300). [Commit record](research/01_commit_order/31_05af84360/README.md) · [Exact patch](research/01_commit_order/31_05af84360/COMMIT_PATCH.txt)  
   Recorded headings: Phase 2 — Step 2.27 purchase_delay provenance search unavailable locally (2026-11-03)
32. **`bec0a543c` — docs: note purchase delay provenance status** (Tue Nov 3 09:33:20 2026 +0300). [Commit record](research/01_commit_order/32_bec0a543c/README.md) · [Exact patch](research/01_commit_order/32_bec0a543c/COMMIT_PATCH.txt)  
   Recorded headings: Purchase delay provenance status

## Subsequent terminal and nine-domain evidence

These sources are intentionally **not interleaved as if they were commits**:

- **October 29–November 3:** Git patch and the recovered [Phase 1 notebook](research/02_phase1_and_workflow/ProofFlow_Odoo19_Temporary_Research_Notebook_FROM_PATCH.md).
- **November 4:** [Original raw terminal transcripts](research/03_original_terminal_transcripts/), preserved individually.
- **Nine-domain checkpoint sequence:** [Domain index](research/04_nine_domain_checkpoints/), which differs from the earlier Phase 1 tax/price source-review numbering.
- **November 5:** [New recovery observations](research/05_new_recovery_2026_11_05/NEW_OBSERVATIONS_20261105_114030.txt), including Domain 9 Commands 6–10. These are newly executed inspections, not historical outputs from October.

**Interpretation constraint:** Commit messages and file additions prove documentation existed at commit time; they do not independently prove that a documented command executed. A raw transcript proves an observed output; it does not prove runtime correctness of the broader accounting behavior.