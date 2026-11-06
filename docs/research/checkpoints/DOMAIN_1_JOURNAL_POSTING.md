> Historical research checkpoint (2026-11-04). These findings summarize the originally preserved evidence, not newly executed runtime tests. Referenced raw terminal outputs remain in the private evidence archive.

# ProofFlow — Odoo 19 Accounting Research
## Domain 1: Journal Entries and Posting — Evidence Checkpoint
Date: 2026-11-04
Status: SOURCE PARTIALLY VERIFIED; RUNTIME BEHAVIOR UNVERIFIED; DO NOT MARK DOMAIN COMPLETE

## Evidence files preserved
- Domain1_Commands_3_to_5_Observed_Output.txt
- Domain1_Commands_6_to_7_Observed_Output.txt
- Domain1_Commands_7_to_8_Observed_Output.txt
- Domain1_Commands_9_to_10_Observed_Output.txt

## Observations grounded in the command outputs
1. `account.move.create()` (`models/source/account_move.py` ~3915) rejects `state='posted'` on creation, calls `_sanitize_vals()`, `_sync_dynamic_lines()`, and wraps in `_check_balanced()`.
2. `account.move._check_balanced()` (~2803) calls `_get_unbalanced_moves()`; the latter groups move lines, joins the company's currency, and filters based on rounded sum of line balance.
3. `account.move.line._compute_debit_credit()` (~747) maps balance to debit/credit differently when `is_storno` is true.
4. `account.move._post()` (~5593) checks `account.group_account_invoice` unless superuser, validates document/journal/account/company/currency constraints and handles future-dated moves based on `soft`; later writes `state='posted'` and `posted_before=True` for the records to post.
5. `account.move.action_post()` (~6214) delegates to `_post(soft=False)` except certain optional validation-wizard paths.
6. `_check_fiscal_lock_dates()` (~2844) uses `res.company._get_lock_date_violations()`; relevant lock date behavior depends on company and journal.
7. `account.move.write()` (~3933) restricts modifications to hashed entries and some posted-entry fields; exact effect depends on conditions and downstream methods.
8. `_reverse_moves()` (~5519) creates reversal moves and optionally posts/reconciles; `button_draft()` (~6303) checks eligibility and runs cleanup. Detailed branch coverage remains open.
9. The `odoo19-research-db` container accepted PostgreSQL connections; the read-only SQL transaction against `odoo19_security_research` executed and rolled back successfully.
10. In this database, `account_move` returned zero records, `account_move_line` returned zero rows (0 lines, 0 distinct move IDs), and the grouped journal balancing query also returned zero rows.

## Interpretation
- Source-level evidence supports the broad lifecycle from draft creation through validations, posting, reversal and reset-to-draft.
- The sampled database contains no journal records, so it does not verify actual posting, balancing, security, reversal, or lock-date behavior in executed transactions.
- No writes to the research database were performed by the supplied SQL commands; they used `BEGIN READ ONLY` and `ROLLBACK`.

## Uncertainty and missing checks
- Independent checksum results for the source manifest are not included in the preserved outputs listed above; do not record checksum verification as passing without its result.
- No controlled runtime transaction tests exist in the supplied Command 9/10 output.
- Full dependency inspection remains needed for `_check_draftable`, `_get_violated_lock_dates`, sequence hashing, audit trail, `account.journal`, company lock date logic and relevant security record rules.
- An empty database provides no evidence regarding multi-company isolation or accounting access controls.

## Decision
Leave Domain 1 unchecked. Retain source findings as verified to the extent directly shown; runtime behavior unverified. Do not manufacture sample data in the user's protected research DB. Proceed with a separately approved isolated runtime test fixture or continue dependency inspection using read-only source and metadata.

## Next action
Create a narrowly scoped Domain 1 closure plan identifying the minimal outstanding source dependencies and controlled runtime tests; reuse preserved source observations without re-running them unnecessarily.