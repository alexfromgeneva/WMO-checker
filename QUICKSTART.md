# Quick Start Guide

Get started with Billie Jean - WMO Web Content Reviewer in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/alexfromgeneva/WMO-checker.git
cd WMO-checker

# Make the script executable (optional)
chmod +x billie_jean.py
```

No dependencies required! Pure Python 3.7+.

## Basic Usage

### Interactive Mode (Recommended for First-Time Users)

Simply run without arguments:

```bash
python billie_jean.py
```

You'll be asked:
1. What type of content (web page or news article)
2. To paste your content

### Command-Line Mode

Review a file:
```bash
# Web page
python billie_jean.py --type page content.html

# News article
python billie_jean.py --type article news.md
```

### Try the Examples

Test the tool with provided examples:

```bash
# Good example - should show minimal issues
python billie_jean.py --type page examples/good_web_page.html

# Problematic example - will show various issues
python billie_jean.py --type page examples/problematic_web_page.html

# News article examples
python billie_jean.py --type article examples/good_news_article.md
python billie_jean.py --type article examples/problematic_news_article.md
```

## Understanding the Output

The review report includes:

1. **Strategic Alignment** - How well content aligns with WMO's mission
2. **Review Summary** - Count of issues by severity
3. **Detailed Findings** - Specific issues with suggestions

### Severity Levels

- **CRITICAL**: Major issues (strategic misalignment, accessibility violations)
- **ERROR**: Must fix (style guide violations, missing alt text)
- **WARNING**: Should fix (unclear content, undefined abbreviations)
- **SUGGESTION**: Nice to have (improvements for clarity, engagement)

## Common Use Cases

### Before Publishing

```bash
python billie_jean.py --type page draft.html
```

Fix all CRITICAL and ERROR issues before publishing.

### Content Audit

```bash
# Check multiple files
for file in content/*.html; do
  python billie_jean.py --type page "$file"
done
```

### CI/CD Integration

```bash
# Exit with error code if critical issues found
python billie_jean.py --type page --severity CRITICAL,ERROR content.html
```

### JSON Output for Automation

```bash
python billie_jean.py --type page --format json content.html > report.json
```

## What Gets Checked?

✓ **WMO Style Guide**: Terminology, capitalization, abbreviations
✓ **Accessibility**: WCAG 2.1 compliance (alt text, headings, links)
✓ **Readability**: Sentence length, jargon, clarity
✓ **Strategic Alignment**: Connection to WMO mission
✓ **SEO**: Meta descriptions, titles, structure
✓ **Technical Accuracy**: Units, date formats, scientific terms

## Tips for Best Results

1. **Fix in Priority Order**: Critical → Errors → Warnings → Suggestions
2. **Use Context**: Some suggestions may not apply - use editorial judgment
3. **Review Regularly**: Check content during writing, not just before publishing
4. **Check Strategic Fit**: Ensure content connects to WMO's mission
5. **Test Accessibility**: Pay special attention to CRITICAL accessibility issues

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Place WMO reference PDFs in the `docs/` directory
- Customize checks by editing `billie_jean.py` constants
- Create your own content examples

## Getting Help

- Documentation: See [README.md](README.md)
- Examples: Check the `examples/` directory
- Issues: Report at GitHub issues page

## Two Tools Available

This repository includes two tools:

1. **billie_jean.py** (Recommended)
   - Full-featured with strategic alignment checking
   - Interactive mode
   - Mimics the ChatGPT custom GPT functionality

2. **wmo_content_reviewer.py** (Alternative)
   - Simpler, focused on technical checks
   - Good for basic linting

Both tools work similarly, but `billie_jean.py` provides more comprehensive WMO-specific analysis.

---

**Ready to review?** Try: `python billie_jean.py --type page examples/good_web_page.html`
