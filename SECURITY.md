# Security Policy

This repository contains no application code that handles user data or secrets — it's a static
profile and documentation repo. The GitHub Actions workflows here use only the default,
repo-scoped `GITHUB_TOKEN` with `contents: write` permission; no external secrets are stored.

## Reporting a vulnerability

If you spot something concerning (e.g. a workflow misconfiguration, an overly broad permission,
or a dependency issue in `scripts/`), please open an issue or email
yashovardhanbangur2801@gmail.com directly rather than filing a public issue if it's sensitive.
