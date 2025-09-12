import os
import torch
import pickle
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from .utils import Vocab, BATCH_SIZE, HIDDEN_SIZE, MAX_LENGTH, NUM_EPOCHS, LEARNING_RATE


# File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'dialogues.txt')
VOCAB_FILE = os.path.join(BASE_DIR, 'data', 'vocab.pkl')
MODEL_FILE = os.path.join(BASE_DIR, 'rem.pth')

# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load and preprocess data
def load_data(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    pairs = []
    for line in lines:
        line = line.strip()
        sentences = line.split('__eou__')
        sentences = [s.strip() for s in sentences if s.strip()]
        for i in range(len(sentences) - 1):
            pairs.append((sentences[i].lower(), sentences[i+1].lower()))
    return pairs

# Dataset class
class ChatDataset(Dataset):
    def __init__(self, pairs, vocab):
        self.pairs = pairs
        self.vocab = vocab

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        input, target = self.pairs[idx]
        input_ids = [1] + self.vocab.sentence_to_indices(input)[:MAX_LENGTH] + [2]
        target_ids = [1] + self.vocab.sentence_to_indices(target)[:MAX_LENGTH] + [2]
        return torch.tensor(input_ids), torch.tensor(target_ids)

def collate_fn(batch):
    input_batch, target_batch = zip(*batch)
    input_batch = nn.utils.rnn.pad_sequence(input_batch, padding_value=0)
    target_batch = nn.utils.rnn.pad_sequence(target_batch, padding_value=0)
    return input_batch, target_batch

# Model
class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.GRU(embed_size, hidden_size)

    def forward(self, src):
        embedded = self.embed(src)
        outputs, hidden = self.rnn(embedded)
        return outputs, hidden

class Decoder(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.GRU(embed_size, hidden_size)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, tgt, hidden):
        embedded = self.embed(tgt)
        outputs, hidden = self.rnn(embedded, hidden)
        predictions = self.fc(outputs)
        return predictions, hidden

# Training
def train():
    pairs = load_data(DATA_FILE)
    vocab = Vocab()
    for inp, tgt in pairs:
        vocab.add_sentence(inp)
        vocab.add_sentence(tgt)

    dataset = ChatDataset(pairs, vocab)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)

    encoder = Encoder(len(vocab.word2idx), HIDDEN_SIZE, HIDDEN_SIZE).to(device)
    decoder = Decoder(len(vocab.word2idx), HIDDEN_SIZE, HIDDEN_SIZE).to(device)

    criterion = nn.CrossEntropyLoss(ignore_index=0)
    optimizer = optim.Adam(list(encoder.parameters()) + list(decoder.parameters()), lr=LEARNING_RATE)

    for epoch in range(NUM_EPOCHS):
        for src, tgt in dataloader:
            src, tgt = src.to(device), tgt.to(device)
            optimizer.zero_grad()
            _, hidden = encoder(src)
            output, _ = decoder(tgt[:-1], hidden)
            loss = criterion(output.view(-1, output.size(-1)), tgt[1:].reshape(-1))
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch+1} Loss: {loss.item():.4f}")

    # Save
    torch.save({'encoder': encoder.state_dict(), 'decoder': decoder.state_dict()}, MODEL_FILE)
    with open(VOCAB_FILE, 'wb') as f:
        pickle.dump(vocab, f)

if __name__ == "__main__":
    train()