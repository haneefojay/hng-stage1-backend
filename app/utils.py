import hashlib
from collections import Counter


def analize_string(value: str) -> dict:
    v = value.strip()
    length = len(v)
    word_count = len(v.split())
    is_pal = v.lower() == v[::-1].lower()
    unique_chars = len(set(v))
    sha = hashlib.sha256(v.encode()).hexdigest()
    char_freq = dict(Counter(v))
    
    return {
        "length": length,
        "is_palindrome": is_pal,
        "unique_characters": unique_chars,
        "word_count": word_count,
        "sha256_hash": sha,
        "character_frequency_map": char_freq,
    }


def parse_nl_query(query: str) -> dict:
    q = query.lower()
    filters = {}
    if "palind" in q:
        filters["is_palindrome"] = True
    if "single word" in q or "single-word" in q or "one word" in q:
        filters["word_count"] = 1
    
    import re
    m = re.search(r"longer than (\d+)", q)
    if m:
        filters["min_length"] = int(m.group(1)) + 0
        filters["min_length_exclusive"] = True
        filters["min_length_raw"] = int(m.group(1))
    m2 = re.search(r"longer than or equal to (\d+)", q)
    if m2:
        filters["min_length"] = int(m2.group(1))
    
    m3 = re.search(r"contain(?:ing|s)? the letter (\w)", q)
    if m3:
        filters["contains_character"] = m3.group(1)
    
    m4 = re.search(r"contain(?:ing|s)? (\w)", q)
    if m4 and "contains_character" not in filters:
        filters["contains_character"] = m4.group(1)
    return filters
