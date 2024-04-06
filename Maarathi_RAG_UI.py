import os
import streamlit as st
from pdf2image import convert_from_path
import pytesseract
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.core import StorageContext
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.vector_stores.astra_db import AstraDBVectorStore
from llama_index.core import Settings
from dotenv import load_dotenv
import requests
from contextlib import suppress

# Get the absolute path of the current directory where the script is located
base_path = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file
load_dotenv()

cohere_api_key = os.getenv("CO_API_KEY")
token = os.getenv("token")
api_endpoint = os.getenv("api_endpoint")
openai = os.getenv("OPENAI_API_KEY")

def download_file_from_google_drive(url, file_name):
    try:
        session = requests.Session()
        response = session.get(url, stream=True)
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        st.success("File downloaded successfully!")
    except Exception as e:
        st.error(f"Error downloading the file: {e}")

# Create a text input for the Google Drive link
google_drive_link = st.text_input("Paste Google Drive link:", "")

def pdf_to_markdown(pdf_path, markdown_path, save_file=True, language='mar'):
    # Suppress exceptions that may occur during PDF conversion
    with suppress(Exception):
        # Convert PDF to images
        images = convert_from_path(pdf_path)

        # Initialize a variable to store the accumulated text
        accumulated_text = ''

        # Check if the output directory exists, create it if it doesn't
        output_directory = os.path.dirname(markdown_path)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Perform OCR on each image
        for i, image in enumerate(images):
            # Perform OCR on the image
            text = pytesseract.image_to_string(image, lang=language)

            # Accumulate the extracted text
            accumulated_text += f'# Page {i+1}\n\n{text}\n\n'

        # Save the accumulated text to the Markdown file if the flag is True
        if save_file:
            with open(markdown_path, 'w', encoding='utf-8') as md_file:
                md_file.write(accumulated_text)
            print('Text extraction complete. Markdown file saved as:', markdown_path)

        return accumulated_text


# Create a form
with st.form(key='query_form'):
    # Initialize variables
    user_query = ""
    response = None
    # If Google Drive link is provided
    if google_drive_link:
        try:
            # Download the file from Google Drive
            file_name = "file.pdf"  # Provide a suitable file name with extension
            download_file_from_google_drive(google_drive_link, file_name)
            # Add a button to submit the form
            submit_button = st.form_submit_button(label='Submit PDF')
            # Debug statement
            st.write("PDF downloaded successfully.")
            pdf_file_name = "input.pdf"
            # Define the markdown file path
            markdown_path = "output.md"

            # Extract PDF to Markdown
            st.write("Converting PDF to Markdown...")
            markdown_content = pdf_to_markdown(pdf_path=pdf_file_name,
                                               markdown_path=markdown_path,
                                               save_file=True,
                                               language='mar')
            # Debug statement
            st.write("PDF converted to Markdown successfully.")

            # Load documents from directory
            documents = SimpleDirectoryReader(os.path.join(base_path, "New folder")).load_data()
            st.write(f"Loaded {len(documents)} document(s).")

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
                collection_name="test5",
                embedding_dimension=1024,
                )

            # Create storage context
            storage_context = StorageContext.from_defaults(vector_store=astra_db_store)

            # Create VectorStoreIndex and query engine
            index = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context)
            query_engine = index.as_query_engine()
            # Prompt user to enter query
            user_query = st.text_input("Enter your query:", key="user_query")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Add a submit button
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if user_query:
        response = query_engine.query(user_query)
        st.write("Response:")
        st.write(response)
