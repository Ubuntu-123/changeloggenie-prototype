# Privacy Notes

ChangelogGenie has two modes:

1. Technical changelog generation from public GitHub commits.
2. Optional AI-assisted transformation of a technical changelog into customer-facing JSON.

## Technical changelog mode

The technical changelog generator reads public GitHub commit metadata from the GitHub API.

It does not require a GitHub token for public repositories.

It does not write to the target repository.

## AI-assisted mode

The AI runner uses the OpenAI API only when the user runs `business_changelog_ai.py` and provides their own `OPENAI_API_KEY`.

When AI-assisted mode is used, the technical changelog text is sent to OpenAI for transformation into customer-facing JSON.

Do not use AI-assisted mode with private, confidential, or sensitive repository data unless you understand and accept the data handling implications of the API provider you choose.

## API keys

Do not commit API keys to this repository.

Set API keys through environment variables, for example:

OPENAI_API_KEY='your-api-key-here'

## Current project status

ChangelogGenie is currently a public read-only CLI and GitHub Action. It does not currently provide a hosted service, database, account system, or persistent changelog storage.
