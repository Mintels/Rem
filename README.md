# <img width="50" alt="Remicon" src="https://github.com/user-attachments/assets/c585e026-5946-4c37-a5f2-094ac5fbba8e" /> Rem: An AI Conversational Companion

Rem is a proof-of-concept memory and personality-based AI personal companion. Unlike conventional chatbots, Rem creates engaging, customized interactions through conversational memory and natural language understanding — built to feel more human.

## Example Application
<div align="center">
    <img width="700" src="https://github.com/user-attachments/assets/7a11f842-63d7-4352-aeb1-11119d6d1b0a" />
</div>
<br>

## Tech Stack 

### AI/ML Development
[PyTorch](https://pytorch.org/), [Pandas](https://pandas.pydata.org/), and [Hugging Face Datasets](https://huggingface.co/datasets/)

### Backend Development
[Django](https://www.djangoproject.com/), [Discord API](https://discord.com/developers/docs/reference), and [PythonAnywhere](https://www.pythonanywhere.com/)

### Frontend Development
[React.JS](https://react.dev/) and [Node.JS](https://nodejs.org/)

## Dataset Format

This project utilizes a modified version of the <a href="https://huggingface.co/datasets/roskoN/dailydialog">DailyDialog Multi-turn Dialog Dataset</a>, with 21,000 additional input-output pairs specialized towards A1-A2 CEFR English responses added.

The supplementary data was introduced to mitigate overfitting and broaden response coverage beyond the scope of the original 21,000 custom input-output pairs.

## Expanding Past Proof-of-Concept

When deciding to create this model, I decided to not scale it in order to account for things such as server cost, storage, and training requirements in performace power.

If I were to train and scale it to a production level product, I would implement the following strategies:
- Increasing the amount of data trained on the model to prevent overfitting and allow for more accurate, diverse responses.
- Introducing dropout and regularization techniques to further reduce overfitting on the limited training set.
<br>
<div align="center">
	<img width="700" src="https://github.com/user-attachments/assets/d2e08277-c592-433c-b341-94791fe7ebd5" />
</div>
<br>
