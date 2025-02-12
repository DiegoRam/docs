"""
Web Scraper Documentation

This script is a web scraper that extracts text content from a website and its linked pages.
It saves the extracted content to a text file.

Usage:
    python scrap.py URL [-o OUTPUT_FILE]

Example:
    python scrap.py https://example.com -o results.txt
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
import os

def fetch_page(url):
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        str: The HTML content of the page.

    Raises:
        requests.RequestException: If the page cannot be fetched.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.text

def extract_links(soup, base_url):
    """
    Extracts all links from a BeautifulSoup object and converts them to absolute URLs.

    Args:
        soup (BeautifulSoup): Parsed HTML content.
        base_url (str): The base URL for converting relative URLs to absolute URLs.

    Returns:
        set: A set of absolute URLs found in the page.
    """
    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = urljoin(base_url, a_tag['href'])
        links.add(link)
    return links

def scrape_page_to_text(url):
    """
    Scrapes a webpage and extracts its text content, removing script and style elements.

    Args:
        url (str): The URL of the page to scrape.

    Returns:
        str: The extracted text content with stripped whitespace.
    """
    html = fetch_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    text = soup.get_text(separator='\n')
    return text.strip()

def parse_arguments():
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing:
            - url: The target URL to scrape
            - output: The output file path
    """
    parser = argparse.ArgumentParser(
        description='Web scraper that extracts text from a website and its linked pages'
    )
    parser.add_argument(
        'url',
        type=str,
        help='The URL of the website to scrape (e.g., https://example.com)'
    )
    parser.add_argument(
        '--output', 
        '-o',
        type=str,
        default='documentation.txt',
        help='Output file path (default: documentation.txt)'
    )
    return parser.parse_args()

def main():
    """
    Main function that orchestrates the web scraping process.
    
    - Parses command line arguments
    - Fetches the main page
    - Extracts all links
    - Scrapes text content from each link
    - Saves the content to the specified output file
    """
    try:
        args = parse_arguments()
        base_url = args.url
        output_file = args.output
        
        print(f"Starting to scrape {base_url}")
        print(f"Output will be saved to {output_file}")
        
        # Get and print the absolute file path
        absolute_path = os.path.abspath(output_file)
        file_uri = f"file://{absolute_path}"
        print(f"\nFile URI: {file_uri}")
        
        main_page_html = fetch_page(base_url)
        soup = BeautifulSoup(main_page_html, 'html.parser')
        links = extract_links(soup, base_url)

        with open(output_file, 'w', encoding='utf-8') as file:
            for link in links:
                print(f"Scraping {link}...")
                try:
                    text = scrape_page_to_text(link)
                    file.write(f"URL: {link}\n")
                    file.write(text)
                    file.write("\n\n")
                except requests.RequestException as e:
                    print(f"Failed to scrape {link}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()