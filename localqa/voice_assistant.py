from typing import List, Dict, Union
from pywhispercpp.examples.assistant import Assistant
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from rich.console import Console
from rich.theme import Theme

from configs import ELEVEN_LABS_API_KEY, VOICE_ID
from llm.invoke import LLM
from localqa.qa import VideoQA

custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "error": "bold red",
    "prompt": "dim cyan",
    "user_input": "bold green",
    "assistant": "bold blue",
})
console = Console(theme=custom_theme)

llm = LLM("./model/Phi-3-mini-4k-instruct-q4.gguf")

assistant_client = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)

video_url = console.input("YouTube Video URL: ")

vqa = VideoQA(llm, video_url)


def voice_assistant_callback(text):
    console.print(text, style="user_input")
    # ans = vqa(text)
    # console.print(ans, style="assistant")
    audio_stream = assistant_client.generate(text=vqa(text),
                                             stream=True,
                                             voice=VOICE_ID)
    stream(audio_stream)


assistant = Assistant(model="small",
                      commands_callback=voice_assistant_callback,
                      n_threads=8)
assistant.start()
