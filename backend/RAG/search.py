import json
import os
import torch
from torch import topk
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pathlib import Path

class VectorDatabase:
    def __init__(self, database, vector_database, model="model/sbert_minilm"):
        self.database = database
        self.vector_database = vector_database
        self.model = SentenceTransformer(str(Path(model).resolve()))
        self.data = None
        self.index = None
        self.embeddings = None

    def load_data(self, data_file):
        if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Data file {data_file} is missing or empty.")

    def get_data(self):
        data_block = self.load_data(self.database)
        self.data = [block["positive"] for block in data_block]
        return self.data

    def convert_to_embeddings(self, data=None):
        if data is None:
            data = self.data
        self.embeddings = self.model.encode(data, convert_to_tensor=True)
        return self.embeddings

    def build_index(self, embeddings=None, query_embeddings=None):
        if embeddings is None:
            embeddings = self.embeddings
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        if query_embeddings is not None:
            faiss.normalize_L2(query_embeddings)

    def save_vectors(self):
        if self.index is None:
            raise ValueError("Index not built yet")
        faiss.write_index(self.index, "saved_vectors.bin")

    def save_sentences(self, sentences=None):
        if sentences is None:
            sentences = self.data
        torch.save(sentences, "saved_sentences.torch")
