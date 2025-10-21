from collections import Counter


def get_string_length(value: str) -> int:
    return len(value)


def is_palindrome(value: str) -> bool:
    cleaned = value.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def count_unique_characters(value: str) -> int:
    return len(set(value))


def count_words(value: str) -> int:
    return len(value.split())


def get_character_frequency(value: str) -> dict[str, int]:
    return dict(Counter(value))
