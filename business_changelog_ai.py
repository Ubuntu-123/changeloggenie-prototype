#!/usr/bin/env python3
"""Generate a customer-facing business changelog using the OpenAI API.

This script reads:
- prompts/business_changelog_system.md
- a technical changelog Markdown file

It prints strictly valid JSON if the model follows the prompt.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from openai import OpenAI


DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.5")


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Transform a technical changelog into customer-facing JSON using OpenAI."
    )
    parser.add_argument(
        "input_file",
        help="Path to a technical changelog Markdown file, or '-' to read from stdin.",
    )
    parser.add_argument(
        "--prompt",
        default="prompts/business_changelog_system.md",
        help="Path to the business changelog system prompt.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenAI model to use. Default: {DEFAULT_MODEL}",
    )
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        return 2

    system_prompt = read_text(args.prompt)
    technical_changelog = read_text(args.input_file)

    client = OpenAI()

    response = client.responses.create(
        model=args.model,
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    "Transform the following technical changelog into the required "
                    "customer-facing JSON format. Return only JSON.\n\n"
                    f"{technical_changelog}"
                ),
            },
        ],
    )

    output = response.output_text.strip()

    try:
        parsed = json.loads(output)
    except json.JSONDecodeError as exc:
        print("ERROR: Model output was not valid JSON.", file=sys.stderr)
        print(f"JSON error: {exc}", file=sys.stderr)
        print("\n--- RAW MODEL OUTPUT ---", file=sys.stderr)
        print(output, file=sys.stderr)
        return 1

    print(json.dumps(parsed, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
