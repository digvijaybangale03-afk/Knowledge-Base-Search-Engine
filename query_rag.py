import os, json, numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from backend.utils import load_meta, format_answer_with_sources
from backend.modules.query import answer_query
import openai
import os

MODEL_NAME = 'all-MiniLM-L6-v2'
INDEX_DIR = os.path.join(os.getcwd(), 'index_data')
FAISS_INDEX = os.path.join(INDEX_DIR, 'faiss.index')
EMBED_MODEL = SentenceTransformer(MODEL_NAME)

def retrieve(query, top_k=5):
    if not os.path.exists(FAISS_INDEX):
        return []
    q_emb = EMBED_MODEL.encode([query])
    import numpy as np, faiss
    q_emb = np.array(q_emb).astype('float32')
    faiss.normalize_L2(q_emb)
    index = faiss.read_index(FAISS_INDEX)
    D, I = index.search(q_emb, top_k)
    meta = load_meta()
    results = []
    for idx in I[0]:
        if idx < len(meta):
            results.append(meta[idx]['text'])
    return results

def answer_query(query, top_k=5):
    docs = retrieve(query, top_k=top_k)
    # Build RAG prompt
    system = "You are an assistant that answers using only provided documents. When you cannot answer, say you don't know."
    prompt = f"""{system}\n\nDocuments:\n"""
    for i,d in enumerate(docs):
        prompt += f"[DOC {i+1}] {d}\n\n"
    prompt += f"User question: {query}\n\nProvide a short, referenced answer (cite DOC numbers)."
    # Call OpenAI (ChatCompletion)
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        # Fallback: return a concise synthetic answer using retrieved docs (useful for offline tests)
        combined = '\\n\\n'.join(docs[:3])
        synth = 'Summary (offline fallback): ' + (combined[:400] + '...' if combined else 'No documents')
        return {'answer': synth, 'documents_retrieved': len(docs), 'sources': [f'DOC {i+1}' for i in range(len(docs))]}
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini' if False else 'gpt-4o-mini', # placeholder, adjust in deployment
            messages=[{'role':'system','content': system},
                      {'role':'user','content': prompt}],
            max_tokens=400,
            temperature=0.0
        )
        text = resp['choices'][0]['message']['content'].strip()
    except Exception as e:
        return {'error': str(e), 'documents_retrieved': len(docs)}
    return {'answer': text, 'documents_retrieved': len(docs), 'sources': [f'DOC {i+1}' for i in range(len(docs))]}
