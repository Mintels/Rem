import re
import torch
import torch.nn as nn

# Hyperparameters
BATCH_SIZE = 64 # Feeds the model {BATCH_SIZE} sentences at a time.
HIDDEN_SIZE = 256 # Hidden Size of the Model.
NUM_EPOCHS = 30 # Number of Training Rounds 
LEARNING_RATE = 0.0005 # How Fast the Model Learns
MAX_LENGTH = 15 # Maximum Sentence Length

def tokenize(sentence: str) -> list[str]:
    ''' Tokenizes a sentence into a list of words. '''
    tokens = sentence.lower().split() # Split Tokens by Whitespace/Spaces.
    tokens = [re.sub(r'[^a-z0-9]', '', t) for t in tokens]  # Removal of Special Characters. 
    return [t for t in tokens if t]  # Removes Empty Tokens.


def clean_content(text: str) -> str:
    ''' Cleaning Content for Model Input. '''
    content = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Substitutes every non-letter, non-digit, and non-whitespace character with an empty string.
    return re.sub(r"\s+", " ", content).strip() # Replaces multiple whitespace characters with a single space and removes leading/trailing whitespace.


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
    


# ----------- Model Specifications ----------- 
class Encoder(nn.Module):
    def __init__(self, vocab_size: int, embed_size: int, hidden_size: int):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_size) # Lookup Table for Dense Vector Representation of Words
        self.rnn = nn.GRU(embed_size, hidden_size)  # Update hidden state based on input and previous hidden state

    def forward(self, src: torch.Tensor, hidden=None): 
        embedded = self.embed(src) # Convert indices to dense vectors
        outputs, hidden = self.rnn(embedded, hidden) # Keeps track of what it has heard.
        return outputs, hidden 
    
class Decoder(nn.Module):
    def __init__(self, vocab_size: int, embed_size: int, hidden_size: int):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_size) # Lookup Table for Dense Vector Representation of Words
        self.rnn = nn.GRU(embed_size, hidden_size)  # Update hidden state based on input and previous hidden state
        self.fc = nn.Linear(hidden_size, vocab_size) # Map hidden state to vocab distribution

    def forward(self, tgt: torch.Tensor, hidden: torch.Tensor):
        embedded = self.embed(tgt) # Convert indices to dense vectors
        outputs, hidden = self.rnn(embedded, hidden) # Keeps track of what it has said.
        predictions = self.fc(outputs) # Probability distribution over the vocabulary for each time step
        return predictions, hidden