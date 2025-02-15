"""
String manipulation functions

Printer, February 2025
"""

def is_article(word):
    """
    Determines if str is an article (e.g. a, an, the)
    :param word: word to be checked
    :return: `True` if `str` is an article, `False` otherwise
    """
    articles = ["a", "an", "the"]
    return word.lower() in articles

def title_case(phrase):
    """
    Convert a string to title case, capitalizing each word. Articles won't be capitalized unless it's the first word.
    :param phrase: a string to be converted
    :return: `phrase` in title case
    """
    if not phrase:
        return ""

    words = phrase.split()
    converted_words = [word.lower() if is_article(word) else word.capitalize() for word in words]
    phrase = " ".join(converted_words)
    return phrase[0].upper() + phrase[1:]
