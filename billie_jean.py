#!/usr/bin/env python3
"""
Billie Jean - WMO Web Content Reviewer 2.0

A comprehensive content review tool for World Meteorological Organization (WMO)
web content. Reviews content against WMO Writing and Style Guide, WCAG 2.1
accessibility guidelines, readability standards, and strategic alignment with
WMO's mission and priorities.
"""

import re
import sys
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import argparse


class ContentType(Enum):
    """Type of web content being reviewed"""
    WEB_PAGE = "web_page"
    NEWS_ARTICLE = "news_article"
    UNKNOWN = "unknown"


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "CRITICAL"  # Strategic misalignment, major accessibility issues
    ERROR = "ERROR"  # Style guide violations, accessibility errors
    WARNING = "WARNING"  # Recommendations for improvement
    SUGGESTION = "SUGGESTION"  # Optional enhancements


@dataclass
class ReviewIssue:
    """Represents a content issue found during review"""
    category: str
    severity: Severity
    message: str
    suggestion: str = ""
    line_number: int = 0
    context: str = ""
    flagged_text: str = ""

    def format_output(self) -> str:
        """Format the issue for display"""
        location = f"Line {self.line_number}: " if self.line_number > 0 else ""

        output = f"[{self.severity.value}] {self.category}\n"
        if self.flagged_text:
            output += f"  Flagged: {self.flagged_text}\n"
        output += f"  {location}{self.message}\n"
        if self.suggestion:
            output += f"  *[Suggestion: {self.suggestion}]*\n"
        if self.context and not self.flagged_text:
            output += f"  Context: {self.context[:150]}...\n"

        return output


@dataclass
class StrategicAlignment:
    """Tracks alignment with WMO strategic priorities"""
    earth_system_monitoring: bool = False
    early_warnings: bool = False
    climate_action: bool = False
    capacity_development: bool = False
    hydrometeorological_services: bool = False

    def get_coverage(self) -> float:
        """Get percentage of strategic areas covered"""
        total = 5
        covered = sum([
            self.earth_system_monitoring,
            self.early_warnings,
            self.climate_action,
            self.capacity_development,
            self.hydrometeorological_services
        ])
        return (covered / total) * 100

    def get_covered_areas(self) -> List[str]:
        """Get list of covered strategic areas"""
        areas = []
        if self.earth_system_monitoring:
            areas.append("Earth system monitoring")
        if self.early_warnings:
            areas.append("Early warnings")
        if self.climate_action:
            areas.append("Climate action")
        if self.capacity_development:
            areas.append("Capacity development")
        if self.hydrometeorological_services:
            areas.append("Hydrometeorological services")
        return areas

    def get_missing_areas(self) -> List[str]:
        """Get list of missing strategic areas"""
        areas = []
        if not self.earth_system_monitoring:
            areas.append("Earth system monitoring")
        if not self.early_warnings:
            areas.append("Early warnings")
        if not self.climate_action:
            areas.append("Climate action")
        if not self.capacity_development:
            areas.append("Capacity development")
        if not self.hydrometeorological_services:
            areas.append("Hydrometeorological services")
        return areas


class BillieJean:
    """
    WMO Web Content Reviewer - "Billie Jean"

    Reviews web content for:
    - WMO Writing and Style Guide compliance
    - WCAG 2.1 accessibility
    - Readability guidelines
    - Strategic alignment with WMO mission
    - Storytelling and engagement (for news articles)
    - SEO best practices
    """

    # WMO Strategic Priority Keywords
    STRATEGIC_KEYWORDS = {
        'earth_system_monitoring': [
            'observation', 'monitoring', 'data collection', 'satellite', 'weather station',
            'WIGOS', 'Global Observing System', 'measurement', 'sensor'
        ],
        'early_warnings': [
            'early warning', 'forecast', 'prediction', 'alert', 'warning system',
            'preparedness', 'risk reduction', 'disaster', 'severe weather'
        ],
        'climate_action': [
            'climate change', 'climate action', 'adaptation', 'mitigation', 'greenhouse gas',
            'Paris Agreement', 'UNFCCC', 'global warming', 'carbon', 'climate services'
        ],
        'capacity_development': [
            'capacity', 'training', 'education', 'knowledge transfer', 'technical assistance',
            'development', 'partnership', 'cooperation', 'support'
        ],
        'hydrometeorological_services': [
            'water', 'hydrology', 'flood', 'drought', 'water resources', 'precipitation',
            'river', 'hydrological', 'water management', 'NMHS'
        ]
    }

    # WMO Abbreviations that need definition on first use
    WMO_ABBREVIATIONS = {
        'WMO': 'World Meteorological Organization',
        'GCOS': 'Global Climate Observing System',
        'WIGOS': 'WMO Integrated Global Observing System',
        'WIS': 'WMO Information System',
        'GAW': 'Global Atmosphere Watch',
        'GDPFS': 'Global Data-Processing and Forecasting System',
        'IPCC': 'Intergovernmental Panel on Climate Change',
        'UNFCCC': 'United Nations Framework Convention on Climate Change',
        'GHG': 'Greenhouse Gas',
        'NMHS': 'National Meteorological and Hydrological Services',
        'AMDAR': 'Aircraft Meteorological Data Relay',
        'GTS': 'Global Telecommunication System'
    }

    # Target audiences for WMO content
    TARGET_AUDIENCES = [
        'public', 'journalists', 'media', 'policymakers', 'scientists',
        'UN agencies', 'governments', 'researchers', 'meteorologists'
    ]

    def __init__(self, content_type: ContentType = ContentType.UNKNOWN):
        self.content_type = content_type
        self.issues: List[ReviewIssue] = []
        self.content: str = ""
        self.content_lines: List[str] = []
        self.strategic_alignment = StrategicAlignment()
        self.defined_abbreviations: set = set()

    def review(self, content: str) -> Tuple[List[ReviewIssue], StrategicAlignment]:
        """
        Perform comprehensive review of WMO web content.

        Args:
            content: The content to review (HTML, Markdown, or plain text)

        Returns:
            Tuple of (list of issues, strategic alignment assessment)
        """
        self.content = content
        self.content_lines = content.split('\n')
        self.issues = []
        self.strategic_alignment = StrategicAlignment()
        self.defined_abbreviations = set()

        # Core checks
        self.check_strategic_alignment()
        self.check_style_guide_compliance()
        self.check_accessibility_wcag()
        self.check_readability()
        self.check_terminology()
        self.check_abbreviations()

        # Content-type specific checks
        if self.content_type == ContentType.NEWS_ARTICLE:
            self.check_news_article_standards()

        # Additional checks
        self.check_seo()
        self.check_target_audience()
        self.check_formatting()
        self.check_links_and_references()

        return sorted(self.issues, key=lambda x: (x.severity.value, x.line_number)), self.strategic_alignment

    def check_strategic_alignment(self):
        """Check alignment with WMO strategic priorities"""
        content_lower = self.content.lower()

        # Check for strategic priority keywords
        for priority, keywords in self.STRATEGIC_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    setattr(self.strategic_alignment, priority, True)
                    break

        # If no strategic alignment detected, flag it
        if self.strategic_alignment.get_coverage() < 20:
            self.issues.append(ReviewIssue(
                category="Strategic Alignment",
                severity=Severity.CRITICAL,
                message="Content shows minimal alignment with WMO strategic priorities",
                suggestion="Consider explicitly connecting content to WMO's mission: Earth system monitoring, early warnings, climate action, capacity development, or hydrometeorological services"
            ))

    def check_style_guide_compliance(self):
        """Check compliance with WMO Writing and Style Guide"""

        for i, line in enumerate(self.content_lines, 1):
            line_lower = line.lower()

            # Check for proper WMO capitalization
            if 'world meteorological organization' in line_lower:
                if 'World Meteorological Organization' not in line:
                    self.issues.append(ReviewIssue(
                        category="Style Guide",
                        severity=Severity.ERROR,
                        message="'World Meteorological Organization' must be properly capitalized",
                        suggestion="Use 'World Meteorological Organization' with capital letters",
                        line_number=i,
                        flagged_text=self._extract_phrase(line, 'world meteorological organization')
                    ))

            # Check for overly long sentences (>30 words for web content)
            sentences = re.split(r'[.!?]+', line)
            for sentence in sentences:
                if not sentence.strip():
                    continue
                word_count = len(sentence.split())
                if word_count > 30:
                    self.issues.append(ReviewIssue(
                        category="Style Guide - Clarity",
                        severity=Severity.WARNING,
                        message=f"Sentence is too long for web content ({word_count} words)",
                        suggestion="Break into shorter sentences (aim for 20-25 words max) for better web readability",
                        line_number=i,
                        context=sentence.strip()[:100]
                    ))

            # Check for passive voice
            passive_patterns = [
                (r'\bis being\b', 'is being'),
                (r'\bwas being\b', 'was being'),
                (r'\bhas been\b', 'has been'),
                (r'\bhave been\b', 'have been'),
                (r'\bhad been\b', 'had been')
            ]

            for pattern, phrase in passive_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(ReviewIssue(
                        category="Style Guide - Voice",
                        severity=Severity.SUGGESTION,
                        message="Passive voice detected",
                        suggestion="Consider using active voice for more direct, engaging communication",
                        line_number=i,
                        flagged_text=phrase
                    ))
                    break

            # Check for abbreviations in formal writing
            abbrev_issues = [
                (r'\btemp\b', 'temp', 'temperature'),
                (r'\bmax\b', 'max', 'maximum'),
                (r'\bmin\b', 'min', 'minimum'),
                (r'\binfo\b', 'info', 'information')
            ]

            for pattern, abbrev, full in abbrev_issues:
                if re.search(pattern, line_lower):
                    self.issues.append(ReviewIssue(
                        category="Style Guide - Abbreviations",
                        severity=Severity.ERROR,
                        message=f"Avoid informal abbreviation '{abbrev}' in formal content",
                        suggestion=f"Use '{full}' instead",
                        line_number=i,
                        flagged_text=abbrev
                    ))

            # Check for italics used for emphasis (should be avoided per guidelines)
            if re.search(r'\*[^*]+\*|_[^_]+_|<em>|<i>', line):
                # This is a simplified check - in reality would need more context
                self.issues.append(ReviewIssue(
                    category="Style Guide - Formatting",
                    severity=Severity.WARNING,
                    message="Possible use of italics detected",
                    suggestion="Italics should only be used for publication titles, Latin names, etc., not for emphasis in web content",
                    line_number=i
                ))

    def check_accessibility_wcag(self):
        """Check WCAG 2.1 accessibility compliance"""

        # Check for images without alt text
        img_pattern = r'<img[^>]+>'
        for match in re.finditer(img_pattern, self.content, re.IGNORECASE):
            img_tag = match.group(0)
            line_num = self.content[:match.start()].count('\n') + 1

            if 'alt=' not in img_tag.lower():
                self.issues.append(ReviewIssue(
                    category="Accessibility (WCAG 2.1)",
                    severity=Severity.CRITICAL,
                    message="Image missing alt text (WCAG 2.1 Level A requirement)",
                    suggestion="Add descriptive alt text: alt='[description of image content and function]'",
                    line_number=line_num,
                    flagged_text=img_tag[:80]
                ))
            elif re.search(r'alt=["\'][\s]*["\']', img_tag):
                self.issues.append(ReviewIssue(
                    category="Accessibility (WCAG 2.1)",
                    severity=Severity.WARNING,
                    message="Image has empty alt text",
                    suggestion="If decorative, use alt=''. If meaningful, provide descriptive text",
                    line_number=line_num
                ))

        # Check heading hierarchy
        headings = []
        for i, line in enumerate(self.content_lines, 1):
            # Markdown headings
            md_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if md_match:
                level = len(md_match.group(1))
                headings.append((i, level, md_match.group(2)))

            # HTML headings
            for match in re.finditer(r'<h([1-6])[^>]*>(.*?)</h\1>', line, re.IGNORECASE):
                level = int(match.group(1))
                text = re.sub(r'<[^>]+>', '', match.group(2))
                headings.append((i, level, text))

        # Check for proper hierarchy
        if headings:
            if headings[0][1] != 1:
                self.issues.append(ReviewIssue(
                    category="Accessibility (WCAG 2.1)",
                    severity=Severity.ERROR,
                    message="Document should start with H1 heading",
                    suggestion="Use H1 for main title, then H2 for sections, H3 for subsections",
                    line_number=headings[0][0]
                ))

            for idx in range(1, len(headings)):
                prev_level = headings[idx-1][1]
                curr_level = headings[idx][1]
                if curr_level > prev_level + 1:
                    self.issues.append(ReviewIssue(
                        category="Accessibility (WCAG 2.1)",
                        severity=Severity.ERROR,
                        message=f"Heading hierarchy skip: H{prev_level} to H{curr_level}",
                        suggestion="Maintain sequential heading levels for screen reader users",
                        line_number=headings[idx][0]
                    ))

        # Check for generic link text
        generic_texts = ['click here', 'read more', 'here', 'this link', 'link']
        link_pattern = r'<a[^>]*>([^<]+)</a>|\[([^\]]+)\]\([^)]+\)'

        for match in re.finditer(link_pattern, self.content, re.IGNORECASE):
            link_text = (match.group(1) or match.group(2) or '').strip().lower()
            if link_text in generic_texts:
                line_num = self.content[:match.start()].count('\n') + 1
                self.issues.append(ReviewIssue(
                    category="Accessibility (WCAG 2.1)",
                    severity=Severity.ERROR,
                    message=f"Generic link text: '{link_text}'",
                    suggestion="Use descriptive link text that makes sense out of context (e.g., 'WMO Climate Report 2025' instead of 'click here')",
                    line_number=line_num,
                    flagged_text=link_text
                ))

    def check_readability(self):
        """Check readability for web audiences"""

        # Count words and sentences for rough readability check
        total_words = len(self.content.split())
        sentences = re.split(r'[.!?]+', self.content)
        sentence_count = len([s for s in sentences if s.strip()])

        if sentence_count > 0:
            avg_words_per_sentence = total_words / sentence_count

            if avg_words_per_sentence > 25:
                self.issues.append(ReviewIssue(
                    category="Readability",
                    severity=Severity.WARNING,
                    message=f"Average sentence length is high ({avg_words_per_sentence:.1f} words)",
                    suggestion="Aim for average of 15-20 words per sentence for web content"
                ))

        # Check for jargon without explanation
        technical_terms = [
            'synoptic', 'baroclinic', 'geopotential', 'meridional', 'zonal',
            'advection', 'adiabatic', 'convection', 'parameterization'
        ]

        content_lower = self.content.lower()
        for term in technical_terms:
            if term in content_lower:
                # Check if term is explained nearby
                pattern = f'{term}[^.!?]*?(?:is|means|refers to|defined as)'
                if not re.search(pattern, content_lower, re.IGNORECASE):
                    self.issues.append(ReviewIssue(
                        category="Readability - Jargon",
                        severity=Severity.WARNING,
                        message=f"Technical term '{term}' may need explanation",
                        suggestion=f"Consider adding a brief explanation for general audiences or linking to a glossary",
                        flagged_text=term
                    ))

    def check_terminology(self):
        """Check for proper meteorological terminology"""

        terminology_guide = {
            'global warming': ('climate change', 'WMO prefers "climate change" for broader scientific accuracy'),
            'weather prediction': ('weather forecast', 'Use "forecast" as the standard meteorological term'),
            'rainfall': ('precipitation', 'Use "precipitation" for accuracy (includes rain, snow, etc.) unless specifically rain'),
        }

        for i, line in enumerate(self.content_lines, 1):
            line_lower = line.lower()

            for term, (preferred, reason) in terminology_guide.items():
                if term in line_lower:
                    self.issues.append(ReviewIssue(
                        category="Terminology",
                        severity=Severity.SUGGESTION,
                        message=f"Consider terminology: '{term}'",
                        suggestion=f"WMO prefers '{preferred}'. {reason}",
                        line_number=i,
                        flagged_text=term
                    ))

    def check_abbreviations(self):
        """Check that abbreviations are defined on first use"""

        for i, line in enumerate(self.content_lines, 1):
            for abbrev, full_form in self.WMO_ABBREVIATIONS.items():
                if abbrev in line:
                    # Check if defined in same line
                    patterns = [
                        f'{abbrev}\\s*\\([^)]*{re.escape(full_form)}[^)]*\\)',
                        f'{re.escape(full_form)}\\s*\\({abbrev}\\)'
                    ]

                    is_defined = any(re.search(p, line, re.IGNORECASE) for p in patterns)

                    if is_defined:
                        self.defined_abbreviations.add(abbrev)
                    elif abbrev not in self.defined_abbreviations and abbrev != 'WMO':
                        self.issues.append(ReviewIssue(
                            category="Style Guide - Abbreviations",
                            severity=Severity.WARNING,
                            message=f"Abbreviation '{abbrev}' not defined on first use",
                            suggestion=f"Define as: {full_form} ({abbrev})",
                            line_number=i,
                            flagged_text=abbrev
                        ))
                        self.defined_abbreviations.add(abbrev)

    def check_news_article_standards(self):
        """Additional checks for news articles"""

        # Check for sentence case in title
        first_heading = None
        for i, line in enumerate(self.content_lines, 1):
            if re.match(r'^#\s+(.+)$', line) or re.search(r'<h1[^>]*>(.+?)</h1>', line, re.IGNORECASE):
                first_heading = (i, line)
                break

        if first_heading:
            i, line = first_heading
            # Simple check for title case vs sentence case
            words = re.findall(r'\b[A-Z][a-z]*\b', line)
            if len(words) > len(line.split()) * 0.5:  # More than half are capitalized
                self.issues.append(ReviewIssue(
                    category="News Article Standards",
                    severity=Severity.WARNING,
                    message="Title appears to use title case",
                    suggestion="News articles should use sentence case: 'New climate report shows...' not 'New Climate Report Shows...'",
                    line_number=i
                ))

        # Check for engaging opening
        first_paragraph = None
        for line in self.content_lines[:20]:  # Check first 20 lines
            if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('<'):
                if len(line.split()) > 10:
                    first_paragraph = line
                    break

        if first_paragraph:
            # Check if it answers key questions
            has_what = any(word in first_paragraph.lower() for word in ['announce', 'reveal', 'show', 'report', 'find'])
            has_when = any(re.search(pattern, first_paragraph, re.IGNORECASE)
                          for pattern in [r'\b\d{4}\b', r'\btoday\b', r'\byesterday\b', r'\bthis week\b'])

            if not (has_what or has_when):
                self.issues.append(ReviewIssue(
                    category="News Article Standards - Storytelling",
                    severity=Severity.SUGGESTION,
                    message="Opening paragraph could be more engaging",
                    suggestion="Lead with the news value: What happened? When? Why does it matter? Hook readers immediately"
                ))

        # Check article length (news articles should be concise)
        word_count = len(self.content.split())
        if word_count > 800:
            self.issues.append(ReviewIssue(
                category="News Article Standards",
                severity=Severity.SUGGESTION,
                message=f"Article is lengthy ({word_count} words)",
                suggestion="Web news articles are most effective at 400-600 words. Consider breaking into multiple articles or adding subheadings"
            ))

    def check_seo(self):
        """Check SEO best practices"""

        content_lower = self.content.lower()

        # Check for meta description
        has_meta_desc = bool(re.search(r'<meta\s+name=["\']description["\']', self.content, re.IGNORECASE))

        if '<meta' in content_lower and not has_meta_desc:
            self.issues.append(ReviewIssue(
                category="SEO",
                severity=Severity.WARNING,
                message="Missing meta description",
                suggestion="Add meta description (150-160 characters) to improve search visibility"
            ))

        if has_meta_desc:
            meta_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
                                  self.content, re.IGNORECASE)
            if meta_match:
                desc_len = len(meta_match.group(1))
                if desc_len < 120:
                    self.issues.append(ReviewIssue(
                        category="SEO",
                        severity=Severity.SUGGESTION,
                        message=f"Meta description is short ({desc_len} characters)",
                        suggestion="Aim for 150-160 characters for optimal search result display"
                    ))
                elif desc_len > 160:
                    self.issues.append(ReviewIssue(
                        category="SEO",
                        severity=Severity.WARNING,
                        message=f"Meta description is too long ({desc_len} characters)",
                        suggestion="Keep under 160 characters to avoid truncation in search results"
                    ))

    def check_target_audience(self):
        """Check if content is appropriate for target audiences"""

        # Check for audience-appropriate language
        content_lower = self.content.lower()

        # Look for indicators of audience consideration
        audience_indicators = ['public', 'everyone', 'people', 'communities', 'citizens']
        technical_density = len(re.findall(r'\b(?:parameter|algorithm|methodology|analysis|data|system)\b',
                                          content_lower))

        total_words = len(self.content.split())

        if total_words > 0 and technical_density / total_words > 0.05:  # More than 5% technical terms
            has_audience_consideration = any(ind in content_lower for ind in audience_indicators)

            if not has_audience_consideration:
                self.issues.append(ReviewIssue(
                    category="Target Audience",
                    severity=Severity.WARNING,
                    message="Content appears highly technical",
                    suggestion="WMO content serves diverse audiences (public, policymakers, journalists, scientists). Consider adding context or explanations for general readers"
                ))

    def check_formatting(self):
        """Check formatting issues"""

        for i, line in enumerate(self.content_lines, 1):
            # Check for multiple spaces
            if '  ' in line:
                self.issues.append(ReviewIssue(
                    category="Formatting",
                    severity=Severity.ERROR,
                    message="Multiple consecutive spaces found",
                    suggestion="Use single spaces between words",
                    line_number=i
                ))

            # Check for inconsistent punctuation spacing
            if re.search(r'\w[.!?,;:][A-Z]', line):
                self.issues.append(ReviewIssue(
                    category="Formatting",
                    severity=Severity.ERROR,
                    message="Missing space after punctuation",
                    suggestion="Add space after punctuation marks",
                    line_number=i
                ))

    def check_links_and_references(self):
        """Check links and external references"""

        # HTML links
        for match in re.finditer(r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']*)["\']', self.content, re.IGNORECASE):
            url = match.group(1)
            line_num = self.content[:match.start()].count('\n') + 1

            if not url or url in ['#', '']:
                self.issues.append(ReviewIssue(
                    category="Links",
                    severity=Severity.ERROR,
                    message="Empty or placeholder link",
                    suggestion="Provide valid URL or remove link",
                    line_number=line_num
                ))
            elif url.startswith('http://') and 'localhost' not in url:
                self.issues.append(ReviewIssue(
                    category="Links",
                    severity=Severity.WARNING,
                    message="Link uses HTTP instead of HTTPS",
                    suggestion="Use HTTPS for security and SEO",
                    line_number=line_num,
                    flagged_text=url
                ))

        # Markdown links
        for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', self.content):
            url = match.group(2)
            line_num = self.content[:match.start()].count('\n') + 1

            if not url or url == '#':
                self.issues.append(ReviewIssue(
                    category="Links",
                    severity=Severity.ERROR,
                    message="Empty or placeholder link",
                    suggestion="Provide valid URL or remove link",
                    line_number=line_num
                ))

    def _extract_phrase(self, line: str, phrase: str) -> str:
        """Extract a phrase from a line (case-insensitive)"""
        match = re.search(phrase, line, re.IGNORECASE)
        return match.group(0) if match else phrase

    def generate_report(self, strategic_alignment: StrategicAlignment) -> str:
        """Generate formatted review report"""

        report = []
        report.append("=" * 80)
        report.append("BILLIE JEAN - WMO WEB CONTENT REVIEW REPORT")
        report.append("=" * 80)
        report.append("")

        # Content type
        if self.content_type == ContentType.NEWS_ARTICLE:
            report.append("Content Type: NEWS ARTICLE")
        elif self.content_type == ContentType.WEB_PAGE:
            report.append("Content Type: WEB PAGE")
        report.append("")

        # Strategic Alignment Summary
        report.append("STRATEGIC ALIGNMENT WITH WMO MISSION")
        report.append("-" * 80)
        coverage = strategic_alignment.get_coverage()
        covered = strategic_alignment.get_covered_areas()
        missing = strategic_alignment.get_missing_areas()

        report.append(f"Overall Coverage: {coverage:.0f}%")
        report.append("")

        if covered:
            report.append("✓ Strategic Areas Addressed:")
            for area in covered:
                report.append(f"  • {area}")
            report.append("")

        if missing:
            report.append("Areas Not Addressed:")
            for area in missing:
                report.append(f"  • {area}")
            report.append("")

        if coverage < 40:
            report.append("*[Consider: Could this content better connect to WMO's core mission areas?]*")
            report.append("")

        # Issues Summary
        report.append("REVIEW SUMMARY")
        report.append("-" * 80)

        critical = sum(1 for i in self.issues if i.severity == Severity.CRITICAL)
        errors = sum(1 for i in self.issues if i.severity == Severity.ERROR)
        warnings = sum(1 for i in self.issues if i.severity == Severity.WARNING)
        suggestions = sum(1 for i in self.issues if i.severity == Severity.SUGGESTION)

        report.append(f"Total Issues: {len(self.issues)}")
        report.append(f"  • Critical: {critical}")
        report.append(f"  • Errors: {errors}")
        report.append(f"  • Warnings: {warnings}")
        report.append(f"  • Suggestions: {suggestions}")
        report.append("")

        if not self.issues:
            report.append("✓ Excellent! No issues found. Content meets WMO standards.")
            report.append("")
        else:
            # Group by category
            by_category = {}
            for issue in self.issues:
                if issue.category not in by_category:
                    by_category[issue.category] = []
                by_category[issue.category].append(issue)

            report.append("DETAILED FINDINGS")
            report.append("=" * 80)
            report.append("")

            # Number issues for summary
            issue_num = 1
            for category in sorted(by_category.keys()):
                report.append(f"{category.upper()}")
                report.append("-" * 80)

                for issue in by_category[category]:
                    report.append(f"{issue_num}. {issue.format_output()}")
                    issue_num += 1

                report.append("")

        # Recommendations
        if self.issues:
            report.append("PRIORITY RECOMMENDATIONS")
            report.append("-" * 80)
            report.append("")
            report.append("1. Address CRITICAL and ERROR level issues first")
            report.append("2. Review strategic messaging alignment")
            report.append("3. Ensure WCAG 2.1 accessibility compliance")
            report.append("4. Apply WMO style guide consistently")
            report.append("5. Optimize for target audiences")
            report.append("")

        return "\n".join(report)


def interactive_review():
    """Interactive review mode"""
    print("=" * 80)
    print("BILLIE JEAN - WMO Web Content Reviewer 2.0")
    print("=" * 80)
    print("")
    print("Before I begin reviewing your content, could you tell me what kind of")
    print("web product this is for?")
    print("")
    print("1. Standard Web Page")
    print("   (Accessible, impactful content for diverse audiences: public,")
    print("   journalists, UN agencies, policymakers, scientists)")
    print("")
    print("2. Web News Article")
    print("   (Impactful, concise, engaging news writing with storytelling)")
    print("")

    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == '1':
            content_type = ContentType.WEB_PAGE
            break
        elif choice == '2':
            content_type = ContentType.NEWS_ARTICLE
            break
        else:
            print("Please enter 1 or 2")

    print("")
    print("Please paste your content (press Ctrl+D when finished):")
    print("")

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    content = '\n'.join(lines)

    if not content.strip():
        print("No content provided.")
        return

    print("")
    print("Reviewing content...")
    print("")

    reviewer = BillieJean(content_type)
    issues, alignment = reviewer.review(content)
    reviewer.issues = issues

    print(reviewer.generate_report(alignment))


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Billie Jean - WMO Web Content Reviewer 2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python billie_jean.py

  # Review a file as web page
  python billie_jean.py --type page content.html

  # Review a file as news article
  python billie_jean.py --type article news.md

  # From stdin
  cat content.md | python billie_jean.py --type page -

  # JSON output
  python billie_jean.py --type page --format json content.html
        """
    )

    parser.add_argument(
        'file',
        nargs='?',
        help='File to review (use "-" for stdin, omit for interactive mode)'
    )

    parser.add_argument(
        '--type',
        choices=['page', 'article'],
        help='Content type: "page" for web page, "article" for news article'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--severity',
        default='CRITICAL,ERROR,WARNING,SUGGESTION',
        help='Filter by severity levels (comma-separated)'
    )

    args = parser.parse_args()

    # Interactive mode if no file specified
    if not args.file:
        interactive_review()
        return

    # Determine content type
    if args.type == 'article':
        content_type = ContentType.NEWS_ARTICLE
    elif args.type == 'page':
        content_type = ContentType.WEB_PAGE
    else:
        content_type = ContentType.UNKNOWN

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

    # Review content
    reviewer = BillieJean(content_type)
    issues, alignment = reviewer.review(content)

    # Filter by severity
    severity_filter = set(s.strip().upper() for s in args.severity.split(','))
    filtered_issues = [i for i in issues if i.severity.value in severity_filter]
    reviewer.issues = filtered_issues

    # Output
    if args.format == 'json':
        import json
        output = {
            'content_type': content_type.value,
            'strategic_alignment': {
                'coverage_percentage': alignment.get_coverage(),
                'covered_areas': alignment.get_covered_areas(),
                'missing_areas': alignment.get_missing_areas()
            },
            'summary': {
                'total_issues': len(filtered_issues),
                'critical': sum(1 for i in filtered_issues if i.severity == Severity.CRITICAL),
                'errors': sum(1 for i in filtered_issues if i.severity == Severity.ERROR),
                'warnings': sum(1 for i in filtered_issues if i.severity == Severity.WARNING),
                'suggestions': sum(1 for i in filtered_issues if i.severity == Severity.SUGGESTION)
            },
            'issues': [
                {
                    'number': idx + 1,
                    'category': i.category,
                    'severity': i.severity.value,
                    'message': i.message,
                    'suggestion': i.suggestion,
                    'line_number': i.line_number,
                    'flagged_text': i.flagged_text,
                    'context': i.context
                }
                for idx, i in enumerate(filtered_issues)
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print(reviewer.generate_report(alignment))

    # Exit code
    if any(i.severity in [Severity.CRITICAL, Severity.ERROR] for i in filtered_issues):
        sys.exit(1)


if __name__ == '__main__':
    main()
