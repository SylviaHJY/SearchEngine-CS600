"""
stopword_utils.py

This module loads a set of English stop words from a local stopwords.txt file.
It provides a function `is_stopword(word)` that returns True if the given word is a stop word,
and False otherwise.
"""

def load_stopwords(filepath='stopwords.txt') -> set:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            stop_words = set(line.strip() for line in file if line.strip())
        return stop_words
    except FileNotFoundError:
        print(f"Stopwords file '{filepath}' not found.")
        return set()

# Load once at import
stop_words = load_stopwords()

def is_stopword(word: str) -> bool:
    """
    Determines whether a given word is a stop word.

    Parameters:
        word (str): The word to check.

    Returns:
        bool: True if the word is a stop word, otherwise False.
    """
    return word in stop_words
