#!/usr/bin/env python3
"""
ChangelogGenie: A minimal prototype for generating categorized changelog drafts.

Reads public GitHub commits for a given owner/repo and date range,
then outputs a categorized changelog in Markdown format.
"""

import argparse
import sys
import requests
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
            r"add.*support",
            r"implement",
            r"new.*feature",
        ],
        "Bug Fixes": [
            r"^fix:",
            r"^bugfix:",
            r"^bug:",
            r"resolve.*issue",
            r"fix.*bug",
        ],
        "Performance": [
            r"perf:",
            r"optimize",
            r"performance",
            r"speed.*up",
        ],
        "Documentation": [
            r"^docs:",
            r"documentation",
            r"readme",
            r"update.*docs",
        ],
        "Breaking Changes": [
            r"^BREAKING",
            r"breaking change",
            r"breaking:",
        ],
        "Dependencies": [
            r"^deps:",
            r"^chore\(deps\)",
            r"update.*depend",
            r"bump.*version",
        ],
        "Refactoring": [
            r"^refactor:",
            r"refactor",
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

        while True:
            try:
                url = f"https://api.github.com/repos/{owner}/{repo}/commits"
                params = {
                    "since": f"{start_date}T00:00:00Z",
                    "until": f"{end_date}T23:59:59Z",
                    "per_page": per_page,
                    "page": page,
                }
                headers = {"Accept": "application/vnd.github.v3+json"}

                response = requests.get(url, params=params, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()
                if not data:
                    break

                commits.extend(data)
                page += 1

            except requests.exceptions.RequestException as e:
                print(f"Error fetching commits: {e}")
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
        commits: List[Dict], owner: str, repo: str, version: str = None
    ) -> str:
        """
        Generate a Markdown changelog from categorized commits.

        Args:
            commits: List of commit dictionaries
            owner: Repository owner
            repo: Repository name
            version: Version identifier (optional)

        Returns:
            Markdown-formatted changelog
        """
        if not commits:
            return "# Changelog\n\nNo commits found for the specified date range.\n"

        categorized = ChangelogGenie.group_commits_by_category(commits)

        # Generate header
        date_range = f"{ChangelogGenie._get_commit_date(commits[-1])} to {ChangelogGenie._get_commit_date(commits[0])}"
        if version:
            header = f"# Changelog - {version}\n\n"
        else:
            header = f"# Changelog\n\n"

        header += f"**Date Range:** {date_range}\n"
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
        return

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
            commits, args.owner, args.repo, args.version
        )
        print(changelog)
        return

    print(f"Found {len(commits)} commits. Generating changelog...", file=sys.stderr)
    changelog = ChangelogGenie.generate_markdown(
        commits, args.owner, args.repo, args.version
    )

    print(changelog)


if __name__ == "__main__":
    main()
