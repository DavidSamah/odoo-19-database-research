# Odoo source code grouped by original module and file path

This is a navigation index for **observed** code paths and complete file snapshots. The presence of a path in the research does not mean its full source was preserved. Each available link opens the actual corresponding source file. No invented `.py` files are present.

| Module | Full files | Referenced but missing |
|---|---:|---:|
| `account` | 4 | 54 |
| `base` | 0 | 1 |
| `purchase` | 6 | 0 |
| `purchase_stock` | 3 | 0 |
| `stock` | 1 | 3 |
| `uom` | 0 | 1 |

## `account`

Accounting: journals, journal lines, tax, payment, reconciliation, reporting, fiscal controls and authorization.

- **Path observed; complete code unavailable:** `account/controllers/portal.py`
- **Path observed; complete code unavailable:** `account/data/account_data.xml`
- **Path observed; complete code unavailable:** `account/data/account_reports_data.xml`
- **Path observed; complete code unavailable:** `account/models/__init__.py`
- **Path observed; complete code unavailable:** `account/models/account_account.py`
- **Path observed; complete code unavailable:** `account/models/account_account_tag.py`
- **Path observed; complete code unavailable:** `account/models/account_bank_statement.py`
- **Path observed; complete code unavailable:** `account/models/account_bank_statement_line.py`
- **Path observed; complete code unavailable:** `account/models/account_journal.py`
- **Path observed; complete code unavailable:** `account/models/account_journal_dashboard.py`
- **Path observed; complete code unavailable:** `account/models/account_lock_exception.py`
- **Full source:** [`account/models/account_move.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/account/models/account_move.py) — SHA-256 `284f859f0ac33e3…`
- **Full source:** [`account/models/account_move_line.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/account/models/account_move_line.py) — SHA-256 `d1023d3c738b405…`
- **Path observed; complete code unavailable:** `account/models/account_move_send.py`
- **Path observed; complete code unavailable:** `account/models/account_partial_reconcile.py`
- **Path observed; complete code unavailable:** `account/models/account_payment.py`
- **Path observed; complete code unavailable:** `account/models/account_payment_term.py`
- **Path observed; complete code unavailable:** `account/models/account_report.py`
- **Path observed; complete code unavailable:** `account/models/account_tax.py`
- **Path observed; complete code unavailable:** `account/models/company.py`
- **Path observed; complete code unavailable:** `account/models/ir_actions_report.py`
- **Path observed; complete code unavailable:** `account/models/onboarding_onboarding_step.py`
- **Path observed; complete code unavailable:** `account/models/partner.py`
- **Path observed; complete code unavailable:** `account/models/res_currency.py`
- **Path observed; complete code unavailable:** `account/models/res_partner.py`
- **Path observed; complete code unavailable:** `account/models/res_partner_bank.py`
- **Path observed; complete code unavailable:** `account/models/sequence_mixin.py`
- **Path observed; complete code unavailable:** `account/report/account_hash_integrity_templates.py`
- **Path observed; complete code unavailable:** `account/report/account_invoice_report.py`
- **Path observed; complete code unavailable:** `account/report/account_invoice_report_view.xml`
- **Full source:** [`account/security/account_security.xml`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/account/security/account_security.xml) — SHA-256 `1cdc88906e0336b…`
- **Full source:** [`account/security/ir.model.access.csv`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/account/security/ir.model.access.csv) — SHA-256 `4d2520a2a7f76d3…`
- **Path observed; complete code unavailable:** `account/tests/__init__.py`
- **Path observed; complete code unavailable:** `account/tests/test_account_invoice_report.py`
- **Path observed; complete code unavailable:** `account/tests/test_account_move_send.py`
- **Path observed; complete code unavailable:** `account/tests/test_account_report.py`
- **Path observed; complete code unavailable:** `account/tests/test_chart_template.py`
- **Path observed; complete code unavailable:** `account/tests/test_early_payment_discount.py`
- **Path observed; complete code unavailable:** `account/tests/test_invoice_taxes.py`
- **Path observed; complete code unavailable:** `account/tests/test_ir_actions_report.py`
- **Path observed; complete code unavailable:** `account/tests/test_portal_invoice.py`
- **Path observed; complete code unavailable:** `account/tests/test_tax_report.py`
- **Path observed; complete code unavailable:** `account/views/account_account_views.xml`
- **Path observed; complete code unavailable:** `account/views/account_portal_templates.xml`
- **Path observed; complete code unavailable:** `account/views/account_report.xml`
- **Path observed; complete code unavailable:** `account/views/ir_actions_views.xml`
- **Path observed; complete code unavailable:** `account/views/report_invoice.xml`
- **Path observed; complete code unavailable:** `account/views/report_payment_receipt_templates.xml`
- **Path observed; complete code unavailable:** `account/views/report_statement.xml`
- **Path observed; complete code unavailable:** `account/views/report_templates.xml`
- **Path observed; complete code unavailable:** `account/wizard/account_automatic_entry_wizard.py`
- **Path observed; complete code unavailable:** `account/wizard/account_move_send_wizard.py`
- **Path observed; complete code unavailable:** `account/wizard/account_payment_register.py`
- **Path observed; complete code unavailable:** `account/wizard/account_resequence.py`
- **Path observed; complete code unavailable:** `account/wizard/account_secure_entries_wizard.py`
- **Path observed; complete code unavailable:** `account/wizard/base_document_layout.py`
- **Path observed; complete code unavailable:** `account/wizard/setup_wizards.py`
- **Path observed; complete code unavailable:** `account/wizard/setup_wizards_view.xml`

## `base`

Base utilities, including currency support used by accounting.

- **Path observed; complete code unavailable:** `base/models/res_currency.py`

## `purchase`

Purchasing: orders, order lines, bill matching and approval.

- **Full source:** [`purchase/models/account_invoice.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/purchase/models/account_invoice.py) — SHA-256 `a336f0b91abdc2c…`
- **Full source:** [`purchase/models/product.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/purchase/models/product.py) — SHA-256 `7d79d7f8e9faa90…`
- **Full source:** [`purchase/models/purchase_bill_line_match.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_bill_line_match.py) — SHA-256 `2ac5089b3361093…`
- **Full source:** [`purchase/models/purchase_order.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order.py) — SHA-256 `2fc418ca054aadb…`
- **Full source:** [`purchase/models/purchase_order_line.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/purchase/models/purchase_order_line.py) — SHA-256 `226499e27c7b662…`
- **Full source:** [`purchase/models/wizard/bill_to_po_wizard.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/purchase/models/wizard/bill_to_po_wizard.py) — SHA-256 `55b000741edf0bc…`

## `purchase_stock`

Purchase-to-stock bridge: receipt creation, stock-move linkage, billed/received quantities.

- **Full source:** [`purchase_stock/models/purchase_order.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order.py) — SHA-256 `c8f3dcde3e772be…`
- **Full source:** [`purchase_stock/models/purchase_order_line.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/purchase_order_line.py) — SHA-256 `8d44778579da75e…`
- **Full source:** [`purchase_stock/models/stock_move.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/purchase_stock/models/stock_move.py) — SHA-256 `c18b5df3c7aea61…`

## `stock`

Inventory: stock moves, routing, replenishment, procurement actions.

- **Path observed; complete code unavailable:** `stock/models/product.py`
- **Full source:** [`stock/models/stock_move.py`](odoo_source_tree/usr/lib/python3/dist-packages/odoo/addons/stock/models/stock_move.py) — SHA-256 `b867349664caaa4…`
- **Path observed; complete code unavailable:** `stock/models/stock_orderpoint.py`
- **Path observed; complete code unavailable:** `stock/models/stock_rule.py`

## `uom`

Unit of measure: quantity/price conversion methods identified in Phase 1.

- **Path observed; complete code unavailable:** `uom/models/uom_uom.py`
