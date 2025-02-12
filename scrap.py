import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.text

def extract_links(soup, base_url):
    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = urljoin(base_url, a_tag['href'])
        links.add(link)
    return links

def scrape_page_to_text(url):
    html = fetch_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    text = soup.get_text(separator='\n')
    return text.strip()

def parse_arguments():
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
    try:
        args = parse_arguments()
        base_url = args.url
        output_file = args.output
        
        print(f"Starting to scrape {base_url}")
        print(f"Output will be saved to {output_file}")
        
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