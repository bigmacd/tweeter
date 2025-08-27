"""
Parse email.html file and extract specific sections:
- Attacks & Vulnerabilities
- Strategies & Tactics
- Miscellaneous
- Quick Links
"""

from bs4 import BeautifulSoup
import re
import os

def parse_email_sections(html_content):
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Dictionary to store extracted sections
    sections = {
        "Attacks & Vulnerabilities": [],
        "Strategies & Tactics": [],
        "Miscellaneous": [],
        "Quick Links": []
    }
    
    # Find all h1 elements which contain section headers
    section_headers = soup.find_all('h1')
    
    current_section = None
    
    # Iterate through the document to find section content
    for header in section_headers:
        header_text = header.get_text(strip=True)
        
        # Check if this header matches one of our target sections
        if "Attacks" in header_text and "Vulnerabilities" in header_text:
            current_section = "Attacks & Vulnerabilities"
        elif "Strategies" in header_text and "Tactics" in header_text:
            current_section = "Strategies & Tactics"
        elif "Miscellaneous" in header_text:
            current_section = "Miscellaneous"
        elif "Quick Links" in header_text:
            current_section = "Quick Links"
        else:
            current_section = None
            continue
        
        if current_section:
            # Find the parent table/container that contains this section
            section_container = header.find_parent('table')
            if section_container:
                # Find the next sibling table that contains the actual content
                content_table = section_container.find_next_sibling('table')
                if content_table:
                    articles = extract_articles_from_table(content_table)
                    sections[current_section].extend(articles)
    
    return sections


def fixUpHref(href):
    # href is 'https://tracking.tldrnewsletter.com/CL0/https:%2F%2Fwww.bleepingcomputer.com%2Fnews%2Fsecurity%2Fnetherlands-citrix-netscaler-flaw-cve-2025-6543-exploited-to-breach-orgs%2F%3Futm_source=tldrinfosec/1/01000198a38abf5c-1df751a1-4ff3-45f8-9a34-6ef5f324d7f4-000000/yCsUCrlwhItaPww2IcSKVDOt_jS-GXFAehMaXQmiK1A=418'
    parts = href.split('https')
    part = parts[2].replace('%2F', '/')
    part = part.split('%3F')[0]
    return 'https' + part


def extract_articles_from_table(table):
    """
    Extract article information from a content table.
    
    Args:
        table: BeautifulSoup table element
        
    Returns:
        list: List of article dictionaries
    """
    articles = []
    
    # Find all links within the table that have article titles
    article_links = table.find_all('a', href=True)
    
    for link in article_links:
        # Skip navigation links and referral links
        href = link.get('href', '')
        if any(skip_term in href.lower() for skip_term in ['refer.', 'advertise', 'unsubscribe', 'manage']):
            continue
            
        # Get the article title from the strong tag within the link
        strong_tag = link.find('strong')
        if strong_tag:
            title = strong_tag.get_text(strip=True)
            
            # Find the description text that follows the link
            description = ""
            
            # Look for the next span with description text
            parent_div = link.find_parent('div', class_='text-block')
            if parent_div:
                # Get all text after the link, excluding the title
                text_parts = []
                for element in parent_div.find_all(string=True):
                    text = element.strip()
                    # Skip the title text and empty strings
                    if text and text != title and not text.startswith('http'):
                        # Clean up the text
                        cleaned_text = re.sub(r'\s+', ' ', text).strip()
                        if cleaned_text and len(cleaned_text) > 10:  # Only add meaningful text
                            text_parts.append(cleaned_text)
                
                # Join the text parts and clean up
                if text_parts:
                    description = ' '.join(text_parts)
                    # Remove HTML entities and clean up
                    description = re.sub(r'&[a-zA-Z0-9#]+;', ' ', description)
                    description = re.sub(r'\s+', ' ', description).strip()
            
            if title:  # Only add if we have a title
                article = {
                    'title': title,
                    'url': fixUpHref(href),
                    'description': description
                }
                articles.append(article)
    
    return articles


def parseSections(html_content):
    # main function to call from your code
    try:
        # Parse the email sections
        print("Parsing email.html file...")
        sections = parse_email_sections(html_content)
        return sections
            
    except Exception as e:
        print(f"An error occurred: {e}")


