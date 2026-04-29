# Fast Forward Agents

Packaged Fast Forward project agents and skills for consumer repositories.

This package is the standalone distribution point for the `.agents` payload that
is currently being split out of `fast-forward/dev-tools`. It is part of the
package split tracked by [php-fast-forward/dev-tools#195](https://github.com/php-fast-forward/dev-tools/issues/195).

## Installation Model

The package uses the custom Composer type `fast-forward-resource-bundle`.
Consumer repositories are expected to install Fast Forward resource bundles
through `fast-forward/composer-installers` instead of copying or linking package
contents manually.

```json
{
  "require": {
    "fast-forward/agents": "dev-main"
  },
  "config": {
    "allow-plugins": {
      "fast-forward/composer-installers": true
    }
  },
  "extra": {
    "installer-paths": {
      ".agents/": ["fast-forward/agents"]
    }
  }
}
```

`fast-forward/composer-installers` is required by this package so consumers do
not need to require the installer explicitly once the package is available from
normal Composer metadata. Until the first tagged installer release exists,
consumer smoke projects can add a repository entry for
`php-fast-forward/composer-installers` and install the `dev-main` version.

The resource-bundle type is intentionally generic. Each bundle can still install
to a different target by using a package-specific installer-path match. For
example, a consumer that later installs both agents and a GitHub workflow bundle
could declare:

```json
{
  "extra": {
    "installer-paths": {
      ".agents/": ["fast-forward/agents"],
      ".github/workflows/": ["fast-forward/github-workflows"]
    }
  }
}
```

Consumer roots still own the plugin allow-list and the `installer-paths` entries
because Composer treats those settings as root configuration. The installer
copies only the declared payload contents into each target, so `fast-forward/agents`
materializes `.agents/agents` and `.agents/skills` directly under the consumer
`.agents/` directory.

`fast-forward/dev-tools` will use that stable installed package path in a later
change so consumer sync commands can resolve packaged agent assets without
assuming they live inside the `dev-tools` archive.

## Payload

- `.agents/agents/` contains project-agent prompts.
- `.agents/skills/` contains reusable procedural skills and reference material.

The copied payload is intentionally kept close to the current `dev-tools`
version. Content changes should stay minimal unless they are required for the
standalone bundle layout.

The Composer metadata in `composer.json` is the package contract. This package
does not expose a runtime PHP API yet; one can be introduced later when
`dev-tools` has a concrete integration need.

## Development

Install dependencies:

```bash
composer install
```

Install `fast-forward/dev-tools` globally while this package is being split out:

```bash
composer global config --no-plugins allow-plugins.fast-forward/dev-tools true
composer global require fast-forward/dev-tools:dev-main
composer global config --no-plugins allow-plugins.fast-forward/dev-tools false
```

Validate the package metadata:

```bash
composer validate --strict
```

Check changelog discipline on PR branches:

```bash
composer dev-tools changelog:check -- --file=CHANGELOG.md --against=origin/main
```

The root package intentionally does not require `fast-forward/dev-tools` as a
local dependency. `composer dev-tools` delegates to the global binary so this
package can later become a dependency of `dev-tools` without creating a package
cycle while the installer-paths work from `php-fast-forward/dev-tools#195`
continues. Until `dev-tools` has a standalone shim for its bundled toolchain,
the full `composer dev-tools` standards command is not the local gate for this
repository.
