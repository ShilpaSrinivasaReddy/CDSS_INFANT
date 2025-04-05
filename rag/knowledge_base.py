# knowledge_base.py
# -----------------------------
# This file loads clinical documents, embeds them,
# and allows semantic similarity search using FAISS.

import os
import faiss
import pickle

from sentence_transformers import SentenceTransformer
from langchain.docstore.document import Document

class KnowledgeBase:
    def __init__(self, doc_folder="data/knowledge_base_docs", index_file="rag/faiss_index"):
        self.doc_folder = doc_folder
        self.index_file = index_file
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.text_chunks = []

        if os.path.exists(index_file):
            self.load_index()
        else:
            self.build_index()

    def build_index(self):
        texts = []
        metadata = []

        for filename in os.listdir(self.doc_folder):
            if filename.endswith(".txt"):
                path = os.path.join(self.doc_folder, filename)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    chunks = self.split_into_chunks(content)
                    texts.extend(chunks)
                    metadata.extend([{"source": filename}] * len(chunks))

        self.text_chunks = texts
        embeddings = self.model.encode(texts)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

        # Save metadata
        with open(self.index_file + "_meta.pkl", "wb") as f:
            pickle.dump(metadata, f)

        # Save index
        faiss.write_index(self.index, self.index_file)

    def load_index(self):
        self.index = faiss.read_index(self.index_file)
        with open(self.index_file + "_meta.pkl", "rb") as f:
            self.text_chunks = pickle.load(f)

    def split_into_chunks(self, text, max_tokens=300):
        paragraphs = text.split("\n\n")
        return [p.strip() for p in paragraphs if len(p.strip()) > 50]

    def query(self, question, top_k=3):
        question_embedding = self.model.encode([question])
        distances, indices = self.index.search(question_embedding, top_k)
        results = [self.text_chunks[i] for i in indices[0]]
        return results  # ✅ Now it's a list of strings
