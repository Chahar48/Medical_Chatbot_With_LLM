from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, download_hugging_face_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec 
from langchain_pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

# Fetch Pinecone API Key
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Step 1: Load and preprocess documents
extracted_data = load_pdf_file(data='data/')
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)

# Step 2: Download Hugging Face embeddings
embeddings = download_hugging_face_embeddings()

# Step 3: Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define index name
index_name = "medical-chatbot"  # change if desired

# Step 4: Create Pinecone index if it doesn’t exist
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Step 5: Get Pinecone index
index = pc.Index(index_name)

# Step 6: Store documents in Pinecone Vector Store
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings, 
)
