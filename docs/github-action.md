# GitHub Action Usage

ChangelogGenie can be used as a GitHub Action to generate a technical Markdown changelog from GitHub commits.

This first Action version generates only the technical changelog. It does not call the OpenAI API.

## Minimal workflow

Create this file in your repository:

.github/workflows/changeloggenie.yml

Use this workflow:

    name: Generate changelog

    on:
      workflow_dispatch:
        inputs:
          start_date:
            description: Start date in YYYY-MM-DD format
            required: true
          end_date:
            description: End date in YYYY-MM-DD format
            required: true
          version:
            description: Optional changelog version label
            required: false
            default: ""

    permissions:
      contents: read

    jobs:
      changelog:
        runs-on: ubuntu-latest

        steps:
          - name: Generate changelog
            uses: Ubuntu-123/changeloggenie-prototype@v0.1.7
            with:
              start_date: ${{ inputs.start_date }}
              end_date: ${{ inputs.end_date }}
              version: ${{ inputs.version }}
              output_path: changelog-output.md
              github_token: ${{ github.token }}

          - name: Upload changelog artifact
            uses: actions/upload-artifact@v4
            with:
              name: changelog-output
              path: changelog-output.md

## Inputs

owner: optional. Defaults to the current repository owner.

repo: optional. Defaults to the current repository name.

start_date: required. Start date in YYYY-MM-DD format.

end_date: required. End date in YYYY-MM-DD format.

version: optional. Version label for the changelog heading.

output_path: optional. Defaults to changelog.md.

github_token: optional. Helps reduce GitHub API rate-limit issues.

## Output

The Action writes a Markdown changelog file to output_path.

It also exposes changelog_path, which contains the generated changelog file path.

## Notes

This Action currently generates a technical changelog only.

It does not commit files back to the repository.

It does not open pull requests.

It does not call OpenAI.

AI-assisted changelog transformation remains available only through the local changeloggenie-ai command.
