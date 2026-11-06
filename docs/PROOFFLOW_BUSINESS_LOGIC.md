# ProofFlow — Research-grounded accounting exception business logic

> **Classification:** Proposed product behavior derived from inspected Odoo 19 accounting, stock and purchase implementation. Not evidence of a completed product integration or production runtime verification.

## Problem and business outcome

A purchase order defines a commitment, a stock movement provides receipt/return evidence, a vendor bill states what a supplier charged, and journal/payment records represent booked and settled financial obligations. An inconsistency between these records may be legitimate or may require correction.

**ProofFlow's intended outcome:** a case is closed only when a justified discrepancy has been resolved **and independently rechecked against authoritative Odoo records**.

## Authoritative record graph

| Role | Odoo object | Evidence to preserve |
|---|---|---|
| Commitment | `purchase.order` and `purchase.order.line` | PO state, company, supplier, product, ordered qty, price, currency, UoM, invoice policy |
| Physical movement | `stock.picking`, `stock.move` | Picking and move IDs, done state, quantities, source/destination, return links, UoM |
| Billing | `account.move`, `account.move.line` | Bill/refund type, posting state, company, partner, invoice date, linked purchase line, price and tax |
| Accounting | `account.move.line`, `account.account`, `account.journal` | Debit/credit/balance, reconciliation state, journal and fiscal constraints |
| Settlement | `account.payment`, partial/full reconciliation records | Amount, currency, matched lines, residual and settlement date |
| Authorization | `ir.model.access`, `ir.rule`, groups, company | Permitted actor, company scope, review/approval authorization |

These are **provenance candidates**. The exact fields and data-access contract must be validated for the installed Odoo configuration.

## Business-rule pipeline

```text
read-only acquisition
  → identity and company scope checks
  → link records by Odoo relationships
  → normalize UoM / currency / tax context
  → compute justified ordered / received / invoiced values
  → classify discrepancy and evidence completeness
  → create case and immutable provenance reference
  → review and approve proposed intervention
  → authorized correction in authoritative system
  → refresh evidence and independently verify outcome
  → close / reopen / escalate
```

### Quantity calculation is contextual

- **Ordered**: contractual ordered quantity from purchase order lines.
- **Received**: computed from eligible completed stock movements; account for returns, manual receipt method, dropshipping and UoM conversions.
- **Invoiced**: computed from qualifying linked supplier bills and credit notes; a credit note can reduce net billed quantity.
- **To invoice**: depends on the configured purchase product billing policy, not a universally fixed comparison.

**Example (hypothetical, not a recorded Odoo transaction):**

Ordered **100**, qualifying received **80**, invoiced **100**. Under a policy that bills based on received quantities, the difference **20** is a review candidate; it is not automatically proof of vendor fraud, erroneous posting or a permitted write. Under a policy billing ordered quantities, the initial comparison can be different. Return/refund, timing, tolerance, UoM, tax, multiple bills and source status must still be evaluated.

### Financial amount calculation

`account.move.line._compute_totals()` delegates to `account.tax` helpers for prepared tax bases, included/excluded subtotals and rounding. Unit price × quantity alone cannot reproduce every Odoo result. The proposed case engine must preserve the actual Odoo currency, fiscal position, discount and tax method inputs rather than silently using floating point arithmetic.

### Posting, reconciliation and closing

A draft vendor bill is not a posted journal entry. A posted journal entry is not a paid bill. The amount remaining to settle is not generally the original debit/credit balance. Period locks and explicit posting authorization can block actions even if the raw database supports a column change.

### Security and multi-company

Never infer authorization from the user interface alone. Odoo access depends on ACLs, record rules, contextual company scope and explicit checks. `sudo()` is a high-risk privileged operation. Proposed actions must record the target company, actor, basis for authority, source state, intended change and audit outcome.

## Proposed exception states

```text
detected → awaiting_evidence → ready_for_review → approved_for_action
         ↘ insufficient_evidence → escalated
approved_for_action → correction_requested → pending_verification
pending_verification → verified_resolved
pending_verification → unresolved / stale_evidence / reopened
```

These are **design proposals**, not Odoo native model states or proof of implemented ProofFlow endpoints.

## Safety requirements

1. Default to read-only discovery; require explicit authorization for any correction.
2. Store audit events separately from computed snapshots; preserve original evidence hashes/IDs.
3. Do not delete or overwrite supplier invoice/receipt history as a shortcut.
4. Recheck source data after a proposed correction, using fresh authoritative reads.
5. Keep reviewer identity independent where policy requires it.
6. Mark incomplete source, missing receipts, inconsistent company scopes, or stale evidence as **uncertain**, not as verified.
7. Avoid production use until isolated runtime, reconciliation, authorization, and concurrency tests pass.

## Evidence and next verification

Detailed paths and limitations: [Odoo 19 framework map](architecture/ODOO19_FRAMEWORK_MAP.md), [nine domains](research/NINE_DOMAIN_EVIDENCE_INDEX.md), [original workflow](ProofFlow_Odoo19_Purchase_Receipt_Workflow.md).

**Outstanding:** Runtime validation of quantity scenarios, real posting/reconciliation, cross-company authorization, lock exceptions, reports, tax/currency edge cases and end-to-end ProofFlow integration.
