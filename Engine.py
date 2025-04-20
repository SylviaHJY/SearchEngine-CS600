# engine.py

from collections import defaultdict
from parseLinks import fetch_text, process_text
# from crawler_parser import crawl_and_extract, process_text
from trie import Trie
from rank import RankedPage

class SearchEngine:
    """
    The SearchEngine class implements a simplified search engine that supports:
    - Inverted indexing using a Trie structure
    - Single-word search
    - Multi-word AND search (intersection)
    - Ranked search (partial match)
    - Strict ranked search (intersection + ranking)

    This follows the structure described in Section 23.6.4 of the textbook.
    """

    def __init__(self):
        # Trie for storing index terms
        self.trie = Trie()
        # External occurrence list: index -> list of URLs where the word appears
        self.occurrence_list = []
        # Word to index in occurrence list
        self.word_to_index = {}
        # Frequency table: word -> {url -> frequency in that page}
        self.freq_table = defaultdict(lambda: defaultdict(int))

    def build_index(self, urls):
        """
        Build the search index from a list of input URLs.
        For each word found in the page content:
        - Track its frequency per page
        - Record its occurrence list
        - Insert the word into the Trie, with a pointer to the occurrence index
        """
        occurrence_map = defaultdict(set)

        for url in urls:
            text = fetch_text(url)
            # text = crawl_and_extract(url, depth=1, max_depth=2)
            words = process_text(text)

            for word in words:
                word = word.lower()
                occurrence_map[word].add(url)
                self.freq_table[word][url] += 1

        for word, url_set in occurrence_map.items():
            index = len(self.occurrence_list)
            self.occurrence_list.append(sorted(url_set))
            self.word_to_index[word] = index
            self.trie.insert(word, index)

    def search_single(self, word):
        """
        Return a list of URLs that contain the given word.
        """
        word = word.lower()
        index = self.trie.search(word)
        if index is not None:
            return self.occurrence_list[index]
        return []

    def search_multiple(self, words):
        """
        Return a list of URLs that contain all of the given words (AND search).
        Intersection is computed across all words' occurrence lists.
        """
        result_sets = []

        for word in words:
            word = word.lower()
            index = self.trie.search(word)
            if index is None:
                return []
            result_sets.append(set(self.occurrence_list[index]))

        if not result_sets:
            return []

        return list(set.intersection(*result_sets))

    def ranked_search(self, words):
        """
        Return all URLs that contain at least one of the given words,
        ranked by:
        - Number of matched keywords
        - Total frequency of matched words

        This is a relaxed search (OR logic + sorting).
        """
        page_map = {}
        words = list(set(words))

        for word in words:
            word = word.lower()
            index = self.trie.search(word)
            if index is None:
                continue

            urls = self.occurrence_list[index]
            for url in urls:
                if url not in page_map:
                    page_map[url] = RankedPage(url)
                count = self.freq_table[word][url]
                page_map[url].insert_word(word, count)

        ranked_pages = list(page_map.values())
        # ranked_pages.sort(key=lambda page: page.get_score(), reverse=True)
        # In strict_ranked_search() or ranked_search()
        ranked_pages.sort(key=lambda page: (page.get_score(), page.url),reverse=True)

        return ranked_pages

    def strict_ranked_search(self, words):
        """
        Return only the URLs that contain all the given words (AND search),
        ranked by the same criteria as ranked_search:
        - Number of matched keywords
        - Total frequency

        This combines intersection filtering with ranking.
        """
        result_sets = []
        words = list(set(words))

        for word in words:
            word = word.lower()          
            index = self.trie.search(word)
            if index is None:
                return []
            result_sets.append(set(self.occurrence_list[index]))

        if not result_sets:
            return []

        common_urls = set.intersection(*result_sets)
        ranked_pages = []

        for url in common_urls:
            page = RankedPage(url)
            for word in words:
                count = self.freq_table[word][url]
                page.insert_word(word, count)
            ranked_pages.append(page)

        # ranked_pages.sort(key=lambda page: page.get_score(), reverse=True)
        ranked_pages.sort(key=lambda page: (page.get_score(), page.url),reverse=True)
        return ranked_pages


