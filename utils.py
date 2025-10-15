import os, json, re
def chunk_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(' '.join(words[start:end]))
        start = max(end - overlap, end)
    return chunks

def ensure_dirs(d):
    os.makedirs(d, exist_ok=True)

def load_meta():
    path = os.path.join(os.getcwd(), 'index_data', 'meta.jsonl')
    if not os.path.exists(path):
        return []
    out = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            out.append(json.loads(line))
    return out

def format_answer_with_sources(answer, sources):
    return {'answer': answer, 'sources': sources}
