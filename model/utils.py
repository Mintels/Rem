import re

# Hyperparameters
BATCH_SIZE = 32
HIDDEN_SIZE = 256
NUM_EPOCHS = 20
LEARNING_RATE = 0.001
MAX_LENGTH = 20

# Tokenization and Learned Vocabulary
def tokenize(sentence):
    return re.findall(r"\b\w+\b", sentence.lower())

class Vocab:
    def __init__(self):
        self.word2idx = {'<pad>': 0, '<sos>': 1, '<eos>': 2, '<unk>': 3}
        self.idx2word = {0: '<pad>', 1: '<sos>', 2: '<eos>', 3: '<unk>'}
        self.word_count = {}

    def add_sentence(self, sentence):
        for word in tokenize(sentence):
            if word not in self.word2idx:
                idx = len(self.word2idx)
                self.word2idx[word] = idx
                self.idx2word[idx] = word

    def sentence_to_indices(self, sentence):
        return [self.word2idx.get(word, self.word2idx['<unk>']) for word in tokenize(sentence)]

    def indices_to_sentence(self, indices):
        return ' '.join([self.idx2word.get(idx, '<unk>') for idx in indices if idx > 2])