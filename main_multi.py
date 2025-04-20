# main_multi.py

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

    print("Indexing complete. You can now enter multiple keywords.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter keywords (space-separated): ").strip().lower()
        if user_input == "exit":
            break

        words = user_input.split()
        if not words:
            print("Please enter at least one keyword.\n")
            continue

        # Perform strict AND-based ranked search
        results = engine.strict_ranked_search(words)

        if not results:
            print("No pages contain all of the given keywords.\n")
        else:
            print(f"\nTop {len(results)} matching pages (ranked):")
            for i, page in enumerate(results, 1):
                print(f"\nRank #{i}")
                print(page)
            print("\n")

if __name__ == "__main__":
    main()

