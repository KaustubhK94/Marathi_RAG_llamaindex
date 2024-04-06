import os
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.core import StorageContext
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.vector_stores.astra_db import AstraDBVectorStore
from llama_index.core import Settings
from dotenv import load_dotenv
from pdf_to_markdown import pdf_to_markdown

# Load environment variables from .env file
load_dotenv()

cohere_api_key = os.getenv("CO_API_KEY")
token = os.getenv("token")
openai = os.getenv("OPENAI_API_KEY")
api_endpoint = os.getenv("api_endpoint")

# Define base path
base_path = r"C:\Users\Kaustubh_k\PycharmProjects\Marathi_RAG\pythonProject2"

# Define the markdown file path
markdown_path = os.path.join(base_path, "New Folder", "your_markdown_file.md")

# Extract PDF to Markdown
markdown_content = pdf_to_markdown(pdf_path=os.path.join(base_path, "ToshieMaruki-FireOfHiroshima (1).pdf"),
                                   markdown_path=markdown_path,
                                   save_file=True,
                                   language='mar')

# Load documents from directory
documents = SimpleDirectoryReader(os.path.join(base_path, "New folder")).load_data()
print(f"Loaded {len(documents)} document(s).")

# Configure Settings
Settings.embed_model = CohereEmbedding(
    cohere_api_key=cohere_api_key,
    model_name="embed-multilingual-v3.0"
)

Settings.llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=256,
    tokenizer_name="Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa-2.0",
    model_name="Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa-2.0",
    device_map="auto",
)

Settings.chunk_size = 256

# Create a vector store instance
astra_db_store = AstraDBVectorStore(
    token=token,
    api_endpoint=api_endpoint,
    collection_name="test3",
    embedding_dimension=1024,
)

# Create storage context
storage_context = StorageContext.from_defaults(vector_store=astra_db_store)

# Create VectorStoreIndex
index = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context)

# Create query engine
query_engine = index.as_query_engine()

# Query examples
queries = [
    "लेखकाचे नाव काय आहे?",
    "स्फोट  होण्याच्या काही क्षणाआधी शहरावरून फिरणाऱ्या अमेरिकन विमानाचे नाव काय होते?",
    "पुस्तकाविषयी थोडी माहिती हवी आहे",
    "छोटा मुलगा कोणत्या दिवशी आणि किती वाजता हिरोशिमा वर कोसळला?",
    "नागासाकी वर अणुबॉम्ब कधी टाकण्यात आला?"
]

for query in queries:
    print("\n**********************")
    print(f"Query: {query}")
    response = query_engine.query(query)
    print("Response:", response)
