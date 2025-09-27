# <img width="40" height="40" alt="logo" src="https://github.com/user-attachments/assets/48fb8b0c-2a17-4c7e-af49-0e24d0a6e599" />  Rem: An AI Conversational Assistant

Rem: An AI Conversational Assistant
Rem is a voice, memory, and personality-based AI personal assistant. compared to conventional chatbots, Rem is an AI-powered assistant with the goal to feel more human. Rem, compared with conventional assistants, creates engaging, customized interactions by combining expressive voice synthesis, conversational memory, and natural language understanding.

<br>
<div align="center">
  <img width="558" height="234" alt="Screenshot 2025-09-27 at 9 01 43 PM" src="https://github.com/user-attachments/assets/90128078-ca34-4bed-8d1c-ed721fc8d622" />
  <br>
  <img width="558" height="234" alt="image" src="https://github.com/user-attachments/assets/280f08fb-5e4e-4ede-9811-695c2ecb8dab" />
</div>
<br>


This project combines PyTorch, Coqui TTS, SpeechRecognition, and Discords Application API to create a next generation conversational experience.

**Dataset Format**

The dataset is stored in a plain text file where each line represents a dialogue pair.
The input (what the user says) and the target (Rem’s possible response) are separated by __eou__.

```
Hey Rem, are you awake? __eou__ Of course, I never really sleep.  
Rem, what’s your favorite color? __eou__ Purple, always purple—you should know that by now.  
Do you ever get bored, Rem? __eou__ Not when I’m with you, honestly.  
Rem, can you keep a secret? __eou__ I can, but only if it’s about snacks or winter outfits.
```

How to Read This: <br>
	•	Input (before __eou__) → What the user says to Rem. <br>
	•	Target (after __eou__) → Example of how Rem COULD reply. <br>
	•	Each line = one training example. <br>
