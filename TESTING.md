# Testing ChangelogGenie

This guide explains how to test the current ChangelogGenie local CLI and optional AI-assisted runner.

## What this guide covers

ChangelogGenie has two testable layers:

1. Technical changelog generation from public GitHub commits.
2. AI-assisted transformation of the technical changelog into customer-facing JSON.

The local CLI and AI-assisted runner can be tested without a hosted account system. The GitHub Action is documented separately in `docs/github-action.md`.

## Requirements

- Python 3.12 or compatible Python 3 version
- GitHub access to public repositories
- An OpenAI API key for the AI runner

Install dependencies:

```bash
pip install -r requirements.txt
```

## 1. Test the technical changelog generator

Run:

```bash
python changelog_genie.py Ubuntu-123 changeloggenie-prototype 2026-05-20 2026-05-21
```

Expected result:

- Markdown output
- a `# Changelog` heading
- repository and date range metadata
- categorized commit entries

To save the output:

```bash
python changelog_genie.py Ubuntu-123 changeloggenie-prototype 2026-05-20 2026-05-21 > technical-changelog.md
```
## 2. Test the AI business changelog runner with a saved file

Set your OpenAI API key as an environment variable. Do not commit API keys.

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Run:

```bash
python business_changelog_ai.py examples/real_repo_technical_changelog.md
```

Expected result:

- valid JSON
- the keys `features`, `improvements`, `fixes`, and `ignored`
- no markdown or explanatory text outside the JSON

## 3. Test the full pipeline

Run the technical generator and pipe its output directly into the AI runner:

```bash
python changelog_genie.py Ubuntu-123 changeloggenie-prototype 2026-05-20 2026-05-21 \
  | python business_changelog_ai.py -
```

To save the AI output:

```bash
python changelog_genie.py Ubuntu-123 changeloggenie-prototype 2026-05-20 2026-05-21 \
  | python business_changelog_ai.py - \
  > examples/real_repo_business_output_pipeline.json
```

Validate the JSON:

```bash
python -m json.tool examples/real_repo_business_output_pipeline.json >/dev/null && echo "JSON OK"
```
## Safety checks

Before committing, verify that no API key was added to the repository:

```bash
git grep -n "sk-" || true
git status --short
```

Expected result:

- no `sk-` key appears
- only intentional files are modified

## Current limitations

- public repositories only for the technical changelog generator
- local CLI and GitHub Action only
- no hosted API
- no database
- no GitHub App installation flow
- no automatic publishing of changelogs

## No-key smoke test

You can verify that the AI runner fails safely without an API key.

Command:

unset OPENAI_API_KEY
python business_changelog_ai.py examples/real_repo_technical_changelog.md
echo $?

Expected result:

- ERROR: OPENAI_API_KEY is not set.
- exit code 2
