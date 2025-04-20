"""
parseLinks.py

This module is responsible for:
1. Fetching web page content from a given URL using the requests and BeautifulSoup libraries,
   and extracting text from all <p> tags.
2. Preprocessing the fetched text by removing punctuation, tokenizing into words,
   converting them to lowercase, and filtering out stop words.

Project Requirement:
Use all the words from the pages as index terms, excluding stop words such as articles,
prepositions, and pronouns.
"""
# parser.py
import requests
from bs4 import BeautifulSoup
import re
from stopword_utils import is_stopword
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import hashlib


def get_cache_filename(url, cache_dir="cached_pages"):
    """
    Generates a unique filename for the cached version of a URL
    using an MD5 hash (safe for filesystem).
    """
    os.makedirs(cache_dir, exist_ok=True)
    hash_name = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(cache_dir, f"{hash_name}.txt")

def fetch_text(url):
    """
    Fetch the raw text content from a given URL (HTML <p> tags only).
    Uses local cache if available to avoid re-downloading.
    """
    cache_file = get_cache_filename(url)

    # Try reading from cache
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as file:
            return file.read()

    # Else, fetch from the web
    try:
        response = requests.get(url, verify=False, timeout=120)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)

        # Save to cache
        with open(cache_file, 'w', encoding='utf-8') as file:
            file.write(text)

        return text
    except Exception as e:
        print(f"[Error] Failed to fetch {url}: {e}")
        return ""

def process_text(text):
    """
    Clean raw text:
    - Remove common punctuation
    - Split into lowercase tokens
    - Filter out stopwords
    """
    text = re.sub(r"[!@#$%^&*(),.?\":;'\-_/]", " ", text)
    tokens = text.split()
    return [token.lower() for token in tokens if token and not is_stopword(token.lower())]



# def fetch_text(url):
#     """
#     Fetch the raw text content from a given URL (HTML <p> tags only).
#     """
#     try:
#         response = requests.get(url, verify=False, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")
#         paragraphs = soup.find_all("p")
#         return " ".join(p.get_text() for p in paragraphs)
#     except Exception as e:
#         print(f"[Error] Failed to fetch {url}: {e}")
#         return ""
