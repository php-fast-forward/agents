# AGENTS.md

## Project Overview

`fast-forward/agents` is the packaged agent bundle for Fast Forward repositories.
It carries reusable project-agent prompts under `.agents/agents/` and procedural
skills under `.agents/skills/`.

This repository is intentionally content-first. Keep runtime PHP source limited
to tiny metadata helpers such as `src/AgentBundle.php` unless a future issue
explicitly expands the package contract.

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

- `.agents/agents/` packaged role prompts for repository work.
- `.agents/skills/` packaged procedural skills and their reference material.
- `src/AgentBundle.php` constants for the Composer installer type and payload paths.
- `composer.json` package metadata, custom Composer type, installer dependencies,
  and bundle path hints.
- `tests/` validation for Composer metadata and expected payload layout.
- `.github/workflows/` CI, changelog, label, review, and project automation.

Keep edits focused on agent content, skill instructions, metadata, or repository
automation. Changes required in `php-fast-forward/dev-tools` belong in a
separate branch and issue.

## Testing Instructions

Use the smallest relevant check while editing:

```bash
composer validate --strict
./vendor/bin/phpunit tests
```

Run the global Fast Forward test wrapper before publishing a PR:

```bash
composer dev-tools tests -- --coverage=.dev-tools/coverage --min-coverage=0
```

If `composer dev-tools` reports auto-fixable formatting or generated-output
drift, run:

```bash
composer dev-tools:fix
```

`fast-forward/dev-tools` is intentionally consumed globally in this root package
for now. Keep `composer.json` on `type: fast-forward-resource-bundle` and preserve
the `composer/installers` plus `oomphinc/composer-installers-extender` contract
for the installer-paths work tracked in `php-fast-forward/dev-tools#195`. Until
`dev-tools` has a standalone shim for its bundled toolchain, the full
`composer dev-tools` standards command is not the local gate for this repository.

## Code Style

Keep documentation, agent prompts, skill files, and tests in English. Preserve
the existing Fast Forward markdown structure and avoid rewriting copied skill
references unless the standalone package layout requires it.

For PHP test files, keep `declare(strict_types=1);`, the repository header, and
PHPUnit attributes consistent with other Fast Forward packages.

## Pull Request Guidelines

Do not push implementation work directly to `main`. Use one issue-focused branch
per PR, include verification notes, and keep `CHANGELOG.md` updated for
user-visible package, automation, or prompt changes.
