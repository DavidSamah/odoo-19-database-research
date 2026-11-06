> Historical research checkpoint (2026-11-04). These findings summarize the originally preserved evidence, not newly executed runtime tests. Referenced raw terminal outputs remain in the private evidence archive.

# ProofFlow — Odoo 19 Accounting Research
## Domain 2: General Ledger and Account Balances — Evidence Checkpoint
Date: 2026-11-04
**Research execution: prescribed Commands 1–10 complete (user-reported, with available output evidence).**
**Runtime ledger behavior: NOT VERIFIED.**

### Evidence archive
- `Domain2_Chart_of_Accounts_Observed_Output_01.txt` — chart of accounts source field and constraints inspection.
- `Domain2_Commands_4_to_5_Observed_Output.txt` — journal–move–line relationships, signed amounts, currency and running-balance sources.
- `Domain2_Commands_6_to_8_Observed_Output.txt` — residual and cumulative calculations, reporting module discovery and seven existing accounting-related database tables.
- `Domain2_Commands_9_to_10_Observed_Output.txt` — posted ledger aggregate, record counts and final clean working-tree status.

### Observed source findings
1. `account.account` defines `account_type`, account code, name, currency, reconciliation flag, company association, and opening/current balance-related fields. Receivable/payable accounts require reconciliation. Off-balance accounts cannot be reconcilable or have taxes (per inspected constraints).
2. Account code depends on company mapping (`code_store` company-dependent; `company_ids` many-to-many); account identity and access cannot be assumed globally uniform across companies.
3. `account.journal` contains journal name/code/type, `default_account_id`, `company_id`, and hash restriction configuration. `account.move` links a journal, company, date/state and lines; `account.move.line` links the parent move, account, company and journal.
4. Signed journal-line `balance` is distinguished from `debit`, `credit` and `amount_currency`. The currency-rate logic uses invoice rate or dated conversion with special branches; inspect exact relevant branch before reuse.
5. `_compute_cumulated_balance()` uses the requested domain and order context, with a SQL window `SUM(balance) OVER (...)`; without the ordering context the computed value is zero. A cumulative value is therefore context-dependent, not a universal persisted period closing balance.
6. `_compute_amount_residual()` calculates residual company- and foreign-currency amounts from partial-reconciliation sums. For non-reconcilable accounts it sets residual amounts to zero, which does **not** mean their booked ledger balance is zero.
7. Discovery located installed `account.report` model and reporting artifacts. This is *not* exhaustive general-ledger report analysis; Domain 8 investigates reporting.
8. Read-only schema discovery returned: `account_account`, `account_journal`, `account_move`, `account_move_line`, `account_partial_reconcile`, `res_company`, `res_currency`.

### Database observations
- Command 9 posted-ledger aggregation: **0 rows**.
- Command 10 `account_move`: **0** records; `account_move_line`: **0** records; per-account grouping: **0 rows**.
- Read-only transactions ended with `ROLLBACK`.
- `git status --short` printed no changes; `DOMAIN 2 COMMANDS FINISHED` printed.

### Interpretation and limitations
- Source-level model and calculation paths have been mapped for the assigned research sequence, with dependencies suitable for later domains.
- The empty accounting tables do not demonstrate runtime ledger correctness, currency calculations, account opening balances, reporting, reconciliations or company isolation.
- The supplied preserved Command 8 output shows the seven-table listing, but **does not include the second schema-column query's output**. Do not falsely mark that particular evidence as observed.
- The full implementation of `account.account` opening/current balance methods and general-ledger reporting has not been traced to completion by these excerpts. Retain as separate source follow-up, not a retroactive obligation to repeat the ten commands.
- No independent test fixture or posting transactions have been run in these recorded outputs. Do not create transactions in the protected research database.

### Decision
**Domain 2 assigned ten-command research sequence completed and checkpoint closed with explicit evidence gaps.** The runtime-verification backlog remains separate. No repeats of completed commands are required.

### Next
Domain 3 — Accounts Payable and Receivable. Reuse findings on account types, posted lines, residual amounts, company/currency mapping. Preserve unverified method and schema details in a cross-domain backlog.