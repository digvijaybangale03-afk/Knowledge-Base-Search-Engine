import requests, time, json, os

BASE = os.getenv('BASE_URL', 'http://localhost:8000')

def ingest_file(path):
    with open(path, 'rb') as f:
        files = {'file': (os.path.basename(path), f)}
        r = requests.post(f'{BASE}/ingest', files=files)
        return r.json()

def query(q, top_k=3):
    r = requests.post(f'{BASE}/query', data={'q': q, 'top_k': top_k})
    try:
        return r.json()
    except Exception as e:
        return {'error': str(e), 'status_code': r.status_code, 'text': r.text}

def main():
    sample_dir = os.path.join(os.path.dirname(__file__), '..', 'sample_data')
    sample_paths = [os.path.join(sample_dir, f) for f in os.listdir(sample_dir) if f.endswith('.txt')]
    outputs = {'ingest': [], 'queries': []}
    for p in sample_paths:
        print('Ingesting', p)
        out = ingest_file(p)
        print(' ->', out)
        outputs['ingest'].append({'file': os.path.basename(p), 'response': out})
        time.sleep(0.5)
    # Wait a bit for embeddings/index to persist
    print('Waiting 2s for index to update...')
    time.sleep(2)
    queries = [
        'What features does the ACME Cloud Platform provide?',
        'How do I authenticate to the API?',
        'What is the remote work policy?'
    ]
    for q in queries:
        print('Querying:', q)
        res = query(q, top_k=3)
        print(' ->', res)
        outputs['queries'].append({'q': q, 'response': res})
    out_path = os.path.join(os.path.dirname(__file__), 'demo_outputs.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(outputs, f, indent=2)
    print('Saved outputs to', out_path)

if __name__ == '__main__':
    main()
