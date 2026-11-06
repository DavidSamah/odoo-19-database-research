# Local reconstruction checkpoints — evidence summary

These checks were run by the researcher on a **Windows 11 + Git Bash + Docker** host, not executed in the connected GitHub environment.

## Framework capture

- Odoo application container: `odoo19-research-app`.
- Installed path: `/usr/lib/python3/dist-packages/odoo`.
- Extra-addons folder: empty at observed capture time.
- Docker copy onto NTFS initially failed while materializing a POS font symlink. Switched to an in-container `tar` stream.
- TAR created and verified: **1.3 GB**.
- Framework TAR SHA-256 recorded: `ebe2f5cdb7275e11dea7c542ba9c6168e0cd8e1526f95419b2e051355fe3b5c0`.
- Live vs TAR path lists: **71,801 each; 0 missing; 0 unexpected**.

## Missing research-referenced source code

- Original 59-path manifest included an invalid `account/models/res_partner.py`.
- Correct installed path: `account/models/partner.py` (recorded SHA-256 `8adc930fd4663318d89990da4f03d465182d4a00ca9430775d3aae2c782e8da2`).
- Corrected inventory: **58 valid; 58 copied; 0 outstanding**.
- Historic Git-era snapshots and new Docker captures must remain separate.

## Dependencies

- Container Python version observed: **3.12.3**.
- OS and Python package inventories and Docker-image provenance were collected per local run reports.
- Their full contents are **not** committed to this public repository.
- Installed-image/container metadata may differ from the historically pinned Odoo git SHA.

## Database schema

- PostgreSQL container: `odoo19-research-db`.
- Research database: `odoo19_security_research`.
- Schema-only dump via `pg_dump --schema-only`: **458 CREATE TABLE statements**, including `public.account_move` and `public.account_move_line`.
- Schema SQL checksum: **passed**.
- This DDL does **not** include original company/accounting record contents, installed module data, credentials, or filestore.
- A proposed live catalog comparison was not preserved in the supplied evidence; do not claim it passed.

## ZIP reconstruction and verification

- Resulting local ZIP: approx **414,811,076 bytes**.
- TAR inventory: **60,706 regular files**, **19 symlinks**, **11,076 directories**.
- ZIP source files+symlinks: **60,725**; zero missing/extra/incorrect link type.
- All regular source payloads compared **60,706/60,706 byte-for-byte**.
- Link targets compared **19/19**.
- Supporting evidence hashes **35/35**; ZIP CRC **PASS**.
- The earlier check for a root `odoo/__init__.py` file was erroneous: the original TAR did not contain it. The verifier was corrected.

## What these checks do not establish

They establish a sound **source-and-schema preservation artifact**. They do not establish a runnable restored deployment, authenticated runtime security, functional posting, reconciliation, complete all-module interpretation, or production readiness.

**Privacy:** Do not push the private framework TAR, the full reconstructed ZIP, database dumps or local data directories to this public repo.
