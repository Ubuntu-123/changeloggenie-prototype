# ChangelogGenie

[![Test ChangelogGenie Action](https://github.com/Ubuntu-123/changeloggenie-prototype/actions/workflows/test-changeloggenie-action.yml/badge.svg)](https://github.com/Ubuntu-123/changeloggenie-prototype/actions/workflows/test-changeloggenie-action.yml)

Generate a deterministic technical Markdown changelog directly from GitHub commits.

ChangelogGenie is a lightweight, read-only GitHub Action and CLI that:

- works with ordinary Git commit history — no Conventional Commits required;
- automatically categorizes commits into features, fixes, performance, documentation, maintenance, and other technical categories;
- accepts an explicit calendar date range;
- preserves commit metadata and links to the source commits;
- does not modify the repository, create commits, or open pull requests.

## Real output example

ChangelogGenie Free was validated against the public `outline/outline` repository.

**Selected date range:** March 15–18, 2026  
**Commits collected:** 21  
**Output:** deterministic categorized Markdown changelog

ChangelogGenie generates the Markdown file inside the GitHub Actions workflow; the example below uploads it as a workflow artifact for review or downstream processing.

The Quick Start below targets the repository where the workflow runs; replace the date range as needed. It is separate from the outline/outline validation example above.

## Quick Start

```yaml
- name: Generate changelog
  uses: Ubuntu-123/changeloggenie-prototype@v0.1.7
  with:
    owner: ${{ github.repository_owner }}
    repo: ${{ github.event.repository.name }}
    start_date: "2026-08-01"
    end_date: "2026-08-31"
    version: "draft"
    output_path: "changelog-output.md"
    github_token: ${{ secrets.GITHUB_TOKEN }}

- name: Upload changelog artifact
  uses: actions/upload-artifact@v4
  with:
    name: changelog-output
    path: changelog-output.md
```

## Current Product Shape

ChangelogGenie currently has three usable layers:

- local CLI for generating technical Markdown changelogs from public GitHub commits
- GitHub Action for generating technical Markdown changelogs in repository workflows
- optional local AI-assisted runner for transforming technical changelogs into customer-facing JSON, using the user's own OpenAI API key

The GitHub Action does not call OpenAI, does not commit files, and does not open pull requests. It generates a Markdown artifact only.

## Quick Start: GitHub Action

Use the released Action from another repository:

```yaml
name: Generate changelog

on:
  workflow_dispatch:

jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - name: Generate changelog
        uses: Ubuntu-123/changeloggenie-prototype@v0.1.7
        with:
          owner: ${{ github.repository_owner }}
          repo: ${{ github.event.repository.name }}
          start_date: "2026-01-01"
          end_date: "2026-12-31"
          version: "draft"
          output_path: "changelog-output.md"
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

The Action accepts a date range, optional version label, output path, and optional `github_token`. It generates a Markdown file inside the workflow run only.

More details:

- [GitHub Action usage](docs/github-action.md)
- [GitHub Action validation](docs/action-validation.md)

## Project Documentation

- [Changelog](CHANGELOG.md)
- [Testing guide](TESTING.md)
- [Support](SUPPORT.md)
- [Privacy notes](docs/privacy.md)
- [Roadmap](docs/roadmap.md)
- [GitHub Action usage](docs/github-action.md)
- [GitHub Action validation](docs/action-validation.md)

## Usage

### Basic Usage

```bash
python changelog_genie.py <owner> <repo> <start_date> <end_date>
```

### With Version Identifier

```bash
python changelog_genie.py --version <version> <owner> <repo> <start_date> <end_date>
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `owner` | string | GitHub repository owner (username or organization) |
| `repo` | string | GitHub repository name |
| `start_date` | string | Start date in `YYYY-MM-DD` format |
| `end_date` | string | End date in `YYYY-MM-DD` format |
| `--version` | string (optional) | Version identifier for the changelog header |

### Installed CLI usage

After installing the project with `python -m pip install -e .`, you can run:

    changeloggenie <owner> <repo> <start_date> <end_date>

For the optional AI-assisted layer:

    changeloggenie-ai examples/real_repo_technical_changelog.md

## AI-Assisted Business Changelog Layer

The repository includes prompt and example files for converting technical changelog content into customer-facing SaaS changelog entries:

- `prompts/business_changelog_system.md` – system instructions for the AI transformation layer
- `examples/business_changelog_input.txt` – synthetic test input
- `examples/business_changelog_expected.json` – expected JSON output for the synthetic test
- `examples/real_repo_technical_changelog.md` – real technical changelog generated from this repository
- `examples/real_repo_business_output.json` – AI-produced business changelog output for the real repository example
- `examples/real_repo_business_output_api.json` – OpenAI API-produced business changelog output for the same real repository example

The AI layer is designed to:

- ignore internal-only commits, merge commits, documentation cleanup, and tooling changes unless they have explicit user impact
- avoid inventing features, metrics, or business value
- return strictly valid JSON with `features`, `improvements`, `fixes`, and `ignored`
- rewrite included changes as customer-facing changelog entries rather than lightly rephrased commit messages

The current API runner is intentionally minimal and local. It reads a technical changelog file and prints validated JSON output.

### Running the AI API Runner

Set your OpenAI API key as an environment variable. Do not commit API keys to the repository.

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Then run:

```bash
python business_changelog_ai.py examples/real_repo_technical_changelog.md
```

To save the output:

```bash
python business_changelog_ai.py examples/real_repo_technical_changelog.md > examples/real_repo_business_output_api.json
```

The script validates that the model output is parseable JSON before printing the formatted result.


## Example Output

```markdown
# Changelog - v19.0.0

**Requested Date Range:** 2026-05-01 to 2026-05-20
**Commit Date Range:** 2026-05-13 to 2026-05-20
**Repository:** [facebook/react](https://github.com/facebook/react)

**Total Commits:** 42

## Features

- Add new hooks API ([a1b2c3d](https://github.com/facebook/react/commit/a1b2c3d)) - John Doe (2026-05-18)

## Bug Fixes

- Fix memory leak in reconciler ([b2c3d4e](https://github.com/facebook/react/commit/b2c3d4e)) - Jane Smith (2026-05-17)

## Documentation

- Update README with new API docs ([c3d4e5f](https://github.com/facebook/react/commit/c3d4e5f)) - Alex Johnson (2026-05-16)
```

## How It Works

1. **Fetch**: Queries the GitHub API endpoint `/repos/{owner}/{repo}/commits` with `since` and `until` parameters
2. **Parse**: Extracts commit messages and metadata (author, date, SHA)
3. **Categorize**: Classifies each commit into one of these categories:
   - **Features**: New functionality
   - **Bug Fixes**: Resolves issues
   - **Improvements**: Clarifications and non-breaking enhancements
   - **Performance**: Optimizations
   - **Documentation**: Doc updates
   - **CI/CD**: Workflow, automation, and pre-commit updates
   - **Release Management**: Versioning and publishing work
   - **Dependencies**: Dependency updates
   - **Refactoring**: Code restructuring
   - **Maintenance**: Metadata, cleanup, test coverage, and type-checking work
   - **Breaking Changes**: API-incompatible changes
   - **Other**: Unclassified commits
4. **Generate**: Produces a formatted Markdown changelog with links to commit details

## API Endpoint

ChangelogGenie uses the public GitHub API:

```
GET /repos/{owner}/{repo}/commits
```

**Parameters:**
- `since`: ISO 8601 date (start of range, inclusive)
- `until`: ISO 8601 date (end of range, inclusive)

**No authentication required** – works with public repositories only.

### Optional GitHub token

For public repositories, ChangelogGenie can run without a GitHub token.

To reduce GitHub API rate-limit issues, set `GITHUB_TOKEN` before running the CLI:

    export GITHUB_TOKEN='your-github-token-here'

When `GITHUB_TOKEN` is set, ChangelogGenie sends it only as an Authorization header to the GitHub API.

## Limitations

- **Public repositories only**: Cannot access private repository commits without authentication
- **API rate limiting**: GitHub's public API allows 60 requests/hour unauthenticated
- **Max commits**: Returns up to 250 commits per request (paginated)
- **Pattern-based categorization**: Uses regex matching on commit messages; custom categories are not currently supported
- **No filtering**: Returns all commits in date range

## Not Included

By design, ChangelogGenie does not include:

- ❌ Required login flow or hosted account system
- ❌ Database persistence
- ❌ File writing operations
- ❌ Deployment configuration
- ❌ GitHub write actions
- ❌ Web server or hosted API
- ❌ Persistent storage for AI-generated changelogs
- ❌ Configuration files
- ❌ Interactive CLI UI

## Development

### Installation

```bash
pip install -r requirements.txt
```

### Running the CLI

```bash
python changelog_genie.py facebook react 2026-05-01 2026-05-20
```

### Running with Version

```bash
python changelog_genie.py --version "Release v19.0" facebook react 2026-05-01 2026-05-20
```

### Example: Last 30 Days

```bash
python changelog_genie.py nodejs node 2026-04-20 2026-05-20
```

## Future Enhancements

Potential improvements not currently included:

- Optional GitHub token support for private repositories
- Database storage of changelog history
- Custom category configuration
- Output to file (Markdown, JSON, HTML)
- Advanced filtering (author, labels, commit type)
- Web UI for interactive changelog generation
- Slack/email integration
- Changelog comparison across versions

## License

MIT
