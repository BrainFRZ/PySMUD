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
