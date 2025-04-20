# rank.py

class RankedPage:
    """
    Represents a web page that matched one or more search terms.

    Stores:
    - The page's URL
    - The list of matched keywords
    - The total number of occurrences of those keywords
    """

    def __init__(self, url):
        self.url = url
        self.matched_words = []     # List of matched keywords
        self.total_occurrence = 0   # Total number of times all matched words appear

    def insert_word(self, word, count):
        """
        Add a matched word and its count to the page's record.

        Parameters:
            word (str): The matched keyword
            count (int): Number of times the word appears in this page
        """
        self.matched_words.append(word)
        self.total_occurrence += count

    def get_score(self):
        """
        Return a tuple representing this page's rank.
        Higher number of words and occurrences yield higher score.

        Returns:
            (int, int): A tuple (num_matched_words, total_occurrence)
                        used for sorting pages by relevance
        """
        return (len(self.matched_words), self.total_occurrence)

    def __str__(self):
        """
        Return a formatted string showing the page's ranking details.

        Returns:
            str: Description of the ranked page
        """
        return (f"{self.url}\n"
                f"  Matched Words: {self.matched_words}\n"
                f"  Total Occurrences: {self.total_occurrence}\n"
                f"  Score: {self.get_score()}")
