import os
import torch
import pickle
import pandas as pd
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from .utils import Vocab, Encoder, Decoder, BATCH_SIZE, HIDDEN_SIZE, MAX_LENGTH, NUM_EPOCHS, LEARNING_RATE # Specifications For Model


# ----------- File Paths & Configurations ----------- 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CUSTOM_DATA = os.path.join(BASE_DIR, "data", "daily_dialog.csv") # Custom Dialogue Data
EXAMPLE_DATA = os.path.join(BASE_DIR, "data", "dialogues.csv") # Custom Dialogue Data

DATA = CUSTOM_DATA if os.path.exists(CUSTOM_DATA) else EXAMPLE_DATA
VOCAB_FILE = os.path.join(BASE_DIR, 'data', 'vocab.pkl') # Vocabulary File 
MODEL_FILE = os.path.join(BASE_DIR, 'rem.pth') # Current Model

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') # Use GPU if available for faster training

# ----------- Data Loading & Preprocessing -----------

dialogues = pd.read_csv(DATA, dtype=str)

input_col = "input"  # CSV Column Name for Inputs.
output_col = "outputs"  # CSV Column Name for Target Responses.


def clean_column(column: pd.Series) -> pd.Series: 
    """Clean a pandas Series by converting to string and stripping whitespace."""
    return (
        column.astype(str)
            .str.strip()
            .str.replace('"', '', regex=False)
    )

dialogues[input_col] = clean_column(dialogues[input_col])
dialogues[output_col] = clean_column(dialogues[output_col])

column_pairs = []
for row in dialogues.itertuples():
    inps = getattr(row, input_col)  # Gets the cell value from specified row & column
    outs = getattr(row, output_col).split('||')
    for out in outs:
        inp, out = inps.strip(), out.strip()
        column_pairs.append((inp, out))
column_pairs = list(set(column_pairs))

class ChatDataset(Dataset): # Inherits from PyTorch's Dataset class 

    def __init__(self, pairs: list[tuple[str,str]], vocab: Vocab):
        self.pairs = pairs
        self.vocab = vocab

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        '''Converts the idx-th input/output pair into tensors of vocab indices with <sos> and <eos> tokens'''

        input, target = self.pairs[idx] 

        input_ids = [1] + self.vocab.sentence_to_indices(input)[:MAX_LENGTH] + [2]
        target_ids = [1] + self.vocab.sentence_to_indices(target)[:MAX_LENGTH] + [2]

        return torch.tensor(input_ids), torch.tensor(target_ids) # Expected tensors for training.


def collate_fn(batch: list[tuple[torch.Tensor, torch.Tensor]]) -> tuple[torch.Tensor, torch.Tensor]:
    '''Padding sequences to the same length within a batch'''

    input_batch, target_batch = zip(*batch)

    input_batch = nn.utils.rnn.pad_sequence(input_batch, padding_value=0)
    target_batch = nn.utils.rnn.pad_sequence(target_batch, padding_value=0) 

    return input_batch, target_batch


# ----------- Model Traning Loop ----------- 

def train():
    vocab = Vocab() # Initializing our Vocabulary Class.
    for inp, tgt in column_pairs: # Split into input and target sentences
        vocab.add_sentence(inp) 
        vocab.add_sentence(tgt)

    dataset = ChatDataset(column_pairs, vocab)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)

    encoder = Encoder(len(vocab.word2idx), HIDDEN_SIZE, HIDDEN_SIZE).to(device)
    decoder = Decoder(len(vocab.word2idx), HIDDEN_SIZE, HIDDEN_SIZE).to(device)

    criterion = nn.CrossEntropyLoss(ignore_index=0)
    optimizer = optim.Adam(list(encoder.parameters()) + list(decoder.parameters()), lr=LEARNING_RATE)

    for epoch in range(NUM_EPOCHS):
        total_loss = 0 # Track loss across batches
        for src, tgt in dataloader:
            src, tgt = src.to(device), tgt.to(device)
            optimizer.zero_grad() # Reset gradients pre backpropagation
            _, hidden = encoder(src) # encoder hidden state
            output, _ = decoder(tgt[:-1], hidden) # predictions 
            loss = criterion(output.view(-1, output.size(-1)), tgt[1:].reshape(-1)) # Shifted target for teacher forcing
            loss.backward() # Compute new gradients
            optimizer.step() # Update model parameters
            total_loss += loss.item()
        print(f"Epoch: {epoch+1}, Loss: {total_loss / len(dataloader):.6f}")

    # Save
    torch.save({'encoder': encoder.state_dict(), 'decoder': decoder.state_dict()}, MODEL_FILE)
    with open(VOCAB_FILE, 'wb') as f:
        pickle.dump(vocab, f) 

if __name__ == "__main__":
    train()