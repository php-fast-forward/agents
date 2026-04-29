Fast Forward Agents
===================

``fast-forward/agents`` packages the Fast Forward project-agent prompts and
procedural skills used by consumer repositories.

The package exists so ``fast-forward/dev-tools`` can depend on a dedicated
agent bundle and resolve packaged assets from a stable Composer-installed path
instead of carrying the ``.agents`` tree in the main development-tools archive.

Payload
-------

The package currently contains two payload directories:

- ``.agents/agents`` for role-based project prompts.
- ``.agents/skills`` for reusable procedural skills and reference material.

Composer Installation
---------------------

Consumer repositories are expected to install Fast Forward resource bundles with
``fast-forward/composer-installers``:

.. code-block:: json

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

``fast-forward/composer-installers`` is a package dependency of this bundle, so
consumers do not need to require the installer separately once the package is
available from normal Composer metadata. Until the first tagged installer
release exists, consumer smoke projects can add a repository entry for
``php-fast-forward/composer-installers`` and install the ``dev-main`` version.
Consumer roots still own the plugin allow-list and the ``installer-paths``
configuration.

The resource-bundle type is generic on purpose. Different bundle kinds can still
install into different target directories by matching explicit package names in
``installer-paths``:

.. code-block:: json

   {
     "extra": {
       "installer-paths": {
         ".agents/": ["fast-forward/agents"],
         ".github/workflows/": ["fast-forward/github-workflows"]
       }
     }
   }

This keeps the Composer type reusable while preserving one target directory per
bundle package or bundle kind. The installer copies only the declared payload
contents into each target, so ``fast-forward/agents`` materializes
``.agents/agents`` and ``.agents/skills`` directly under the consumer
``.agents/`` directory.

The follow-up ``fast-forward/dev-tools`` work tracked in
`php-fast-forward/dev-tools#195 <https://github.com/php-fast-forward/dev-tools/issues/195>`_
will teach consumer sync commands to require this package and resolve the
installed bundle path.

Useful Links
------------

- `Repository <https://github.com/php-fast-forward/agents>`_
- `Issue Tracker <https://github.com/php-fast-forward/agents/issues>`_
- `Parent dev-tools issue <https://github.com/php-fast-forward/dev-tools/issues/195>`_
