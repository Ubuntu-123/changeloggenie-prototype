# Changelog

All notable changes to this project will be documented in this file.

ChangelogGenie is currently an early prototype. This changelog is based on generated commit output and manually reviewed before publication.

## Unreleased

### Added

- Added Python package metadata with `pyproject.toml`.
- Added editable local installation support.
- Added console commands: `changeloggenie` and `changeloggenie-ai`.
- Added `.gitignore` for Python cache, build, and environment files.
- Added MIT license file.
- Added support guide for issues, feedback, and sensitive reports.
- Added privacy notes covering public GitHub API usage, optional OpenAI API usage, and bring-your-own-key operation.
- Added project roadmap documentation.

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
