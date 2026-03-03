import os
import torch
import pickle
from torch.serialization import add_safe_globals
from train import Encoder, Decoder
from utils import Vocab, BATCH_SIZE, HIDDEN_SIZE, MAX_LENGTH, NUM_EPOCHS, LEARNING_RATE



BASE_DIR = os.path.dirname(__file__)

MODEL_FILE = os.path.join(BASE_DIR, "rem.pth")
VOCAB_FILE = os.path.join(BASE_DIR, "data", "vocab.pkl")


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load vocab
with open(VOCAB_FILE, "rb") as f:
    vocab = pickle.load(f)

# Initialize models
encoder = Encoder(len(vocab.word2idx), HIDDEN_SIZE, HIDDEN_SIZE).to(device)
decoder = Decoder(len(vocab.word2idx), HIDDEN_SIZE, HIDDEN_SIZE).to(device)

# Load weights
checkpoint = torch.load(MODEL_FILE, map_location=device)
encoder.load_state_dict(checkpoint["encoder"])
decoder.load_state_dict(checkpoint["decoder"])
encoder.eval()
decoder.eval()



def generate_reply(input_sentence: str) -> str:
    with torch.no_grad():
        input_indices = [1] + vocab.sentence_to_indices(input_sentence.lower())[:MAX_LENGTH] + [2]
        input_tensor = torch.tensor(input_indices).unsqueeze(1).to(device)
        _, hidden = encoder(input_tensor)

        tgt_input = torch.tensor([[1]]).to(device)
        result = []
        for _ in range(MAX_LENGTH):
            output, hidden = decoder(tgt_input, hidden)
            top1 = output.argmax(2)[-1]
            if top1.item() == 2:  # EOS
                break
            result.append(top1.item())
            tgt_input = top1.unsqueeze(0)

        return vocab.indices_to_sentence(result).capitalize()
