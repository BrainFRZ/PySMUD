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


class OneArgumentTests(unittest.TestCase):
    """This tests the `one_argument` function"""

    def test_one_argument(self):
        """Tests a single argument that should be returned"""
        output = one_argument("test")
        expected_output = ("test", "")
        self.assertEqual(output, expected_output)
    def test_two_arguments(self):
        """Tests two arguments where the first should be peeled off"""
        output = one_argument("apples bananas")
        expected_output = ("apples", "bananas")
        self.assertEqual(output, expected_output)
    def test_quotes(self):
        """Tests an argument wrapped in double quotes"""
        output = one_argument('"apples cherries" bananas')
        expected_output = ("apples cherries", "bananas")
        self.assertEqual(output, expected_output)
    def test_single_quote_in_doubles(self):
        """Tests an argument with a single quote in double quotes"""
        output = one_argument("\"it's too\" hot")
        expected_output = ("it's too", "hot")
        self.assertEqual(output, expected_output)
    def test_unmatched_quote(self):
        """Tests an argument with no ending quote"""
        output = one_argument('"apples cherries')
        expected_output = ("apples cherries", "")
        self.assertEqual(output, expected_output)
    def test_mismatched_quotes(self):
        """Tests an argument with mismatched quotes"""
        output = one_argument('"apples cherries\' bananas')
        expected_output = ("apples cherries' bananas", "")
        self.assertEqual(output, expected_output)


class NumberArgumentTests(unittest.TestCase):
    """This tests the `number_argument` function"""

    def test_single_number_argument(self):
        """Tests a single argument"""
        output = number_argument("10")
        expected_output = (None, "10", "")
        self.assertEqual(output, expected_output)
    def test_number_no_dot(self):
        """Tests a number with a space before its argument"""
        output = number_argument("10 apples")
        expected_output = (None, "10", "apples")
        self.assertEqual(output, expected_output)
    def test_number_with_dot(self):
        """Tests a number with a dot before its argument"""
        output = number_argument("10.apples and bananas")
        expected_output = (10, "apples", "and bananas")
        self.assertEqual(output, expected_output)
    def test_no_number(self):
        """Tests an argument with no number"""
        output = number_argument("apples and bananas")
        expected_output = (None, "apples", "and bananas")
        self.assertEqual(output, expected_output)
