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

namespace FastForward\Agents\Tests;

use FastForward\Agents\AgentBundle;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

#[CoversClass(AgentBundle::class)]
final class ComposerMetadataTest extends TestCase
{
    /**
     * @return void
     */
    #[Test]
    public function composerMetadataDeclaresTheAgentBundlePackage(): void
    {
        $composer = $this->readComposerJson();

        $metadata = $composer['extra'][AgentBundle::METADATA_KEY];

        self::assertSame(AgentBundle::PACKAGE_NAME, $composer['name']);
        self::assertSame(AgentBundle::INSTALLER_TYPE, $composer['type']);
        self::assertSame('README.md', $composer['readme']);
        self::assertSame(AgentBundle::INSTALLER_NAME, $composer['extra']['installer-name']);
        self::assertSame(AgentBundle::BUNDLE_KIND, $metadata['kind']);
        self::assertSame(AgentBundle::INSTALLER_TYPE, $metadata['installer-type']);
    }

    /**
     * @return void
     */
    #[Test]
    public function composerMetadataDescribesThePackagedPayloadPaths(): void
    {
        $composer = $this->readComposerJson();

        $metadata = $composer['extra'][AgentBundle::METADATA_KEY];

        self::assertSame(AgentBundle::INSTALLER_PATH_PATTERN, $metadata['installer-path']);
        self::assertSame(AgentBundle::INSTALLER_PATH_MATCH, $metadata['installer-path-match']);
        self::assertSame(AgentBundle::PAYLOAD_PATH, $metadata['payload-path']);
        self::assertSame(AgentBundle::PROJECT_AGENTS_PATH, $metadata['project-agents-path']);
        self::assertSame(AgentBundle::SKILLS_PATH, $metadata['skills-path']);
    }

    /**
     * @return void
     */
    #[Test]
    public function packageContainsTheExpectedAgentPayload(): void
    {
        self::assertDirectoryExists($this->packagePath(AgentBundle::PROJECT_AGENTS_PATH));
        self::assertDirectoryExists($this->packagePath(AgentBundle::SKILLS_PATH));
        self::assertFileExists($this->packagePath('.agents/agents/issue-implementer.md'));
        self::assertFileExists($this->packagePath('.agents/skills/github-pull-request/SKILL.md'));
    }

    /**
     * @return void
     */
    #[Test]
    public function composerMetadataProvidesInstallerDependenciesForConsumers(): void
    {
        $composer = $this->readComposerJson();

        self::assertArrayHasKey(AgentBundle::INSTALLERS_PACKAGE, $composer['require']);
        self::assertArrayHasKey(AgentBundle::INSTALLERS_EXTENDER_PACKAGE, $composer['require']);
        self::assertTrue($composer['config']['allow-plugins'][AgentBundle::INSTALLERS_PACKAGE]);
        self::assertTrue($composer['config']['allow-plugins'][AgentBundle::INSTALLERS_EXTENDER_PACKAGE]);
        self::assertArrayNotHasKey('fast-forward/dev-tools', $composer['require-dev']);
    }

    /**
     * @return array<string, mixed>
     */
    private function readComposerJson(): array
    {
        $contents = file_get_contents($this->packagePath('composer.json'));

        self::assertIsString($contents);

        $composer = json_decode($contents, true, 512, \JSON_THROW_ON_ERROR);

        self::assertIsArray($composer);

        return $composer;
    }

    /**
     * @param string $path
     *
     * @return string
     */
    private function packagePath(string $path): string
    {
        return \dirname(__DIR__) . '/' . $path;
    }
}
