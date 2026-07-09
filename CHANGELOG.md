# Changelog

All notable changes to this project will be documented in this file.

ChangelogGenie is a public read-only CLI and GitHub Action for generating technical Markdown changelog drafts from GitHub commits. This changelog is based on generated commit output and manually reviewed before publication.

## Unreleased

### Changed

- Added push-triggered validation for the GitHub Action workflow on main.
- Added categorization coverage for test-related maintenance commits.
- Added categorization coverage for refinement commits.
- Refined commit categorization patterns after post-implementation audit.
- Expanded commit categorization to reduce valid commits falling into `Other`.
- Removed remaining outdated prototype wording from current README sections.
- Updated support, privacy, testing, and roadmap wording to match the current public Action state.
- Updated public documentation wording to remove outdated prototype framing.
- Updated the roadmap to reflect the current public CLI and GitHub Action state.
- Documented the current monetization position for the public MIT Action.

## v0.1.6 - 2026-07-03

### Added

- Added a GitHub Action status badge to the README.
- Added manual workflow inputs for validating the ChangelogGenie Action against external public repositories.
- Added manual GitHub Action validation notes.
- Documented successful external repository validation for the GitHub Action.
- Added a fuller GitHub Action Quick Start workflow example to the README.

### Changed

- Clarified README positioning for CLI, GitHub Action, and optional local AI-assisted usage.
- Updated current GitHub Action usage examples to `Ubuntu-123/changeloggenie-prototype@v0.1.6`.

### Fixed

- Clarified changelog date headers by separating the requested date range from the actual commit date range.

## v0.1.5 - 2026-07-02

### Added

- Added composite GitHub Action for generating technical Markdown changelogs.
- Added `action.yml` with configurable repository, date range, version label, output path, and optional GitHub token.
- Added GitHub Action usage documentation.
- Added README link to GitHub Action documentation.
- Added package version bump to `0.1.5`.

### Notes

- The Action generates a technical changelog only.
- The Action does not call OpenAI.
- The Action does not commit files, open pull requests, or write to repositories.
- The generated changelog can be uploaded as a workflow artifact.

## v0.1.4 - 2026-07-02

### Added

- Added optional `GITHUB_TOKEN` support for GitHub API requests.
- Added GitHub API version header for commit fetching.
- Added README documentation for using `GITHUB_TOKEN`.

### Changed

- Moved GitHub fetch errors to stderr so redirected Markdown output stays clean.

## v0.1.3 - 2026-07-02

### Added

- Added Python package metadata with `pyproject.toml`.
- Added editable local installation support.
- Added console commands: `changeloggenie` and `changeloggenie-ai`.
- Added `.gitignore` for Python cache, build, and environment files.

## v0.1.2 - 2026-07-02

### Added

- Added MIT license file.
- Added reviewed project changelog.
- Added support guide for issues, feedback, and sensitive reports.
- Added privacy notes covering public GitHub API usage, optional OpenAI API usage, and bring-your-own-key operation.
- Added project roadmap documentation.
- Added README links to project documentation.

## v0.1.1 - 2026-05-23

### Fixed

- Fixed CLI help behavior so `--help` can run before installing optional runtime dependencies.
- Returned a non-zero exit code when the start date is later than the end date.
- Improved categorization for release-relevant commits.
- Added a no-key smoke test for the OpenAI API runner.

### Changed

- Updated testing documentation based on external prototype feedback.

## v0.1.0 - 2026-05-21

### Added

- Added initial public CLI prototype for generating technical changelog drafts from public GitHub commits.
- Added date-range based changelog generation.
- Added Markdown changelog output.
- Added pattern-based commit categorization.
- Added optional version heading support.
- Added AI-assisted business changelog prompt examples.
- Added customer-facing JSON output examples.
- Added OpenAI API runner using the user's own `OPENAI_API_KEY`.
- Added stdin pipeline support for passing generated technical changelog output into the AI runner.
- Added local testing guide.
- Added example technical and business changelog files.

### Notes

- The prototype is local-only.
- It does not require a GitHub token for public repositories.
- It does not write to repositories.
- AI-assisted mode is optional and requires the user to provide their own OpenAI API key.
