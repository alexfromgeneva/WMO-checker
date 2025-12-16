#!/usr/bin/env python3
"""
Billie Jean - WMO Web Content Reviewer 2.0

A comprehensive content review tool for World Meteorological Organization (WMO)
web content that checks for style compliance, accessibility, terminology accuracy,
and overall content quality.
"""

import re
import sys
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Issue severity levels"""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    SUGGESTION = "SUGGESTION"


@dataclass
class Issue:
    """Represents a content issue"""
    category: str
    severity: Severity
    message: str
    line_number: int = 0
    context: str = ""

    def __str__(self):
        location = f"Line {self.line_number}: " if self.line_number > 0 else ""
        context = f"\n  Context: {self.context}" if self.context else ""
        return f"[{self.severity.value}] {self.category}: {location}{self.message}{context}"


class WMOContentReviewer:
    """
    Main content reviewer class for WMO web content.

    This tool checks content against WMO standards including:
    - Meteorological terminology accuracy
    - Style guide compliance
    - Accessibility standards (WCAG)
    - Grammar and clarity
    - Technical accuracy
    - Link validity
    - SEO best practices
    """

    # WMO-approved meteorological terms and their preferred usage
    WMO_TERMINOLOGY = {
        "weather forecast": ["weather prediction", "forecast"],
        "climate change": ["global warming"],  # Preferred term over alternatives
        "meteorological": ["weather-related"],
        "precipitation": ["rainfall"],  # Use specific terms
        "temperature": ["temp"],  # Avoid abbreviations in formal content
        "humidity": [],
        "atmospheric pressure": ["barometric pressure", "air pressure"],
        "wind speed": [],
        "climate": [],
        "meteorology": [],
    }

    # Common WMO abbreviations that should be defined on first use
    WMO_ABBREVIATIONS = [
        "WMO", "GCOS", "GCW", "WIGOS", "WIS", "GAW", "WWW", "GDPFS",
        "IPCC", "UNFCCC", "GHG", "UTC", "NMHS", "AMDAR", "GTS"
    ]

    # Units that should use standard WMO format
    STANDARD_UNITS = {
        "celsius": ["°C", "degrees Celsius"],
        "fahrenheit": ["°F", "degrees Fahrenheit"],
        "kelvin": ["K"],
        "meters": ["m", "metres"],
        "kilometers": ["km", "kilometres"],
        "millimeters": ["mm", "millimetres"],
        "hectopascal": ["hPa"],
        "pascal": ["Pa"],
        "meters per second": ["m/s", "m s⁻¹"],
    }

    # Common issues in meteorological content
    COMMON_ISSUES = {
        r"\btemp\b": "Use 'temperature' instead of abbreviation 'temp' in formal content",
        r"\bmax\b": "Use 'maximum' instead of abbreviation 'max' in formal content",
        r"\bmin\b": "Use 'minimum' instead of abbreviation 'min' in formal content",
        r"global warming": "Consider using 'climate change' as the preferred WMO term",
        r"\d+\s*degrees": "Ensure temperature units are specified (°C, °F, K)",
    }

    def __init__(self):
        self.issues: List[Issue] = []
        self.content_lines: List[str] = []
        self.content: str = ""

    def review(self, content: str) -> List[Issue]:
        """
        Review the provided content and return a list of issues.

        Args:
            content: The web content to review (HTML, Markdown, or plain text)

        Returns:
            List of Issue objects found during review
        """
        self.content = content
        self.content_lines = content.split('\n')
        self.issues = []

        # Run all checks
        self.check_terminology()
        self.check_abbreviations()
        self.check_style_guide()
        self.check_accessibility()
        self.check_grammar_and_clarity()
        self.check_technical_accuracy()
        self.check_heading_structure()
        self.check_links()
        self.check_seo()

        return sorted(self.issues, key=lambda x: (x.severity.value, x.line_number))

    def check_terminology(self):
        """Check for proper WMO meteorological terminology usage."""
        for i, line in enumerate(self.content_lines, 1):
            line_lower = line.lower()

            # Check for common terminology issues
            for pattern, message in self.COMMON_ISSUES.items():
                if re.search(pattern, line_lower):
                    self.issues.append(Issue(
                        category="Terminology",
                        severity=Severity.SUGGESTION,
                        message=message,
                        line_number=i,
                        context=line.strip()[:100]
                    ))

    def check_abbreviations(self):
        """Check that WMO abbreviations are properly defined on first use."""
        defined_abbrevs = set()

        for i, line in enumerate(self.content_lines, 1):
            for abbrev in self.WMO_ABBREVIATIONS:
                if abbrev in line:
                    # Check if abbreviation is defined in the same line or nearby
                    pattern = rf"{abbrev}\s*\([^)]+\)|[^)]+\({abbrev}\)"
                    if re.search(pattern, line):
                        defined_abbrevs.add(abbrev)
                    elif abbrev not in defined_abbrevs and abbrev != "WMO":
                        self.issues.append(Issue(
                            category="Abbreviations",
                            severity=Severity.WARNING,
                            message=f"Abbreviation '{abbrev}' should be defined on first use",
                            line_number=i,
                            context=line.strip()[:100]
                        ))
                        defined_abbrevs.add(abbrev)  # Only warn once

    def check_style_guide(self):
        """Check compliance with WMO style guide."""
        for i, line in enumerate(self.content_lines, 1):
            # Check for proper capitalization of "World Meteorological Organization"
            if re.search(r"world meteorological organization", line, re.IGNORECASE):
                if "World Meteorological Organization" not in line:
                    self.issues.append(Issue(
                        category="Style Guide",
                        severity=Severity.WARNING,
                        message="'World Meteorological Organization' should be properly capitalized",
                        line_number=i,
                        context=line.strip()[:100]
                    ))

            # Check for overly long sentences (>40 words)
            sentences = re.split(r'[.!?]+', line)
            for sentence in sentences:
                word_count = len(sentence.split())
                if word_count > 40:
                    self.issues.append(Issue(
                        category="Style Guide",
                        severity=Severity.SUGGESTION,
                        message=f"Sentence is very long ({word_count} words). Consider breaking it up for clarity",
                        line_number=i,
                        context=sentence.strip()[:100]
                    ))

            # Check for passive voice indicators
            passive_indicators = [
                r"\bis being\b", r"\bwas being\b", r"\bhas been\b",
                r"\bhave been\b", r"\bhad been\b", r"\bwill be\b"
            ]
            for pattern in passive_indicators:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(Issue(
                        category="Style Guide",
                        severity=Severity.INFO,
                        message="Consider using active voice for clearer communication",
                        line_number=i,
                        context=line.strip()[:100]
                    ))
                    break  # Only report once per line

    def check_accessibility(self):
        """Check for accessibility compliance (WCAG standards)."""
        content_lower = self.content.lower()

        # Check for images without alt text
        img_pattern = r'<img[^>]+>'
        for match in re.finditer(img_pattern, self.content, re.IGNORECASE):
            img_tag = match.group(0)
            if 'alt=' not in img_tag.lower():
                line_num = self.content[:match.start()].count('\n') + 1
                self.issues.append(Issue(
                    category="Accessibility",
                    severity=Severity.ERROR,
                    message="Image missing alt text attribute (required for WCAG compliance)",
                    line_number=line_num,
                    context=img_tag[:100]
                ))
            elif re.search(r'alt=["\'][\s]*["\']', img_tag):
                line_num = self.content[:match.start()].count('\n') + 1
                self.issues.append(Issue(
                    category="Accessibility",
                    severity=Severity.WARNING,
                    message="Image has empty alt text. Provide descriptive text or use alt='' for decorative images",
                    line_number=line_num,
                    context=img_tag[:100]
                ))

        # Check for proper heading hierarchy
        headings = re.findall(r'<h([1-6])[^>]*>.*?</h\1>', self.content, re.IGNORECASE | re.DOTALL)
        if headings and headings[0] != '1':
            self.issues.append(Issue(
                category="Accessibility",
                severity=Severity.WARNING,
                message="Page should start with an H1 heading for proper document structure",
                line_number=0
            ))

        # Check for links with generic text
        generic_link_texts = ['click here', 'read more', 'link', 'here']
        link_pattern = r'<a[^>]*>(.*?)</a>'
        for match in re.finditer(link_pattern, self.content, re.IGNORECASE):
            link_text = re.sub(r'<[^>]+>', '', match.group(1)).strip().lower()
            if link_text in generic_link_texts:
                line_num = self.content[:match.start()].count('\n') + 1
                self.issues.append(Issue(
                    category="Accessibility",
                    severity=Severity.WARNING,
                    message=f"Avoid generic link text '{link_text}'. Use descriptive text instead",
                    line_number=line_num,
                    context=match.group(0)[:100]
                ))

    def check_grammar_and_clarity(self):
        """Check for common grammar issues and clarity problems."""
        for i, line in enumerate(self.content_lines, 1):
            # Check for double spaces
            if '  ' in line:
                self.issues.append(Issue(
                    category="Grammar",
                    severity=Severity.INFO,
                    message="Multiple consecutive spaces found",
                    line_number=i,
                    context=line.strip()[:100]
                ))

            # Check for common grammar mistakes
            if re.search(r"\bit's\b.*\b(own|properties|data)", line, re.IGNORECASE):
                self.issues.append(Issue(
                    category="Grammar",
                    severity=Severity.WARNING,
                    message="Check if 'it's' should be 'its' (possessive)",
                    line_number=i,
                    context=line.strip()[:100]
                ))

            # Check for unclear pronouns
            if re.search(r"^\s*(This|These|Those|They|It)\s", line):
                self.issues.append(Issue(
                    category="Clarity",
                    severity=Severity.INFO,
                    message="Sentence starts with pronoun. Ensure the reference is clear",
                    line_number=i,
                    context=line.strip()[:100]
                ))

    def check_technical_accuracy(self):
        """Check for technical accuracy in meteorological content."""
        for i, line in enumerate(self.content_lines, 1):
            # Check for temperature values without units
            if re.search(r'\b\d+\s*degree(?:s)?\b', line, re.IGNORECASE):
                if not re.search(r'°[CFK]|celsius|fahrenheit|kelvin', line, re.IGNORECASE):
                    self.issues.append(Issue(
                        category="Technical Accuracy",
                        severity=Severity.ERROR,
                        message="Temperature mentioned without specifying unit (°C, °F, or K)",
                        line_number=i,
                        context=line.strip()[:100]
                    ))

            # Check for inconsistent date formats
            date_formats = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', line)
            if date_formats:
                self.issues.append(Issue(
                    category="Technical Accuracy",
                    severity=Severity.SUGGESTION,
                    message="Use ISO 8601 date format (YYYY-MM-DD) for international consistency",
                    line_number=i,
                    context=line.strip()[:100]
                ))

    def check_heading_structure(self):
        """Check for proper heading structure and hierarchy."""
        heading_pattern = r'^(#{1,6})\s+(.+)$|<h([1-6])[^>]*>(.*?)</h\3>'
        headings = []

        for i, line in enumerate(self.content_lines, 1):
            # Markdown headings
            md_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if md_match:
                level = len(md_match.group(1))
                text = md_match.group(2)
                headings.append((i, level, text))

            # HTML headings
            html_matches = re.finditer(r'<h([1-6])[^>]*>(.*?)</h\1>', line, re.IGNORECASE)
            for match in html_matches:
                level = int(match.group(1))
                text = re.sub(r'<[^>]+>', '', match.group(2))
                headings.append((i, level, text))

        # Check heading hierarchy
        for idx, (line_num, level, text) in enumerate(headings):
            if idx > 0:
                prev_level = headings[idx - 1][1]
                if level > prev_level + 1:
                    self.issues.append(Issue(
                        category="Document Structure",
                        severity=Severity.WARNING,
                        message=f"Heading level jumps from H{prev_level} to H{level}. Maintain sequential hierarchy",
                        line_number=line_num,
                        context=text[:100]
                    ))

            # Check heading length
            if len(text) > 70:
                self.issues.append(Issue(
                    category="Document Structure",
                    severity=Severity.SUGGESTION,
                    message=f"Heading is very long ({len(text)} characters). Consider shortening for clarity",
                    line_number=line_num,
                    context=text[:100]
                ))

    def check_links(self):
        """Check for link validity and proper formatting."""
        # HTML links
        html_link_pattern = r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']*)["\'][^>]*>(.*?)</a>'
        for match in re.finditer(html_link_pattern, self.content, re.IGNORECASE):
            url = match.group(1)
            text = match.group(2)
            line_num = self.content[:match.start()].count('\n') + 1

            if not url or url == '#':
                self.issues.append(Issue(
                    category="Links",
                    severity=Severity.ERROR,
                    message="Link has empty or placeholder href",
                    line_number=line_num,
                    context=match.group(0)[:100]
                ))

            # Check for external links to non-HTTPS
            if url.startswith('http://') and not url.startswith('http://localhost'):
                self.issues.append(Issue(
                    category="Links",
                    severity=Severity.WARNING,
                    message="External link uses HTTP instead of HTTPS (security concern)",
                    line_number=line_num,
                    context=url
                ))

        # Markdown links
        md_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(md_link_pattern, self.content):
            text = match.group(1)
            url = match.group(2)
            line_num = self.content[:match.start()].count('\n') + 1

            if not url or url == '#':
                self.issues.append(Issue(
                    category="Links",
                    severity=Severity.ERROR,
                    message="Link has empty or placeholder URL",
                    line_number=line_num,
                    context=match.group(0)
                ))

    def check_seo(self):
        """Check for SEO best practices."""
        content_lower = self.content.lower()

        # Check for meta description
        if '<meta' in content_lower and 'name="description"' not in content_lower:
            self.issues.append(Issue(
                category="SEO",
                severity=Severity.WARNING,
                message="Missing meta description tag for search engine optimization",
                line_number=0
            ))

        # Check meta description length
        meta_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
                             self.content, re.IGNORECASE)
        if meta_desc:
            desc_length = len(meta_desc.group(1))
            if desc_length < 120:
                self.issues.append(Issue(
                    category="SEO",
                    severity=Severity.SUGGESTION,
                    message=f"Meta description is short ({desc_length} chars). Aim for 150-160 characters",
                    line_number=0
                ))
            elif desc_length > 160:
                self.issues.append(Issue(
                    category="SEO",
                    severity=Severity.WARNING,
                    message=f"Meta description is too long ({desc_length} chars). Keep it under 160 characters",
                    line_number=0
                ))

        # Check for title tag
        if '<title>' not in content_lower and '# ' not in self.content:
            self.issues.append(Issue(
                category="SEO",
                severity=Severity.WARNING,
                message="Missing title tag or H1 heading",
                line_number=0
            ))

    def generate_report(self) -> str:
        """Generate a formatted report of all issues found."""
        if not self.issues:
            return "✓ No issues found! Content looks great.\n"

        report = ["=" * 80]
        report.append("WMO WEB CONTENT REVIEW REPORT")
        report.append("=" * 80)
        report.append("")

        # Summary
        error_count = sum(1 for i in self.issues if i.severity == Severity.ERROR)
        warning_count = sum(1 for i in self.issues if i.severity == Severity.WARNING)
        info_count = sum(1 for i in self.issues if i.severity == Severity.INFO)
        suggestion_count = sum(1 for i in self.issues if i.severity == Severity.SUGGESTION)

        report.append(f"SUMMARY:")
        report.append(f"  Total Issues: {len(self.issues)}")
        report.append(f"  - Errors: {error_count}")
        report.append(f"  - Warnings: {warning_count}")
        report.append(f"  - Info: {info_count}")
        report.append(f"  - Suggestions: {suggestion_count}")
        report.append("")
        report.append("-" * 80)
        report.append("")

        # Group issues by category
        issues_by_category = {}
        for issue in self.issues:
            if issue.category not in issues_by_category:
                issues_by_category[issue.category] = []
            issues_by_category[issue.category].append(issue)

        # Print issues by category
        for category in sorted(issues_by_category.keys()):
            report.append(f"{category.upper()}:")
            report.append("-" * 80)
            for issue in issues_by_category[category]:
                report.append(str(issue))
                report.append("")
            report.append("")

        return "\n".join(report)


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Billie Jean - WMO Web Content Reviewer 2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Review a file
  python wmo_content_reviewer.py review.html

  # Review content from stdin
  cat content.md | python wmo_content_reviewer.py -

  # Review with only errors and warnings
  python wmo_content_reviewer.py --severity ERROR,WARNING content.html
        """
    )

    parser.add_argument(
        'file',
        help='File to review (use "-" for stdin)'
    )

    parser.add_argument(
        '--severity',
        default='ERROR,WARNING,INFO,SUGGESTION',
        help='Comma-separated list of severity levels to report (default: all)'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    # Read content
    if args.file == '-':
        content = sys.stdin.read()
    else:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)

    # Parse severity filter
    severity_filter = set(s.strip().upper() for s in args.severity.split(','))

    # Review content
    reviewer = WMOContentReviewer()
    issues = reviewer.review(content)

    # Filter by severity
    filtered_issues = [i for i in issues if i.severity.value in severity_filter]
    reviewer.issues = filtered_issues

    # Output results
    if args.format == 'json':
        import json
        output = {
            'total_issues': len(filtered_issues),
            'errors': sum(1 for i in filtered_issues if i.severity == Severity.ERROR),
            'warnings': sum(1 for i in filtered_issues if i.severity == Severity.WARNING),
            'info': sum(1 for i in filtered_issues if i.severity == Severity.INFO),
            'suggestions': sum(1 for i in filtered_issues if i.severity == Severity.SUGGESTION),
            'issues': [
                {
                    'category': i.category,
                    'severity': i.severity.value,
                    'message': i.message,
                    'line_number': i.line_number,
                    'context': i.context
                }
                for i in filtered_issues
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print(reviewer.generate_report())

    # Exit with error code if there are errors
    if any(i.severity == Severity.ERROR for i in filtered_issues):
        sys.exit(1)


if __name__ == '__main__':
    main()
