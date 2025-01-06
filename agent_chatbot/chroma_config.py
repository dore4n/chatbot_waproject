import chromadb
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def load_or_create_chroma(persist_directory="./chroma"):
    client = chromadb.Client()


    collection = client.get_or_create_collection("chatbot")


    embedding_model = HuggingFaceEmbeddings(model_name="distilbert-base-uncased")


    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)


    vectorstore._collection = collection

    return vectorstore


def add_message_to_chroma(message: str, vectorstore):

    metadata = {"source": "user_message"}
    
    vectorstore.add_texts([message], metadatas=[metadata])
