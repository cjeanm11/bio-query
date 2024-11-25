from typing import List, Final
from dataclasses import dataclass
from collections import defaultdict
from pprint import pformat
import zlib
from abc import ABC, abstractmethod

class PatternMatchingQuery(ABC):
    @abstractmethod
    def compress(self) -> bytes:
        """Compress the text or pattern."""
        pass
    
    @abstractmethod
    def unpack(self) -> tuple[str, str]:
        """Unpack the pattern and text into a tuple."""
        pass
    
    @staticmethod
    def decompress(compressed_data: bytes) -> tuple:
        """Decompress the combined pattern and text."""
        decompressed_data = zlib.decompress(compressed_data)
        delimiter = b'\x00'
        parts = decompressed_data.split(delimiter)
        return tuple(part.decode('utf-8') for part in parts)
    
    @staticmethod
    def display(compressed_query_key, result):
        query_type, pattern, text = PatternMatchingQuery.decompress(compressed_query_key)
        # Truncate pattern and text if they are too long
        query_type = query_type if len(query_type) < 10 else query_type[:10] + ".."
        displayed_pattern = pattern if len(pattern) < 10 else pattern[:10] + ".."
        displayed_text = text if len(text) < 10 else text[:10] + ".."

        # Define column widths
        type_width, pattern_width, text_width, result_width = 13, 13, 13, 30
        # Format and print in fixed-width columns
        print(f"query_type:{query_type.ljust(type_width)}pattern:{displayed_pattern.ljust(pattern_width)}text:{displayed_text.ljust(text_width)} : {str(result).ljust(result_width)}")
        
        
@dataclass(frozen=True) # hashable / immutable -> can store as a key!
class DNAQuery(PatternMatchingQuery):
    text: Final[str]
    pattern: Final[str]
    def unpack(self) -> tuple[str, str]:
         return self.text, self.pattern
    def compress(self) -> bytes:
        """Compress the text using zlib to save space."""
        delimiter: Final = b'\x00'  # This is a unique byte that won't appear in text or pattern
        query_type: Final[str] = self.__class__.__name__ 
        attibutes = [part.encode('utf-8') for part in [query_type, self.pattern, self.text]]
        combined_data = delimiter.join(attibutes)
        return zlib.compress(combined_data)

@dataclass(frozen=True) # hashable / immutable -> can store as a key!
class PatientQuery(PatternMatchingQuery):
    text: Final[str]
    pattern: Final[str]
    def unpack(self) -> tuple[str, str]:
         return self.text, self.pattern
    def compress(self) -> bytes:
        """Compress the text using zlib to save space."""
        delimiter: Final = b'\x00'  # This is a unique byte that won't appear in text or pattern
        query_type: Final[str] = self.__class__.__name__ 
        attibutes = [part.encode('utf-8') for part in [query_type, self.pattern, self.text]]
        combined_data = delimiter.join(attibutes)
        return zlib.compress(combined_data)
        
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
    

def obtain_occurences(text, pattern) -> List[int]:
    
    if not text or not pattern or len(text) < len(pattern):
        return []
        
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
    
    queries: List[PatternMatchingQuery] = [
        DNAQuery(text="ABABDABACDABABCABAB", pattern="ABA"),
        DNAQuery(text="ABABDABACDABABCABAB", pattern="ABABCABAB"),
        DNAQuery(text="ABCDEFABCABC", pattern="ABC"),
        PatientQuery(text="ABCDEFABCABCC", pattern="ABC"),
        PatientQuery(text="ABCDEFABCABCC", pattern="ABCADSewdwed")
    ]
    
    query_results = execute_queries(queries, query_result_store)
    
    for compressed_query_key, result in query_results.items():
        PatternMatchingQuery.display(compressed_query_key, result)
 
 # Display results