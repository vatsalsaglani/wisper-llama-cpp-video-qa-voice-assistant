import numpy as np


def computeSimilarity(query_embedding: np.ndarray, video_embedding: np.ndarray,
                      top_similar: int):
    normalized_video = np.linalg.norm(video_embedding, axis=1)
    normalized_question = np.linalg.norm(query_embedding)
    emb_mat = np.dot(query_embedding, video_embedding.T)
    consie_sim = emb_mat / (normalized_video * normalized_question)
    consie_sim = consie_sim.flatten()
    return np.argsort(consie_sim)[::-1][:top_similar]
