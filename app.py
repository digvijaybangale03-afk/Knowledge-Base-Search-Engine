import streamlit as st
import requests
st.set_page_config(page_title='RAG Search Demo', layout='wide')
st.title('Knowledge-base Search Engine — Demo')

with st.sidebar:
    st.header('Upload documents')
    uploaded = st.file_uploader('Upload PDF / txt', accept_multiple_files=True)
    if st.button('Ingest'):
        for f in uploaded or []:
            files = {'file': (f.name, f.getvalue())}
            r = requests.post('http://localhost:8000/ingest', files=files)
            st.write(r.json())

st.header('Ask a question')
q = st.text_input('Your question here')
k = st.slider('Top-k retrieved docs', min_value=1, max_value=10, value=5)
if st.button('Ask') and q.strip():
    r = requests.post('http://localhost:8000/query', data={'q': q, 'top_k': k})
    if r.status_code == 200:
        data = r.json()
        st.subheader('Answer')
        st.write(data.get('answer') or data)
        st.subheader('Sources')
        st.write(data.get('sources'))
    else:
        st.error(f'Error: {r.text}')
