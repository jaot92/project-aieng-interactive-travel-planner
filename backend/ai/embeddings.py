from sentence_transformers import SentenceTransformer

class MultilingualEmbedder:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    def embed(self, text: str):
        return self.model.encode(text) 