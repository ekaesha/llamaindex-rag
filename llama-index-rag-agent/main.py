import os
import logging
import sys

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
)
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.ollama import Ollama
import qdrant_client

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the embedding model
Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")

Settings.llm = Ollama(model="llama3.2:3b", request_timeout=300.0)

# Define the path to your markdown notes
notes_directory = "./obsidian"

# Load documents from the specified directory
documents = SimpleDirectoryReader(
    notes_directory, recursive=True, required_exts=[".md"]
).load_data(show_progress=True)

# Initialize Qdrant client
client = qdrant_client.QdrantClient(
    location=":memory:"
    # For Qdrant Cloud, provide the URL and API key:
    # url="https://your-qdrant-url",
    # api_key="your_qdrant_api_key",
)

# Create a Qdrant vector store
vector_store = QdrantVectorStore(client=client, collection_name="obsidian_notes")

# Create a storage context
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Build the vector store index
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# Create a query engine
query_engine = index.as_query_engine()

# Define your query
query = "Summarize my notes about business."

# Execute the query
response = query_engine.query(query)

# Print the response
print(f"Response:\n{response}")
