**Marathi RAG Application**
Ask questions over A PDF that too in Marathi.
-
using opensource Huggingface model ***"Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa-2.0"***
And Cohere's ***"embed-multilingual-v3.0"***
- Create a Virtual Environment.
- Clone the Repository.
- `pip install -r requirements.txt`
- once done you'll need API keys for Cohere (Embedding Model) and our Vector database Datastax (astra DB) along with its api endpoint.
  - [click here](https://dashboard.cohere.com/api-keys) for Cohere API Key
  - [click here](https://astra.datastax.com/org/5cbd84bf-4cde-4e36-87dd-8302ee7d8eca/database) For creating your Vector DB.
- you need to save these API KEYS and Endpoint in a separate '.env' file.
- once properly set open the terminal on your IDE and run `streamlit run Maarathi_RAG_UI.py`.
