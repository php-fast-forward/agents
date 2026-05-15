#!/usr/bin/env python3
"""
Structural validation tests for packaged Fast Forward agents and skills.

Tests cover the files added in the PR that introduced the .agents/agents/
directory, the .agents/agents/README.md naming-convention document, all
packaged agent Markdown files, and the three new skill directories:
  - fast-forward-changelog-generator
  - fast-forward-create-agentsmd
  - fast-forward-github-issues

Run:
  python3 tests/validate-agents-payload.py
"""

import os
import re
import sys
import yaml  # PyYAML

# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------

passed = 0
failed = 0
failures: list[str] = []


def ok(message: str) -> None:
    global passed
    passed += 1
    print(f"  PASS  {message}")


def fail(message: str, detail: str = "") -> None:
    global failed
    full = f"  FAIL  {message}" + (f": {detail}" if detail else "")
    print(full)
    failed += 1
    failures.append(full)


def assert_file_exists(path: str) -> bool:
    if os.path.isfile(path):
        ok(f"File exists: {path}")
        return True
    fail("File must exist", path)
    return False


def assert_dir_exists(path: str) -> bool:
    if os.path.isdir(path):
        ok(f"Directory exists: {path}")
        return True
    fail("Directory must exist", path)
    return False


def read_file(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        fail("Cannot read file", path)
        return None


def parse_front_matter(path: str) -> dict | None:
    """
    Parse YAML front matter delimited by --- lines.
    Returns a dict on success, or None if the file has no front matter.
    """
    content = read_file(path)
    if content is None:
        return None
    if not content.startswith("---"):
        return None
    end = content.find("---", 3)
    if end == -1:
        return None
    yaml_block = content[3:end]
    try:
        payload = yaml.safe_load(yaml_block)
    except yaml.YAMLError:
        fail("YAML front matter is invalid", path)
        return None
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        fail("YAML front matter must be a mapping", path)
        return None
    return payload


def assert_front_matter_field(fm: dict, field: str, context: str) -> None:
    """Assert that a required scalar field is present and non-empty."""
    if field not in fm:
        fail(f"Front matter must contain '{field}'", context)
        return
    value = fm[field]
    if value == "" or value is None:
        fail(f"Front matter field '{field}' must not be empty", context)
        return
    ok(f"Front matter field '{field}' present in {context}")


def assert_front_matter_field_exists(fm: dict, field: str, context: str) -> None:
    """Assert that a field is declared (may be an empty list)."""
    if field not in fm:
        fail(f"Front matter must declare '{field}'", context)
        return
    ok(f"Front matter field '{field}' declared in {context}")


def assert_front_matter_field_type(fm: dict, field: str, expected_type: type | tuple[type, ...], context: str, *, allow_empty: bool = False) -> None:
    if field not in fm:
        return

    value = fm[field]
    if not isinstance(value, expected_type):
        fail(f"Front matter field '{field}' must be {expected_type}", context)
        return

    if not allow_empty and (value == "" or value == []):
        fail(f"Front matter field '{field}' must not be empty", context)
        return

    ok(f"Front matter field '{field}' has expected type in {context}")


def assert_markdown_section(path: str, section: str) -> None:
    """Assert that '## section' is present in a Markdown file."""
    content = read_file(path)
    if content is None:
        return
    pattern = rf"^##\s+{re.escape(section)}\s*$"
    if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
        ok(f"Section '## {section}' found in {os.path.basename(path)}")
    else:
        fail(f"Section '## {section}' missing", path)


def assert_file_contains(path: str, needle: str, description: str) -> None:
    content = read_file(path)
    if content is None:
        return
    if needle in content:
        ok(f"{description} found in {os.path.basename(path)}")
    else:
        fail(f"{description} missing", f"{path} (expected: {needle!r})")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS_DIR = os.path.join(ROOT, ".agents", "agents")
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

# Agent files added by the PR (excluding README.md which has no front matter).
NEW_AGENT_FILES = [
    "fast-forward-agents-maintainer.md",
    "fast-forward-changelog-maintainer.md",
    "fast-forward-consumer-sync-auditor.md",
    "fast-forward-docs-writer.md",
    "fast-forward-issue-editor.md",
    "fast-forward-issue-implementer.md",
    "fast-forward-php-style-curator.md",
    "fast-forward-quality-pipeline-auditor.md",
    "fast-forward-readme-maintainer.md",
    "fast-forward-review-guardian.md",
    "fast-forward-test-guardian.md",
]

# Required markdown body sections for every agent file.
REQUIRED_AGENT_SECTIONS = [
    "Purpose",
    "Responsibilities",
    "Use When",
    "Boundaries",
    "Primary Skill",
    "Supporting Skills",
]

# New skill directories added by the PR.
NEW_SKILL_DIRS = [
    "fast-forward-changelog-generator",
    "fast-forward-create-agentsmd",
    "fast-forward-github-issues",
]

# Reference files that must exist per skill.
REQUIRED_SKILL_REFERENCES: dict[str, list[str]] = {
    "fast-forward-changelog-generator": [
        "references/change-categories.md",
        "references/description-patterns.md",
        "references/keep-a-changelog-format.md",
        "references/official-example-template.md",
    ],
    "fast-forward-create-agentsmd": [
        "references/content-outline.md",
    ],
    "fast-forward-github-issues": [
        "references/architectural-criteria.md",
        "references/context.md",
    ],
}

# ---------------------------------------------------------------------------
# Helper: resolve known skill slugs from installed directories
# ---------------------------------------------------------------------------

def known_skill_slugs() -> list[str]:
    slugs = []
    if os.path.isdir(SKILLS_DIR):
        for entry in os.scandir(SKILLS_DIR):
            if entry.is_dir():
                slug = re.sub(r"^fast-forward-", "", entry.name)
                slugs.append(slug)
    return slugs


# ---------------------------------------------------------------------------
# Suite 1: agents/README.md naming-convention document
# ---------------------------------------------------------------------------

print("\n=== Suite 1: agents/README.md naming-convention document ===")

agents_readme = os.path.join(AGENTS_DIR, "README.md")
assert_file_exists(agents_readme)

for section in ["Naming Convention", "File Format", "Scope"]:
    assert_markdown_section(agents_readme, section)

assert_file_contains(agents_readme, "fast-forward-", "fast-forward- prefix rule")

# Front-matter field names must be documented.
for field in ["name", "description", "primary-skill", "supporting-skills"]:
    assert_file_contains(agents_readme, f"`{field}`", f"Front matter field '{field}' documented")

# Body section names must be documented.
for section in ["Purpose", "Responsibilities", "Use When", "Boundaries", "Primary Skill", "Supporting Skills"]:
    assert_file_contains(agents_readme, f"`{section}`", f"Body section '{section}' documented")

# ---------------------------------------------------------------------------
# Suite 2: Agent file existence and naming convention
# ---------------------------------------------------------------------------

print("\n=== Suite 2: Agent file existence and naming convention ===")

for filename in NEW_AGENT_FILES:
    path = os.path.join(AGENTS_DIR, filename)
    assert_file_exists(path)

    if filename.startswith("fast-forward-") and filename.endswith(".md"):
        ok(f"Naming convention satisfied: {filename}")
    else:
        fail("Filename must use fast-forward- prefix and .md extension", filename)

# ---------------------------------------------------------------------------
# Suite 3: Agent YAML front matter
# ---------------------------------------------------------------------------

print("\n=== Suite 3: Agent YAML front matter fields ===")

for filename in NEW_AGENT_FILES:
    path = os.path.join(AGENTS_DIR, filename)
    if not os.path.isfile(path):
        continue

    fm = parse_front_matter(path)
    if fm is None:
        fail("Front matter is missing or unparseable", path)
        continue

    ctx = os.path.basename(path)

    assert_front_matter_field(fm, "name", ctx)
    assert_front_matter_field(fm, "description", ctx)
    assert_front_matter_field(fm, "primary-skill", ctx)
    assert_front_matter_field_type(fm, "primary-skill", str, ctx)
    assert_front_matter_field_exists(fm, "supporting-skills", ctx)
    assert_front_matter_field_type(fm, "supporting-skills", list, ctx)

    # 'name' slug must match the slug derived from the filename.
    expected_slug = re.sub(r"^fast-forward-", "", os.path.splitext(filename)[0])
    if isinstance(fm.get("name"), str):
        if fm["name"] == expected_slug:
            ok(f"name slug matches filename slug in {ctx}")
        else:
            fail(
                f"name slug '{fm['name']}' must match filename slug '{expected_slug}'",
                ctx,
            )

# ---------------------------------------------------------------------------
# Suite 4: Agent required markdown sections
# ---------------------------------------------------------------------------

print("\n=== Suite 4: Agent required markdown body sections ===")

for filename in NEW_AGENT_FILES:
    path = os.path.join(AGENTS_DIR, filename)
    if not os.path.isfile(path):
        continue
    for section in REQUIRED_AGENT_SECTIONS:
        assert_markdown_section(path, section)

# ---------------------------------------------------------------------------
# Suite 5: Skill directory structure
# ---------------------------------------------------------------------------

print("\n=== Suite 5: Skill directory structure ===")

for skill_slug in NEW_SKILL_DIRS:
    skill_path = os.path.join(SKILLS_DIR, skill_slug)
    assert_dir_exists(skill_path)
    assert_file_exists(os.path.join(skill_path, "SKILL.md"))
    assert_dir_exists(os.path.join(skill_path, "agents"))
    assert_file_exists(os.path.join(skill_path, "agents", "openai.yaml"))
    assert_dir_exists(os.path.join(skill_path, "references"))

# ---------------------------------------------------------------------------
# Suite 6: SKILL.md YAML front matter
# ---------------------------------------------------------------------------

print("\n=== Suite 6: SKILL.md YAML front matter ===")

for skill_slug in NEW_SKILL_DIRS:
    skill_md = os.path.join(SKILLS_DIR, skill_slug, "SKILL.md")
    if not os.path.isfile(skill_md):
        continue

    fm = parse_front_matter(skill_md)
    ctx = f"{skill_slug}/SKILL.md"
    if fm is None:
        fail("Front matter missing or invalid", ctx)
        continue

    assert_front_matter_field(fm, "name", ctx)
    assert_front_matter_field(fm, "description", ctx)

    expected_slug = re.sub(r"^fast-forward-", "", skill_slug)
    if isinstance(fm.get("name"), str):
        if fm["name"] == expected_slug:
            ok(f"SKILL.md name slug matches directory slug in {ctx}")
        else:
            fail(
                f"SKILL.md name '{fm['name']}' must match directory slug '{expected_slug}'",
                ctx,
            )

# ---------------------------------------------------------------------------
# Suite 7: openai.yaml interface structure
# ---------------------------------------------------------------------------

print("\n=== Suite 7: openai.yaml interface structure ===")

for skill_slug in NEW_SKILL_DIRS:
    yaml_path = os.path.join(SKILLS_DIR, skill_slug, "agents", "openai.yaml")
    if not os.path.isfile(yaml_path):
        continue

    ctx = f"{skill_slug}/agents/openai.yaml"
    content = read_file(yaml_path)
    if content is None:
        continue

    # Parse and validate structure.
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError:
        fail("openai.yaml is not valid YAML", ctx)
        continue

    if not isinstance(data, dict):
        fail("openai.yaml must be a YAML mapping", ctx)
        continue

    if "interface" in data:
        ok(f"interface key present in {ctx}")
    else:
        fail("interface key missing", ctx)
        continue

    iface = data["interface"]
    if not isinstance(iface, dict):
        fail("interface value must be a mapping", ctx)
        continue

    for field in ["display_name", "short_description", "default_prompt"]:
        if field in iface and iface[field]:
            ok(f"interface.{field} present in {ctx}")
        else:
            fail(f"interface.{field} missing or empty", ctx)

    # default_prompt must reference the skill by the $slug convention.
    expected_skill_slug = re.sub(r"^fast-forward-", "", skill_slug)
    prompt = iface.get("default_prompt", "")
    if f"${expected_skill_slug}" in prompt:
        ok(f"default_prompt references ${expected_skill_slug} in {ctx}")
    else:
        fail(f"default_prompt must reference ${expected_skill_slug}", ctx)

# ---------------------------------------------------------------------------
# Suite 8: Skill reference files
# ---------------------------------------------------------------------------

print("\n=== Suite 8: Skill reference files ===")

for skill_slug, refs in REQUIRED_SKILL_REFERENCES.items():
    for ref in refs:
        assert_file_exists(os.path.join(SKILLS_DIR, skill_slug, ref))

# ---------------------------------------------------------------------------
# Suite 9: SKILL.md cross-reference integrity
# ---------------------------------------------------------------------------

print("\n=== Suite 9: SKILL.md cross-reference integrity ===")

for skill_slug in NEW_SKILL_DIRS:
    skill_md = os.path.join(SKILLS_DIR, skill_slug, "SKILL.md")
    if not os.path.isfile(skill_md):
        continue

    content = read_file(skill_md)
    if content is None:
        continue

    # Find all Markdown link targets pointing to files inside references/.
    for ref_file in re.findall(r"\(references/([^)]+)\)", content):
        ref_path = os.path.join(SKILLS_DIR, skill_slug, "references", ref_file)
        if os.path.isfile(ref_path):
            ok(f"Referenced file exists: {skill_slug}/references/{ref_file}")
        else:
            fail("SKILL.md references missing file", f"{skill_slug}/references/{ref_file}")

# ---------------------------------------------------------------------------
# Suite 10: SKILL.md workflow section
# ---------------------------------------------------------------------------

print("\n=== Suite 10: SKILL.md workflow section ===")

for skill_slug in NEW_SKILL_DIRS:
    skill_md = os.path.join(SKILLS_DIR, skill_slug, "SKILL.md")
    if not os.path.isfile(skill_md):
        continue
    assert_markdown_section(skill_md, "Workflow")

# ---------------------------------------------------------------------------
# Suite 11: changelog-generator skill-specific checks
# ---------------------------------------------------------------------------

print("\n=== Suite 11: changelog-generator skill-specific content ===")

cl_skill = os.path.join(SKILLS_DIR, "fast-forward-changelog-generator", "SKILL.md")
if os.path.isfile(cl_skill):
    for cmd in ["changelog:entry", "changelog:check", "changelog:next-version", "changelog:promote", "changelog:show"]:
        assert_file_contains(cl_skill, cmd, f"Command '{cmd}' documented")

    assert_file_contains(cl_skill, "Keep a Changelog", "Keep a Changelog reference")
    assert_markdown_section(cl_skill, "Output Contract")
    assert_markdown_section(cl_skill, "Consumer Repository Notes")

    cat_path = os.path.join(SKILLS_DIR, "fast-forward-changelog-generator", "references", "change-categories.md")
    if os.path.isfile(cat_path):
        for cat in ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]:
            assert_markdown_section(cat_path, cat)

    format_path = os.path.join(SKILLS_DIR, "fast-forward-changelog-generator", "references", "keep-a-changelog-format.md")
    if os.path.isfile(format_path):
        assert_file_contains(format_path, "Footer references", "Footer references section")
        assert_file_contains(format_path, "Section order", "Section order guidance")
        assert_file_contains(format_path, "changelog:entry", "Local command mapping in format reference")

# ---------------------------------------------------------------------------
# Suite 12: create-agentsmd skill-specific checks
# ---------------------------------------------------------------------------

print("\n=== Suite 12: create-agentsmd skill-specific content ===")

ca_skill = os.path.join(SKILLS_DIR, "fast-forward-create-agentsmd", "SKILL.md")
if os.path.isfile(ca_skill):
    assert_markdown_section(ca_skill, "Required Coverage")
    assert_markdown_section(ca_skill, "Writing Rules")
    assert_markdown_section(ca_skill, "Anti-patterns")

    outline_path = os.path.join(SKILLS_DIR, "fast-forward-create-agentsmd", "references", "content-outline.md")
    if os.path.isfile(outline_path):
        assert_markdown_section(outline_path, "Core Sections")
        assert_markdown_section(outline_path, "Quality Checklist")

# ---------------------------------------------------------------------------
# Suite 13: github-issues skill-specific checks
# ---------------------------------------------------------------------------

print("\n=== Suite 13: github-issues skill-specific content ===")

gi_skill = os.path.join(SKILLS_DIR, "fast-forward-github-issues", "SKILL.md")
if os.path.isfile(gi_skill):
    assert_markdown_section(gi_skill, "Output Contract")
    assert_markdown_section(gi_skill, "Fast Forward Defaults")
    assert_markdown_section(gi_skill, "Anti-patterns")

    ac_path = os.path.join(SKILLS_DIR, "fast-forward-github-issues", "references", "architectural-criteria.md")
    if os.path.isfile(ac_path):
        assert_file_contains(ac_path, "Base Block for Code Changes", "Code-change base block heading")
        assert_file_contains(ac_path, "Base Block for Documentation or Content Work", "Docs base block heading")
        assert_file_contains(ac_path, "CLI Add-on Bullets", "CLI add-on bullets heading")
        assert_file_contains(ac_path, "Testing Expectations", "Testing expectations section")

    ctx_path = os.path.join(SKILLS_DIR, "fast-forward-github-issues", "references", "context.md")
    if os.path.isfile(ctx_path):
        assert_markdown_section(ctx_path, "Repository Resolution")
        assert_markdown_section(ctx_path, "Authentication")
        assert_file_contains(ctx_path, "gh auth status", "auth status command")
        assert_file_contains(ctx_path, "gh auth refresh", "auth refresh command")

# ---------------------------------------------------------------------------
# Suite 14: Agent primary-skill references a known skill slug
# ---------------------------------------------------------------------------

print("\n=== Suite 14: Agent primary-skill references a resolvable skill slug ===")

skill_slugs = known_skill_slugs()

for filename in NEW_AGENT_FILES:
    path = os.path.join(AGENTS_DIR, filename)
    if not os.path.isfile(path):
        continue

    fm = parse_front_matter(path)
    if fm is None:
        continue

    assert_front_matter_field_type(fm, "primary-skill", str, filename)
    if not isinstance(fm.get("primary-skill"), str):
        continue

    primary = fm["primary-skill"]
    if primary in skill_slugs:
        ok(f"primary-skill '{primary}' resolves to a known skill in {filename}")
    else:
        fail(f"primary-skill '{primary}' does not match any installed skill slug", filename)

# ---------------------------------------------------------------------------
# Suite 15: Agent supporting-skills reference known skill slugs
# ---------------------------------------------------------------------------

print("\n=== Suite 15: Agent supporting-skills reference resolvable skill slugs ===")

for filename in NEW_AGENT_FILES:
    path = os.path.join(AGENTS_DIR, filename)
    if not os.path.isfile(path):
        continue

    fm = parse_front_matter(path)
    if fm is None or "supporting-skills" not in fm:
        continue

    supporting = fm["supporting-skills"]
    if not isinstance(supporting, list):
        fail(f"supporting-skills must be a list", filename)
        continue

    for idx, slug in enumerate(supporting):
        if not isinstance(slug, str):
            fail(f"supporting-skills[{idx}] must be a string", filename)
            continue

    if not supporting:
        ok(f"No supporting-skills declared (empty list OK) in {filename}")
        continue

    if isinstance(supporting, list):
        for slug in supporting:
            if slug in skill_slugs:
                ok(f"supporting-skill '{slug}' resolves to a known skill in {filename}")
            else:
                fail(f"supporting-skill '{slug}' does not match any installed skill slug", filename)

# ---------------------------------------------------------------------------
# Suite 16: Boundary and regression checks
# ---------------------------------------------------------------------------

print("\n=== Suite 16: Boundary and regression checks ===")

# agents/README.md must NOT start with YAML front matter.
readme_content = read_file(agents_readme) if os.path.isfile(agents_readme) else ""
if readme_content and not readme_content.startswith("---"):
    ok("agents/README.md correctly has no YAML front matter")
elif readme_content:
    fail("agents/README.md must not start with YAML front matter", agents_readme)

# Each agent file must start with YAML front matter.
for filename in NEW_AGENT_FILES:
    path = os.path.join(AGENTS_DIR, filename)
    if not os.path.isfile(path):
        continue
    content = read_file(path)
    if content and content.startswith("---"):
        ok(f"YAML front matter delimiter present in {filename}")
    else:
        fail("Agent file must start with --- YAML front matter", filename)

# Verify no agent has a trivially short description.
for filename in NEW_AGENT_FILES:
    path = os.path.join(AGENTS_DIR, filename)
    if not os.path.isfile(path):
        continue
    fm = parse_front_matter(path)
    if fm and isinstance(fm.get("description"), str) and len(fm["description"]) >= 10:
        ok(f"Description is non-trivially long in {filename}")
    else:
        fail("description must be at least 10 characters", filename)

# Verify each new SKILL.md description is non-trivially long.
for skill_slug in NEW_SKILL_DIRS:
    skill_md = os.path.join(SKILLS_DIR, skill_slug, "SKILL.md")
    if not os.path.isfile(skill_md):
        continue
    fm = parse_front_matter(skill_md)
    if fm and isinstance(fm.get("description"), str) and len(fm["description"]) >= 20:
        ok(f"SKILL.md description is non-trivially long in {skill_slug}")
    else:
        fail("SKILL.md description must be at least 20 characters", skill_slug)

# Verify openai.yaml files are non-stub (larger than 50 bytes).
for skill_slug in NEW_SKILL_DIRS:
    yaml_path = os.path.join(SKILLS_DIR, skill_slug, "agents", "openai.yaml")
    if not os.path.isfile(yaml_path):
        continue
    size = os.path.getsize(yaml_path)
    if size >= 50:
        ok(f"openai.yaml is not a stub (size {size} bytes) in {skill_slug}")
    else:
        fail("openai.yaml appears to be a stub or empty", skill_slug)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

total = passed + failed
print(f"\n=== Results: {passed}/{total} passed", end="")
if failed:
    print(f", {failed} failed", end="")
print(" ===")

if failed:
    print("\nFailed checks:")
    for err in failures:
        print(f"  {err}")
    sys.exit(1)

print("All checks passed.")
sys.exit(0)
