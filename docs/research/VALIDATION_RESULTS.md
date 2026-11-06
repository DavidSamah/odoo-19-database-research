# Verification of research and Odoo-source archive

- Original Git `commit_changes.patch` split into **32 commit records** and reassembled with byte-for-byte identical text: **PASS**.
- **8/8** snapshots in the original `models/source/SHA256SUMS.txt` match their reconstructed Python source files (see `metadata/PATCH_SOURCE_SHA256_VERIFICATION.csv`).
- **12/12** recovered Python files pass Python syntax parsing, without imports or runtime execution.
- **14** complete mapped Odoo code/configuration source files; **2** extra original security copies with unverified installed path.
- **73** observed Odoo addon source paths cataloged; **59** lack complete content in supplied historical evidence. They are **not** fabricated.
- **37** indexed early Phase 1 notebook sections copied.
- **24** November 4 terminal transcripts copied byte-for-byte.
- **34** later accounting-domain checkpoint files copied byte-for-byte.
- **0** broken internal Markdown links after reconciliation: **0**.
- November 5 newly executed Domain 9 source/database results preserved in separate folder.

These are **artifact reconstruction and structural checks**, not a live Odoo accounting test.