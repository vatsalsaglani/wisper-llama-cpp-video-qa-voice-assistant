from typing import List, Dict
from transformers import AutoTokenizer, AutoModel
import torch

# Load model from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en-v1.5')
model = AutoModel.from_pretrained('BAAI/bge-small-en-v1.5')
model.eval()


def generateEmbeddings(sentences: List[str]):

    encoded_input = tokenizer(sentences,
                              padding=True,
                              truncation=True,
                              return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
        sentence_embeddings = model_output[0][:, 0]
    sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings,
                                                        p=2,
                                                        dim=1)
    return sentence_embeddings.numpy()


if __name__ == "__main__":
    e = generateEmbeddings(["Hello World"])
    print(e.shape)
