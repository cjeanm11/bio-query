from collections import deque, defaultdict

class AhoCorasick:
    def __init__(self):
        self.trie = defaultdict(dict)  # Trie structure
        self.fail = defaultdict()      # Failure links
        self.output = defaultdict(list)  # Outputs (patterns found at this node)
        self.state_count = 0

    def add_pattern(self, pattern: str, index: int):
        node = 0
        for char in pattern:
            if char not in self.trie[node]:
                self.trie[node][char] = self.state_count
                self.state_count += 1
            node = self.trie[node][char]
        self.output[node].append(index)

    def build(self):
        queue = deque()
        # Initialize the fail links for depth 1 nodes
        for char in range(256):  # ASCII characters
            if chr(char) in self.trie[0]:
                self.fail[self.trie[0][chr(char)]] = 0
                queue.append(self.trie[0][chr(char)])
            else:
                self.trie[0][chr(char)] = 0  # Failure link points to the root
        
        # Build fail links for all other nodes
        while queue:
            state = queue.popleft()
            for char, next_state in self.trie[state].items():
                queue.append(next_state)
                f = self.fail[state]
                while char not in self.trie[f]:
                    f = self.fail[f]
                self.fail[next_state] = self.trie[f][char]
                self.output[next_state].extend(self.output[self.fail[next_state]])

    def search(self, text: str):
        state = 0
        results = defaultdict(list)
        for i, char in enumerate(text):
            while char not in self.trie[state]:
                state = self.fail[state]  # Follow failure links if mismatch
            state = self.trie[state][char]
            for pattern_index in self.output[state]:
                results[pattern_index].append(i)  # Found a match
        return results


# Example usage:
patterns = ["ab", "bc", "abc"]
text = "abcabcab"

# Create Aho-Corasick automaton and add patterns
ac = AhoCorasick()
for index, pattern in enumerate(patterns):
    ac.add_pattern(pattern, index)

# Build the Aho-Corasick automaton
ac.build()

# Search for patterns in the text
matches = ac.search(text)

# Print results
for pattern_index, positions in matches.items():
    print(f"Pattern '{patterns[pattern_index]}' found at positions: {positions}")