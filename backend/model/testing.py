import os

from .train import MODEL_FILE, VOCAB_FILE
from .response import generate_reply
from .utils import clean_content


def run_chat() -> None:
	if not os.path.exists(MODEL_FILE):
		print(f"Model file not found: {MODEL_FILE}")
		return

	if not os.path.exists(VOCAB_FILE):
		print(f"Vocab file not found: {VOCAB_FILE}")
		return

	print("Rem local model test")
	print("Type 'quit' to exit.")

	while True:
		user_input = input("You: ").strip()
		if user_input.lower() in {"quit", "exit", "q"}:
			print("Bye.")
			break

		cleaned_input = clean_content(user_input)
		if not cleaned_input:
			print("Rem: Please type a message.")
			continue

		reply = generate_reply(cleaned_input)
		print(f"Rem: {reply}")


if __name__ == "__main__":
	run_chat()
