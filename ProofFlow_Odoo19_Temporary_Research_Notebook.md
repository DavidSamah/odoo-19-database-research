# ProofFlow / Odoo 19 — Temporary research notebook

Purpose: Keep commands, observed output, interpretations, uncertainties, and next actions together for later review. This is a temporary working record, not a verified end-to-end implementation log.

## Research tracker
Phase 1 — Source-code evidence review complete as of 2026-11-02; controlled runtime validation explicitly deferred to Phase 7. Phase 2 — transaction lifecycle research is next.

## Evidence received — task 1.1
Source supplied by user: installed Odoo 19 Python source, excerpt from `account_move_line.py` (earlier grep located `_compute_totals` near line 918).

Command used:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '900,975p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_move_line.py
```

Observed:
- `_compute_totals` depends on `quantity`, `discount`, `price_unit`, `tax_ids`, `currency_id`, `amount_currency`.
- For permitted `display_type` values (`product`, `cogs`, `non_deductible_product`, `non_deductible_product_total`) where `move_id` exists, it obtains a base line from `line.move_id._prepare_product_base_line_for_taxes_computation(line)`.
- Calls `account.tax._add_tax_details_in_base_line` and `_round_base_lines_tax_details`.
- Assigns `price_subtotal` from `total_excluded_currency` and `price_total` from `total_included_currency`.
- Other lines or those without a move have both totals set to False.
- `_compute_price_unit` calls product `_get_tax_included_unit_price` for eligible lines, depending on document type, currency, date, fiscal position, and UoM.
- Excerpt also shows `_compute_tax_ids` and beginning of `_get_computed_taxes`, but its full implementation is not shown.

Interpretation: Invoice-line totals delegate to shared tax-computation machinery rather than a simple multiplication in this method.

Unverified: The behavior of `_prepare_product_base_line_for_taxes_computation`, detailed application of discount, tax inclusivity, currency conversion, and rounding; applicability to specific vendor bill examples; no transaction tests performed.

Decision: Mark method body inspected, but do not consider entire invoice pricing pipeline verified until dependencies inspected.

## Next command — trace tax-base preparation
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -n 'def _prepare_product_base_line_for_taxes_computation' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_move.py
```

Next: Inspect located method body and dependencies; remain in Phase 1.

## Prior verified checkpoints (summarized from conversation)
- PostgreSQL 17 container `odoo19-research-db`; database `odoo19_security_research`, user `odoo_research`; application container `odoo19-research-app`.
- Five relevant Odoo modules installed; eight target tables found.
- Selected PostgreSQL FK constraints and 30 matching columns verified; separate 22-column query verified pricing/status fields (overlapping sets).
- Five selected transaction categories had zero records.
- Source examined for receipt calculations (`purchase_stock` and `purchase`) and invoiced quantity calculations (`purchase`).
- Purchase-side pricing methods inspected; Git remote merge/push completion not yet verified.

## Recording convention for further steps
Research question → command/source → observed result → interpretation → uncertainty → risk → next action. Never promote an inference to an observation.

## Phase 1 — Dependency-location checkpoint (2026-11-02)
Research question: Where is `account.move._prepare_product_base_line_for_taxes_computation` defined in the installed Odoo 19 source?
Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -n 'def _prepare_product_base_line_for_taxes_computation' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_move.py
```
Observed output: `1597:    def _prepare_product_base_line_for_taxes_computation(self, product_line):`
Interpretation: The named method declaration is located at line 1597 in `account_move.py`.
Uncertainty: Implementation and dependencies not yet inspected; no billing-price calculations validated end-to-end.
Risk: Read-only source inspection.
Next action: Read source lines 1585–1665 and examine the complete relevant method (extend range if needed).
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '1585,1665p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_move.py
```

## Phase 1 — Invoice tax-base preparation inspected (2026-11-02)
Research question: How does `account.move` assemble the product-line inputs to Odoo's tax engine?
Source inspected: `/usr/lib/python3/dist-packages/odoo/addons/account/models/account_move.py`, excerpt lines 1585–1665 (provided by user).
Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '1585,1665p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_move.py
```
Observed:
- `_get_product_base_line_currency_rate` returns `invoice_currency_rate` for invoices/receipts; for other documents it computes `abs(amount_currency / balance)` when balance is nonzero, otherwise `0.0`.
- `_prepare_product_base_line_for_taxes_computation` checks `is_invoice(include_receipts=True)` and sets `sign = direction_sign` for invoices, otherwise `1`.
- For invoices it passes line `price_unit`, `quantity`, and `discount`; for non-invoices, it passes `amount_currency`, quantity `1.0`, and discount `0.0`.
- It passes the calculated `rate`, `sign`, `name`, and `special_mode` (`False` for invoices; `total_excluded` otherwise).
- `extra_tax_data.computation_key` prefixes `global_discount` and `down_payment` select corresponding `special_type`.
- It delegates to `account.tax._prepare_base_line_for_taxes_computation(product_line, **kwargs)`.
- Separate early-payment discount (`epd`) path includes `is_refund` for refund move types and `special_type='early_payment'` (not yet traced further).
Interpretation: The invoice product-line preparation carries price, quantity, discount, currency-rate/sign context into the shared tax engine; the computation of totals occurs downstream.
Uncertainty: Exact calculations and rounding inside `account.tax`, treatment of tax-included amounts, special discounts and currency variations, and applicability to complete test cases remain unverified.
Risk: Read-only source inspection; no changes to database or containers.
Decision: Do not check off the whole tax calculation/price comparison tasks. Continue tracing the delegated method.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -R -n -F 'def _prepare_base_line_for_taxes_computation' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models
```

## Phase 1 — Shared account.tax preparation method located (2026-11-02)
Research question: Where does Odoo 19 implement the shared tax-base preparation called by invoice-line pricing?
Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -R -n -F 'def _prepare_base_line_for_taxes_computation' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models
```
Observed output: `/usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py:1596:    def _prepare_base_line_for_taxes_computation(self, record, **kwargs):`
Interpretation: The declaration is present at line 1596 of `account_tax.py`, as reported by the user's local source search.
Uncertainty: The implementation and any helper calculations are not inspected yet. Nothing about tax inclusion, discounts, or rounding is established by this location search alone.
Risk: Read-only search; no database modifications indicated.
Decision: Keep Phase 1 tax-related checklist tasks open until the implementation and dependencies are inspected.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '1590,1685p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```

## Phase 1 — Shared tax-base preparation inspected, first excerpt (2026-11-02)
Research question: Which inputs does `account.tax._prepare_base_line_for_taxes_computation` collect, and does the excerpt establish tax calculation behavior?
Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '1590,1685p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```
Observed (user-provided excerpt):
- `load(field, fallback)` delegates field retrieval to `_get_base_line_field_value_from_record`, using record / kwargs and fallbacks.
- Currency is chosen from `currency_id`, `company_currency_id`, company currency, or an empty currency recordset in that order.
- The returned `base_line` dictionary includes `record`, `id`, `product_id`, `product_uom_id`, `tax_ids`, `price_unit`, `quantity`, `discount`, `currency_id`.
- `special_mode` supports normal, `total_included`, and `total_excluded` modes; `special_type` covers cases such as early payment, cash rounding and non-deductibility.
- It includes `rate`, `filter_tax_function`, `sign`, `is_refund`, `partner_id`, `account_id`, and `analytic_distribution`.
- Additional data includes `computation_key`, `manual_total_excluded_currency`, `manual_total_excluded`, and `manual_tax_amounts`.
- Docstring identifies this as a Python dictionary preparation method and requests consistency with `account_tax.js`.
- Supplied excerpt stops at `if 'price_unit' in extra_tax_data:`; subsequent logic and return have not been inspected.
Interpretation: This method gathers and normalizes inputs for downstream tax computation; the provided portion does not demonstrate the tax calculation formula, tax rounding, or final totals.
Uncertainty: Remainder of method, `_add_tax_details_in_base_line`, `_round_base_lines_tax_details`, and correctness of behavior in transaction tests remain unverified.
Risk: Read-only source inspection.
Decision: Keep Phase 1 tax/rounding checklist tasks open. Continue with remaining portion of this method before tracing downstream calculators.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '1680,1735p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```

## Phase 1 — Tax-base preparation completed; tax-line preparation begins (2026-11-02)
Research question: Does `_prepare_base_line_for_taxes_computation` do calculations, and how does its implementation end?
Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '1680,1735p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```
Observed (user-supplied output):
- If `extra_tax_data` contains `price_unit`, it overrides `base_line['price_unit']`.
- For dictionary-based `record`, additional keys beginning `_` are copied into `base_line` only if not already present.
- Method returns the prepared `base_line` dictionary.
- A separate method, `_prepare_tax_line_for_taxes_computation`, begins immediately afterward. Its docstring says it creates dictionaries of tax-line data for detecting tax lines to update, create or delete; it is not the requested tax arithmetic method.
Interpretation: The entire inspected base-line method prepares input data; the actual numerical tax details and rounding happen elsewhere. An extra-data unit price override matters when tracing price discrepancies.
Uncertainty: Implementation of `_add_tax_details_in_base_line` and `_round_base_lines_tax_details` remains uninspected. No full behavioral or transaction-level verification.
Risk: Read-only source inspection.
Decision: Do not mark Phase 1 tax and rounding tasks complete. Locate both calculation methods next.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -n -E 'def _add_tax_details_in_base_line|def _round_base_lines_tax_details' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```

## Phase 1 — Locate tax arithmetic and rounding methods (2026-11-02)
Research question: Where are tax detail computation and rounding implemented in the installed Odoo 19 account module?
Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -n -E 'def _add_tax_details_in_base_line|def _round_base_lines_tax_details' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```
Observed (user-supplied output):
- line 1742: `def _add_tax_details_in_base_line(self, base_line, company, rounding_method=None):`
- line 1816: `def _add_tax_details_in_base_lines(self, base_lines, company):`
- line 2190: `def _round_base_lines_tax_details(self, base_lines, company, tax_lines=None):`
Interpretation: Both requested method definitions were located in `account_tax.py`; grep also returned a plural base-lines helper because its name contains the matching string.
Uncertainty: These methods' bodies and exact tax/rounding semantics have not yet been inspected or tested.
Risk: Read-only grep; no environment changes indicated.
Decision: Keep Phase 1 tax computation and rounding checklist open. Inspect the single-base-line calculator first.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '1740,1818p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```

## Phase 1 — Inspect `_add_tax_details_in_base_line` (2026-11-02)
Research question: How does Odoo 19 calculate tax detail input quantities and amounts, including discounts, exchange-rate handling, and per-line rounding?
Source: User-supplied excerpt of `/usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`, lines approximately 1742–1815.
Command used:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '1740,1818p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```
Observed:
- Takes `rounding_method` from the caller or `company.tax_calculation_rounding_method`.
- Computes `price_unit_after_discount = price_unit * (1 - discount/100.0)`.
- Calls `tax_ids._get_tax_details(...)` with discounted price, quantity, currency rounding precision, rounding method, product, UoM, special mode, tax filter.
- For `non_deductible` special type, treats reverse-charge tax entries differently.
- Stores raw tax-exclusive/inclusive totals in document currency and converts to local currency by dividing by `rate` (or assigns 0 if rate is zero).
- When `round_per_line`, rounds local-currency totals, tax amounts and tax bases using company currency rounding.
- Stores per-tax entries with document- and local-currency amounts.
Interpretation: This method computes discounted tax detail data, but delegates actual tax calculations to `_get_tax_details`; further rounding/final subtotal handling is done downstream.
Uncertainty: `_get_tax_details` arithmetic, rounding method `_round_base_lines_tax_details`, complete behavior of special types and tested results remain unverified. No end-to-end transaction tests.
Risk: Source inspection only; no database modification indicated.
Decision: Keep Phase 1 rounding and invoice/pricing checklist items open.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '2185,2285p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```

## Phase 1 — Inspect `_round_base_lines_tax_details` part 1 (2026-11-02)
Research question: How does Odoo round and redistribute amounts following tax calculation?
Source: User-supplied excerpt of `/usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`, beginning at line 2190; method excerpt incomplete.
Command used:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '2185,2285p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```
Observed:
- Docstring describes global rounding by aggregate tax, with differences redistributed across base lines, and warns against independently rounding Odoo amounts.
- Iterates over document and company currencies; rounds `raw_total_excluded`, `raw_base_amount`, and `raw_tax_amount` into their non-raw counterparts using each currency's rounding.
- Begins handling manual total overrides and per-tax manual amounts, including reverse-charge sign adjustments and rate-dependent company-currency conversions.
- Docstring example illustrates global rounding adjustments for two tax-inclusive lines; this is documentation, not an observed runtime test.
Interpretation: Odoo has a dedicated rounding stage with per-currency rounding, optional manual overrides and potentially distributed rounding differences; copying single-line arithmetic into ProofFlow risks inconsistent results.
Uncertainty: The excerpt cuts off inside manual amount processing; the remainder of the method (including actual distribution code) has not been inspected. No runtime test performed.
Risk: Read-only source inspection, no database changes indicated.
Decision: Keep Phase 1 tax rounding tasks pending until full method and dependencies are reviewed.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '2280,2380p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```

## Phase 1 — Inspect `_round_base_lines_tax_details` part 2 (2026-11-02)
Research question: What does the remainder of Odoo's tax rounding coordinator do?
Source: User-supplied continuation of `/usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`, approximately lines 2280–2380.
Command used:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '2280,2380p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```
Observed:
- Completes the manual-tax amount override loop, including converting override amounts into company currency when the rate is nonzero.
- Initializes `delta_total_excluded{suffix}` to 0.0 and `total_included{suffix}` to `total_excluded{suffix}` for both document and company currency, then adds tax amounts to included totals.
- Calls three downstream methods in sequence: `_round_tax_details_tax_amounts`, `_round_tax_details_base_lines`, and `_round_tax_details_tax_amounts_from_tax_lines`.
- Following code defines tax-line grouping keys; this is a separate part of the file, not the rounding coordinator.
Interpretation: The coordinator's visible body is now fully examined; actual difference distribution occurs in delegated helpers, which remain uninspected. Do not infer their detailed algorithms from method names or docstrings alone.
Uncertainty: The three helper implementations and behavior under actual transactions have not been verified. Phase 1 still open.
Risk: Read-only source inspection, no modifications indicated.
Decision: Next locate and inspect delegated rounding helpers before marking rounding verified.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -n -E 'def _round_tax_details_tax_amounts\(|def _round_tax_details_base_lines\(|def _round_tax_details_tax_amounts_from_tax_lines\(' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```

### Phase 1 — Rounding helper locations verified (2026-11-02)
Research question: Where are the three rounding helpers called by `_round_base_lines_tax_details` defined?
Command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -E 'def _round_tax_details_tax_amounts\(|def _round_tax_details_base_lines\(|def _round_tax_details_tax_amounts_from_tax_lines\(' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`
Observed (user-provided output):
- `1902: def _round_tax_details_tax_amounts(self, base_lines, company, mode='mixed'):`
- `2000: def _round_tax_details_base_lines(self, base_lines, company, mode='mixed'):`
- `2111: def _round_tax_details_tax_amounts_from_tax_lines(self, base_lines, company, tax_lines):`
Interpretation: All three helper definitions are located in `account_tax.py`. Location alone does not verify their behavior.
Uncertainty: Their bodies and rounding edge cases remain uninspected.
Risk: Read-only grep, no database edits indicated.
Decision: Continue Phase 1; do not check off final rounding yet.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '1900,1999p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`

### Phase 1 — First rounding helper inspected (2026-11-02)
Research question: How does Odoo redistribute rounding differences across tax amounts and tax bases?
Source/command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '1900,1999p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`
Observation (user-provided source excerpt): `_round_tax_details_tax_amounts(base_lines, company, mode='mixed')` aggregates tax details by tax, currency, refund flag, reverse-charge status, price-inclusion flag, and computation key. In both document and company currency, it compares the rounded aggregate tax amount against the sum of allocated tax amounts, and distributes nonzero differences via `_distribute_delta_amount_smoothly`. It similarly redistributes differences for base amounts, calculating the target differently under price-included and price-excluded modes. Modes documented: `excluded`, `included`, and `mixed`.
Interpretation: This helper explicitly reconciles per-line tax/base values with rounded aggregate targets, with handling dependent on price-included configuration. It is not appropriate for ProofFlow to independently round and compare each invoice line without considering Odoo's rounding rules.
Uncertainty: `_distribute_delta_amount_smoothly`, grouping helpers, the other two rounding helpers, and practical outcomes in transactions remain unverified.
Risk: Read-only source inspection; no database modification indicated.
Decision: Continue Phase 1; no complete phase checklist signoff yet.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '2000,2110p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```

### Phase 1 — Second rounding helper inspected (2026-11-02)
Research question: How does Odoo reconcile tax-exclusive bases after rounding, including price-included taxes?
Source/command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '2000,2110p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`
Observation (user-provided source excerpt): `_round_tax_details_base_lines(base_lines, company, mode='mixed')` groups by currency, refund status, and computation key; in mixed mode it selects `excluded` if a nonzero price-excluded tax is present, otherwise `included`. In document and company currencies, it computes a delta between rounded aggregate totals and existing totals (using tax-exclusive totals for excluded mode, or tax-inclusive totals for included mode). It distributes the delta using `_distribute_delta_amount_smoothly`, adding allocations to `tax_details['delta_total_excluded{suffix}']`. This helper does not directly modify `taxes_data` rounding.
Interpretation: Base-line rounding adjustments are separately tracked; a line's displayed subtotal and its accounting balance may differ under global rounding. Comparing independently rounded quantities in ProofFlow may create false mismatches.
Uncertainty: The third helper `_round_tax_details_tax_amounts_from_tax_lines` (line 2111), distribution algorithm, and actual runtime behavior remain uninspected or untested.
Risk: Read-only source inspection; no database changes indicated.
Decision: Keep Phase 1 active; no overall task signoff yet.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '2111,2189p' \
  /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py
```

### Phase 1 — Third rounding helper inspected (2026-11-02)
Research question: How are already-existing tax-line amounts reconciled to computed base-line tax amounts?
Source/command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '2111,2189p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`
Observation (user-provided source excerpt): `_round_tax_details_tax_amounts_from_tax_lines(base_lines, company, tax_lines)` returns without changes if `tax_lines` is absent. Otherwise, it aggregates tax-line amounts by tax ID, currency ID and refund-document flag, using signed `amount_currency` and `balance`. It groups base-line tax details by tax, currency and refund status, calculates the difference between existing tax-line targets and computed tax totals in both document and company currency, and apportions that difference through `_distribute_delta_amount_smoothly` to individual tax-data amounts. Groups with no matching tax lines or with zero current totals are skipped.
Interpretation: Odoo can respect existing/manual tax-line values during reconciliation, rather than always replacing them with freshly calculated values. Tax comparison in ProofFlow must be context-aware.
Uncertainty: The actual distribution helper implementation and end-to-end runtime tests remain uninspected. Need avoid claiming all edge cases validated.
Risk: Read-only source inspection; no database modifications indicated.
Decision: Three rounding helper bodies have now been inspected; Phase 1 is still open pending remaining required evidence and checklist review.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -F 'def _distribute_delta_amount_smoothly' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`

### Phase 1 — Rounding delta distribution helper located (2026-11-02)
Research question: Where is the implementation that distributes tax rounding deltas?
Source/command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -F 'def _distribute_delta_amount_smoothly' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`
Observation (user-provided output): `1845:    def _distribute_delta_amount_smoothly(self, precision_digits, delta_amount, target_factors):`
Interpretation: Helper definition is located in `account_tax.py` at line 1845; its implementation has not yet been inspected.
Uncertainty: Actual delta allocation logic, tie handling and edge cases remain unverified.
Risk: Read-only grep; no changes to application or database.
Decision: Keep Phase 1 open and inspect definition before drawing conclusions.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '1835,1901p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`

### Phase 1 — Rounding delta distribution algorithm inspected (2026-11-02)
Research question: How does Odoo distribute tax rounding differences among base lines or tax details?
Source/command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '1835,1901p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`
Observation (user-provided source excerpt): `_normalize_target_factors` takes absolute factor magnitudes, sorts descending, and normalizes weights, using equal weights if their sum is zero. `_distribute_delta_amount_smoothly` returns an empty list for no targets; returns zeros when the delta is zero at supplied precision; converts the absolute delta to a count of smallest currency units; allocates rounded proportional units, capped by remaining units; then assigns residual units in sorted factor order, with sign restored.
Interpretation: The helper apportions rounded residuals by factor magnitude and distributes remaining precision units deterministically in the supplied ordering; it is not simply a uniform or per-line independent rounding procedure. This source supports avoiding self-rounded comparisons in ProofFlow.
Uncertainty: This is source inspection only; no runtime validation of actual invoice scenarios or edge cases. Tied factors preserve input order via Python's stable sorting, but business behavior with ties is not empirically verified. Odoo's remaining tax calculation helper `_get_tax_details` not inspected in this sequence.
Risk: Read-only source inspection; no database changes indicated.
Decision: First Phase 1 checklist item (`_compute_totals` inspection) has source evidence. Leave remaining checklist items pending comparative source analysis and controlled validation.
Next action: Compare vendor-bill versus purchase-order discount treatment using the already inspected `_compute_price_unit_discounted` and the observed `_compute_totals`/`_add_tax_details_in_base_line` paths; inspect relevant source context only if needed.

### Phase 1 — Price/discount field definitions located (2026-11-02)
Research question: Where are the purchase-order and accounting-line discount and unit-price fields defined?
Source/command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -E 'discount = fields|price_unit = fields|price_unit_discounted = fields' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order_line.py /usr/lib/python3/dist-packages/odoo/addons/account/models/account_move_line.py`
Observation (user-provided): `purchase_order_line.py`: `discount` line 29, `price_unit` line 46, computed `price_unit_discounted` line 52, and `technical_price_unit` line 121. `account_move_line.py`: `price_unit` line 399 and `discount` line 414.
Interpretation: Both purchase and accounting lines define unit-price and discount fields. A computed discounted unit-price field was located for purchase lines; the absence of an analogous hit in this particular grep does not establish that no other discount-related field or calculation exists for accounting lines. Earlier inspected code applies a discount to the tax-base unit price.
Uncertainty: Field attributes, defaults, constraints, and any further override semantics have not yet been inspected in their full declarations. No runtime comparison has been tested.
Risk: Read-only search.
Decision: Continue Phase 1, task 3 (discount comparison); do not mark comparison complete based on search results alone.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sh -c "sed -n '20,62p' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order_line.py; sed -n '390,432p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_move_line.py"`

### Phase 1 — Purchase versus accounting discount field definitions inspected (2026-11-02)
Research question: How do the two Odoo models declare discount and unit-price fields, and what can we conclude about their pricing paths?
Source: User-provided output of `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sh -c "sed -n '20,62p' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order_line.py; sed -n '390,432p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_move_line.py"`.
Observation: Purchase order lines define `discount` as a computed, stored, writable Float with `digits='Discount'`; `price_unit` as a computed, stored, writable Float; `price_unit_discounted` as a computed Float; and `price_subtotal`, `price_total`, `price_tax` using `_compute_amount`. Accounting move lines define `discount` as a Float with `digits='Discount'`, default 0; `price_unit` as a computed, stored, writable Float; and `price_subtotal` and `price_total` as stored Monetary fields computed using `_compute_totals`. They also expose company-related `tax_calculation_rounding_method`.
Interpretation: Field definitions differ in how purchase and accounting discounts are populated: purchase discount is computed (but writable); accounting discount has a direct default. Previously inspected code confirms both flow through Odoo's tax-base computation, which applies a discount to unit price. This is code-path evidence, not experimental equivalence of vendor-bill and PO results.
Uncertainty: Purchase price/discount computation's supplier selection and the invoice's defaulting/copying of discount from PO remain unverified; different taxes, units or currencies may yield different effective amounts. Runtime equivalence is untested.
Risk: Read-only source inspection; no database modification indicated.
Decision: Keep Phase 1 active; do not claim full purchase-versus-bill discount equivalence. Next examine how purchase order line values are transferred into vendor bill lines, instead of repeating previously examined rounding code.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -R -n -F 'def _prepare_account_move_line' /usr/lib/python3/dist-packages/odoo/addons/purchase/models /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models`

### Phase 1 — Purchase-to-bill preparation methods located (2026-11-02)
Research question: Which Odoo methods prepare purchase-order lines as accounting lines, including any discount transfer?
Source/command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -R -n -F 'def _prepare_account_move_line' /usr/lib/python3/dist-packages/odoo/addons/purchase/models /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models`
Observation (user-provided): `purchase/models/purchase_order_line.py:632` defines `_prepare_account_move_line`; `purchase_stock/models/purchase_order_line.py:316` defines a method with the same name.
Interpretation: The two method definitions are located; no conclusion yet about inheritance, discount propagation or bill-line prices without reading the bodies.
Uncertainty: Values passed to invoice lines and any override behavior, conversion and special cases remain unverified.
Risk: Read-only source discovery.
Decision: Continue Phase 1, task 3; no additional checklist item signed off.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sh -c "sed -n '625,695p' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order_line.py; sed -n '310,345p' /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order_line.py"`

### Phase 1 — Purchase-to-vendor-bill price and discount transfer inspected (2026-11-02)
Research question: What values are transferred from an Odoo purchase order line to a vendor-bill line, and what does purchase_stock add?
Source: User-supplied Git Bash `sed` output from `/usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order_line.py` lines 625–695 and `purchase_stock/models/purchase_order_line.py` lines 310–345.
Observation: Base `_prepare_account_move_line(move=False)` sets `discount` to `self.discount`; sets `price_unit` through `self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date, round=False)`; transfers `product_id`, `product_uom_id`, `tax_ids`, and `purchase_line_id`; and sets quantity to negative `qty_to_invoice` for an `in_refund` move, otherwise positive. The `purchase_stock` override calls `super()` and, when `balance` is absent, computes a tax-exclusive amount from `self.price_unit_discounted` using `tax_ids.compute_all(... quantity=self.qty_to_invoice ...)`, then converts this amount to company currency with `round=False` and adds `balance`.
Interpretation: Code directly supports copying the PO discount and transferring the PO unit price with currency conversion into prepared accounting-line values. The purchase_stock override supplements the prepared values with an accounting balance if missing. This does not prove that final saved vendor bills always retain these exact values or that prices match in every unit/currency case.
Uncertainty: Call sites, possible later onchange/recomputation or overrides, currency-date effects, tax configurations, UOM conversions, and transactional tests remain unverified. `balance` is not necessarily the bill-line `price_subtotal`. No end-to-end transaction was present in the research database.
Risk: Read-only source inspection. No database write observed.
Decision: Phase 1 discount comparison now has direct preparation-path evidence; defer final sign-off of full pricing equivalence until controlled validation. Next investigate currency and unit-of-measure normalization.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -E 'def _compute_price_unit_product_uom|def _compute_price_unit_discounted|def _prepare_account_move_line' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order_line.py`

### Phase 1 — PO discounted price and unit-of-measure price expression inspected (2026-11-02)
Research question: How does the PO line calculate discounted price and normalize a unit price to the product's unit of measure?
Source: User-provided Git Bash output from `sed -n '155,175p' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order_line.py`.
Observation: `_compute_price_unit_discounted()` assigns `line.price_unit * (1 - line.discount / 100)`; `_compute_price_unit_product_uom()` assigns `not line.display_type and not line.is_downpayment and line.product_uom_id._compute_price(line.price_unit, line.product_id.uom_id)`. Both carry `@api.depends` decorators for their respective fields. The excerpt also shows tax selection via fiscal position and `_compute_qty_invoiced` beginning, but not the UoM `_compute_price` implementation.
Interpretation: The discounted-unit-price formula is explicit. A PO unit price is normalized using the UoM `_compute_price` helper for applicable ordinary lines, while display/downpayment lines short-circuit. The formula for normalized price includes the raw price unit; it does not itself apply the discount.
Uncertainty: The `_compute_price` implementation and its rounding behavior remain uninspected; final vendor bill matching and cross-currency normalization are not experimentally verified.
Risk: Read-only source inspection; no database change indicated.
Decision: Continue Phase 1 task 4; do not mark complete. Trace the UoM conversion implementation using read-only search.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -R -n -F 'def _compute_price(' /usr/lib/python3/dist-packages/odoo/addons/uom/models`

### Phase 1 — UoM price conversion helper located (2026-11-02)
Research question: Where is the implementation of the Odoo unit-of-measure price conversion helper used by purchase lines?
Action/source: User ran a read-only grep for `def _compute_price(` under `/usr/lib/python3/dist-packages/odoo/addons/uom/models` in the Odoo application container.
Observed result: `/usr/lib/python3/dist-packages/odoo/addons/uom/models/uom_uom.py:196:    def _compute_price(self, price: float, to_unit: Self) -> float:`
Interpretation: Method definition located in `uom_uom.py` at line 196. Its logic has not yet been inspected.
Uncertainty: Conversion formula, category compatibility handling, and any rounding or error conditions.
Risk: Search is read-only; no database modification indicated.
Decision: Continue Phase 1, Task 4; do not mark it complete.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '185,230p' /usr/lib/python3/dist-packages/odoo/addons/uom/models/uom_uom.py`

### Phase 1, Task 4 — UoM price conversion implementation inspected (2026-11-02)
Research question: What conversion and rounding behavior does `uom.uom._compute_price` implement?
Action/source: User provided output of `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '185,230p' /usr/lib/python3/dist-packages/odoo/addons/uom/models/uom_uom.py`.
Observed result: Method calls `self.ensure_one()` and returns original `price` when no source unit, price, target unit, or when source and target units are equal. Otherwise computes `amount = price * to_unit.factor` and then `amount = amount / self.factor`. The shown method does not explicitly round or check UoM category compatibility. Nearby `_has_common_reference` checks common parent paths but is not called in the shown `_compute_price`.
Interpretation: For nonzero price and distinct units with valid factors, `converted_price = price * target.factor / source.factor`. No explicit rounding happens inside this helper; upstream/downstream logic might still round. Category-compatibility validation is not established by this source excerpt.
Uncertainty: How factors are defined and validated; compatibility enforcement in caller/model; quantity-conversion rounding; end-to-end currency and invoice matching.
Risk: Read-only source inspection, no database changes indicated.
Decision: Keep Phase 1 Task 4 open; proceed to quantity conversion helper inspection and then currency conversion rules. Do not conflate UoM with currency conversion.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -F 'def _compute_quantity(' /usr/lib/python3/dist-packages/odoo/addons/uom/models/uom_uom.py`

### Phase 1, Task 4 — Quantity conversion helper located (2026-11-02)
Research question: Where is the implementation of Odoo's UoM quantity conversion helper?
Action/source: User executed read-only grep for `def _compute_quantity(` inside `uom_uom.py`.
Observed result: `147:    def _compute_quantity(`.
Interpretation: Definition starts at line 147; implementation not yet inspected.
Uncertainty: Quantity conversion formula, rounding options, compatibility and failure conditions.
Risk: Read-only search; no database change indicated.
Decision: Phase 1 Task 4 remains open.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '140,185p' /usr/lib/python3/dist-packages/odoo/addons/uom/models/uom_uom.py`

### Phase 1, Task 4 — UoM quantity conversion implementation inspected (2026-11-02)
Research question: How does `uom.uom._compute_quantity` convert and round quantities?
Action/source: User supplied output from `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '140,185p' /usr/lib/python3/dist-packages/odoo/addons/uom/models/uom_uom.py`.
Observation: Signature defines `round=True`, `rounding_method='UP'`, `raise_if_failure=True`. For missing source or zero quantity it returns input. When source equals destination it retains `qty`; otherwise computes `qty * self.factor / to_unit.factor` if destination exists. When a destination exists and `round` is true, calls `tools.float_round` with `precision_rounding=to_unit.rounding` and the chosen method. Despite the docstring discussing incompatible categories and `raise_if_failure`, the shown method body does not inspect that flag or enforce a category check.
Interpretation: The quantity helper applies target-UoM rounding by default, unlike the examined price helper which does not explicitly round. Caller-specific parameters can change the rounding behavior. The docstring is not sufficient evidence of a compatibility guard.
Uncertainty: Whether compatibility checks occur elsewhere; expected behavior in controlled transactions; currency conversion implementation.
Risk: Read-only source inspection, no database changes indicated.
Decision: Keep Phase 1 Task 4 open pending currency conversion and broader validation.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -R -n -E 'def _convert\(' /usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py`

### Phase 1, Task 4 — Currency conversion method located (2026-11-02)
Research question: Where is the implementation of Odoo's currency conversion used for purchase-to-invoice pricing?
Action/source: User ran read-only grep for `def _convert(` in `/usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py`.
Observed result: `284:    def _convert(self, from_amount, to_currency, company=None, date=None, round=True):  # noqa: A002 builtin-argument-shadowing`.
Interpretation: The `res.currency._convert` method is defined at line 284 and accepts an optional company, date, and `round=True` parameter. No internal conversion formula has been inspected yet.
Uncertainty: Rate lookup, date handling, no-rate and same-currency behavior, rounding details.
Risk: Read-only source search; no database modification indicated.
Decision: Phase 1 Task 4 remains open.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '275,330p' /usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py`

### Phase 1, Task 4 — Currency conversion body inspected (2026-11-02)
Research question: How does `res.currency._convert` calculate and round converted amounts?
Action/source: User supplied source output from `sed -n '275,330p' /usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py` inside `odoo19-research-app`.
Observation: `_convert(from_amount, to_currency, company=None, date=None, round=True)` selects available currencies and asserts both are present. For nonzero `from_amount`, it calculates `from_amount * self._get_conversion_rate(self, to_currency, company, date)`; for zero amount it returns `0.0`. It returns `to_currency.round(to_amount)` when `round=True`, otherwise the unrounded amount. The preceding excerpt shows other code referencing the root company and contextual date but its complete method context was not included.
Interpretation: The conversion result depends on a separate exchange-rate lookup method; rounded-versus-unrounded results depend on the caller's `round` option. Earlier PO-to-bill preparation explicitly used `round=False`.
Uncertainty: Exact rate lookup and historical rate selection inside `_get_conversion_rate`; handling missing rates, company-specific rates and same-currency conversion; runtime tests.
Risk: Read-only source inspection; no modifications indicated.
Decision: Phase 1 Task 4 remains open; inspect rate retrieval next.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -F 'def _get_conversion_rate(' /usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py`

### Phase 1, Task 4 — Exchange-rate method located (2026-11-02)
Research question: How does Odoo select a conversion rate for a currency pair, company, and date?
Action/source: User ran `grep -n -F 'def _get_conversion_rate(' /usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py` in the application container.
Observation: `273:    def _get_conversion_rate(self, from_currency, to_currency, company=None, date=None):`
Interpretation: The requested method is present at line 273; locating a definition alone does not establish the complete behavior.
Uncertainty: The calculation, date/company selection and fallback are not fully inspected.
Risk: Read-only source search; no database changes indicated.
Decision: Phase 1 Task 4 remains open.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '255,285p' /usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py`

### Phase 1 / Task 4 — Currency conversion rate selection (source inspected)
Research question: How does `_get_conversion_rate` select the effective exchange rate?
Source/command: User ran `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '255,285p' /usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py`.
Observed: The method returns 1 for equal currencies; resolves the company to `(company or self.env.company).root_id`; conditionally uses `from_currency.sudo()` if the user has access to that root company; defaults the date to `fields.Date.context_today(self)`; returns `from_currency.with_company(company).with_context(to_currency=to_currency.id, date=str(date)).inverse_rate`. It refers in comments to `_get_rates` and `_check_company_id`.
Interpretation: The conversion rate used by `_convert` is the context-dependent `inverse_rate` under root-company/date/target-currency context, rather than a hardcoded exchange rate. The code shown does not itself reveal how that field obtains historical rates.
Uncertainty: The definition/computation of `inverse_rate`, fallback for missing rates, and company/date rate selection remain to be inspected. No runtime tests yet.
Risk: Read-only inspection; no database writes indicated.
Decision: Phase 1 Task 4 remains open.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -E 'inverse_rate =|def _compute_inverse_rate|def _get_rates\(' /usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py`

### Phase 1 / Task 4 — Currency inverse-rate definitions located
Research question: How is the context-dependent inverse rate calculated and where does it obtain exchange rates?
Action/source: User ran source search for `inverse_rate =`, `def _compute_inverse_rate`, and `def _get_rates(` in `/usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py`.
Observed output:
```
33:    inverse_rate = fields.Float(compute='_compute_current_rate', digits=0, readonly=True,
120:    def _get_rates(self, company, date):
156:            currency.inverse_rate = 1 / currency.rate
```
Interpretation: `inverse_rate` is a computed field associated with `_compute_current_rate`; `_get_rates` is defined at line 120; the source includes a reciprocal assignment at line 156. The surrounding conditions and rate selection are not yet inspected.
Uncertainty: How `_get_rates` chooses rates (including missing data and company/date), how `_compute_current_rate` populates `rate`, and whether a zero-rate guard exists.
Risk: Source-only search; no database changes indicated.
Decision: Phase 1 / Task 4 still open. Do not infer full rate selection from the three matching lines.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '110,165p' /usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py`

### Phase 1 / Task 4 — Historical currency-rate selection inspected
Research question: How does Odoo 19 select company/date-dependent rates for currency conversion?
Action/source: User inspected lines 110–165 of `/usr/lib/python3/dist-packages/odoo/addons/base/models/res_currency.py` using `sed` inside the Odoo container.
Observation: `_get_rates(company,date)` searches `res.currency.rate` with `name <= date`, allowing global or root-company rates, ordered with `company_id.id, name DESC` and `limit=1`, correlated per currency. It provides a fallback query without the date limit, ordered with `company_id.id, name ASC` and `limit=1`. SQL `COALESCE` uses the dated result, then fallback, then `1.0`. `_compute_current_rate` reads date/company/to_currency from context, calls `_get_rates`, calculates `currency.rate = (currency_rates.get(currency.id) or 1.0) / currency_rates.get(to_currency.id)`, and `inverse_rate = 1 / currency.rate`.
Interpretation: Rate selection is date-sensitive with an earliest-available fallback if no prior dated rate is found; absent rates may ultimately default to 1.0. Rate choice is also influenced by global and root-company records. The precise preference and missing target-rate edge cases should be tested rather than asserted from the excerpt alone.
Uncertainty: Effective precedence between company-specific and global rates for all scenarios, zero/missing target rate behavior, effective conversion rates for controlled data, access contexts, and rounding behavior at runtime.
Risk: Source inspection only; no database changes.
Decision: Phase 1 Task 4 remains open for controlled validation, but source-level rate selection has been traced. Avoid further recursive code chasing unless a concrete unresolved requirement demands it. Continue with Phase 1 Task 5, tax-inclusive versus tax-exclusive behavior, using focused source inspection.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -F 'def _get_tax_details(' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`

### Phase 1 / Task 5 — Tax calculation method located
Research question: How does Odoo 19 calculate tax-inclusive versus tax-exclusive amounts in the shared tax engine?
Action/source: User searched for `def _get_tax_details(` in `/usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`.
Observed output: `1141:    def _get_tax_details(`.
Interpretation: The method definition is located at line 1141. Its calculation behavior is not established by this search result alone.
Uncertainty: Price-included vs price-excluded branches, special modes, actual arithmetic, and follow-on helpers have not been inspected.
Risk: Read-only source search; no database mutation indicated.
Decision: Phase 1 Task 5 remains open.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '1140,1235p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`

### Phase 1 / Task 5 — Tax inclusivity selection (partial method inspection)
Research question: How does `_get_tax_details()` determine whether tax is price-included, price-excluded, or overridden by a special computation mode?
Action/source: User supplied output of `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '1140,1235p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`.
Observation: `_get_tax_details()` accepts price, quantity, precision, rounding method, product/UoM, `special_mode`, manual amounts and optional filter. `prepare_tax_extra_data()` sets `price_include=False` for taxes with `has_negative_factor`, `True` for `special_mode='total_included'`, `False` for `special_mode='total_excluded'`, otherwise uses `tax.price_include`. `add_tax_amount_to_results()` applies `float_round` to individual tax amounts when rounding is `round_per_line`. Tax batches are flattened/ordered by `_batch_for_taxes_computation`. The excerpt stops before the final tax/base computations.
Interpretation: The source confirms explicit overrides for inclusion/exclusion, a reverse-charge-related precedence for negative-factor taxes, and per-line rounding of tax amounts. The arithmetic of the full method and special-mode behavior beyond classification remain unverified.
Uncertainty: Subsequent calculation branches, total construction, and runtime behavior; full method extends beyond inspected excerpt.
Risk: Read-only source inspection; no database changes.
Decision: Keep Phase 1 Task 5 open; continue inspecting the same method, avoiding a premature completion claim.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '1230,1325p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`

### Phase 1 / Task 5 — Tax computation order and totals (continuation)
Research question: How does `_get_tax_details()` evaluate price-included/excluded taxes and construct totals?
Action/source: User provided output from `sed -n '1230,1325p'` of `/usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`.
Observation: Starts with `raw_base = quantity * price_unit`; rounds raw base for `round_per_line`. Evaluates fixed tax amounts first (reverse order), then included tax amounts (reverse order), then excluded tax amounts (forward order). Computes tax base with propagated extras; for included taxes under normal or `total_included` mode subtracts tax amounts from base. Considers included-base dependencies and reverse-charge data. With applicable tax data, sets `total_excluded` to first tax base, sums tax amounts, and sets `total_included = total_excluded + tax_amount`. Without tax data, both totals equal raw base. The pasted excerpt ends partway through the returned dictionary.
Interpretation: The evaluation order and aggregate calculation are verified directly from source. Tax computation is not a universal single-rate multiplication and can depend on tax ordering, inclusion mode, base-affecting taxes and reverse charges.
Uncertainty: Final returned dictionary fields, helper function behavior and controlled runtime examples remain unverified; do not claim entire tax machinery validated.
Risk: Read-only source inspection; no database change indicated.
Decision: Task 5 source review substantially advanced; leave open until method ending and final evidence review.
Next command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '1310,1345p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`

### Phase 1 / Task 5 — `_get_tax_details()` return structure inspected (method end)
Research question: What does Odoo's tax calculation return after computing inclusive/exclusive totals?
Action/source: User supplied the output of `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '1310,1345p' /usr/lib/python3/dist-packages/odoo/addons/account/models/account_tax.py`.
Observation: For tax entries, method uses the first tax data base as `total_excluded`, sums `tax_amount`, and calculates `total_included = total_excluded + tax_amount`. Without entries both totals equal `raw_base`. Returned dictionary contains `total_excluded`, `total_included`, and `taxes_data` entries with tax, taxes, group, batch, tax_amount, price_include, base_amount, and is_reverse_charge. The method then ends before the `MAPPING PRICE_UNIT` section.
Interpretation: We have inspected this method's return structure and source-level included/excluded calculation order. This is not runtime validation of all tax configurations.
Uncertainty: Results for concrete tax configurations, rounding combinations and edge cases remain to be tested during controlled transactions. Some invoked helpers have not been independently examined.
Risk: Read-only source inspection, no database modification.
Decision: Task 5 source-code inspection can be considered complete, subject to later controlled verification. Do not claim the complete Odoo tax engine was experimentally validated. Next: consolidate Phase 1 findings and distinguish source-level verified items from runtime-open items instead of recursive searches.
Next action: Phase 1 evidence review of Tasks 1-6; record unresolved test cases for later isolated experiments.


## Phase 1 — Consolidated evidence review and transition (2026-11-02)

Research question: What accounting-calculation behavior is supported by the inspected installed Odoo 19 source, and what remains untested?

Evidence/source: User-pasted installed-source excerpts and the Git Bash commands already recorded above. No live Odoo transactions were generated during this phase.

Checklist sign-off **for source inspection only** (not runtime behavior):
- [x] 1. Inspect `account.move.line._compute_totals()` and the reachable tax-base preparation path. It delegates subtotal/total computation to `account.tax` helpers and uses rounded currency-denominated results.
- [x] 2. Trace tax-base preparation and subtotals. Purchase and invoice lines prepare base-line dictionaries; tax engine uses prices, quantities, discounts, tax settings and currencies; tax calculation returns tax-exclusive and tax-inclusive results.
- [x] 3. Compare purchase-order and bill-side discounts. Both expose price and discount fields. `_prepare_account_move_line()` transfers the PO discount and converts the unit price with `round=False`; `purchase_stock` can supply a balance. Later edits and runtime invariants not tested.
- [x] 4. Inspect currency, UoM and rounding source paths. `_compute_price` uses target/source factors without explicit rounding; `_compute_quantity` uses source/target factors and may round using destination precision; `res.currency._convert` applies `_get_conversion_rate` and optional destination-currency rounding. `_get_rates` selects dated rates with fallback. Tax rounding distributes aggregate deltas according to weighted factors.
- [x] 5. Inspect inclusive/exclusive tax calculations. `_get_tax_details` handles included/excluded modes, evaluates fixed tax first, included taxes in reverse order and excluded in forward order; returns `total_excluded`, `total_included`, and `taxes_data`.
- [x] 6. Consolidate evidence, method locations and unresolved questions (this entry).

Interpretation: We have sufficient **source-level** understanding of the scoped calculation path to stop recursive source tracing and advance to lifecycle analysis. This is **not** verification that real vendor bills, exchange-rate edge cases, and all tax combinations behave correctly.

Uncertainty / deferred experiments: Controlled runtime cases must cover posted vs draft bills, price-included/mixed taxes, global vs per-line rounding, supplier discounts, negative/refund quantities, multi-currency/missing historical rates, mismatched UoMs, and edited bill lines. Record as Phase 7 tests (and related Phase 2/3/4 dependencies) rather than silently signing them off.

Risk: Research commands to date were read-only; experimental tests must use an isolated environment and verified backups. No database changes reported from this phase.

Decision: **Phase 1 source-inspection checklist = 6/6. Overall application research not complete. Proceed to Phase 2: transaction lifecycle.** No claim of experimentally validated accounting calculations.

Next research question (Phase 2, task 1): Where does Odoo 19 define the purchase-order confirmation and cancellation transitions, and what are their entry points?

Next Git Bash command (read-only):
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -R -n -E '^    def (button_confirm|button_approve|button_cancel|action_cancel)\(' \
  /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py
```
Observation: Pending user command output. Do not assume definitions exist in both files.

## Phase 2 — Step 2.1 method locations (2026-11-02)
Research question: Where are purchase-order approval, confirmation, and cancellation entry points defined?
Command: `MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -R -n -E '^    def (button_confirm|button_approve|button_cancel|action_cancel)\(' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py`
Observed output (user-provided):
- `purchase/models/purchase_order.py:615` `button_approve(force=False)`
- `purchase/models/purchase_order.py:625` `button_confirm()`
- `purchase/models/purchase_order.py:641` `button_cancel()`
- `purchase_stock/models/purchase_order.py:179` `button_approve(force=False)`
- `purchase_stock/models/purchase_order.py:188` `button_cancel()`
Interpretation: The base purchase module defines all three entry points; purchase_stock defines additional approval and cancellation methods. Their behavior and inheritance have NOT been inspected.
Uncertainty: State transitions, approvals, effects on stock pickings, cancellation constraints and methods beyond the search pattern.
Risk: Read-only grep. No DB operations.
Decision: Continue Phase 2, task 1; method-location discovery complete, behavior unverified.
Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sh -c "sed -n '605,670p' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py; sed -n '170,215p' /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py"
```

## Supplemental Phase 1 evidence — tax rounding and accounting repartition (2026-11-02)

Research question: How does Odoo 19 round tax details and convert computed tax amounts into accounting repartition data?

Source: User-provided continuation from the installed Odoo 19 `account_tax.py`, covering `_round_base_lines_tax_details` and `_add_accounting_data_to_base_line_tax_details` around lines 2189 onward. Read-only source evidence; no runtime transaction was executed.

Observed:
- `_round_base_lines_tax_details` rounds raw `total_excluded` and each raw base/tax amount separately in the line currency and company currency.
- `manual_tax_amounts` can replace total-excluded, base, and tax amounts. When a foreign-currency rate is available, the corresponding company-currency amount is recalculated from the manual foreign amount.
- `total_included` is rebuilt from the rounded total-excluded amount plus rounded tax amounts, and each line starts with zero `delta_total_excluded`.
- The method then delegates tax-amount rounding, base-line rounding, and optional existing-tax-line reconciliation to `_round_tax_details_tax_amounts`, `_round_tax_details_base_lines`, and `_round_tax_details_tax_amounts_from_tax_lines`.
- `_add_accounting_data_to_base_line_tax_details` selects invoice or refund repartition lines. Reverse-charge data selects negative-factor tax repartition lines and applies a negative sign; ordinary tax data selects non-negative factors.
- Each repartition amount is rounded in both the transaction currency and company currency. If `compute_all_use_raw_base_lines` is set, the raw tax amount is used for the transaction-currency calculation.
- The supplied continuation sorts repartition targets by absolute tax amounts and distributes residual deltas through `_distribute_delta_amount_smoothly`. It also prepares accounts, tax tags, subsequent-tax data, and grouping keys for tax-line generation.

Interpretation: Odoo's accounting result is reconciled across currencies, tax lines, and repartition lines. Global rounding can move a small residual to a selected line or repartition target so aggregate totals remain consistent. Manual tax amounts and existing tax lines are explicit inputs to this reconciliation path. This strengthens the source-level rounding findings; it does not constitute runtime validation.

Uncertainty: The helper implementations and behavior under concrete multi-line, multi-currency, manual-tax, and reverse-charge transactions remain untested. The exact residual target should be verified with controlled fixtures in Phase 7.

Risk: Read-only source inspection; no database or container changes.

Decision: Treat this as supplemental evidence for Phase 1 Tasks 4–5. Keep the Phase 1 source-inspection sign-off at 6/6 and preserve the distinction between source evidence and runtime validation. Continue Phase 2 transaction-lifecycle research.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sh -c "sed -n '605,670p' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py; sed -n '170,215p' /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py"
```

## Phase 2 — Step 2.2 purchase-order lifecycle behavior (2026-11-02)

Research question: What state transitions, approval guards, invoice guards, and stock-side effects are implemented by the purchase-order confirmation, approval, and cancellation entry points?

Source: User-provided output from:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sh -c "sed -n '605,670p' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py; sed -n '170,215p' /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py"
```

Observed in `purchase/models/purchase_order.py`:
- `button_approve(force=False)` filters orders through `_approval_allowed()`, writes `state='purchase'` and the current approval datetime, locks orders whose `lock_confirmed_po` is `'lock'`, and returns an empty dictionary.
- `button_confirm()` processes only `draft` and `sent` orders. It checks `_confirmation_error_message()`, validates analytic distributions, adds the supplier to the product, and either calls `button_approve()` or sets the order to `to approve` when double validation is required.
- `_confirmation_error_message()` rejects non-display, non-downpayment lines without a product.
- `button_cancel()` blocks locked orders and orders with related vendor bills whose state is neither `cancel` nor `draft`; otherwise it writes `state='cancel'`.
- `button_draft()` resets the order state to `draft`; `button_lock()` and `button_unlock()` change the lock flag.

Observed in `purchase_stock/models/purchase_order.py`:
- The stock override of `button_approve()` calls the base implementation and then `_create_picking()`.
- `_prepare_grouped_data()` adds `picking_type_id` to the grouping fields.
- The stock override of `button_cancel()` begins by collecting relevant order lines and non-final pickings. It leaves done pickings untouched, posts a cancellation note on them, gathers non-done stock moves for cancellation, and begins handling destination moves and purchase-line relationships. The supplied excerpt ends before the method completes.

Interpretation: Confirmation is a guarded transition from `draft`/`sent` either to `purchase` or `to approve`. Approval records the approval time and may lock the order. In the stock extension, approval also creates incoming picking records. Cancellation has accounting and lock safeguards in the base module, while the stock extension performs additional move and picking coordination before the final purchase-order state transition is established.

Uncertainty: The remainder of `purchase_stock.button_cancel()`, the exact `_approval_allowed()` rules, `_create_picking()` behavior, and runtime effects on pickings and moves remain unverified. No transaction test has been run.

Risk: Read-only source inspection; no database or container changes.

Decision: Mark Phase 2 method-location and partial behavior inspection as complete for the supplied ranges. Do not mark the full lifecycle task complete until the stock cancellation method and approval dependencies are inspected.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '205,275p' \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py
```

## Phase 2 — Step 2.3 stock cancellation completion (2026-11-02)

Research question: How does `purchase_stock.purchase.order.button_cancel()` finish cancellation of linked stock moves and pickings?

Source: User-provided continuation from `purchase_stock/models/purchase_order.py`, following the previously inspected `button_cancel()` excerpt.

Observed:
- For each relevant order line, non-done source moves are added to `moves_to_cancel_ids`.
- Destination moves that are non-done and do not end in inventory are split into recomputation and cancellation paths based on their route.
- If a destination move has more than one originating purchase line, the current purchase-line relation is unlinked before further action.
- With `propagate_cancel`, remaining destination moves are added to the cancellation set. Without it, they are added to the recomputation set.
- Cancellation candidates are browsed as `stock.move` records and cancelled through `_action_cancel()`.
- Recomputed moves receive `procure_method='make_to_stock'` and then `_recompute_state()`.
- Open linked pickings are cancelled with `action_cancel()`; done pickings were preserved and logged in the preceding excerpt.
- The method calls `super().button_cancel()` only after the stock moves and pickings have been processed.

Interpretation: Purchase cancellation propagates through the stock graph. It cancels eligible moves and pickings, detaches shared purchase-line links when needed, and converts selected downstream moves to make-to-stock when cancellation should not propagate. The source order places stock-side actions before the base method's lock and vendor-bill guards execute through `super()`.

Uncertainty: Runtime transaction rollback behavior if the later base guard raises, exact route conditions, effects on shared moves, and behavior for done or partially processed receipts remain untested. No live cancellation was performed.

Risk: Source inspection only. The ordering of stock mutations before the base cancellation call is a lifecycle risk to verify in an isolated transaction test; do not infer data loss from source order alone because transaction handling was not tested.

Decision: Phase 2 purchase-order cancellation source path is complete for the inspected methods. Keep runtime lifecycle validation open. Continue with approval dependencies and stock picking creation.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -R -n -E '^    def (_approval_allowed|_create_picking)\\(' \
  /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py
```

## Phase 2 — Step 2.4 approval and picking method locations (2026-11-02)

Research question: Where are the purchase approval gate and stock receipt creation methods defined?

Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -R -n -E '^    def (_approval_allowed|_create_picking)\\(' \
  /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py
```

Observed output:
- `purchase/models/purchase_order.py:1251: def _approval_allowed(self)`
- `purchase_stock/models/purchase_order.py:377: def _create_picking(self)`

Interpretation: The approval decision is implemented in the base purchase module, while stock receipt creation is implemented in the `purchase_stock` extension. Locations alone do not establish their conditions or side effects.

Uncertainty: Approval thresholds, user/company configuration dependencies, picking grouping, move creation, duplicate-picking safeguards, and error handling remain uninspected.

Risk: Read-only method-location search; no database or container changes.

Decision: Method-location discovery complete. Keep Phase 2 lifecycle research open until both bodies are inspected.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sh -c "sed -n '1238,1265p' /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py; sed -n '360,435p' /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py"
```

## Phase 2 — Step 2.5 approval threshold and receipt creation (2026-11-02)

Research question: What conditions permit direct purchase approval, and how does `purchase_stock` create or reuse receipts after approval?

Source: User-provided output from `purchase/models/purchase_order.py` and `purchase_stock/models/purchase_order.py`, including `_approval_allowed()`, `_prepare_picking()`, and `_create_picking()`.

Observed:
- `_approval_allowed()` permits direct approval when the company uses `one_step` validation.
- Under `two_step` validation, it permits direct approval when `amount_total` is strictly less than the converted company threshold. The threshold is converted using the order currency, company, and order date (or today when no order date is present).
- A user in `purchase.group_purchase_manager` bypasses the threshold condition.
- `_prepare_picking()` creates missing reference records, requires the vendor's supplier stock location, and prepares a draft receipt with picking type, vendor, source and destination locations, company, origin, and references.
- `_create_picking()` processes only orders in `purchase` state and only when at least one order-line product has type `consu`.
- It reuses an existing open receipt when available; otherwise it creates a receipt with `SUPERUSER_ID`.
- It creates stock moves from purchase lines, excludes done/cancelled moves, assigns the vendor to negative-quantity moves, confirms and sequences moves, and calls `_action_assign()`.
- Forward pickings affected by push rules are retrieved and confirmed together with the current picking.
- A newly created receipt with no moves is deleted. A source message linking the receipt to the purchase order is posted when the receipt still exists.

Interpretation: Two-step approval is controlled by a strict amount comparison, with a manager override. Approval triggers receipt preparation only after the order reaches `purchase`; receipt creation is idempotent for open pickings and integrates move confirmation, reservation, push-rule propagation, and cleanup of empty receipts.

Uncertainty: The exact meaning of the `consu` product-type filter in this Odoo build, cross-company currency context behavior, destination-location selection, stock-move preparation, reservation outcomes, and duplicate or partial receipt cases remain untested.

Risk: Read-only source inspection; no database or transaction changes. The strict `<` threshold and currency conversion context should be covered by controlled boundary tests.

Decision: Source inspection of approval and primary receipt creation is complete for the supplied methods. Continue tracing `_get_destination_location()`, `_prepare_reference_vals()`, and `purchase.order.line._create_stock_moves()` before closing the lifecycle source review.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -R -n -E '^    def (_get_destination_location|_prepare_reference_vals|_create_stock_moves)\\(' \
  /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order_line.py \
  /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order_line.py
```

## Phase 2 — Step 2.6 receipt dependency locations (2026-11-02)

Research question: Where are receipt destination selection, receipt reference preparation, and purchase-line stock-move creation implemented?

Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -R -n -E '^    def (_get_destination_location|_prepare_reference_vals|_create_stock_moves)\\(' \
  /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order_line.py \
  /usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order_line.py
```

Observed output:
- `purchase_stock/models/purchase_order.py:327: def _get_destination_location(self)`
- `purchase_stock/models/purchase_order.py:354: def _prepare_reference_vals(self)`
- `purchase_stock/models/purchase_order_line.py:364: def _create_stock_moves(self, picking)`

Interpretation: The stock extension owns destination-location and reference preparation at purchase-order level, while purchase-line stock-move creation is implemented in `purchase_stock`.

Uncertainty: Warehouse and route precedence, reference fields, move quantities and dates, UoM conversion, source links, and cancellation propagation are not established by location search alone.

Risk: Read-only method-location search; no database or container changes.

Decision: Location discovery complete. Keep Phase 2 lifecycle research open until the three method bodies are inspected.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sh -c "sed -n '315,375p' /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py; sed -n '350,435p' /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order_line.py"
```

## Phase 2 — Step 2.7 receipt destinations and purchase-line move handoff (2026-11-02)

Research question: How are receipt destinations and references selected, and how do purchase lines become stock moves?

Source: User-provided output from `purchase_stock/models/purchase_order.py` and `purchase_stock/models/purchase_order_line.py`.

Observed:
- `_get_destination_location()` uses the destination partner's customer stock location for dropshipping when `dest_address_id` is set; otherwise it uses the picking type's default destination location.
- `_get_final_location_record()` uses the dropship customer location for dropshipping. For ordinary receipts, it prefers the picking type's default destination when that location is within the warehouse stock hierarchy; otherwise it falls back to the warehouse stock location.
- `_get_picking_type(company_id)` searches for an incoming picking type for the company's warehouse, then a company-independent incoming type, then an inactive company-independent incoming type, and returns the first result.
- `_prepare_reference_vals()` creates a reference whose name is the purchase-order name.
- `_create_stock_moves(picking)` ignores display-only purchase lines, calls each remaining line's `_prepare_stock_moves(picking)`, collects the returned value dictionaries, and creates `stock.move` records in one operation.
- The supplied adjacent continuation shows move values carrying destination move links, a final location, orderpoint information, cancellation propagation, and product description or variant metadata.
- The adjacent `_find_candidate()` logic can merge or match purchase lines using cancellation-propagation settings, orderpoint conditions, forced UoM, and partner-language product descriptions.

Interpretation: Receipt routing is configuration-driven and supports dropshipping separately from warehouse receipts. Purchase-line stock-move creation is a two-stage process: `_create_stock_moves()` filters and persists moves, while `_prepare_stock_moves()` supplies the actual quantities, dates, UoMs, routes, and links. Those numerical and scheduling inputs remain to be inspected.

Uncertainty: The complete `_prepare_stock_moves()` implementation, source-location selection, quantity and UoM conversion, planned-date calculation, and route propagation are not yet verified. The adjacent candidate-merging logic was only partially inspected.

Risk: Read-only source inspection; no database or transaction changes.

Decision: Destination and move-creation handoff are source-inspected. Keep the lifecycle review open until `_prepare_stock_moves()` is traced.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -n -E '^    def _prepare_stock_moves|^    def _prepare_stock_move_values' \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order_line.py
```

## Phase 2 — Step 2.8 stock-move preparation location (2026-11-02)

Research question: Where does Odoo 19 prepare the stock-move value dictionaries for purchase-order lines?

Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -n -E '^    def _prepare_stock_moves|^    def _prepare_stock_move_values' \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order_line.py
```

Observed output:
- `purchase_stock/models/purchase_order_line.py:206: def _prepare_stock_moves(self, picking)`

Interpretation: Purchase-line stock-move value preparation is implemented in the stock extension at line 206. The location search does not establish its field values or filtering behavior.

Uncertainty: Move quantity, UoM, planned date, source and destination locations, procurement links, cancellation propagation, and product tracking values remain uninspected.

Risk: Read-only method-location search; no database or container changes.

Decision: Keep Phase 2 receipt and procurement research open until `_prepare_stock_moves()` is inspected.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '190,315p' \
  /usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order_line.py
```

## Phase 2 — Step 2.9 purchase-line stock-move preparation (2026-11-02)

Research question: How does Odoo 19 calculate procurement quantity, split downstream demand, price, and prepare stock-move values for a purchase line?

Source: User-provided output from `purchase_stock/models/purchase_order_line.py`, including `_prepare_stock_moves()`, `_get_stock_move_price_unit()`, `_get_qty_procurement()`, `_check_orderpoint_picking_type()`, and `_prepare_stock_move_vals()`.

Observed:
- `_prepare_stock_moves()` accepts only `consu` products and returns no moves for other product types.
- It starts from the discounted purchase price and the procurement quantity already represented by related incoming and outgoing moves.
- Destination moves are taken from `move_dest_ids` or, when absent, from `move_ids.move_dest_ids`; cancelled moves and purchase-return moves are excluded.
- The ordered quantity is compared with the initial demand of destination moves after conversion from the product UoM to the purchase-line UoM.
- When downstream demand exists, one move is created for the quantity that can be attached to those destinations. Any remaining quantity becomes an extra move with `move_dest_ids=False`.
- `_get_stock_move_price_unit()` starts from `price_unit_discounted`. When taxes exist, it calls `tax_ids.compute_all()` with `rounding_method='round_globally'`, uses the returned `total_void` value, divides by quantity, converts between purchase-line and product UoMs, converts foreign currency without immediate rounding, and finally applies Product Price precision.
- `_get_qty_procurement()` adds non-return incoming quantities and subtracts outgoing quantities. Done moves use `quantity`; other moves use `product_uom_qty`. Both are converted with `HALF-UP` rounding.
- `_check_orderpoint_picking_type()` raises a `UserError` when the reordering-rule destination is outside the warehouse hierarchy of the purchase operation type.
- `_prepare_stock_move_vals()` sets product, planned and deadline dates, supplier source location, computed destination and final location, picking, partner, linked destination moves, purchase line, company, price, operation type, references, origin, cancellation propagation, warehouse, quantity, UoM, and sequence.
- When the final location is a child of the default destination, it replaces the immediate destination with that final location.

Interpretation: Purchase receipt generation is quantity-aware and graph-aware. Odoo accounts for already-procured quantities, downstream demand, returns, UoM conversion, taxes, currency conversion, warehouse hierarchy, and cancellation propagation before creating stock moves. A single purchase line can produce an attached move and a separate unlinked remainder move.

Uncertainty: The exact structure and semantics of the `compute_all()` result field `total_void`, the runtime effect of global tax rounding on move prices, stock reservation behavior after `_action_confirm()` and `_action_assign()`, and boundary cases involving negative or over-received quantities remain untested.

Risk: Read-only source inspection; no database or transaction changes. Quantity splitting, tax price conversion, and warehouse consistency require controlled runtime cases.

Decision: Purchase-side receipt and stock-move preparation source path is complete for the inspected methods. Continue Phase 2 by tracing the stock move confirmation, assignment, and cancellation methods called by this path.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -n -E '^    def (_action_confirm|_action_assign|_action_cancel)\\(' \
  /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py
```

## Phase 2 — Step 2.10 stock-move lifecycle method locations (2026-11-02)

Research question: Where are stock-move confirmation, reservation assignment, and cancellation implemented in Odoo 19?

Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -n -E '^    def (_action_confirm|_action_assign|_action_cancel)\\(' \
  /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py
```

Observed output:
- `stock/models/stock_move.py:1691: def _action_confirm(self, merge=True, merge_into=False, create_proc=True)`
- `stock/models/stock_move.py:2053: def _action_assign(self, force_qty=False)`
- `stock/models/stock_move.py:2192: def _action_cancel(self)`

Interpretation: The stock extension contains the three lifecycle methods called by purchase receipt generation and cancellation. The location search does not establish their state transitions, procurement effects, reservation rules, or cancellation constraints.

Uncertainty: Merge behavior, procurement creation, route propagation, reservation allocation, partial availability, chained moves, and cancellation side effects remain uninspected.

Risk: Read-only method-location search; no database or transaction changes.

Decision: Method-location discovery complete. Keep Phase 2 open until the three stock-move method bodies are inspected.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sh -c "sed -n '1680,1785p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py; sed -n '2040,2145p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py; sed -n '2180,2245p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py"
```

## Phase 2 — Step 2.11 stock-move confirmation, assignment, and cancellation (2026-11-02)

Research question: How do stock moves transition through confirmation, reservation assignment, and cancellation?

Source: User-provided attachment `Pasted text(20261102-191222).txt`, containing excerpts from `stock/models/stock_move.py` around `_action_confirm()`, `_action_assign()`, and `_action_cancel()`.

Observed in `_action_confirm()`:
- Draft moves with origins become `waiting`; `make_to_order` moves also become waiting and can create procurement requests; `mts_else_mto` moves are confirmed and can create procurement requests; other draft moves become `confirmed`.
- Procurement requests are prepared from move quantities, values, origins, products, UoMs, locations, rules, and companies, then passed to `stock.rule.run()`.
- Confirmed and waiting moves receive state updates, reservation dates when the picking type reserves at confirmation, and picking assignment in batches by references and locations.
- Moves are company-checked and optionally merged.
- Negative-quantity moves can create push moves, be transformed into return-like moves by swapping locations and negating quantity, adopt a return picking type, and switch to `make_to_stock`.
- Moves eligible for immediate or reservation-bypassing assignment call `_action_assign()`. Newly created push moves are confirmed recursively.

Observed in `_action_assign()`:
- The method compares requested quantities with current reserved availability using product-UoM precision and `HALF-UP` conversion.
- Reservation-bypassing moves create or update move lines without changing quants. Serial-tracked products can receive one move line per unit.
- Ordinary moves reserve available quants through `_update_reserved_quantity()` unless they are make-to-order moves that still await origins.
- It collects assigned and partially available moves, creates move lines, updates states to `assigned` or `partially_available`, checks entire-pack constraints, and applies putaway strategies.

Observed in `_action_cancel()`:
- A done move whose destination is not inventory cannot be cancelled; Odoo raises a `UserError` directing the user to create a return.
- Non-cancelled moves are unreserved, set to `cancel`, and their cancellation can propagate through destination and origin move chains according to `propagate_cancel` and the `stock.cancel_moves_origin` configuration parameter.
- When all relevant sibling moves are cancelled or completed, destination moves may be converted to `make_to_stock` and detached from the cancelled origin.
- Cancellation activity is logged unless `skip_cancel_activity` is set. Final cleanup clears origin links and sets the procurement method to `make_to_stock`.

Evidence boundary and formatting issue:
- The attachment begins with the tail of a preceding helper before `_action_confirm()` and includes another preceding-helper tail immediately before `_action_assign()`. Those lines were not attributed to the lifecycle methods.
- The pasted `_action_assign()` excerpt shows an indentation anomaly around a `break` near the full-reservation branch. The exact source control flow for that small range must be re-read before treating the assignment method as fully verified.

Interpretation: Stock confirmation converts draft moves into confirmed or waiting states and may launch procurement; assignment creates reservations or move lines and records availability; cancellation unreserves and propagates through the move graph with return protection for completed physical moves.

Uncertainty: Exact `_action_assign()` control flow around the malformed excerpt, full procurement behavior inside `stock.rule.run()`, merge effects, and runtime state transitions remain untested.

Risk: Source inspection only; no database or transaction changes. The assignment branch and procurement dispatcher require focused follow-up before runtime test design.

Decision: Mark `_action_confirm()` and `_action_cancel()` source behavior substantially inspected. Keep `_action_assign()` partially open because the supplied excerpt has a formatting/control-flow ambiguity. Continue with an exact narrow source read, then inspect `stock.rule.run()`.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sh -c "nl -ba /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py | sed -n '2095,2135p'; sed -n '2130,2145p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py"
```

## Phase 2 — Step 2.12 assignment branch clarified (2026-11-02)

Research question: Does the exact `_action_assign()` excerpt confirm the control flow around bypass reservation and ordinary quant reservation?

Source: User-provided numbered excerpt from `stock/models/stock_move.py`, lines 2095–2135 and continuation beginning at the ordinary-reservation branch.

Observed:
- In the reservation-bypass path, available move-line quantities are consumed until the missing quantity reaches zero; the `break` is correctly nested inside that loop.
- Serial-tracked products create one move line per unit when the picking type permits lot creation or reuse.
- For other products, Odoo updates the first compatible unpicked move line when one exists; otherwise it prepares a new move line. Compatibility includes product UoM, source and destination locations, picking, and absence of lot, package, result-package, and owner values.
- A bypass-reservation move is then marked assigned and scheduled for putaway redirection.
- In the ordinary path, zero-quantity moves are assigned immediately unless forced; make-to-order moves with no origins remain unassigned; otherwise Odoo calculates the needed quantity and calls `_update_reserved_quantity()` with non-strict location matching.
- If no quantity is taken, the move is left for later processing. When the taken quantity equals the need, the move is added to the assigned set. The excerpt ends before the partial-availability branch and final state writes.

Correction: The prior concern about malformed indentation was caused by the pasted excerpt boundary. The narrow numbered lines show valid control flow for the inspected range.

Interpretation: Assignment distinguishes reservation-bypassing flows from quant-reserving flows. It creates or updates move lines in the first path and reserves available quants in the second path, with explicit handling for serial tracking and make-to-order dependencies.

Uncertainty: The remainder after the full-reservation comparison, including partial-availability classification, move-line creation and final state writes, still requires exact inspection. No runtime reservation test has been run.

Risk: Read-only source inspection; no database or transaction changes.

Decision: Close the formatting ambiguity for lines 2095–2135. Keep `_action_assign()` open only for the remaining branch and method epilogue.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sh -c "nl -ba /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py | sed -n '2130,2165p'; sed -n '2160,2185p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py"
```

## Phase 2 — Step 2.13 partial and chained reservation logic (2026-11-02)

Research question: How does `_action_assign()` classify partial availability and reserve quantities for chained moves?

Source: User-provided numbered excerpt from `stock/models/stock_move.py`, lines 2130–2165 and continuation.

Observed:
- For a move without origins, `_update_reserved_quantity()` is called for the missing amount. A full reservation adds the move to `assigned_moves_ids`; a smaller positive reservation adds it to `partially_available_moves_ids`; zero reservation leaves it for later processing.
- For a move with origins, Odoo obtains available move-line quantities from parent and sibling moves. It converts and distributes those quantities through `_update_reserved_quantity_vals()` using strict locations and tracks the quantities taken for each location, lot, package, and owner combination.
- Newly prepared move lines are created in a batch. The method then checks the quantities actually taken from quants; a full remaining reservation marks the move assigned, while an incomplete reservation marks it partially available.
- Serial-tracked moves update `next_serial_count` to the requested move quantity.
- The excerpt reaches the final creation of accumulated move lines, but the subsequent state writes and putaway processing are not included in this submission.

Interpretation: Odoo distinguishes direct reservation from chained-demand distribution. A move can become fully assigned, partially available, or remain unassigned based on actual quant availability and quantities supplied by preceding moves.

Uncertainty: The final state-write epilogue, entire-pack validation, putaway application, and runtime behavior with concurrent reservations remain unverified.

Risk: Read-only source inspection; no database or transaction changes.

Decision: The partial and chained reservation branches are verified from source. Keep `_action_assign()` open only for its epilogue, then close the stock-move lifecycle source review.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sh -c "nl -ba /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py | sed -n '2160,2195p'"
```

## Phase 2 — Step 2.14 stock-move assignment epilogue (2026-11-02)

Research question: What final state and post-processing actions complete `_action_assign()`?

Source: User-provided numbered excerpt from `stock/models/stock_move.py`, lines 2160–2195.

Observed:
- Chained reservation move lines are created in batches through `stock.move.line.create()`.
- Accumulated bypass-reservation move lines are also created in one batch after the assignment loop.
- Moves in `partially_available_moves_ids` are written with `state='partially_available'`.
- Moves in `assigned_moves_ids` are written with `state='assigned'`.
- Unless the context contains `bypass_entire_pack`, the method calls `self.picking_id._check_entire_pack()`.
- Move lines belonging to redirected moves receive putaway processing through `_apply_putaway_strategy()`.
- `_action_cancel()` follows immediately after the assignment epilogue in the source.

Interpretation: `_action_assign()` completes reservation by persisting move lines, classifying moves by availability, validating entire-pack constraints, and applying putaway rules after reservation.

Uncertainty: Runtime reservation results, quant concurrency, and the effects of entire-pack and putaway rules remain untested.

Risk: Read-only source inspection; no database or transaction changes.

Decision: Source inspection of the purchase-to-stock move lifecycle methods is complete for the inspected path: purchase confirmation, picking creation, stock-move confirmation, assignment, and cancellation. Runtime transaction validation remains deferred. Continue by tracing the procurement dispatcher invoked by make-to-order confirmation.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -R -n -E '^    def run\\(' \
  /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_rule.py \
  /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py
```

## GitHub synchronization checkpoint (2026-11-02)

The complete temporary notebook, including all preceding evidence and this entry, is being preserved in the `DavidSamah/odoo-19-database-research` repository so future research details can be appended to the same tracked artifact.

## Phase 2 — Step 2.15 procurement dispatcher location (2026-11-02)

Research question: Where is the procurement dispatcher called by stock-move confirmation implemented?

Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  grep -R -n -E '^    def run\\(' \
  /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_rule.py \
  /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py
```

Observed output:
- `stock/models/stock_rule.py:453: def run(self, procurements, raise_user_error=True)`

Interpretation: The procurement dispatcher invoked by `_action_confirm()` is implemented in `stock.rule` at line 453. The location result does not establish rule selection, grouping, error handling, or downstream move creation.

Uncertainty: Procurement grouping, route and warehouse rule selection, error behavior, and recursion into stock moves remain uninspected.

Risk: Read-only method-location search; no database or transaction changes.

Decision: Method-location discovery complete. Keep the procurement branch open until `stock.rule.run()` is inspected.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app \
  sed -n '440,560p' \
  /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_rule.py
```

## Phase 2 — Step 2.16 procurement dispatch and rule selection (2026-11-02)

Research question: How does stock.rule.run() decide whether and how to fulfil procurement requests?

Source: User-provided excerpt from stock/models/stock_rule.py, including _skip_procurement(), run(), _search_rule_for_warehouses(), and the beginning of _search_rule().

Observed:
- _skip_procurement() skips procurements for products whose type is not consu or whose quantity is zero at the procurement UoM precision.
- run() defines an error handler that raises UserError when raise_user_error=True, otherwise raises ProcurementException with the procurement errors.
- For each procurement, defaults are populated for company, priority ('0'), and planned date (current datetime when absent).
- The method calls _get_rule() for each eligible procurement. If no rule is found, it records an error identifying the product and location and advising verification of product routes.
- Rules with pull_push action are dispatched as pull. Procurements are grouped by action and passed to a dynamically selected _run_<action>() method.
- ProcurementException errors from action methods are collected and raised after processing. Missing _run_<action>() methods are logged. Successful execution returns True.
- _search_rule_for_warehouses() builds valid route candidates from explicit routes, packaging routes, product and category routes, and filtered warehouse routes. It groups matching rules by destination location, route, and warehouse, ordering candidates by route and rule sequence.
- The beginning of _search_rule() shows rule precedence starting with procurement-group routes, then packaging routes, then product and category routes, with warehouse filtering applied.

Interpretation: Procurement dispatch is route-driven and action-based. Odoo validates all eligible requests for a rule before dispatching grouped actions, and it preserves procurement-specific failure information when fulfillment cannot proceed.

Uncertainty: The remaining _search_rule() fallback behavior, _get_rule() implementation, exact action handlers, and runtime behavior when some requests fail remain uninspected.

Risk: Read-only source inspection; no database or transaction changes. Route configuration and missing-rule errors require controlled tests.

Decision: The dispatcher and initial rule-selection logic are source-inspected. Keep procurement routing open until rule precedence and the pull action are traced.

Next command:
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '530,660p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_rule.py

## Phase 2 — Step 2.18 rule precedence, hierarchy fallback, and inter-company routing (2026-11-02)

Research question: How does Odoo resolve a stock rule across routes, warehouses, and location hierarchies?

Source: User-provided continuation from stock/models/stock_rule.py covering _search_rule(), _get_rule(), _check_intercomp_location(), and the beginning of _get_rule_domain().

Observed:
- _search_rule() restricts candidate rules to the requested warehouse or company-independent rules, then searches in this order: procurement-group route IDs, packaging UoM routes, product and category routes, and warehouse routes.
- Each search orders rules by route_sequence and sequence and takes the first match.
- _get_rule() returns no rule when the location is empty. Otherwise it builds the location hierarchy from the requested location to its root.
- _get_rule() builds a domain and obtains a mapping keyed by destination location and route, with warehouse-specific rule records inside each mapping.
- Route extraction prefers product routes in its sorting, then uses the exact warehouse rule and falls back to a company-independent rule. When no warehouse is supplied, the first available warehouse mapping is used.
- Rule resolution first tries the current location, then its parent locations until a valid rule is found.
- For an inter-company transit location, the customer location is added as an additional candidate once, allowing inter-company fulfillment to reuse customer-delivery rules.
- _check_intercomp_location() checks for transit locations and verifies the configured stock inter-company location.
- _get_rule_domain() begins by including the location hierarchy, adds the customer location for inter-company resolution, and excludes push rules. Its superuser company restriction continues beyond the supplied excerpt.

Interpretation: Rule resolution is deterministic and layered. Odoo gives precedence to explicit procurement routes, then packaging, product/category, and warehouse routes, while also allowing location-parent fallback. Inter-company transit uses a deliberate customer-location alias to avoid duplicating delivery rules.

Uncertainty: The remaining superuser/company domain restriction, the complete _get_rule() domain, and the _run_pull() action remain uninspected.

Risk: Read-only source inspection; no database or transaction changes. Route precedence, inter-company rules, and multi-company access require controlled tests.

Decision: Mark route precedence and location hierarchy resolution as source-inspected. Keep the procurement branch open for the remainder of _get_rule_domain() and the pull action.

Next command:
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '650,760p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_rule.py

## Phase 2 — Step 2.19 rule-domain restrictions, push fallback, and scheduler (2026-11-02)

Research question: What company restrictions, push-rule fallback, and scheduler behavior surround procurement rule resolution?

Source: User-provided continuation from stock/models/stock_rule.py covering the remainder of _get_rule_domain(), _get_push_rule(), _get_moves_to_assign_domain(), _run_scheduler_tasks(), run_scheduler(), and _get_orderpoint_domain().

Observed:
- _get_rule_domain() adds the customer location for inter-company transit resolution and excludes rules whose action is push.
- When running as superuser with a company value, the domain allows company-independent rules and rules belonging to the requested companies or their child companies.
- Route company IDs are added to the company restriction set when route_ids are present.
- _get_push_rule() searches from the current destination location upward through parent locations. It accepts push and pull_push rules, applies an optional values domain, and reuses _search_rule() for route, packaging, product, category, and warehouse precedence.
- _get_moves_to_assign_domain() selects confirmed or partially available non-zero moves for the company when their reservation date is due or their picking type reserves at confirmation.
- _run_scheduler_tasks() computes orderpoint quantities and deadlines, confirms orderpoint procurements, searches due moves ordered by reservation date, priority, planned date, and ID, and assigns them in chunks of 1000.
- Scheduler chunks are assigned with sudo()._action_assign(). When use_new_cursor is enabled, each chunk is committed and progress is reported.
- The scheduler also runs quant merge tasks.
- run_scheduler() executes scheduler tasks as superuser to avoid inter-company and access-right issues, logs exceptions, and returns an empty dictionary.
- _get_orderpoint_domain() restricts automatic orderpoints to active products and optionally a specified company.

Interpretation: Odoo separates pull-rule selection from push-rule selection and uses location-parent fallback for both. The scheduler periodically turns due confirmed moves into reservations and confirms replenishment procurements. With a new cursor, assignment progress can be committed in separate batches rather than as one transaction.

Uncertainty: The exact pull action implementation, push-rule creation effects, orderpoint procurement methods, and runtime behavior under partial scheduler failure remain untested.

Risk: Read-only source inspection; no database or transaction changes. Scheduler chunk commits and superuser execution require explicit operational and rollback testing.

Decision: Mark the rule-domain restriction, push fallback, and scheduler source paths as inspected. Continue with _run_pull() to complete the procurement-to-move workflow.

Next command:
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -E '^    def (_run_pull|_run_buy|_run_manufacture)\\(' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_rule.py

## Phase 2 — Step 2.20 pull-action method location (2026-11-02)

Research question: Where does Odoo implement the pull action that fulfils a procurement after stock-rule dispatch?

Command:
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -n -E '^    def (_run_pull|_run_buy|_run_manufacture)\\(' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_rule.py

Observed output:
- stock/models/stock_rule.py:290: def _run_pull(self, procurements)

Interpretation: The stock-rule pull action is implemented at line 290. The location result does not establish how it groups procurements, creates moves, or propagates routes.

Uncertainty: Procurement grouping, move preparation, picking assignment, chained pull rules, push-rule interaction, and error handling remain uninspected.

Risk: Read-only method-location search; no database or transaction changes.

Decision: Keep the procurement branch open until _run_pull() is inspected.

Next command:
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '280,390p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_rule.py

## Phase 2 — Step 2.21 pull action and procurement-to-move construction (2026-11-02)

Research question: How does _run_pull() convert procurement requests into confirmed stock moves?

Source: User-provided excerpt from stock/models/stock_rule.py covering _run_pull() and _get_stock_move_values().

Observed:
- _run_pull() rejects any rule without a source location by raising ProcurementException.
- Procurements are sorted by whether their quantity is positive before move values are prepared.
- The mts_else_mto rule method is converted to make_to_stock for the created move.
- Each procurement is converted through rule._get_stock_move_values() and grouped by procurement company.
- Stock moves are created with sudo() and the relevant company context, then confirmed through _action_confirm(). The method returns True.
- _get_stock_move_values() subtracts the rule delay from the planned date and optional deadline.
- The move partner comes from the rule's partner address or procurement values.
- Downstream move links are carried into move_dest_ids.
- For inter-warehouse transfers ending at the company's internal transit location, partner information can be derived from the destination warehouse and the destination move is assigned the source warehouse or company partner.
- Negative procurement quantities set values['to_refund'] = True.
- Created move values include company, product, UoM, quantity, partner, source and final locations, destination links, rule, references, procurement method, origin, picking type, serialized procurement values, routes, attributes, warehouse, dates, cancellation propagation, priority, and orderpoint.
- A rule can override the destination location through location_dest_from_rule.
- Custom move fields returned by _get_custom_move_fields() are copied from procurement values when present.
- The supplied excerpt ends at the beginning of _serialize_procurement_values().

Interpretation: The pull action turns route-selected procurements into company-batched stock moves, then re-enters the stock-move confirmation lifecycle. It preserves downstream relationships, route context, dates, returns, warehouse partners, cancellation behavior, and custom procurement data.

Uncertainty: The exact procurement-value serialization, downstream _action_confirm() recursion, inter-warehouse runtime behavior, and buy or manufacture action paths remain untested.

Risk: Read-only source inspection; no database or transaction changes. Superuser move creation and negative-quantity refund behavior require controlled tests.

Decision: Mark the pull action and stock-move value construction source path as inspected for the purchase receipt workflow. Keep procurement serialization open until the remaining helper is read.

Next command:
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '390,470p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_rule.py

## Phase 2 — Step 2.22 procurement serialization and lead-time calculation (2026-11-02)

Research question: How are procurement values stored and how are rule delays accumulated?

Source: User-provided excerpt from stock/models/stock_rule.py covering _serialize_procurement_values() and _get_lead_days().

Observed:
- _serialize_procurement_values() iterates through the procurement values dictionary.
- BaseModel values are converted to their record IDs.
- datetime.datetime and datetime.date values are converted with isoformat().
- Other values are preserved.
- The method returns a new serialized dictionary for storage in stock-move procurement_values.
- _get_lead_days() gathers delays from rules whose action is pull or pull_push and whose delay is non-zero.
- It sums rule delays into total_delay and records a description for each delaying rule unless bypass_delay_description is present.
- If bypass_global_horizon_days is set in context, the method returns before adding the global horizon.
- Otherwise it reads global horizon days from stock.warehouse.orderpoint.get_horizon_days(), adds them to horizon_time, and records a Time Horizon description unless delay descriptions are bypassed.
- The source contains a FIXME stating that multiple products are not yet supported by this method as written.
- The supplied excerpt then re-enters the previously inspected _skip_procurement() and run() methods.

Interpretation: Procurement values are made storage-safe before being embedded in stock moves, while lead time is composed from rule delays and an optional global orderpoint horizon. Context flags can suppress either descriptions or the global horizon calculation.

Uncertainty: Callers of _get_lead_days(), the effect of serialized values on later procurement recursion, and multi-product lead-time behavior remain untested.

Risk: Read-only source inspection; no database or transaction changes. Date serialization and lead-time bypass flags require controlled tests.

Decision: Mark procurement serialization and lead-time accumulation as source-inspected. The focused purchase-to-receipt source path is now complete enough for consolidation; runtime behavior remains open.

Next command:
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -R -n -E '_get_lead_days|_serialize_procurement_values' /usr/lib/python3/dist-packages/odoo/addons/stock/models


## Phase 2 — Step 2.23 caller search unavailable in current shell (2026-11-02)

Research question: Where are _get_lead_days() and _serialize_procurement_values() called in the installed stock models?

Command attempted:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -R -n -E '_get_lead_days|_serialize_procurement_values' /usr/lib/python3/dist-packages/odoo/addons/stock/models
```

Observed result:
- The current shell returned `/bin/bash: line 1: docker: command not found`.
- No caller locations were observed from this attempt.

Interpretation: The caller search could not be executed from the current environment. The previous source conclusions about serialization and lead-time behavior remain based only on the user-provided method excerpt.

Uncertainty: Call sites, call timing, and whether serialized procurement values are later deserialized remain unverified.

Risk: Environment/tooling limitation only; no application or database changes were made.

Decision: Keep caller tracing open. Do not infer runtime or call-site behavior from the missing command output.

Next action:
- Re-run the same grep from a shell with access to the Odoo application container, or inspect the mounted source tree directly if available.



## Phase 2 — Step 2.24 serialization and lead-time caller locations (2026-11-02)

Research question: Which installed stock-model methods call procurement serialization and lead-time accumulation?

Command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app grep -R -n -E '_get_lead_days|_serialize_procurement_values' /usr/lib/python3/dist-packages/odoo/addons/stock/models
```

Observed output:
- `stock_rule.py:372` stores `self._serialize_procurement_values(values)` in the stock-move value dictionary.
- `stock_rule.py:389` defines `_serialize_procurement_values()`.
- `stock_rule.py:412` defines `_get_lead_days()`.
- `product.py:743` calls `rules.with_context(bypass_delay_description=True)._get_lead_days(self)`.
- `stock_orderpoint.py:184-185` obtains orderpoint lead-day values, then calls `orderpoint.rule_ids._get_lead_days(orderpoint.product_id, **values)`.
- `stock_orderpoint.py:478` defines `_get_lead_days_values()`.
- `stock_orderpoint.py:570` calls `rules.with_context(bypass_delay_description=True)._get_lead_days(product)[0]`.
- Additional matches were compiled Python `.pyc` files; those binary matches were not treated as source evidence.

Interpretation:
- Procurement serialization is used when pull rules build stock moves, preserving procurement context in the move.
- Lead-time accumulation feeds at least two operational paths: product-level lead-time calculation and orderpoint scheduling/deadline computation.
- Both product and orderpoint calculation paths suppress human-readable delay descriptions, indicating a numeric scheduling use in those callers.
- Orderpoints pass computed values into `_get_lead_days()`, so the orderpoint path can include context-dependent horizon or delay inputs.
- This establishes callers and purpose at the location level, but not the surrounding date calculations.

Uncertainty:
- The exact use of the returned `delays` mapping in `product.py` and `stock_orderpoint.py` is not yet inspected.
- The contents of `_get_lead_days_values()`, the role of `values`, and the interaction with orderpoint deadlines remain open.
- No runtime scheduling behavior was tested.

Risk: Read-only source inspection; no database or transaction changes. Binary cache matches were excluded from interpretation.

Decision: Mark caller locations as source-inspected. Continue with the surrounding product and orderpoint methods before closing this branch.

Next command:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sed -n '720,755p;165,195p;465,490p;550,580p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/product.py /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_orderpoint.py
```



## Phase 2 — Step 2.25 surrounding lead-time callers unavailable in current shell (2026-11-03)

Research question: How do product and orderpoint methods consume the delays returned by _get_lead_days()?

Command attempted:
```bash
MSYS_NO_PATHCONV=1 docker exec odoo19-research-app sh -lc "sed -n '720,755p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/product.py; sed -n '165,195p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_orderpoint.py; sed -n '465,490p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_orderpoint.py; sed -n '550,580p' /usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_orderpoint.py"
```

Observed result:
- The current shell returned `/bin/bash: line 1: docker: command not found`.
- No surrounding method source was retrieved.

Interpretation: The exact date and deadline calculations consuming lead-time values remain unverified. The previously recorded caller locations are still valid, but no further behavior is inferred.

Uncertainty: Product lead-time field updates, orderpoint deadline computation, horizon handling, and date arithmetic remain open.

Risk: Environment/tooling limitation only; no application or database changes were made.

Decision: Keep this branch open and rerun the command from a shell with access to the Odoo application container or mounted source tree.

Next action:
- Retrieve the four source ranges from the Odoo container, then record the calculations before drawing workflow conclusions.

