import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class RAGEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []

    def build_index(self, texts):
        self.texts = texts
        if not texts:
            print("Warning: No texts provided to index.")
            return
        print(f"Indexing {len(texts)} documents...")
        embeddings = self.model.encode(self.texts, show_progress_bar=True)
        dimension = embeddings.shape[1]
        # IndexFlatL2 is precise for datasets under 1 million rows
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        print("FAISS Index built successfully.")

    def search(self, query, k=7):
        """Finds the most relevant context for a query."""
        if self.index is None:
            return "Index not initialized."
            
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        
        # Retrieve the actual text strings using the indices found
        retrieved_chunks = [self.texts[i] for i in indices[0] if i != -1]
        return "\n\n".join(retrieved_chunks)