# trie.py

class TrieNode:
    """
    Represents a single node in the Trie.
    Each node holds a character, a mapping to its children,
    a flag indicating whether it marks the end of a word,
    and an index pointing to the occurrence list (external storage).
    """
    def __init__(self):
        self.children = {}     # Map from character to TrieNode
        self.is_end = False    # True if the node represents the end of a word
        self.index = -1        # Index in the external occurrence list

class Trie:
    """
    Trie (prefix tree) for storing words efficiently and enabling
    fast pattern matching, prefix search, and exact lookup.
    
    Each word inserted is associated with an index that refers to
    an external occurrence list, in line with Section 23.6.4's structure.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, index):
        """
        Inserts a word into the Trie and stores its corresponding
        occurrence list index at the final node.

        Parameters:
            word (str): The word to insert.
            index (int): The index in the external occurrence list
                         that stores where the word appears.
        """
        node = self.root
        for char in word:
            # Create a new node if the path does not exist
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.index = index

    def search(self, word):
        """
        Searches for a word in the Trie and returns the occurrence
        list index if the word exists.

        Parameters:
            word (str): The word to search.

        Returns:
            int or None: The occurrence list index if the word exists,
                         or None if not found.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.index if node.is_end else None
