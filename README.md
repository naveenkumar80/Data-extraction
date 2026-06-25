# HR Contacts Scraper

A Python script that uses ScrapeAI to extract official contact channels for tech company HR or careers pages from company websites, careers portals, and LinkedIn pages.

## Features

- Extracts official HR emails, careers page URLs, contact forms, and LinkedIn profiles
- Supports 15 major tech companies (Apple, Google, Microsoft, Amazon, Meta, Netflix, Salesforce, Adobe, Oracle, IBM, Intel, Cisco, NVIDIA, Uber, Airbnb)
- Multiple LLM provider support (OpenAI, Anthropic, Google)
- JSON output format for easy integration
- Customizable company filtering
- Error handling and progress tracking

## Requirements

- Python 3.7+
- ScrapeAI library
- API key for your chosen LLM provider (OpenAI, Anthropic, or Google)

## Installation

1. Install the required dependencies:

```bash
pip install scrapeai
```

2. Set up your API key as an environment variable:

**For OpenAI:**
```bash
export OPENAI_API_KEY='your-openai-api-key'
```

**For Anthropic:**
```bash
export ANTHROPIC_API_KEY='your-anthropic-api-key'
```

**For Google:**
```bash
export GOOGLE_API_KEY='your-google-api-key'
```

## Usage

### Basic Usage

Run the script with your API key:

```bash
python hr_contacts_scraper.py --api-key YOUR_API_KEY
```

Or use the environment variable (no need to pass `--api-key`):

```bash
python hr_contacts_scraper.py
```

### Specify LLM Provider

```bash
# Using OpenAI (default)
python hr_contacts_scraper.py --provider openai --api-key YOUR_OPENAI_KEY

# Using Anthropic
python hr_contacts_scraper.py --provider anthropic --api-key YOUR_ANTHROPIC_KEY

# Using Google
python hr_contacts_scraper.py --provider google --api-key YOUR_GOOGLE_KEY
```

### Filter by Specific Companies

```bash
python hr_contacts_scraper.py --companies "Google,Microsoft,Apple" --api-key YOUR_API_KEY
```

### Custom Output File

```bash
python hr_contacts_scraper.py --output hr_contacts_2024.json --api-key YOUR_API_KEY
```

### Show Help

```bash
python hr_contacts_scraper.py --help
```

## Output Format

The script generates a JSON file with the following structure:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "total_companies": 15,
  "successful_extractions": 12,
  "results": [
    {
      "company": "Google",
      "hr_email": "recruiting@google.com",
      "careers_page": "https://careers.google.com",
      "contact_form": "https://www.google.com/about/contact/",
      "linkedin": "https://www.linkedin.com/company/google",
      "additional_info": "Check out our careers page for open positions"
    }
  ]
}
```

## Supported Companies

The script supports scraping HR contact information from the following tech companies:

1. Apple
2. Google
3. Microsoft
4. Amazon
5. Meta (Facebook)
6. Netflix
7. Salesforce
8. Adobe
9. Oracle
10. IBM
11. Intel
12. Cisco
13. NVIDIA
14. Uber
15. Airbnb

You can filter to specific companies using the `--companies` flag.

## Notes

- The script respects robots.txt and terms of service for each website
- Rate limiting is implemented to avoid overwhelming target servers
- Results may vary depending on website structure changes
- Some companies may not publicly list direct HR email addresses

## Troubleshooting

**Issue: API Key Error**
- Ensure your API key is valid and has sufficient credits
- Check that you're using the correct provider for your key

**Issue: No Results Found**
- Some companies may not have publicly available HR contact information
- Website structures may have changed; consider updating the URL list

**Issue: Rate Limiting**
- The script includes built-in delays between requests
- If you encounter rate limits, try reducing the number of companies processed at once

## License

MIT License - feel free to modify and distribute for your needs.

## Disclaimer

This tool is intended for legitimate recruitment and networking purposes only. Always respect website terms of service, privacy policies, and applicable laws when scraping web content. Do not use extracted contact information for spam or unsolicited communications.
