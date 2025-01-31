from sentence_transformers import SentenceTransformer

class MultilingualEmbedder:
    def __init__(self, model_name="paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed(self, text):
        return self.model.encode(text).tolist() 