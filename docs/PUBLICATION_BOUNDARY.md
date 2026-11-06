# Public-repository publication boundary

The linked GitHub repository is **public**. It is appropriate for curated source research and references, but not for private customer or system materials.

## Safe to publish after review

- Research-method descriptions and findings with clear confidence labels.
- Non-sensitive source-path inventories and source-architecture diagrams.
- Research scripts that contain no tokens, private hostnames, credentials or production database writes.
- Observed integrity **counts** and hashes (where hashes do not leak private content).
- Small selected source excerpts under applicable upstream licenses/attribution.

## Keep out of GitHub history

- Database schema/row dumps if they reveal local or third-party configuration; always review even schema-only exports.
- Credentials, \`.env\`, API keys, database URLs, authentication cookies and service configuration.
- Full private \`/var/lib/odoo\` or attachments filestore.
- Large Odoo TAR and reconstructed ZIP (use private artifact storage if needed).
- Unreviewed raw terminal transcripts or patches; they may include account identifiers or command secrets.
- Generated \`*.log\`, \`*.dump\`, \`*.backup\`, \`*.sql\` and large \`*.zip\` artifacts.

## Why not upload the entire installed Odoo codebase?

The source code already has an authoritative upstream repository and license obligations. A research repository can link to Odoo upstream and preserve selected, properly attributed snapshots. Independently preserving the entire installation privately provides reproducibility without duplicating a large vendored tree or mixing generated artifacts into the research's commit history.

## Recommended local structure

\`\`\`text
odoo-19-database-research/     # reviewed, publishable Git history
~/Odoo19_Private_Capture/      # TAR, ZIP, dependencies, private schema/evidence
\`\`\`

Review \`git status --short\`, \`git diff --cached --stat\`, \`git diff --cached --check\` and all staged file contents before pushing. Never force-push over existing research.
