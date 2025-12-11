import json
import os
from typing import List, Dict, Any
from datetime import datetime


class AwesomeReadmeGenerator:
    def __init__(self, json_path: str, output_path: str = "README.md"):
        self.json_path = json_path
        self.output_path = output_path
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Loads the JSON data from file."""
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"Could not find {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _generate_badges(self, entry: Dict[str, Any]) -> str:
        """Generates Markdown badges for ArXiv and GitHub if links exist."""
        badges = []

        # ArXiv Badge
        if entry.get("arxiv"):
            badge = f"[![arXiv](https://img.shields.io/badge/arXiv-Paper-b31b1b.svg)]({entry['arxiv']})"
            badges.append(badge)

        # GitHub Badge
        if entry.get("github"):
            badge = f"[![GitHub](https://img.shields.io/badge/GitHub-Repo-181717.svg?logo=github)]({entry['github']})"
            badges.append(badge)

        return " ".join(badges)

    def _format_entry(self, entry: Dict[str, Any]) -> str:
        """
        Formats a single line entry:
        Title [Venue] ArXiv Github Keywords: ...
        """
        title = entry.get("title", "Untitled")
        url = entry.get("url", "#")
        venue = entry.get("venue", "Preprint")
        keywords = ", ".join(entry.get("keywords", []))

        badges = self._generate_badges(entry)

        # Construct the line
        line = f"**{title}** <br> [`{venue}`]({url}) {badges}"

        if keywords:
            line += f" <br> _Keywords: {keywords}_"
        
        line += " <br> <br> "

        return line

    def _parse_date(self, date_str: str):
        """Helper to parse date for sorting. Returns min date if invalid/missing."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            # If date is missing or wrong format, treat as very old
            return datetime.min

    def _generate_section(self, title: str, key: str) -> str:
        """Generates a markdown section, sorted by date (newest first)."""
        entries = self.data.get(key, [])
        if not entries:
            return ""

        # SORTING LOGIC:
        # Sorts the entries list in place using the date field.
        # reverse=True ensures newest dates come first.
        entries.sort(key=lambda x: self._parse_date(x.get("date")), reverse=True)

        section = [f"## {title}\n"]
        for entry in entries:
            section.append(self._format_entry(entry))

        return "\n".join(section) + "\n"

    def _generate_intro(self) -> str:
        """Generates the static introduction text."""
        return (
            "<h1 align=\"center\">Awesome Story Visualization</h1>\n\n"
            "A curated list of resources, papers, and benchmarks focused on "
            "**Story Visualization**.\n\n"
            "Entries are sorted by date (newest first).\n\n"
            "If you want to contribute, please edit the `citations.json` file, "
            "run the generator script, and create a pull request.\n\n"
            "If you are looking for Storytelling, text based, take a look at [Awesome-Story-Generation](https://github.com/yingpengma/Awesome-Story-Generation).\n\n"
            "---\n"
        )

    def generate(self):
        """Main logic to assemble the README."""
        print(f"Reading from {self.json_path}...")

        content = []
        content.append(self._generate_intro())
        content.append(self._generate_section("Papers", "papers"))
        content.append(self._generate_section("Benchmarks", "benchmarks"))
        content.append(self._generate_section("Datasets", "datasets"))

        # Write to file
        final_markdown = "\n".join(content)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(final_markdown)

        print(f"Successfully generated {self.output_path} with sorted entries!")


if __name__ == "__main__":
    generator = AwesomeReadmeGenerator(json_path="citations.json")
    generator.generate()
