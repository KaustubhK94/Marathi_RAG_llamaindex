**Marathi RAG Application**
Query your PDFs in Marathi.
using opensource Huggingface model ***"Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa-2.0"***
And Cohere's ***"embed-multilingual-v3.0"***.

Huggingface Model Card [Click Here](https://huggingface.co/Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa-2.0)

- Ensure that Tesseract is Installed correctly.
  - Download Tesseract's Marathi train data [Click Here to Download](https://tesseract-ocr.github.io/tessdoc/Data-Files) copy the file to `C:\Program Files\Tesseract-OCR\tessdata`
- Create a Virtual Environment.
- Clone the Repository.
- `pip install -r requirements.txt`
- once done you'll need API keys for Cohere (Embedding Model) and our Vector database Datastax (astra DB) along with its api endpoint.
  - [click here](https://dashboard.cohere.com/api-keys) for Cohere API Key
  - [click here](https://astra.datastax.com/org/5cbd84bf-4cde-4e36-87dd-8302ee7d8eca/database) For creating your Vector DB.
- you need to save these API KEYS and Endpoint in a separate '.env' file.
- Ensure that you've downloaded the weights of the huggingface model try running marathi_rag_app.py first locally.
- once properly set open the terminal on your IDE and run `streamlit run Maarathi_RAG_UI.py`.
- ![Results of the Queries.](https://github.com/KaustubhK94/Marathi_RAG_llamaindex/assets/91604508/a724e8bd-efaf-409b-9236-0f140dec3702)


