import unittest
from utils import Vocab

class TestVocabulary(unittest.TestCase):

    def test_BaseWordAndIndexesAreAligned(self):
        vocab = Vocab()
        reverse_idx2word = {v: k for k, v in vocab.idx2word.items()}
        self.assertEqual(vocab.word2idx, reverse_idx2word)

    def test_NewWordsAreAddedCorrectly(self):
        vocab = Vocab()
        sentence = "Hello world!" 
        vocab.add_sentence(sentence)

        self.assertEqual(vocab.word2idx['hello'], 4) 
        self.assertEqual(vocab.idx2word[4], 'hello')

        self.assertEqual(vocab.word2idx['world'], 5) 
        self.assertEqual(vocab.idx2word[5], 'world')