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
Composer installer paths:

.. code-block:: json

   {
     "config": {
       "allow-plugins": {
         "composer/installers": true,
         "oomphinc/composer-installers-extender": true
       }
     },
     "extra": {
       "installer-types": ["fast-forward-resource-bundle"],
       "installer-paths": {
         ".agents/{$name}/": ["fast-forward/agents"]
       }
     }
   }

``composer/installers`` is a package dependency of this bundle, so consumers do
not need to require it separately. The custom ``fast-forward-resource-bundle`` type
is outside the finite list handled directly by ``composer/installers``, so the
bundle also requires ``oomphinc/composer-installers-extender``. Consumer roots
still own the plugin allow-list and the ``installer-types`` /
``installer-paths`` configuration.

The resource-bundle type is generic on purpose. Different bundle kinds can still
install into different target directories by matching explicit package names in
``installer-paths``:

.. code-block:: json

   {
     "extra": {
       "installer-types": ["fast-forward-resource-bundle"],
       "installer-paths": {
         ".agents/{$name}/": ["fast-forward/agents"],
         ".github/workflows/{$name}/": ["fast-forward/github-workflows"]
       }
     }
   }

This keeps the Composer type reusable while preserving one target directory per
bundle package or bundle kind.

The follow-up ``fast-forward/dev-tools`` work tracked in
`php-fast-forward/dev-tools#195 <https://github.com/php-fast-forward/dev-tools/issues/195>`_
will teach consumer sync commands to require this package and resolve the
installed bundle path.

Useful Links
------------

- `Repository <https://github.com/php-fast-forward/agents>`_
- `Issue Tracker <https://github.com/php-fast-forward/agents/issues>`_
- `Parent dev-tools issue <https://github.com/php-fast-forward/dev-tools/issues/195>`_
