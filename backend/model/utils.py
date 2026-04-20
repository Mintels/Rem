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
        self.rnn = nn.GRU(embed_size + hidden_size, hidden_size)  # Decoder consumes token embedding + attention context
        self.fc = nn.Linear(hidden_size * 2, vocab_size) # Combine decoder state and context before prediction

    def forward(self, tgt: torch.Tensor, hidden: torch.Tensor, encoder_outputs: torch.Tensor, src_mask: torch.Tensor | None = None):
        """ Run attention-based decoding over the target sequence. """
        embedded = self.embed(tgt) # [tgt_len, batch, embed_size]
        encoder_outputs_batch = encoder_outputs.transpose(0, 1) # [batch, src_len, hidden_size]

        step_predictions = []
        for step in range(embedded.size(0)):
            # Dot-product attention between current decoder state and encoder outputs.
            query = hidden[-1] # [batch, hidden_size]
            attn_scores = torch.bmm(encoder_outputs_batch, query.unsqueeze(2)).squeeze(2) # [batch, src_len]
            if src_mask is not None:
                attn_scores = attn_scores.masked_fill(~src_mask, -1e9)

            attn_weights = torch.softmax(attn_scores, dim=1) # [batch, src_len]
            context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs_batch).squeeze(1) # [batch, hidden_size]

            rnn_input = torch.cat([embedded[step], context], dim=1).unsqueeze(0) # [1, batch, embed+hidden]
            output, hidden = self.rnn(rnn_input, hidden)

            step_logits = self.fc(torch.cat([output.squeeze(0), context], dim=1)) # [batch, vocab]
            step_predictions.append(step_logits)

        predictions = torch.stack(step_predictions, dim=0) # [tgt_len, batch, vocab]
        return predictions, hidden