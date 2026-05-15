# AGENTS.md

## Project Overview

`fast-forward/agents` is the packaged agent bundle for Fast Forward repositories.
It carries reusable project-agent prompts under `.agents/agents/` and procedural
skills under `.agents/skills/`.

This repository is intentionally content-first. Do not add runtime PHP source
unless a future issue explicitly expands the package contract.

## Setup Commands

Install dependencies with:

```bash
composer install
```

Install `fast-forward/dev-tools` globally while this package is being split out:

```bash
composer global config --no-plugins allow-plugins.fast-forward/dev-tools true
composer global require fast-forward/dev-tools:dev-main
composer global config --no-plugins allow-plugins.fast-forward/dev-tools false
```

This package uses the global `dev-tools` binary for local checks. Do not add
`fast-forward/dev-tools` as a local dependency unless a future issue explicitly
introduces the shim needed to avoid the package cycle.

## Development Workflow

Important paths:

- `.agents/agents/` packaged `fast-forward-*.md` role prompts for repository work.
- `.agents/skills/` packaged `fast-forward-*` procedural skills and their
  reference material.
- `composer.json` package metadata, custom Composer type, installer dependencies,
  and bundle path hints.
- `.github/workflows/` CI, changelog, label, review, and project automation.

Keep edits focused on agent content, skill instructions, metadata, or repository
automation. Changes required in `php-fast-forward/dev-tools` belong in a
separate branch and issue.

## Testing Instructions

Use the smallest relevant check while editing:

```bash
composer validate --strict
```

Check changelog discipline on PR branches:

```bash
composer dev-tools changelog:check -- --file=CHANGELOG.md --against=origin/main
```

If `composer dev-tools` reports auto-fixable formatting or generated-output
drift, run:

```bash
composer dev-tools:fix
```

`fast-forward/dev-tools` is intentionally consumed globally in this root package
for now. Keep `composer.json` on `type: fast-forward-resource-bundle` and preserve
the `fast-forward/composer-installers` contract for the installer-paths work
tracked in `php-fast-forward/dev-tools#195`. Until `dev-tools` has a standalone
shim for its bundled toolchain, the full `composer dev-tools` standards command
is not the local gate for this repository.

## Code Style

Keep documentation, agent prompts, and skill files in English. Preserve the
existing Fast Forward markdown structure and avoid rewriting copied skill
references unless the standalone package layout requires it.

## Pull Request Guidelines

Do not push implementation work directly to `main`. Use one issue-focused branch
per PR, include verification notes, and keep `CHANGELOG.md` updated for
user-visible package, automation, or prompt changes.
