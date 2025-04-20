# main_single.py

from Engine import SearchEngine

def load_urls(filepath):
    """
    Load URLs from a given text file (one per line).
    Ignores empty lines and whitespace.

    Parameters:
        filepath (str): Path to the input file

    Returns:
        List[str]: List of cleaned URLs
    """
    urls = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            if url:
                urls.append(url)
    return urls

def main():
    print("Initializing Search Engine...")
    urls = load_urls("inputLinks.txt")

    engine = SearchEngine()
    engine.build_index(urls)

    print("Indexing complete. You can now enter a single keyword.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter a single keyword: ").strip().lower()
        if user_input == "exit":
            break

        if not user_input:
            print("Please enter a keyword.\n")
            continue

        if len(user_input.split()) > 1:
            print("Please enter only one word.\n")
            continue

        index = engine.trie.search(user_input)
        if index is None:
            print(f"No pages contain the word '{user_input}'.\n")
            continue

        urls_with_freq = []
        for url in engine.occurrence_list[index]:
            freq = engine.freq_table[user_input][url]
            urls_with_freq.append((url, freq))

        # Sort by frequency descending
        urls_with_freq.sort(key=lambda x: x[1], reverse=True)

        print(f"\nThe word '{user_input}' appears in {len(urls_with_freq)} page(s):")
        for i, (url, freq) in enumerate(urls_with_freq, 1):
            print(f"{i}. {url} (occurrences: {freq})")
        print("")

if __name__ == "__main__":
    main()

