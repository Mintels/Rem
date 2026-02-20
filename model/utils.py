import re

# Hyperparameters
BATCH_SIZE = 32 # Feeds the model {BATCH_SIZE} sentences at a time.
HIDDEN_SIZE = 256 # Hidden Size of the Model.
NUM_EPOCHS = 18 # Number of Training Rounds | BEST RESULTS CURRENTLY AT 18 EPOCHS
LEARNING_RATE = 0.003 # Experiment With This Value, Stability vs Speed | BEST RESULTS CURRENTLY AT 0.003
MAX_LENGTH = 20 # Maximum Sentence Length

# Tokenization and Learned Vocabulary.
def tokenize(sentence: str):
    tokens = sentence.lower().split() # Split Tokens by Whitespace/Spaces.
    tokens = [re.sub(r'[^a-z0-9]', '', t) for t in tokens]  # Removal of Special Characters. 
    return [t for t in tokens if t]  # Removes Empty Tokens.

# Vocabulary Class
class Vocab:

    """ Tracks word-to-index and index-to-word mappings for trained vocabulary."""

    def __init__(self):
        self.word2idx = {'<pad>': 0, '<sos>': 1, '<eos>': 2, '<unk>': 3} # Word to Index Mapping.
        self.idx2word = {0: '<pad>', 1: '<sos>', 2: '<eos>', 3: '<unk>'} # Index to Word Mapping.
        self.word_count = {} 

    def add_sentence(self, sentence: str):
        for word in tokenize(sentence):
            if word not in self.word2idx: # New Word not in Rem's vocabulary.
                idx = len(self.word2idx)
                self.word2idx[word] = idx  # For computer readability, words to numbers.
                self.idx2word[idx] = word # For human readability, numbers to words.

    def sentence_to_indices(self, sentence: str) -> list[int]:
        # Tokenized Sentence to Matching Indices, Unknown Words to index <unk>.
        return [self.word2idx.get(word, self.word2idx['<unk>']) for word in tokenize(sentence)]

    def indices_to_sentence(self, indices: list[int]) -> str:
        # Indices to Matching Sentence
        return ' '.join([self.idx2word.get(idx, '<unk>') for idx in indices if idx > 2])