import requests
from bs4 import BeautifulSoup
import re
import os

def fetch_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def parse_html_for_versions(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    possible_elements = []
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        possible_elements.append(heading.text.strip())
    
    version_numbers = []
    version_regex = re.compile(r'\b\d+\b')
    for element in possible_elements:
        match = version_regex.search(element)
        if match:
            version_numbers.append(match.group())
    return version_numbers

def save_version_numbers_to_txt(version_numbers, output_file_path):
    with open(output_file_path, 'w') as file:
        for version in version_numbers:
            extracted_version = f"{version[0]}.{version[1]}"
            file.write(f"{extracted_version}\n")

if __name__ == "__main__":
    # URL of the website you want to scrape
    url = "https://www.manageengine.com/products/ad-manager/release-notes.html"
    
    # File path where you want to save the extracted version numbers
    output_file_path = os.path.join(os.getcwd(), "version_numbers.txt")
    
    # Step 1: Fetch HTML content from website
    html_content = fetch_html_content(url)
    
    if html_content:
        # Step 2: Parse HTML content for version numbers
        version_numbers = parse_html_for_versions(html_content)
        
        # Step 3: Save the version numbers to a text file
        save_version_numbers_to_txt(version_numbers, output_file_path)
