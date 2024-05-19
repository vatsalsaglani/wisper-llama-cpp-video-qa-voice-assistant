import numpy as np
from tqdm.auto import tqdm, trange
from typing import List, Dict, Union
from transcript.collect import getTranscriptData
from embedding.create_embedding import generateEmbeddings
from embedding.similar import computeSimilarity
from localqa.prompts import SYSTEM_PROPMTS
from llm.invoke import LLM


class VideoQA:

    def __init__(self,
                 llm: LLM,
                 video_url: str,
                 top_similar: int = 10,
                 batch_size=8):
        self.llm = llm
        self.video_url = video_url
        self.top_k = top_similar
        self.batch_size = batch_size
        self.video_representations = []
        self.flatten = lambda lst: [
            item for sublist in lst for item in sublist
        ]
        self.__transcript_and_embeddings__()

    def __transcript_and_embeddings__(self):
        self.transcript_data = getTranscriptData(self.video_url)

        for ix in trange(0, len(self.transcript_data), self.batch_size):
            texts = list(
                map(lambda content: content.get("text"),
                    self.transcript_data[ix:ix + self.batch_size]))
            embeddings = generateEmbeddings(texts)
            self.video_representations.append(embeddings)
        self.video_representations = np.concatenate(self.video_representations,
                                                    axis=0)

    def __call__(self, query: str):
        query_emb = generateEmbeddings([query])
        indices = computeSimilarity(query_emb, self.video_representations,
                                    self.top_k)
        retrieved_content = [self.transcript_data[ix] for ix in indices]
        context_doc = "\n".join(
            list(map(lambda content: content.get("text"), retrieved_content)))
        print(f"Context Document: \n", context_doc)
        messages = [{
            "role": "system",
            "content": SYSTEM_PROPMTS.qa
        }, {
            "role":
            "user",
            "content":
            f"User Query: `{query}`\n Context Documents: ```{context_doc}```"
        }]
        yield from self.llm.__stream__(messages, max_tokens=256)
        # return self.llm.__complete__(messages, max_tokens=256)


if __name__ == "__main__":
    llm = LLM("./model/Phi-3-mini-4k-instruct-q4.gguf")
    vqa = VideoQA(
        llm,
        video_url=
        "https://www.youtube.com/watch?v=nSM0xd8xHUM&ab_channel=All-InPodcast")
