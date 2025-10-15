import os, json, math
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from tqdm import tqdm
from backend.utils import chunk_text, ensure_dirs

MODEL_NAME = 'all-MiniLM-L6-v2'  # small, fast model good for assessments
INDEX_DIR = os.path.join(os.getcwd(), 'index_data')

ensure_dirs(INDEX_DIR)

def ingest_file(path, source=None):
    # Extract text (pdf or plain)
    if path.lower().endswith('.pdf'):
        text = extract_text(path)
    else:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    # chunk
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    # create or load FAISS index
    dim = embeddings.shape[1]
    index_path = os.path.join(INDEX_DIR, 'faiss.index')
    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
        existing = True
    else:
        index = faiss.IndexFlatIP(dim)
        existing = False
    # normalize for cosine similarity
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    faiss.write_index(index, index_path)
    # save metadata
    meta_path = os.path.join(INDEX_DIR, 'meta.jsonl')
    with open(meta_path, 'a', encoding='utf-8') as mf:
        for c in chunks:
            mf.write(json.dumps({'text': c, 'source': source or os.path.basename(path)}) + '\n')
    return len(chunks)
