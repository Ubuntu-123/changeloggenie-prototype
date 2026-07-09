# Roadmap

ChangelogGenie is currently a public read-only CLI and GitHub Action for generating categorized technical Markdown changelog drafts from GitHub commits.

The current public Action is intentionally safe by default: it does not call OpenAI, does not commit files, does not open pull requests, and only generates a Markdown artifact.

## Current version

The current version supports:

- technical changelog generation from public GitHub commits
- date-range based changelog generation
- Markdown output
- pattern-based commit categorization
- installable local CLI commands
- optional `GITHUB_TOKEN` support for higher GitHub API rate limits
- GitHub Action usage from repository workflows
- manual workflow validation against external public repositories
- requested date range and actual commit date range headers
- optional local AI-assisted transformation into customer-facing JSON
- local OpenAI API runner using the user's own API key
- stdin pipeline support

## Near-term priorities

- improve commit categorization for real-world repositories
- add clearer examples for common commit patterns such as release commits, dependency updates, CI updates, and documentation-only changes
- test the Action on more external public repositories
- keep the GitHub Action read-only and artifact-only
- improve troubleshooting notes for GitHub API rate limits, workflow permissions, and `GITHUB_TOKEN`
- refine README and Marketplace wording based on actual usage signals

## Monetization position

The current repository is public and MIT licensed. Hard license or trial enforcement over the public GitHub Action is not a near-term priority because the code can be inspected, forked, and modified.

GitHub Marketplace is currently treated as a distribution and discovery channel for the Action, not as a billing layer.

A paid or Pro layer may be considered later only if it provides value that is not just hard enforcement around the public MIT Action, such as:

- hosted or server-side AI transformation
- private repository support
- managed release-note publishing
- dashboard or project history
- team/project configuration
- controlled templates or server-side output profiles

Any future paid backend should prefer existing infrastructure before adding new recurring costs.

## Later possibilities

- BYOK AI workflow mode using the user's own OpenAI API key through GitHub Secrets
- GitHub App for installed repository access
- custom output templates
- changelog history
- release note publishing workflows
- team/project configuration
