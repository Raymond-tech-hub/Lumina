import json
import os
import pickle
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path

class VectorDatabase:
    def __init__(self, index_file="database/vector_index.faiss", sentences_file="database/sentences.pt",
                 database="database/training_data_intent_aware.json", model="model/sbert_minilm"):
        self.database = database
        self.model = SentenceTransformer(str(Path(model).resolve()))
        self.data = None
        self.embeddings = None
        self.index = None
        self.index_file = index_file
        self.sentences_file = sentences_file

    # Load dataset
    def load_data(self):
        if not os.path.exists(self.database) or os.path.getsize(self.database) == 0:
            raise FileNotFoundError(f"{self.database} missing or empty")
        with open(self.database, 'r', encoding='utf-8') as f:
            blocks = json.load(f)
        self.data = [b["positive"] for b in blocks]
        return self.data

    # Convert dataset to embeddings
    def convert_to_embeddings(self):
        self.embeddings = self.model.encode(self.data, convert_to_numpy=True)
        faiss.normalize_L2(self.embeddings)
        return self.embeddings

    # Build FAISS index
    def build_index(self):
        if self.embeddings is None:
            raise ValueError("Embeddings not computed yet")
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)
        print(f"Index built with {self.index.ntotal} vectors")

    # Save index and sentences
    def save_index(self):
        if self.index is None:
            raise ValueError("Index not built yet")
        faiss.write_index(self.index, self.index_file)
        with open(self.sentences_file, "wb") as f:
            pickle.dump(self.data, f)
        print(f"Index saved to {self.index_file}")
        print(f"Sentences saved to {self.sentences_file}")

    def load_index(self):
        if not os.path.exists(self.index_file) or not os.path.exists(self.sentences_file):
            raise FileNotFoundError("Saved index or sentences not found")
        self.index = faiss.read_index(self.index_file)
        with open(self.sentences_file, "rb") as f:
            self.data = pickle.load(f)

    def prepare_index(self):
        self.load_data()
        self.convert_to_embeddings()
        self.build_index()
        self.save_index()

    # Search query
    def search(self, query, top_k=5):
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        D, I = self.index.search(query_embedding, top_k)
        results = [self.data[i] for i in I[0]]
        return results

if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)          
    print("Working directory set to:", os.getcwd())    

    vd = VectorDatabase()

    vd.prepare_index()

    vd.load_index()

    print(vd.search("What is osmosis")[0])
    print(vd.search("What is the importance of osmosis to bacteria")[0])
    print(vd.search("hello")[0])
    print(vd.search("hello how are you today")[0])
    print(vd.search("hi, nice to meet you today")[0])
    


