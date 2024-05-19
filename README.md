# wisper-llama-cpp-video-qa-voice-assistant

A **VideoQA Voice Assistant Engine** with _voice support_ using [`pywhispercpp`](https://github.com/abdeladim-s/pywispercpp), `llama-cpp-python`, and [ElevenLabs](https://elevenlabs.io/).

## Setup

Please follow the following steps to run this locally on your machine.

### Clone the Repo

```sh
git clone https://github.com/vatsalsaglani/wisper-llama-cpp-video-qa-voice-assistant.git
```

### Install dependencies

```sh
pip install -r requirements.txt --no-cache-dir
```

### Create a `model` folder

Create a model folder inside the `local-cpp-search` folder so that we can download the model in that folder.

```sh
mkdir model
```

### Download the model

[Download the quantized Phi-3-mini-4k-Instruct model in GGUF format from HuggingFace](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/tree/main).

![Phi-3 Model Download page](./assets/phi-3-model-download-page.png)

> Remember to move the model to the `model` folder.

### Add ElevenLabs API Key and Voice Id

Create a `.env` file and add the values for the following keys.

```
ELEVEN_LABS_API_KEY="YOUR ELEVEN LABS API KEY"
VOICE_ID="YOUR SELECTED VOICE ID"
```

### Start the Streamlit app

```sh
python -m localqa.voice_assistant
```

## Demo

Let's look at a real-time demo.

**_YouTube Video_**: https://www.youtube.com/watch?v=e1Yhs9BEOSw&t=51s&ab_channel=YCombinator

### Query: What are some interesting facts about new AI Startups?

![What are some interesting facts about new AI Startups?](./assets/talk-to-video-480p.mov)