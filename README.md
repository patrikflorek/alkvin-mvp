# Alkvin MVP

## Description

Alkvin MVP is a proof-of-concept application that showcases the use of a Large Language Model (LLM) in a voice-to-voice interaction context. The application leverages OpenAI's speech-to-text (STT), text-to-speech (TTS), and text-generation models to facilitate user interaction. Users can interact with the application by speaking to it, and the application will respond by speaking back to the user.

The application allows users to choose from predefined set of agents ("User" and "Bot") definitions. The "User" refers to the application user, who can be automatically introduced to the "Bot" using a dedicated prompt. The "Bot" is an AI entity defined by the models it uses and various instruction prompts from the system.

The application is built using the Kivy/KivyMD framework for the GUI and the OpenAI API for the STT, TTS, and text-generation models.


## Requirements

The application requires the following dependencies:

- Python 3.7+
- Kivy 2.2.0+ 
- KivyMD 1.2.0
- OpenAI 1.13+
- PyAudio 0.2.14
- Python-dotenv 1.0.1


## Installation

Follow these steps to install and run the application:

1. **Clone the repository**

```bash
git clone https://github.com/patrikflorek/alkvin-mvp.git
cd alkvin-mvp
```

2. **Install the dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the application**

```bash
python -m alkvin
```
