# WMO Reference Documents

This directory should contain the official WMO reference documents used by Billie Jean for content review.

## Required Documents

Please place the following PDF documents in this directory:

1. **WMO Writing and Style Guide** (`wmo-style-guide.pdf`)
   - Official WMO guidelines for writing and editorial standards
   - Used for: Style compliance, terminology, formatting rules

2. **WMO Web Best Practices** (`wmo-web-best-practices.pdf`)
   - Guidelines for web content creation
   - Used for: Web-specific standards, accessibility, SEO, user experience

## How Documents are Used

The Billie Jean reviewer implements the rules from these documents in its checking algorithms. While the tool doesn't parse PDFs directly, it encodes the key requirements from these guidelines into its review logic.

### Key Areas Covered:

**From WMO Writing and Style Guide:**
- Proper capitalization of organizational names
- Abbreviation definitions on first use
- Sentence structure and length
- Active vs. passive voice
- Punctuation and formatting
- Terminology standards

**From WMO Web Best Practices:**
- WCAG 2.1 accessibility compliance
- Readability for web audiences
- SEO optimization
- Link best practices
- Heading hierarchy
- Content structure

## Updating the Reviewer

When WMO guidelines are updated:

1. Review the new/changed requirements
2. Update the checking logic in `billie_jean.py`
3. Add new test cases in `examples/`
4. Document changes in release notes

## Additional Resources

For the most up-to-date WMO strategic documents, refer to:

- [WMO Strategic Plan](https://library.wmo.int/idurl/4/69591)
- [WMO Strategic Objectives](https://library.wmo.int/idurl/4/67177)
- [WMO Reform](https://library.wmo.int/idurl/4/68578)
- [WMO Public Website](https://wmo.int)

## Contributing

If you identify gaps between the reviewer's checks and the official guidelines, please:

1. Document the discrepancy
2. Propose a fix in the code
3. Add test cases
4. Submit a pull request
