# How this mirror was reconstructed from evidence

## 1. The input boundary

Inputs were the user-supplied `commit_changes.patch`, 24 original November 4 terminal outputs, 34 domain checkpoint files, a 1,047-line Phase 1 notebook recovered from the patch, and one newly supplied November 5 recovery transcript. None of the code was sourced from live Docker or downloaded from GitHub in this operation.

## 2. The 32-commit sequence

Split the Git patch at `commit <40-digit hash>` lines. Each chunk is saved unmodified in `research/01_commit_order/<number>_<hash>/COMMIT_PATCH.txt`, including changed code, added lines and removed lines. Markdown additions are also separately preserved for study. The commit record is a historical evidence source, not an inferred terminal transcript.

## 3. Source reconstruction

For each Git `new file mode 100644` diff containing full content, extract lines beginning `+` within `@@` hunks and remove the one-character diff prefix; preserve the original whitespace and newline. Store complete source files at their Odoo addon module path, e.g. `account/models/account_move.py`.

The Git patch's SHA256SUMS manifest was compared byte-by-byte with the eight original snapshots. **8/8 matched.** There are 14 mapped complete Odoo code/config files. Another two files are copied with unresolved canonical original installed paths. 12 source `.py` files passed AST syntax parsing. These checks do not constitute runtime behavior tests.

## 4. Missing full code

The original patch includes only SELECTIVE committed Odoo files. We found 73 distinct referenced Odoo-source paths across the research evidence and full snapshots; 59 lack full source text in those materials. Never create a `.py` file for them. Instead, their directory contains `_MISSING_FULL_SOURCE.md` and their path appears in the CSV source catalog. Examples include `account/models/account_report.py`, `account/models/company.py`, `stock/models/stock_rule.py`. Those methods can be described from observed excerpts, not asserted to be fully mirrored code.

## 5. Optional later local source recovery

The read-only `scripts/export_missing_source_from_your_docker.sh` can copy the missing referenced paths, or **all installed addons** when called with `--full-addons`, from the existing local Docker container into a separate `supplement_from_live_docker` tree. That source may be newer than the historical Git snapshot and must retain its own timestamp and checksum. Do not silently mix.

## 6. Why this is not a runnable Odoo replica

A runnable installation also requires Odoo framework, all applicable addons, Python dependencies, server configuration and compatible PostgreSQL setup, plus proper initialization. An excerpt or a selective Odoo model snapshot cannot substitute. This package is a **literal research-verified path hierarchy with available full source**, not a simulated system or a claim that every byte has been recovered.