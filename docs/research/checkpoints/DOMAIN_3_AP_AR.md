> Historical research checkpoint (2026-11-04). These findings summarize the originally preserved evidence, not newly executed runtime tests. Referenced raw terminal outputs remain in the private evidence archive.

# ProofFlow — Odoo 19 Accounting Research
## Domain 3: Accounts Payable and Receivable — Evidence Checkpoint
Date: 2026-11-04

**Prescribed ten-command research sequence: completed according to the terminal completion marker and prior submitted batches.**
**Runtime AP/AR financial behavior: NOT VERIFIED (no transaction records).**

### Evidence archive
- `Domain3_Commands_3_to_4_Observed_Output.txt` — invoice, bill, payment term and source excerpts.
- `Domain3_Commands_5_to_6_Observed_Output.txt` — payment states and partner-account linkage; accounting partner model was missing at the checked path.
- `Domain3_Commands_7_to_10_Observed_Output.txt` — credit notes, supplier refund references, schema, read-only SQL results, clean working-tree and completion marker.
- Command 1 availability was submitted in chat: account_move, account_move_line, account_payment and account_payment_term available; account/models/res_partner.py absent at the checked path.
- Command 2 source evidence may be included in earlier conversation output, but no standalone archived file for its entire output is present here; do not imply completeness of captured snippets.

### Verified source-level observations
1. `account.move` has customer invoice/refund and supplier invoice/refund types. `TYPE_REVERSE_MAP` includes `out_invoice` ↔ `out_refund` and `in_invoice` ↔ `in_refund` (source location verified by Command 7 grep). The existence of the map is confirmed; each reversal branch is not runtime-tested.
2. The move links reversal documents through `reversed_entry_id` and `reversal_move_ids`. `_reverse_moves`, `_reconcile_reversed_moves`, and `action_reverse` were found previously in Domain 1; Domain 3 cross-references rather than repeats the analysis.
3. `purchase.order.line.invoice_lines` references `account.move.line` through `purchase_line_id`. `_prepare_qty_invoiced()` distinguishes `in_invoice` from `in_refund`, affecting net invoiced quantities; see preserved purchase model outputs and earlier purchase research for method-body details.
4. `_compute_amount` aggregates tax/product/payment-term line categories, including outstanding invoice balances. `_compute_payment_state` consults residual amounts, partial reconciliation, linked payments and bank statement relationships. Payment state cannot be inferred from a zero residual alone.
5. `account.payment` method locations `_compute_state` (455), `action_post` (1130), `action_cancel` (1156), `action_draft` (1165) were identified; bodies not inspected in this checkpoint. Deep payment lifecycle belongs to Domain 4.
6. `account.payment.term` and `account.payment.term.line` sources exist. Methods `_compute_terms` and `_get_due_date` and invoice `needed_terms`/`date_maturity` references were located. Installments and early-payment discounts are dependencies, not fully runtime-confirmed.
7. `account.move` links `partner_id` and `commercial_partner_id`, references `property_account_receivable_id` and `property_account_payable_id`, and a customer credit-limit calculation. The complete originating partner model was not retrieved from the checked `account/models/res_partner.py` path; its absence at that path does NOT establish missing accounting partner logic.

### Verified database observations
- PostgreSQL accepted connections; all `BEGIN READ ONLY` blocks ended with `ROLLBACK`.
- Schema discovery found seven named tables: `account_account`, `account_move`, `account_move_line`, `account_partial_reconcile`, `account_payment`, `account_payment_term`, `res_partner`.
- Schema columns include move `amount_residual`, `invoice_date`, `invoice_date_due`, `move_type`, `partner_id`, `payment_state`, `state`; line `account_id`, `amount_residual`, `amount_residual_currency`, `date_maturity`, `partner_id`, among others.
- Invoice/refund document distribution and posted invoice-line aggregates returned **0 rows**.
- `account_move` contained **0** records; `account_move_line` contained **0** records. By move type: **0 rows**.
- `git status --short` had no output; `DOMAIN 3 COMMANDS FINISHED` printed.

### Remaining uncertainties / separately tracked verification
- No observed transactions: no invoice, vendor-bill, installment, payment, credit-note, partial-payment or reversal runtime outcomes were tested.
- Partner accounting source location and full fields/credit calculations require targeted later inspection, not a rerun of the ten commands.
- Payment state transitions, discount/maturity edge cases, reconciliation and bank settlement require controlled fixtures and tests in a separate isolated environment.
- The exact source revision for inspected Docker files should be cross-checked with the recorded Odoo baseline before claiming revision identity.

### Decision
**Close Domain 3 prescribed research checkpoint as executed and recorded, with the above source and runtime gaps open.** Do not change the protected research database. Do not describe this as complete AP/AR runtime verification.

### Next
Domain 4 — Payments and Reconciliation. Reuse this record's payment-state method locations, reconciliation dependencies, and partner references; avoid duplicate research. Start with `account_payment.py` and reconciliation models, then read-only schema and record observation.