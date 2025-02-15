"""
String manipulation functions

Printer, February 2025
"""

import inflect

# Create a global instance of the inflect engine
infl = inflect.engine()


def is_article(word: str):
    """
    Determines if str is an article (e.g. a, an, the)
    :param word: word to be checked
    :return: `True` if `str` is an article, `False` otherwise
    """
    articles = ["a", "an", "the"]
    return word.lower() in articles


def title_case(phrase: str):
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


def pluralize(word):
    """
    Pluralizes a word using the Inflect engine.
    :param word: word to be pluralized
    :return: pluralized version of `word`
    """
    return infl.plural(word)


def get_article(word):
    """
    Gets the article for a word using the Inflect engine.
    :param word: word to get the article for
    :return: the article of `word`
    """
    return infl.a(word)


def ordinal(num):
    """
    Gets the ordinal representation of a number, (e.g. 1st, 2nd, 3rd)
    :param num: Number to get the ordinal representation of
    :return: Ordinal representation of `num`
    """
    return infl.ordinal(num)


def literal_num(num):
    """
    Converts a number to a literal representation (e.g. 1000 -> "one thousand")
    :param num: Number to convert
    :return: `num` converted into its English words
    """
    return infl.number_to_words(num)


def dollar_int(num: int):
    """
    Converts an int in cents to a comma-separated dollar representation with a dollar sign in front (e.g. 1000 -> "$1,000.00")
    :param num: Number to convert
    :return: `num` converted to a dollar representation
    """
    if not num:
        return "$0.00"

    negative_sign = "-" if num < 0 else ""
    num = abs(num)
    cents = num % 100
    dollars = num // 100
    return f"{negative_sign}${dollars:,}.{cents:02}"


def dollar_float(num: float):
    """
    Converts a float in dollars and cents to a comma-separated dollar representation with a dollar sign in
    front (e.g. 1000.00 -> "$1,000.00"). Cents will be rounded to two decimal places.
    :param num: Number to convert
    :return: `num` converted to a dollar representation
    """
    num = round(num, 2) * 100
    return dollar_int(int(num))


def listify(words: list):
    """
    Converts a list of words to a string with commas and "and" before the last word. An Oxford comma is used.
    :param words: list of words to be joined into a comma-separated list
    :return: A comma-separated list of `words` with an Oxford comma and "and" before the last word.
    """
    if len(words) == 1:
        return words[0]
    elif len(words) == 2:
        return f"{words[0]} and {words[1]}"
    else:
        return f"{', '.join(words[:-1])}, and {words[-1]}"
