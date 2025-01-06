import chromadb
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def load_or_create_chroma(persist_directory="./chroma"):
    client = chromadb.Client(tenant="default_tenant")  # Use o tenant correto ou configure conforme necessário
    collection = client.get_or_create_collection("chatbot")
    
    embedding_model = HuggingFaceEmbeddings()
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)
    vectorstore._collection = collection

    return vectorstore

def add_message_to_chroma(message: str, vectorstore):
    """
    Adiciona uma mensagem ao ChromaDB.
    """
    metadata = {"source": "user_message"}
    vectorstore.add_texts([message], metadatas=[metadata])
