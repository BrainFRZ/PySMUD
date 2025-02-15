import unittest

from evennia import create_object
from utils.string import *


class TitleCaseTests(unittest.TestCase):
    """This tests the title_case function"""

    def test_normal_phrase(self):
        """Tests a normal phrase that should be entirely capitalized"""
        output = title_case("walking outside")
        expected_output = "Walking Outside"
        self.assertEqual(output, expected_output)
    def test_start_article_phrase(self):
        """Tests a phrase that starts with an article"""
        output = title_case("a walk outside")
        expected_output = "A Walk Outside"
        self.assertEqual(output, expected_output)
    def test_middle_article_phrase(self):
        """Tests a phrase that starts with an article"""
        output = title_case("this is a triumph")
        expected_output = "This Is a Triumph"
        self.assertEqual(output, expected_output)
    def test_capitalized_article_phrase(self):
        """Tests a phrase that has an article that must be made lowercase"""
        output = title_case("this is A triumph")
        expected_output = "This Is a Triumph"
        self.assertEqual(output, expected_output)


class DollarTests(unittest.TestCase):
    """This tests the `dollar_int` function"""

    def test_dollar_short(self):
        """Tests a number less than 1000 that shouldn't have commas"""
        output = dollar_int(100)
        expected_output = "$1.00"
        self.assertEqual(output, expected_output)
    def test_dollar_long(self):
        """Tests a number greater than 1000 that should have commas"""
        output = dollar_int(1000000)
        expected_output = "$10,000.00"
        self.assertEqual(output, expected_output)
    def test_dollar_negative(self):
        """Tests a negative number that should have a minus sign"""
        output = dollar_int(-500000)
        expected_output = "-$5,000.00"
        self.assertEqual(output, expected_output)
    def test_dollars_and_cents(self):
        """Tests a number with both dollars and cents"""
        output = dollar_int(10005)
        expected_output = "$100.05"
        self.assertEqual(output, expected_output)
    def test_cents(self):
        """Tests a number with only cents"""
        output = dollar_int(5)
        expected_output = "$0.05"
        self.assertEqual(output, expected_output)


class ListifyTests(unittest.TestCase):
    """This tests the `listify` function"""

    def test_one_word(self):
        """Tests a single word that should be put into a list"""
        output = listify(["word"])
        expected_output = "word"
        self.assertEqual(output, expected_output)
    def test_two_words(self):
        output = listify(["apples", "bananas"])
        expected_output = "apples and bananas"
        self.assertEqual(output, expected_output)
    def test_multiple_words(self):
        output = listify(["apples", "bananas", "oranges", "pears"])
        expected_output = "apples, bananas, oranges, and pears"
        self.assertEqual(output, expected_output)
