#!/usr/bin/env python3
"""
ScrapeAI Script to Extract Official HR/Careers Contact Channels for Tech Companies

This script uses the ScrapeAI library to scrape official contact information
from tech company websites, careers pages, and LinkedIn profiles.

Usage:
    python hr_contacts_scraper.py [--api-key YOUR_API_KEY] [--llm openai|anthropic|google]

Requirements:
    - ScrapeAI library installed (pip install scrapeai)
    - API key for your chosen LLM provider (OpenAI, Anthropic, or Google)
    - Chrome/Chromium browser installed for Selenium
"""

import argparse
import json
import os
from typing import List, Dict, Optional

try:
    from scrapeAI import WebScraper
except ImportError:
    print("Error: ScrapeAI library not installed. Please run: pip install scrapeai")
    exit(1)


# List of major tech companies with their careers/HR pages
TECH_COMPANIES = [
    {
        "name": "Google",
        "url": "https://careers.google.com/",
        "description": "Google Careers official portal"
    },
    {
        "name": "Microsoft",
        "url": "https://careers.microsoft.com/",
        "description": "Microsoft Careers official portal"
    },
    {
        "name": "Apple",
        "url": "https://www.apple.com/careers/",
        "description": "Apple Careers official page"
    },
    {
        "name": "Amazon",
        "url": "https://www.amazon.jobs/",
        "description": "Amazon Jobs official portal"
    },
    {
        "name": "Meta (Facebook)",
        "url": "https://www.metacareers.com/",
        "description": "Meta Careers official portal"
    },
    {
        "name": "Netflix",
        "url": "https://jobs.netflix.com/",
        "description": "Netflix Jobs official portal"
    },
    {
        "name": "Salesforce",
        "url": "https://www.salesforce.com/company/careers/",
        "description": "Salesforce Careers page"
    },
    {
        "name": "Adobe",
        "url": "https://www.adobe.com/careers.html",
        "description": "Adobe Careers official page"
    },
    {
        "name": "Oracle",
        "url": "https://www.oracle.com/careers/",
        "description": "Oracle Careers official portal"
    },
    {
        "name": "IBM",
        "url": "https://www.ibm.com/employment/",
        "description": "IBM Employment page"
    },
    {
        "name": "Intel",
        "url": "https://www.intel.com/content/www/us/en/jobs.html",
        "description": "Intel Jobs page"
    },
    {
        "name": "NVIDIA",
        "url": "https://www.nvidia.com/en-us/about-nvidia/careers/",
        "description": "NVIDIA Careers page"
    },
    {
        "name": "Tesla",
        "url": "https://www.tesla.com/careers",
        "description": "Tesla Careers page"
    },
    {
        "name": "Uber",
        "url": "https://www.uber.com/careers/",
        "description": "Uber Careers official page"
    },
    {
        "name": "Airbnb",
        "url": "https://careers.airbnb.com/",
        "description": "Airbnb Careers portal"
    }
]


def get_api_key_from_env(llm_provider: str) -> Optional[str]:
    """Retrieve API key from environment variables based on LLM provider."""
    env_vars = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY"
    }
    
    env_var = env_vars.get(llm_provider.lower())
    if not env_var:
        return None
    
    api_key = os.getenv(env_var)
    if not api_key:
        print(f"Warning: {env_var} environment variable not set.")
        print(f"Please set it using: export {env_var}=your_api_key_here")
    
    return api_key


def scrape_company_contacts(company: Dict, llm_provider: str, api_key: str, verbose: bool = False) -> Dict:
    """
    Scrape a single company's website for HR/careers contact information.
    
    Args:
        company: Dictionary containing company name, URL, and description
        llm_provider: The LLM provider to use (openai, anthropic, google)
        api_key: API key for the LLM provider
        verbose: Whether to show detailed logs
    
    Returns:
        Dictionary containing scraped contact information
    """
    print(f"\n{'='*60}")
    print(f"Scraping: {company['name']}")
    print(f"URL: {company['url']}")
    print(f"Description: {company['description']}")
    print(f"{'='*60}\n")
    
    # Configure the scraper
    config = {
        "url": company["url"],
        "prompt": """Find all official HR and careers contact information including:
        - Official HR email addresses
        - Careers/recruitment email addresses
        - Contact forms for job inquiries
        - Phone numbers for HR departments
        - Links to contact pages
        - Social media links for careers (LinkedIn, Twitter, etc.)
        - Physical addresses for HR offices
        
        Extract only official contact channels listed on this page. 
        Return the information in a structured format with clear labels.""",
        "llm": {
            "provider": llm_provider,
            "api_key": api_key
        },
        "verbose": verbose,
        "headless": True  # Run browser in headless mode
    }
    
    try:
        # Initialize and run the scraper
        scraper = WebScraper(config)
        result = scraper.invoke()
        
        return {
            "company": company["name"],
            "url": company["url"],
            "status": "success",
            "contacts": result if result else "No contact information found"
        }
    
    except Exception as e:
        error_msg = str(e)
        print(f"Error scraping {company['name']}: {error_msg}")
        return {
            "company": company["name"],
            "url": company["url"],
            "status": "error",
            "error": error_msg
        }


def scrape_all_companies(companies: List[Dict], llm_provider: str, api_key: str, 
                         verbose: bool = False, output_file: Optional[str] = None) -> List[Dict]:
    """
    Scrape multiple companies for HR/careers contact information.
    
    Args:
        companies: List of company dictionaries
        llm_provider: The LLM provider to use
        api_key: API key for the LLM provider
        verbose: Whether to show detailed logs
        output_file: Optional file path to save results as JSON
    
    Returns:
        List of dictionaries containing scraped contact information
    """
    results = []
    
    for i, company in enumerate(companies, 1):
        print(f"\n[{i}/{len(companies)}] Processing {company['name']}...")
        result = scrape_company_contacts(company, llm_provider, api_key, verbose)
        results.append(result)
    
    # Save results to JSON file if specified
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\nResults saved to: {output_file}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    return results


def display_results(results: List[Dict]) -> None:
    """Display scraped results in a formatted manner."""
    print("\n\n" + "="*80)
    print("SUMMARY OF SCRAPED HR/CAREERS CONTACT INFORMATION")
    print("="*80)
    
    success_count = sum(1 for r in results if r["status"] == "success")
    error_count = sum(1 for r in results if r["status"] == "error")
    
    print(f"\nTotal companies processed: {len(results)}")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")
    
    for result in results:
        print(f"\n{'-'*60}")
        print(f"Company: {result['company']}")
        print(f"URL: {result['url']}")
        print(f"Status: {result['status'].upper()}")
        
        if result["status"] == "success":
            contacts = result.get("contacts", "No information found")
            if contacts:
                print(f"Contact Information:\n{contacts}")
            else:
                print("No contact information found on this page.")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "="*80)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Scrape official HR/careers contact channels from tech company websites using ScrapeAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --api-key sk-your-openai-key
  %(prog)s --llm anthropic --api-key your-anthropic-key
  %(prog)s --llm google --api-key your-google-key --output results.json
  %(prog)s --verbose --output contacts.json

Environment Variables:
  OPENAI_API_KEY      Your OpenAI API key
  ANTHROPIC_API_KEY   Your Anthropic API key
  GOOGLE_API_KEY      Your Google AI API key

Note: This script requires Chrome/Chromium to be installed for Selenium to work.
        """
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key for the LLM provider (can also be set via environment variable)"
    )
    
    parser.add_argument(
        "--llm",
        type=str,
        choices=["openai", "anthropic", "google"],
        default="openai",
        help="LLM provider to use (default: openai)"
    )
    
    parser.add_argument(
        "--companies",
        type=str,
        nargs="+",
        help="Specific company names to scrape (default: all companies in the list)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Save results to a JSON file"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or get_api_key_from_env(args.llm)
    
    if not api_key:
        print(f"\nError: No API key provided for {args.llm}.")
        print(f"Please provide an API key using --api-key or set the appropriate environment variable:")
        if args.llm == "openai":
            print("  export OPENAI_API_KEY=your_key_here")
        elif args.llm == "anthropic":
            print("  export ANTHROPIC_API_KEY=your_key_here")
        elif args.llm == "google":
            print("  export GOOGLE_API_KEY=your_key_here")
        exit(1)
    
    # Filter companies if specific ones were requested
    companies_to_scrape = TECH_COMPANIES
    if args.companies:
        company_names_lower = [name.lower() for name in args.companies]
        companies_to_scrape = [
            c for c in TECH_COMPANIES 
            if c["name"].lower() in company_names_lower
        ]
        if not companies_to_scrape:
            print(f"No matching companies found. Available companies:")
            for c in TECH_COMPANIES:
                print(f"  - {c['name']}")
            exit(1)
    
    print(f"\nStarting HR/Careers Contact Scraper")
    print(f"LLM Provider: {args.llm}")
    print(f"Companies to scrape: {len(companies_to_scrape)}")
    if args.output:
        print(f"Output file: {args.output}")
    
    # Perform scraping
    results = scrape_all_companies(
        companies=companies_to_scrape,
        llm_provider=args.llm,
        api_key=api_key,
        verbose=args.verbose,
        output_file=args.output
    )
    
    # Display results
    display_results(results)
    
    print("\nScraping complete!")


if __name__ == "__main__":
    main()
