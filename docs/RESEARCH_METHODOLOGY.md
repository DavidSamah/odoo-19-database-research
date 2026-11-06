# Odoo / ProofFlow methodological evidence standard

Every investigation is a traceable sequence, not a collection of conclusions.

## Required record

1. **Question**: exact uncertainty being resolved.
2. **Why this method**: link to earlier observation; mark retrospective rationale when no historical rationale survives.
3. **Command and tool**: verbatim Git Bash, Docker, SQL, grep or other executed text. If missing, mark **NOT RECOVERED**.
4. **Observed output**: complete unmodified evidence or a link to it; distinguish selected excerpts.
5. **Explanation**: explain important paths, fields, error messages and negative results.
6. **Interpretation**: claim only what the output supports.
7. **Uncertainty**: unavailable files, alternative causes, unresolved contexts.
8. **Decision**: historic or explicitly retrospective.
9. **Next investigation**: why it follows; do not repeat already verified steps.
10. **Provenance**: commit SHA, file path, source snapshot, commands, database name and evidence hash.

## Evidence classifications

| Code | Meaning | Does NOT establish |
|---|---|---|
| SOURCE | Original inspected Python/XML implementation | Runtime branch correctness |
| DATABASE | Read-only PostgreSQL metadata or queries | Application-enforced permissions |
| RUNTIME | Executed scenario in a named isolated environment | Other untested scenarios |
| DOC | Upstream documentation for generic framework behavior | Exact installed implementation |
| INFERRED | Explicit explanation of a relationship | Historical verbatim observation |
| UNAVAILABLE | Not present in inspected path / environment | Universally absent across Odoo |
| UNVERIFIED | Requires additional inspection | A successful result |
| CONTRADICTED | Evidence materially disputes earlier interpretation | Silent replacement of history |

## Example: financial-report source discovery

**Question:** Which models implement reporting in the inspected installation?

**Command:**

\`\`\`bash
docker exec odoo19-research-app sh -c '
BASE=/usr/lib/python3/dist-packages/odoo/addons
for MODULE in account_reports account_financial_report; do
  if test -d "$BASE/$MODULE"; then
    find "$BASE/$MODULE" -type f -name "*.py" | sort | head -100
  else
    echo "$MODULE unavailable"
  fi
done
grep -RnE "^[[:space:]]+def .*report|_name = .account.report|_inherit = .account.report" \
  "$BASE/account/models" "$BASE/account/report" 2>/dev/null | head -115
'
\`\`\`

**Selected observed results:** Dedicated addons unavailable; \`account/models/account_report.py\` declared \`account.report\`, \`account.report.line\`, \`account.report.expression\`, \`account.report.column\`, and \`account.report.external.value\`.

**Interpretation:** Base reporting models exist, but a complete financial-reporting calculation run was not demonstrated. **Next:** inspect reporting metadata and calculation/aggregation paths.

## Provenance boundary

The October–November Git patch, Phase 1 notebook, November 4 transcripts, November 5 recovery outputs, later nine-domain checkpoints, and November 6 archive integrity checks have **different collection times and scopes**. Never merge them into a fictional uninterrupted original terminal transcript.

Preserve \`commit_changes.patch\` and full terminal logs privately unless they are reviewed for secrets and personally identifying data before public publication.
