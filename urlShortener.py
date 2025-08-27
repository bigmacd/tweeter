#!/usr/bin/env python3
"""
URL Shortening Service Examples

This script demonstrates how to call various URL shortening services:
1. TinyURL - No API key required
2. Bitly - Requires API key
3. is.gd - No API key required
4. v.gd - No API key required
"""

import requests
import json
from urllib.parse import quote

class URLShortener:
    """URL shortening service wrapper"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'URL-Shortener-Python/1.0'
        })
    
    def shorten_with_tinyurl(self, long_url):
        """
        Shorten URL using TinyURL service (no API key required)
        
        Args:
            long_url (str): The URL to shorten
            
        Returns:
            str: Shortened URL or None if failed
        """
        try:
            api_url = f"http://tinyurl.com/api-create.php?url={quote(long_url)}"
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                short_url = response.text.strip()
                # TinyURL returns the original URL if there's an error
                if short_url.startswith('http') and 'tinyurl.com' in short_url:
                    return short_url
                else:
                    print(f"TinyURL Error: {short_url}")
                    return None
            else:
                print(f"TinyURL HTTP Error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"TinyURL Request Error: {e}")
            return None
    
    def shorten_with_isgd(self, long_url):
        """
        Shorten URL using is.gd service (no API key required)
        
        Args:
            long_url (str): The URL to shorten
            
        Returns:
            str: Shortened URL or None if failed
        """
        try:
            api_url = "https://is.gd/create.php"
            params = {
                'format': 'simple',
                'url': long_url
            }
            
            response = self.session.post(api_url, data=params, timeout=10)
            
            if response.status_code == 200:
                short_url = response.text.strip()
                if short_url.startswith('https://is.gd/'):
                    return short_url
                else:
                    print(f"is.gd Error: {short_url}")
                    return None
            else:
                print(f"is.gd HTTP Error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"is.gd Request Error: {e}")
            return None
    
    def shorten_with_vgd(self, long_url):
        """
        Shorten URL using v.gd service (no API key required)
        
        Args:
            long_url (str): The URL to shorten
            
        Returns:
            str: Shortened URL or None if failed
        """
        try:
            api_url = "https://v.gd/create.php"
            params = {
                'format': 'simple',
                'url': long_url
            }
            
            response = self.session.post(api_url, data=params, timeout=10)
            
            if response.status_code == 200:
                short_url = response.text.strip()
                if short_url.startswith('https://v.gd/'):
                    return short_url
                else:
                    print(f"v.gd Error: {short_url}")
                    return None
            else:
                print(f"v.gd HTTP Error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"v.gd Request Error: {e}")
            return None
    
    def shorten_with_bitly(self, long_url, access_token):
        """
        Shorten URL using Bitly service (requires API key)
        
        Args:
            long_url (str): The URL to shorten
            access_token (str): Bitly API access token
            
        Returns:
            str: Shortened URL or None if failed
        """
        try:
            api_url = "https://api-ssl.bitly.com/v4/shorten"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            data = {
                'long_url': long_url
            }
            
            response = self.session.post(
                api_url, 
                headers=headers, 
                json=data, 
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('link')
            elif response.status_code == 400:
                error_data = response.json()
                print(f"Bitly Error: {error_data.get('message', 'Bad request')}")
                return None
            elif response.status_code == 403:
                print("Bitly Error: Invalid access token or insufficient permissions")
                return None
            else:
                print(f"Bitly HTTP Error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Bitly Request Error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Bitly JSON Error: {e}")
            return None
    
    def shorten_url(self, long_url, service='tinyurl', api_key=None):
        """
        Shorten URL using specified service
        
        Args:
            long_url (str): The URL to shorten
            service (str): Service to use ('tinyurl', 'isgd', 'vgd', 'bitly')
            api_key (str): API key for services that require it
            
        Returns:
            str: Shortened URL or None if failed
        """
        if service.lower() == 'tinyurl':
            return self.shorten_with_tinyurl(long_url)
        elif service.lower() == 'isgd':
            return self.shorten_with_isgd(long_url)
        elif service.lower() == 'vgd':
            return self.shorten_with_vgd(long_url)
        elif service.lower() == 'bitly':
            if not api_key:
                print("Error: Bitly requires an API key")
                return None
            return self.shorten_with_bitly(long_url, api_key)
        else:
            print(f"Error: Unknown service '{service}'")
            return None

def main():
    """Demonstrate URL shortening with different services"""
    
    # Test URL
    test_url = "https://www.example.com/very/long/url/path/that/needs/to/be/shortened"
    
    print("URL Shortening Service Demo")
    print("=" * 50)
    print(f"Original URL: {test_url}")
    print()
    
    # Initialize URL shortener
    shortener = URLShortener()
    
    # Test different services
    services = [
        ('TinyURL', 'tinyurl'),
        ('is.gd', 'isgd'),
        ('v.gd', 'vgd')
    ]
    
    for service_name, service_code in services:
        print(f"Testing {service_name}...")
        short_url = shortener.shorten_url(test_url, service_code)
        
        if short_url:
            print(f"✅ {service_name}: {short_url}")
        else:
            print(f"❌ {service_name}: Failed to shorten URL")
        print()
    
    # Bitly example (commented out since it requires an API key)
    print("Bitly Example (requires API key):")
    print("# To use Bitly, get an API key from https://bitly.com/a/oauth_apps")
    print("# bitly_token = 'YOUR_BITLY_ACCESS_TOKEN_HERE'")
    print("# short_url = shortener.shorten_url(test_url, 'bitly', bitly_token)")
    print()
    
    # Example of how to use in code
    print("Example Usage in Your Code:")
    print("-" * 30)
    print("""
from url_shortener import URLShortener

# Initialize shortener
shortener = URLShortener()

# Shorten with TinyURL (no API key needed)
short_url = shortener.shorten_url('https://example.com/long-url', 'tinyurl')
if short_url:
    print(f"Shortened URL: {short_url}")

# Shorten with Bitly (API key required)
bitly_token = 'your-bitly-token'
short_url = shortener.shorten_url('https://example.com/long-url', 'bitly', bitly_token)
if short_url:
    print(f"Bitly URL: {short_url}")
""")

# Simple function for quick URL shortening
def quick_shorten(url, service='tinyurl'):
    """
    Quick function to shorten a URL
    
    Args:
        url (str): URL to shorten
        service (str): Service to use (default: 'tinyurl')
        
    Returns:
        str: Shortened URL or original URL if failed
    """
    shortener = URLShortener()
    result = shortener.shorten_url(url, service)
    return result if result else url

if __name__ == "__main__":
    main()
