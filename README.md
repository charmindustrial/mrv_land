# MRV_LAND

Shared knowledge base and workflow library for Charm Industrial's MRV (Measurement, Reporting, and Verification) team.

## What This Is

This repo contains:
- **Workflow instructions** (`workflows/`) — step-by-step guides for MRV reporting processes, designed to be read and executed by Claude Code agents
- **Shared context** (`context/`) — reference documents covering Isometric protocols, Charm's project details, emission factors, and operational conventions
- **Automation scripts** (`scripts/`) — future home for Python/Node automation code

## Who This Is For

MRV team members using Claude Code (CLI or VS Code extension) to assist with reporting workflows. The `CLAUDE.md` file at the repo root provides Claude Code with the full context it needs to understand Charm's MRV processes.

## Getting Started

1. Clone this repo
2. Open it in VS Code with Claude Code extension
3. Say "Start [phase name], period [date range]" to kick off a workflow

## Workflow Dependency Chain

```
Phase 1 (Production Period)
    |
    v
Phase 2a (Injection Batch Data)
    |
    v
Phase 2b (Injection Emissions)
    |
    v
Phase 2c (Mangrove Data Entry)
    |
    v
Phase 2d (Certify QA)
    |
    v
Phase 3a (Protocol Documentation / Final Reporting Package)
```

## Contributing

- Update workflow `.md` files when processes change
- Add new context docs to `context/` as needed
- Keep `CLAUDE.md` in sync with any structural changes
