# ProofFlow / Odoo 19 — Purchase-to-Receipt Workflow

Status: source-level workflow reconstruction from the installed Odoo 19 code supplied during the research session.
Repository: DavidSamah/odoo-19-database-research
Detailed evidence record: ProofFlow_Odoo19_Temporary_Research_Notebook.md

## Evidence boundary

This document describes behavior verified from source excerpts. It does not claim that every branch has been validated with live Odoo transactions. Runtime validation remains required for multi-company, tax, currency, reservation, return, cancellation, and partial-receipt cases.

## Workflow map

1. Purchase order confirmation
2. Approval decision
3. Receipt preparation or reuse
4. Purchase-line stock-move preparation
5. Stock-move confirmation
6. Procurement dispatch when required
7. Reservation and assignment
8. Receipt and move cancellation
9. Accounting and tax linkage

## 1. Purchase order confirmation

Source: purchase/models/purchase_order.py.

- button_confirm() processes only orders in draft or sent state.
- _confirmation_error_message() rejects non-display, non-downpayment lines without a product.
- Analytic distributions are validated.
- Supplier information is added to the product.
- If _approval_allowed() is true, button_approve() is called.
- Otherwise, the order is written to to approve.

## 2. Approval decision

Source: purchase/models/purchase_order.py.

_approval_allowed() permits direct approval when:

- the company uses one_step validation;
- two_step validation is enabled and amount_total is strictly less than the converted company threshold; or
- the current user belongs to purchase.group_purchase_manager.

The threshold conversion uses the order currency, company, and order date or the current date. The strict less-than comparison requires a boundary test for orders exactly equal to the configured amount.

button_approve() then:

- filters through _approval_allowed();
- writes state = purchase;
- records date_approve;
- locks orders configured with lock_confirmed_po = lock.

The purchase_stock override calls the base approval method and then _create_picking().

## 3. Receipt preparation and reuse

Source: purchase_stock/models/purchase_order.py.

_create_picking() operates on orders in purchase state and proceeds when at least one order-line product has type consu.

_prepare_picking() establishes:

- incoming picking type;
- vendor partner;
- supplier stock location as the source;
- configured destination location;
- company;
- draft state;
- purchase order origin;
- purchase reference.

A vendor location is required. If an open receipt already exists, Odoo reuses it. Otherwise it creates a receipt with SUPERUSER_ID.

Destination rules:

- dropship orders with dest_address_id use the destination partner customer location;
- ordinary receipts use the picking type default destination;
- final-location logic can select a warehouse stock location or a child final location.

## 4. Purchase-line stock-move preparation

Source: purchase_stock/models/purchase_order_line.py.

_create_stock_moves() skips display-only lines, calls _prepare_stock_moves() for each remaining line, and creates stock.move records from the returned value dictionaries.

_prepare_stock_moves():

- returns no move for products outside the consu type;
- starts from the discounted purchase price;
- computes already-procured quantity from incoming and outgoing moves;
- excludes cancelled moves and purchase returns;
- compares ordered quantity with downstream initial demand;
- creates an attached move for demand that can be linked to downstream moves;
- creates an additional unlinked move for any remaining quantity.

Price preparation includes:

- price_unit_discounted;
- tax computation with round_globally when taxes exist;
- quantity normalization;
- purchase-line to product UoM conversion;
- foreign-currency conversion without immediate rounding;
- Product Price precision rounding.

Move values include product, dates, supplier source, destination and final locations, picking, partner, downstream links, purchase line, company, price, operation type, references, origin, cancellation propagation, warehouse, quantity, UoM, and sequence.

## 5. Stock-move confirmation

Source: stock/models/stock_move.py.

_action_confirm() processes draft moves as follows:

- moves with origins become waiting;
- make_to_order moves become waiting and can create procurements;
- mts_else_mto moves become confirmed and can create procurements;
- other draft moves become confirmed;
- reservation dates are set for picking types reserving at confirmation;
- pickings are assigned in batches using references and locations;
- compatible moves can be merged;
- negative quantities can create push moves or be transformed into return-like moves;
- eligible confirmed moves can immediately call _action_assign().

## 6. Procurement dispatch

Source: stock/models/stock_rule.py.

stock.rule.run():

- skips non-consu and zero-quantity procurements;
- supplies default company, priority, and planned date values;
- calls _get_rule();
- records a product and location error when no rule exists;
- maps pull_push actions to pull;
- groups procurements by action;
- invokes the corresponding _run_<action>() handler;
- collects ProcurementException failures;
- raises UserError or ProcurementException according to raise_user_error.

Rule selection considers procurement-group routes, packaging routes, product routes, category routes, warehouse routes, destination locations, route sequence, and rule sequence.

## 7. Reservation and assignment

Source: stock/models/stock_move.py.

_action_assign():

- calculates missing reserved quantity using product-UoM precision;
- creates move lines without changing quants for reservation-bypassing moves;
- handles serial products one unit at a time when lot creation or reuse is enabled;
- updates compatible existing move lines or creates new ones;
- reserves ordinary moves through _update_reserved_quantity();
- leaves make_to_order moves without origins unassigned;
- distributes quantities from parent and sibling move lines for chained moves;
- marks fully reserved moves assigned;
- marks partially reserved moves partially_available;
- creates accumulated move lines in batches;
- checks entire-pack constraints unless bypassed by context;
- applies putaway strategies to redirected move lines.

## 8. Cancellation

Sources: purchase/models/purchase_order.py, purchase_stock/models/purchase_order.py, and stock/models/stock_move.py.

Base purchase cancellation blocks:

- locked purchase orders;
- purchase orders with related vendor bills that are not draft or cancelled.

The purchase_stock override first coordinates stock-side effects:

- collects non-done source moves;
- preserves done pickings and posts a cancellation note;
- unlinks shared purchase-line relationships when required;
- cancels eligible moves;
- changes selected downstream moves to make_to_stock and recomputes them;
- cancels open pickings;
- then calls the base button_cancel().

Stock-move cancellation:

- rejects cancellation of done physical moves and directs the user to create a return;
- unreserves quantities;
- sets eligible moves to cancel;
- propagates cancellation through destination chains when all sibling origins are cancelled;
- detaches downstream moves and changes them to make_to_stock when propagation is not required;
- can cancel origins when stock.cancel_moves_origin is enabled;
- clears origin links and logs cancellation activity unless skipped.

The source order places stock-side processing before the base purchase cancellation call. This ordering requires an isolated transaction test to verify rollback behavior when a later base guard rejects cancellation.

## 9. Accounting and tax linkage

Source: account/models/account_move_line.py, account/models/account_move.py, and account/models/account_tax.py.

Invoice-line totals delegate to shared tax computation. The inspected path includes:

- account.move.line._compute_totals();
- account.move._prepare_product_base_line_for_taxes_computation();
- account.tax._get_tax_details();
- account.tax._round_base_lines_tax_details();
- account.tax._add_accounting_data_to_base_line_tax_details().

The tax engine handles price-included and price-excluded taxes, tax ordering, currencies, raw and rounded amounts, manual tax amounts, repartition lines, reverse-charge factors, tax tags, and residual delta distribution.

Purchase-line stock pricing calls tax computation and currency conversion before creating stock moves. This links receipt valuation inputs to the accounting calculation path, while actual vendor-bill posting and reconciliation remain runtime work.

## Source-level findings

- Purchase confirmation is guarded by state, product, analytic, approval, and supplier checks.
- Approval can change both accounting workflow state and inventory workflow state.
- Receipt creation is configuration-driven and reuses open receipts.
- Stock moves represent quantity, route, downstream demand, pricing, currency, UoM, and cancellation relationships.
- Reservation is based on actual quant availability and can produce assigned or partially available states.
- Cancellation propagates through a linked move graph rather than only changing a purchase-order state.
- Procurement failures are structured and route-dependent.

## Runtime validation still required

- exact approval threshold equality;
- manager override and multi-company currency context;
- duplicate approval and receipt reuse;
- dropship and warehouse destination behavior;
- partial, over, negative, and returned quantities;
- UoM and foreign-currency conversions;
- tax-inclusive and globally rounded prices;
- quant reservation and concurrent assignment;
- serial and lot tracking;
- cancellation rollback when vendor bills or locks block the order;
- push-rule and make-to-order recursion;
- done receipts, returns, and chained move cancellation;
- posted vendor bills and accounting reconciliation.

## Research rule

Source evidence is recorded separately from runtime observations. No implementation decision should be marked production-safe until the relevant controlled transaction has been executed and its database state verified.

## Procurement rule resolution and inter-company routing

Odoo resolves stock rules in layers:

- explicit procurement-group route IDs;
- packaging UoM routes;
- product and category routes;
- warehouse routes.

Candidate rules are ordered by route_sequence and sequence. Resolution uses the current destination location first, then parent locations up to the root. Warehouse-specific rules are preferred, with company-independent rules as fallback. Product routes receive preference during route extraction.

For inter-company transit locations, Odoo adds the customer location as an additional candidate so customer-delivery rules can serve the inter-company path without duplicating every rule. Push rules are excluded from this pull-rule domain. The final superuser company restriction and pull-action implementation remain under inspection.


## Push fallback and scheduler behavior

Push rules search from a destination location upward through parent locations and allow push or pull_push actions. Superuser rule domains are restricted to company-independent rules and the requested company hierarchy, with route companies included when applicable.

The stock scheduler confirms automatic orderpoint procurements, assigns due confirmed or partially available moves in batches of 1000, optionally commits each batch with a new cursor, and merges duplicated quants. It runs with superuser privileges to avoid access and inter-company filtering issues. Scheduler failure and batch-commit behavior remain runtime validation items.


## Pull-action implementation

The stock-rule pull action is defined in stock/models/stock_rule.py at line 290. Its grouping, move creation, and chained-route effects remain under inspection.


## Pull action and move construction

The pull action validates source locations, sorts procurements, converts mts_else_mto to make_to_stock, groups move creation by company, creates moves with superuser rights, and confirms them. Move values preserve dates after rule delays, UoMs, source and final locations, downstream links, routes, references, priority, orderpoints, cancellation propagation, inter-warehouse partners, and refund flags for negative quantities.


## Procurement serialization and lead time

Procurement values are serialized for stock-move storage: recordsets become IDs, date and datetime values become strings, and other values are preserved. Lead time combines delays from pull and pull_push rules with an optional global orderpoint horizon. Context flags can bypass horizon or descriptions. The source contains a multiple-product limitation that requires runtime validation.


## Caller search environment note

The planned grep for callers of `_get_lead_days()` and `_serialize_procurement_values()` could not run in the current shell because `docker` was unavailable. The detailed notebook records this as an environment limitation; no caller behavior is inferred.


## Lead-time caller evidence

The installed source uses procurement serialization while constructing pull-rule stock moves. Lead-time accumulation is called from product lead-time calculation and from orderpoint scheduling/deadline logic. Those callers suppress descriptive delay text for numeric scheduling. Exact date calculations remain under inspection.


## Lead-time consumer inspection status

The planned inspection of the product and orderpoint methods that consume lead-time values could not run in the current shell because `docker` was unavailable. The detailed notebook records the blocked command; exact date and deadline arithmetic remain unverified.
