import unittest 

from utils import tokenize, clean_content

class TestTokenize(unittest.TestCase):

    def test_TokenizeRemovesSpecialCharacters(self):
        sentence = "Hello, World! This is a test."
        expected_tokens = ['hello', 'world', 'this', 'is', 'a', 'test']
        self.assertEqual(tokenize(sentence), expected_tokens)

    def test_TokenizeHandlesEmptyAndWhitespace(self):
        sentence = "   Hello   World   "
        expected_tokens = ['hello', 'world']
        self.assertEqual(tokenize(sentence), expected_tokens)

    def test_TokenizeIsCaseInsensitive(self):
        sentence = "HeLLo WoRLd"
        expected_tokens = ['hello', 'world']
        self.assertEqual(tokenize(sentence), expected_tokens)

class TestCleanContent(unittest.TestCase): 

    def test_CleanContentRemovesExtraWhitespace(self):
        content = "   Hello   World   "
        expected_content = "Hello World"
        self.assertEqual(clean_content(content), expected_content)

    def test_CleanContentHandlesEmptyString(self):
        content = ""
        expected_content = ""
        self.assertEqual(clean_content(content), expected_content)