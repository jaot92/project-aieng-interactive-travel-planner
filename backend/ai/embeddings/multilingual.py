from sentence_transformers import SentenceTransformer
from chromadb.api.types import Documents, EmbeddingFunction

class MultilingualEmbedder(EmbeddingFunction):
    def __init__(self, model_name="paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
    
    def __call__(self, input: Documents) -> list:
        if isinstance(input, str):
            input = [input]
        return self.model.encode(input).tolist() 