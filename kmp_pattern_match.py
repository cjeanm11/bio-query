from typing import List, Final
from dataclasses import dataclass
from collections import defaultdict
from pprint import pformat
import zlib

# use Knuth-Morris-Prath algorithm,	Rabin-Karp , Boyer-Moore, Aho-Corasick, Z-Algorithm, Suffix Trees
# 
def preprocess_lps(pattern) -> List[int]:
    lps = [0] * len(pattern)
    j = 0  # length of the previous longest prefix suffix
    i = 1
    
    # Building the LPS array
    while i < len(pattern):
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
            i += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            lps[i] = 0
            i += 1
    return lps

def kmp_search(text, pattern, lps) -> List[int]:
    # Searching for pattern in text
    i = 0  # index for text
    j = 0  # index for pattern
    positions = []  # to store starting indices of matches
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == len(pattern):
            positions.append(i - j)  # store the index of the match
            j = lps[j - 1]  # reset j to continue searching

        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions
    
@dataclass(frozen=True) # hashable / immutable -> can store as a key!
class PatternMatchingQuery:
    text: Final[str]
    pattern: Final[str]
    def unpack(self) -> tuple[str, str]:
         return self.text, self.pattern
    def compress(self) -> bytes:
        """Compress the text using zlib to save space."""
        delimiter = b'\x00'  # This is a unique byte that won't appear in text or pattern
        combined_data = self.pattern.encode('utf-8') + delimiter + self.text.encode('utf-8')
        return zlib.compress(combined_data)
    @staticmethod
    def decompress(compressed_data: bytes) -> tuple:
        """Decompress the combined pattern and text."""
        decompressed_data = zlib.decompress(compressed_data)
        delimiter = b'\x00'
        pattern, text = decompressed_data.split(delimiter, 1)
        return pattern.decode('utf-8'), text.decode('utf-8')

# Example usage

def obtain_occurences(text, pattern) -> List[int]:
    lps: List[int] = preprocess_lps(pattern)
    occurences_indexes: List[int] = kmp_search(text, pattern, lps)
    return occurences_indexes
    

def execute_queries(queries: List[PatternMatchingQuery], store: defaultdict) -> dict[bytes, List[int]]:
    query_results = {}
    for query in queries:
        
        compresses_query = query.compress()
        
        if query not in store:
            (text, pattern) = query.unpack()
            occurences_indexes: List[int] = obtain_occurences(text, pattern)
            query_results[compresses_query] = occurences_indexes 
            store[compresses_query] = occurences_indexes # caching result
        else:
            query_results[compresses_query] = store[compresses_query]
            
    return query_results
            
    
if __name__ == "__main__":
    query_result_store = defaultdict(list)
    
    queries = [
        PatternMatchingQuery(text="ABABDABACDABABCABAB", pattern="ABA"),
        PatternMatchingQuery(text="ABABDABACDABABCABAB", pattern="ABABCABAB"),
        PatternMatchingQuery(text="ABCDEFABCABC", pattern="ABC")
    ]
    
    query_results = execute_queries(queries, query_result_store)
    
    
    for compressed_querie_key, result in query_results.items():
        pattern, texte = PatternMatchingQuery.decompress(compressed_querie_key)
        displayed_pattern: str = pattern if len(pattern) < 10 else pattern[:10] + "..."
        displayed_texte: str = pattern if len(texte) < 10 else texte[:10] + "...\t"
        print(f"{displayed_pattern}-{displayed_texte}:  {result}")
        
    
    
    
    
    
    
    
