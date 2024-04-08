**Marathi RAG Application file**
Ask questions over A PDF that too in Marathi.
using **"Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa-2.0"**
And **Cohere's embed-multilingual-v3.0**
Create a Virtual Environment.
Clone the Repository.
`pip install -r requirements.txt`
once done you'll need API keys for Cohere (Embedding Model) and our Vector database Datastax (astra DB) along with its epi endpoint.
you need to save these API KEYS and Endpoint in a separate '.env' file.
once properly set open terminal on your IDE and run `streamlit run Maarathi_RAG_UI.py`.
