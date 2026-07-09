from changelog_genie import ChangelogGenie


def test_categorizes_common_commit_messages():
    cases = {
        "feat: add export command": "Features",
        "Add optional GitHub token support": "Features",
        "fix super call in list comprehension": "Bug Fixes",
        "Fix jinja_loader typehint": "Bug Fixes",
        "Clarify requested and commit date ranges": "Improvements",
        "Refine commit categorization patterns": "Improvements",
        "ci: add ChangelogGenie demo workflow": "CI/CD",
        "[pre-commit.ci] pre-commit autoupdate": "CI/CD",
        "release version 3.0.2": "Release Management",
        "Prepare v0.1.6 release": "Release Management",
        "Bump the python-requirements group in /requirements with 6 updates": "Dependencies",
        "chore(deps): update requests": "Dependencies",
        "address mypy strict findings": "Maintenance",
        "Add Python package metadata": "Maintenance",
        "Add categorization regression tests": "Maintenance",
        "Document v0.1.6 external Action validation": "Documentation",
        "Update roadmap for current Action state": "Documentation",
        "refactor: split parser helpers": "Refactoring",
        "BREAKING: remove legacy output format": "Breaking Changes",
    }

    for message, expected in cases.items():
        assert ChangelogGenie.categorize_commit(message) == expected


def test_keeps_ambiguous_commits_in_other():
    cases = [
        "Initial commit",
        "Merge branch '3.0.x'",
        "untag without object_hook",
    ]

    for message in cases:
        assert ChangelogGenie.categorize_commit(message) == "Other"
