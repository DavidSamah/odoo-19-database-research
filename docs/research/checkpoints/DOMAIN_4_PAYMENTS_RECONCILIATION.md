> Historical research checkpoint (2026-11-04). These findings summarize the originally preserved evidence, not newly executed runtime tests. Referenced raw terminal outputs remain in the private evidence archive.

# ProofFlow — Odoo 19 Accounting Research, Domain 4
Date: 2026-11-04
Scope: Payments and reconciliation
Status: Prescribed research command sequence completed; runtime tests outstanding.

## Preserved evidence
- `Domain4_Commands_2_to_3_Observed_Output.txt`: payment fields, links and payment-state/action methods.
- `Domain4_Commands_4_to_5_Observed_Output.txt`: payment registration wizard, partial and full reconciliation model locations.
- `Domain4_Command_6_Observed_Output.txt`: reconciliation plan, partial/full creation, exchange difference and unreconciliation source excerpts.
- `Domain4_Command_7_Observed_Output.txt`: payment matching, bank statement references, exchange difference, unreconciliation.
- `Domain4_Commands_8_to_10_Observed_Output.txt`: PostgreSQL schema inspection, zero-row diagnostic counts, clean Git status and source revision reference.
- Command 1 environment verification output is not present in the saved batches; do not claim independently verified from a preserved Command 1 file.

## Source findings (source inspection only)
1. `account.payment._compute_state()` around line 455 considers payment move liquidity-line residuals and paid invoice/bill state. `account.payment._compute_reconciliation_status()` around line 474 computes `is_reconciled` and `is_matched` using outstanding-account, currency, residual and journal-account conditions. Different flags have different meanings.
2. `account.payment.action_post` around line 1130 checks outbound bank account trust in applicable cases and sets state; `action_validate`, `action_cancel`, `action_draft` exist. Cancellation may cancel associated moves; draft reset delegates to move method.
3. `account.payment.register` source has batching/grouping, installments, write-offs, duplicate-payment and bank-trust fields; `_init_payments`, `_post_payments`, `_reconcile_payments`, `_create_payments`, `action_create_payments` located. Method bodies not fully captured; full behavior not verified.
4. `account.partial.reconcile` links debit and credit journal lines and carries company, currency, amount, optional full reconcile and exchange move relationships. `account.full.reconcile` links matched lines and partial records.
5. `account.move.line._reconcile_plan_with_sync()` prepares reconciliation partials, may create exchange difference moves and cash-basis tax entries, and groups fully reconciled lines into full reconciliation records. Full-reconcile tests account for same/multiple currencies and residual precision.
6. `account.move.line.reconcile()` delegates to `_reconcile_plan([self])`. `remove_move_reconcile()` unlinks associated partial reconciliation records; never invoke this against the research database.
7. Exchange-difference move creation requires configured gain/loss journal and accounts; corresponding source raises `UserError` when missing.
8. Bank-statement reconciliation source methods discovered (`_compute_is_reconciled`, `action_undo_reconciliation`, `_get_default_amls_matching_domain`); full bank matching behavior not yet exhaustively established.

## Database facts: read-only observation
- `pg_isready`: PostgreSQL accepting connections.
- Relevant tables found: `account_bank_statement_line`, `account_full_reconcile`, `account_journal`, `account_move`, `account_move_line`, `account_partial_reconcile`, `account_payment` (7).
- `information_schema.columns` query returned 114 rows across four tables: `account_full_reconcile`, `account_move_line`, `account_partial_reconcile`, `account_payment`.
- All four counted tables contained **0 records**: `account_payment`, `account_partial_reconcile`, `account_full_reconcile`, `account_bank_statement_line`.
- `account_move` and `account_move_line` contained **0 records** each.
- Commands ran in `BEGIN READ ONLY` transactions with `ROLLBACK`; do not overstate this as proof of every possible security property.
- Final `git status --short` output was empty (working tree clean).
- Source revision cited in README: `7c45959e02b2d8abc52913184237b72f7bae93a2`.
- One initial schema-query attempt was interrupted via Ctrl+C; subsequent complete schema query succeeded.

## Limits and pending verification
- No runtime payment/reconciliation scenarios are verifiable from the empty database.
- Reconciliation eligibility and exceptions (such as cross-account/cross-company combinations) require targeted follow-up reading of `_check_amls_exigibility_for_reconciliation` and test execution in a **separate isolated fixture**, not re-running the completed source command sequence.
- Some method bodies from the wizard and bank matching are discovery-only. Full implementation requirements must be differentiated from provisional source-derived candidates.
- Commands 2–10 are represented in preserved batches; Command 1 output is not separately preserved.

## Research disposition
Prescribed ten-command sequence marked completed based on user's terminal marker and output. This is **not** certification of exhaustive functional coverage or production readiness. Next research domain: 5 — Multi-currency accounting.