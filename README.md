# <img width="40" height="40" alt="logo" src="https://github.com/user-attachments/assets/2a66aef7-99d3-427d-ba25-2adb33dfb3f7" />  Rem: An AI Conversational Companion

Rem is a voice, memory, and personality-based AI personal companion. compared to conventional chatbots, Rem is an AI-powered assistant with the goal to feel more human. Rem, compared with conventional assistants, creates engaging, customized interactions by combining expressive voice synthesis, conversational memory, and natural language understanding.

## Example Application
<br>
<div align="center">
	<img width="558" height="234" src="https://github.com/user-attachments/assets/eb73115e-cc47-4ea5-9fc4-80ebc2da3988" />
	<br>
	<img width="558" height="234" src="https://github.com/user-attachments/assets/57922239-8290-4426-9fc8-a6be8d2731e4" />
</div>
<br>


## Tech Stack

<a href=https://pytorch.org/>PyTorch</a></br> 
<a href=https://pypi.org/project/TTS/>Coqui TTS</a></br>
<a href="https://discord.com/developers/docs/reference">Discord</a></br>
<a href="https://pypi.org/project/discord-ext-voice-recv/">Discord-Ext-Voice-Recv</a></br>

## Dataset Format

The dataset is stored as comma separated values, where each line contains *one* input and *three* outputs.

```
"input","outputs"
"Would you skydive?","Maybe, if I was with friends.||I'd consider it if someone encouraged me.||With support, I might give it a shot."
"Can you name all the US presidents?","I feel a bit embarrassed, but I can't name them all.||I'm not sure I could list every president.||That would be tough for me to do."
"Did you ever have a pen pal?","I never had one, but I always wanted to.||I missed out on that experience.||It sounds like it would have been nice."
```

How to Read This: <br>
	•	Input (First Column) → What the user may say to Rem. <br>
	•	Output (Second Column) → three Examples of how Rem COULD reply, Delimited by "||" <br>
	•	Each line → *three* training examples. <br>

