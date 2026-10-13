# REA Studio — GitHub smoke-test staging

This is an **isolated proof-of-feasibility** directory on a development branch of `giduk05/rea`. It does not modify REA's runtime or analysis providers.

The companion standalone **REA Studio v0.1 desktop web UI** is distributed separately as a source ZIP through the project conversation. This GitHub directory contains only the **zero-paid-API manual CI smoke test** and its static fixture; it is not the entire UI application.

## Manual verification

After this workflow has been reviewed and made available in the repository's default branch, run:

1. Actions → **REA Studio static smoke** → Run workflow.
2. Open the completed job, download the `rea-studio-smoke` artifact.
3. Inspect `summary.json`, `evidence.json` and `rea-stderr.log`.

The workflow checks out **this REA source revision**, installs Node dependencies, builds REA and analyzes only the repository-owned fixture. It does not analyze any proprietary app, install unknown input from third-party repositories or invoke any model API.

This is a staging experiment. For long-term use, move REA Studio into an independent repository so syncing the upstream REA Fork stays straightforward.
