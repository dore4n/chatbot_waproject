import os
import shutil
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('punkt_tab')

CHROMA_PATH = "./chroma"
DATA_PATH = "agent_chatbot/data/books"

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "HUGGINGFACE_API_KEY"

def main():
    try:
        generate_data_store()
    except Exception as e:
        print(f"Erro ocorreu: {e}")

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    try:
        pdf_files = [
            os.path.join(DATA_PATH, file)
            for file in os.listdir(DATA_PATH)
            if file.endswith(".pdf")
        ]

        documents = []
        for pdf_file in pdf_files:
            reader = PdfReader(pdf_file)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text

            documents.append(Document(
                page_content=full_text,
                metadata={"source": pdf_file}
            ))
        
        print(f"Carregados {len(documents)} documentos.")
        return documents
    except Exception as e:
        print(f"Erro ao carregar documentos: {e}")
        return []

def split_text(documents: list):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

        # Apenas para demonstração: mostre o conteúdo do primeiro chunk
        if chunks:
            print(chunks[0].page_content)
            print(chunks[0].metadata)

        return chunks
    except Exception as e:
        print(f"Erro ao dividir texto: {e}")
        return []

def save_to_chroma(chunks: list):
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)

        hf_embeddings = HuggingFaceEmbeddings()

        db = Chroma.from_documents(
            chunks, hf_embeddings, persist_directory=CHROMA_PATH
        )
        db.persist()
        print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    except Exception as e:
        print(f"Erro ao salvar no Chroma: {e}")

if __name__ == "__main__":
    main()
