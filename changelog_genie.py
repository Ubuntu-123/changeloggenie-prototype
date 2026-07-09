#!/usr/bin/env python3
"""
ChangelogGenie: A minimal prototype for generating categorized changelog drafts.

Reads public GitHub commits for a given owner/repo and date range,
then outputs a categorized changelog in Markdown format.
"""

import argparse
import sys
from datetime import datetime
from typing import List, Dict
import re


class ChangelogGenie:
    """Generate categorized changelog from GitHub commits."""

    # Category patterns for commit classification
    CATEGORIES = {
        "Features": [
            r"^feat:",
            r"^feature:",
            r"add support for",
            r"add.*runner",
            r"add.*api",
            r"add.*generator",
            r"add.*github action",
            r"add optional.*support",
            r"optional github token support",
            r"allow.*action",
            r"implement",
            r"new.*feature",
            r"support.*input",
            r"support.*pipeline",
        ],
        "Bug Fixes": [
            r"^fix\b",
            r"^fix:",
            r"^bugfix:",
            r"^bug:",
            r"resolve.*issue",
            r"fix.*bug",
            r"auto fixes",
        ],
        "Improvements": [
            r"^clarify\b",
            r"^improve\b",
            r"improvement",
            r"expand.*categorization",
            r"expand.*patterns",
            r"enhance",
            r"align .*state",
        ],
        "Performance": [
            r"perf:",
            r"optimize",
            r"performance",
            r"speed.*up",
            r"clean.*cli.*output",
        ],
        "Documentation": [
            r"^docs:",
            r"^document\b",
            r"documentation",
            r"readme",
            r"roadmap",
            r"support.*docs",
            r"project docs",
            r"testing docs",
            r"privacy",
            r"update.*docs",
            r"clean up.*changelog",
            r"changelog release sections",
            r"reviewed project changelog",
            r"project changelog",
            r"wording",
            r"badge",
        ],
        "CI/CD": [
            r"^ci:",
            r"\bworkflow\b",
            r"github-actions",
            r"actions versions",
            r"pre-commit",
        ],
        "Release Management": [
            r"release version",
            r"start version",
            r"prepare v?[0-9].*release",
            r"publishing.*pypi",
            r"per-release",
        ],
        "Dependencies": [
            r"^deps:",
            r"^chore\(deps\)",
            r"^bump\b",
            r"update.*depend",
            r"update requirements",
            r"bump.*version",
        ],
        "Refactoring": [
            r"^refactor:",
            r"refactor",
        ],
        "Maintenance": [
            r"metadata",
            r"cleanup",
            r"clean up",
            r"address mypy",
            r"typehint",
            r"annotation",
        ],
        "Breaking Changes": [
            r"^BREAKING",
            r"breaking change",
            r"breaking:",
        ],
    }

    def __init__(self):
        self.github_api_url = "https://api.github.com"

    @staticmethod
    def fetch_commits(
        owner: str, repo: str, start_date: str, end_date: str
    ) -> List[Dict]:
        """
        Fetch commits from GitHub for a given date range.

        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            List of commit dictionaries
        """
        commits = []
        page = 1
        per_page = 100

        import os
        import requests

        github_token = os.getenv("GITHUB_TOKEN")

        while True:
            try:
                url = f"https://api.github.com/repos/{owner}/{repo}/commits"
                params = {
                    "since": f"{start_date}T00:00:00Z",
                    "until": f"{end_date}T23:59:59Z",
                    "per_page": per_page,
                    "page": page,
                }
                headers = {
                    "Accept": "application/vnd.github.v3+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                }

                if github_token:
                    headers["Authorization"] = f"Bearer {github_token}"

                response = requests.get(url, params=params, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()
                if not data:
                    break

                commits.extend(data)
                page += 1

            except requests.exceptions.RequestException as e:
                print(f"Error fetching commits: {e}", file=sys.stderr)
                break

        return commits

    @staticmethod
    def categorize_commit(message: str) -> str:
        """
        Categorize a commit based on its message.

        Args:
            message: Commit message

        Returns:
            Category name
        """
        first_line = message.split("\n")[0]

        for category, patterns in ChangelogGenie.CATEGORIES.items():
            for pattern in patterns:
                if re.search(pattern, first_line, re.IGNORECASE):
                    return category

        return "Other"

    @staticmethod
    def group_commits_by_category(commits: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Group commits by category.

        Args:
            commits: List of commit dictionaries

        Returns:
            Dictionary mapping category names to lists of commits
        """
        categorized = {category: [] for category in ChangelogGenie.CATEGORIES.keys()}
        categorized["Other"] = []

        for commit in commits:
            message = commit.get("commit", {}).get("message", "")
            category = ChangelogGenie.categorize_commit(message)
            categorized[category].append(commit)

        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}

    @staticmethod
    def _get_commit_date(commit: Dict) -> str:
        """Extract and format commit date."""
        date_str = commit.get("commit", {}).get("author", {}).get("date", "")
        if date_str:
            # Parse ISO format and return YYYY-MM-DD
            return date_str.split("T")[0]
        return "Unknown"

    @staticmethod
    def _generate_category_section(
        category: str, commits: List[Dict], owner: str, repo: str
    ) -> str:
        """
        Generate a Markdown section for a category.

        Args:
            category: Category name
            commits: List of commits in this category
            owner: Repository owner
            repo: Repository name

        Returns:
            Markdown section
        """
        section = f"## {category}\n\n"

        for commit in commits:
            message = commit.get("commit", {}).get("message", "").split("\n")[0]
            sha = commit.get("sha", "")[:7]
            author = commit.get("commit", {}).get("author", {}).get("name", "Unknown")
            date = ChangelogGenie._get_commit_date(commit)

            # Clean up message
            message = message.replace("fix: ", "").replace("feat: ", "")
            message = message.replace("docs: ", "").replace("refactor: ", "")

            section += f"- {message} ([{sha}](https://github.com/{owner}/{repo}/commit/{commit.get('sha', '')})) - {author} ({date})\n"

        section += "\n"
        return section

    @staticmethod
    def generate_markdown(
        commits: List[Dict],
        owner: str,
        repo: str,
        start_date: str,
        end_date: str,
        version: str = None,
    ) -> str:
        """
        Generate a Markdown changelog from categorized commits.

        Args:
            commits: List of commit dictionaries
            owner: Repository owner
            repo: Repository name
            start_date: Requested start date in YYYY-MM-DD format
            end_date: Requested end date in YYYY-MM-DD format
            version: Version identifier (optional)

        Returns:
            Markdown-formatted changelog
        """
        if version:
            header = f"# Changelog - {version}\n\n"
        else:
            header = f"# Changelog\n\n"

        header += f"**Requested Date Range:** {start_date} to {end_date}\n"

        if not commits:
            header += "\nNo commits found for the specified date range.\n"
            return header

        categorized = ChangelogGenie.group_commits_by_category(commits)

        # Generate header
        commit_date_range = f"{ChangelogGenie._get_commit_date(commits[-1])} to {ChangelogGenie._get_commit_date(commits[0])}"
        header += f"**Commit Date Range:** {commit_date_range}\n"
        header += f"**Repository:** [{owner}/{repo}](https://github.com/{owner}/{repo})\n\n"
        header += f"**Total Commits:** {len(commits)}\n\n"

        # Generate category sections
        markdown = header
        for category in ChangelogGenie.CATEGORIES.keys():
            if category in categorized and categorized[category]:
                markdown += ChangelogGenie._generate_category_section(
                    category, categorized[category], owner, repo
                )

        if "Other" in categorized and categorized["Other"]:
            markdown += ChangelogGenie._generate_category_section(
                "Other", categorized["Other"], owner, repo
            )

        return markdown


def validate_date(date_string: str) -> str:
    """
    Validate that a date string is in YYYY-MM-DD format.

    Args:
        date_string: Date string to validate

    Returns:
        The validated date string

    Raises:
        argparse.ArgumentTypeError: If date format is invalid
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return date_string
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date format: {date_string}. Use YYYY-MM-DD format."
        )


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Generate a categorized changelog from GitHub commits."
    )
    parser.add_argument(
        "owner",
        help="GitHub repository owner (username or organization)",
    )
    parser.add_argument(
        "repo",
        help="GitHub repository name",
    )
    parser.add_argument(
        "start_date",
        type=validate_date,
        help="Start date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "end_date",
        type=validate_date,
        help="End date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Version identifier for the changelog header (optional)",
    )

    args = parser.parse_args()

    if args.start_date > args.end_date:
        print("Error: start_date must be earlier than or equal to end_date.", file=sys.stderr)
        sys.exit(1)

    print(
        f"Fetching commits from {args.owner}/{args.repo} "
        f"({args.start_date} to {args.end_date})...",
        file=sys.stderr,
    )

    commits = ChangelogGenie.fetch_commits(
        args.owner, args.repo, args.start_date, args.end_date
    )

    if not commits:
        print("No commits found.", file=sys.stderr)
        changelog = ChangelogGenie.generate_markdown(
            commits, args.owner, args.repo, args.start_date, args.end_date, args.version
        )
        print(changelog)
        return

    print(f"Found {len(commits)} commits. Generating changelog...", file=sys.stderr)
    changelog = ChangelogGenie.generate_markdown(
        commits, args.owner, args.repo, args.start_date, args.end_date, args.version
    )

    print(changelog)


if __name__ == "__main__":
    main()
