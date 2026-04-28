<?php

declare(strict_types=1);

/**
 * Packaged Fast Forward agents and skills for consumer repositories.
 *
 * This file is part of fast-forward/agents project.
 *
 * @author   Felipe Sayao Lobato Abreu <github@mentordosnerds.com>
 * @license  https://opensource.org/licenses/MIT MIT License
 *
 * @see      https://github.com/php-fast-forward/agents
 * @see      https://github.com/php-fast-forward/agents/issues
 * @see      https://php-fast-forward.github.io/agents/
 * @see      https://datatracker.ietf.org/doc/html/rfc2119
 */

namespace FastForward\Agents;

/**
 * Describes the Fast Forward packaged agent bundle contract.
 */
final class AgentBundle
{
    public const string PACKAGE_NAME = 'fast-forward/agents';

    public const string METADATA_KEY = 'fast-forward-bundle';

    public const string BUNDLE_KIND = 'agents';

    public const string INSTALLERS_PACKAGE = 'composer/installers';

    public const string INSTALLERS_EXTENDER_PACKAGE = 'oomphinc/composer-installers-extender';

    public const string INSTALLER_NAME = 'agents';

    public const string INSTALLER_TYPE = 'fast-forward-resource-bundle';

    public const string INSTALLER_PATH_PATTERN = '.agents/{$name}/';

    public const string INSTALLER_PATH_MATCH = 'fast-forward/agents';

    public const string PAYLOAD_PATH = '.agents';

    public const string PROJECT_AGENTS_PATH = '.agents/agents';

    public const string SKILLS_PATH = '.agents/skills';

    private function __construct() {}
}
