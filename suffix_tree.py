import pygtrie

# Simple Trie-based implementation
def build_suffix_tree(text):
    trie = pygtrie.CharTrie()
    for i in range(len(text)):
        trie[text[i:]] = i
    return trie

def search_patterns_in_text(text, patterns):
    trie = build_suffix_tree(text)
    results = {}
    for pattern in patterns:
        if pattern in trie:
            results[pattern] = list(trie.items(pattern))
        else:
            results[pattern] = []
    return results

# Example usage
text = "ABABDABACDABABCABAB"
patterns = ["ABA", "ABABCABAB", "ABC"]
matches = search_patterns_in_text(text, patterns)
print("Suffix Tree matches:", matches)


