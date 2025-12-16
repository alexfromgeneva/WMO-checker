# Billie Jean - WMO Web Content Reviewer 2.0

A comprehensive content review tool for World Meteorological Organization (WMO) web content. This tool automatically checks web content for style compliance, accessibility, terminology accuracy, and overall quality to ensure it meets WMO standards.

## Features

### 🌐 WMO-Specific Checks
- **Meteorological Terminology**: Validates proper use of weather and climate terminology
- **Abbreviation Definitions**: Ensures WMO abbreviations (GCOS, WIS, WIGOS, etc.) are defined on first use
- **Technical Accuracy**: Checks for proper units, date formats, and scientific notation
- **Style Guide Compliance**: Enforces WMO writing standards and conventions

### ♿ Accessibility (WCAG Compliance)
- Image alt text validation
- Heading hierarchy checks
- Link text quality (avoiding generic "click here")
- Document structure validation

### 📝 Content Quality
- Grammar and spelling checks
- Sentence length and clarity analysis
- Active vs. passive voice suggestions
- Pronoun clarity verification

### 🔗 Technical Validation
- Link validation and HTTPS enforcement
- SEO optimization checks (meta descriptions, titles)
- Heading structure and hierarchy
- Date format standardization (ISO 8601)

## Installation

### Requirements
- Python 3.7 or higher

### Setup
```bash
# Clone the repository
git clone https://github.com/alexfromgeneva/WMO-checker.git
cd WMO-checker

# Make the script executable (optional)
chmod +x wmo_content_reviewer.py
```

## Usage

### Basic Usage

Review a single file:
```bash
python wmo_content_reviewer.py content.html
```

Review from stdin:
```bash
cat content.md | python wmo_content_reviewer.py -
```

### Advanced Options

Filter by severity level:
```bash
# Only show errors and warnings
python wmo_content_reviewer.py --severity ERROR,WARNING content.html

# Only show errors
python wmo_content_reviewer.py --severity ERROR content.html
```

JSON output for integration:
```bash
python wmo_content_reviewer.py --format json content.html
```

### Command-Line Options

```
usage: wmo_content_reviewer.py [-h] [--severity SEVERITY] [--format {text,json}] file

positional arguments:
  file                  File to review (use "-" for stdin)

optional arguments:
  -h, --help           show this help message and exit
  --severity SEVERITY  Comma-separated list of severity levels to report
                       (ERROR,WARNING,INFO,SUGGESTION)
  --format {text,json} Output format (default: text)
```

## Review Categories

### 1. Terminology
Checks for proper use of WMO meteorological terms:
- Climate change vs. global warming
- Temperature (not "temp")
- Precipitation (specific types preferred)
- Meteorological (not "weather-related")

### 2. Abbreviations
Ensures WMO abbreviations are defined on first use:
- WMO - World Meteorological Organization
- GCOS - Global Climate Observing System
- WIGOS - WMO Integrated Global Observing System
- WIS - WMO Information System
- GAW - Global Atmosphere Watch
- And many more...

### 3. Style Guide
Enforces WMO writing standards:
- Proper capitalization
- Sentence length (recommends <40 words)
- Active voice preference
- Clear pronoun references

### 4. Accessibility
WCAG compliance checks:
- Alt text for images
- Proper heading hierarchy (H1, H2, H3, etc.)
- Descriptive link text
- Document structure

### 5. Technical Accuracy
Scientific content validation:
- Temperature units (°C, °F, K)
- ISO 8601 date format (YYYY-MM-DD)
- Pressure units (hPa, Pa)
- Distance units (m, km)

### 6. Grammar & Clarity
Language quality checks:
- Common grammar mistakes (its vs. it's)
- Double spaces
- Unclear pronoun references
- Sentence clarity

### 7. Links
Link validation and security:
- Empty or placeholder links
- HTTP vs. HTTPS (security)
- Generic link text
- Link accessibility

### 8. SEO
Search engine optimization:
- Meta description presence and length (150-160 chars)
- Title tag validation
- Heading structure for SEO

## Issue Severity Levels

- **ERROR**: Critical issues that must be fixed (e.g., missing alt text, empty links)
- **WARNING**: Important issues that should be addressed (e.g., HTTP links, undefined abbreviations)
- **INFO**: Informational notices that may need attention (e.g., passive voice)
- **SUGGESTION**: Optional improvements for better content (e.g., sentence length)

## Examples

### Example 1: Review HTML Content

```bash
python wmo_content_reviewer.py examples/sample_page.html
```

Output:
```
================================================================================
WMO WEB CONTENT REVIEW REPORT
================================================================================

SUMMARY:
  Total Issues: 5
  - Errors: 1
  - Warnings: 2
  - Info: 1
  - Suggestions: 1

--------------------------------------------------------------------------------

ACCESSIBILITY:
--------------------------------------------------------------------------------
[ERROR] Accessibility: Line 15: Image missing alt text attribute (required for WCAG compliance)
  Context: <img src="weather-map.png">

TERMINOLOGY:
--------------------------------------------------------------------------------
[SUGGESTION] Terminology: Line 23: Use 'temperature' instead of abbreviation 'temp' in formal content
  Context: The temp will rise to 25 degrees tomorrow.

...
```

### Example 2: Review Markdown Content

```bash
python wmo_content_reviewer.py examples/article.md
```

### Example 3: Integration with CI/CD

```bash
# In your CI pipeline
python wmo_content_reviewer.py --severity ERROR --format json content.html > results.json

# Exit code 1 if errors found, 0 otherwise
if [ $? -eq 1 ]; then
  echo "Content review failed with errors"
  exit 1
fi
```

## Use Cases

### 1. Pre-Publication Review
Review content before publishing to ensure it meets WMO standards:
```bash
python wmo_content_reviewer.py draft-article.html
```

### 2. Bulk Content Audit
Review multiple files in a directory:
```bash
for file in content/*.html; do
  echo "Reviewing $file..."
  python wmo_content_reviewer.py "$file"
done
```

### 3. Continuous Integration
Add to your CI/CD pipeline to automatically review content:
```yaml
# .github/workflows/content-review.yml
name: Content Review
on: [push, pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Review Content
        run: |
          python wmo_content_reviewer.py --severity ERROR,WARNING content/*.html
```

### 4. Editor Integration
Use as a linting tool in your text editor or IDE.

## Configuration

The tool comes with sensible defaults for WMO content, but you can customize the checks by modifying the class constants in `wmo_content_reviewer.py`:

- `WMO_TERMINOLOGY`: Preferred meteorological terms
- `WMO_ABBREVIATIONS`: List of abbreviations to check
- `STANDARD_UNITS`: WMO-approved measurement units
- `COMMON_ISSUES`: Patterns to detect and suggest fixes

## Best Practices

1. **Review Early and Often**: Run the reviewer during content creation, not just before publication
2. **Focus on Errors First**: Address ERROR-level issues before WARNING or SUGGESTION level
3. **Context Matters**: Some suggestions may not apply to your specific content - use judgment
4. **Combine with Manual Review**: This tool supplements, not replaces, human editorial review
5. **Update Terminology**: Keep WMO terminology lists updated as standards evolve

## Limitations

- Does not check for factual accuracy of meteorological data
- Cannot validate external links (requires network access)
- May not catch context-specific terminology issues
- Grammar checking is basic - consider using additional tools for comprehensive grammar review

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Adding New Checks

To add a new content check:

1. Create a new method in the `WMOContentReviewer` class:
```python
def check_my_new_rule(self):
    """Check for my new rule."""
    for i, line in enumerate(self.content_lines, 1):
        if some_condition:
            self.issues.append(Issue(
                category="My Category",
                severity=Severity.WARNING,
                message="Description of the issue",
                line_number=i,
                context=line.strip()[:100]
            ))
```

2. Call it from the `review()` method:
```python
def review(self, content: str) -> List[Issue]:
    # ... existing code ...
    self.check_my_new_rule()  # Add this line
    # ... existing code ...
```

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/alexfromgeneva/WMO-checker/issues
- Documentation: This README

## Acknowledgments

Created to support the World Meteorological Organization's mission of excellence in weather, climate, and water information services.

---

**Version**: 2.0
**Last Updated**: 2025-12-16
**Maintainer**: WMO Content Team
