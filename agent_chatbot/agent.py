from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(api_key=os.getenv('GROQ_API_KEY'))
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Você é um assistente virtual especializado e empático. Sua tarefa é fornecer respostas claras e naturais, adaptando-se ao tom do usuário e priorizando uma comunicação fluída e respeitosa.

Instruções principais:

1- Adapte-se ao tom do usuário:
    Se o usuário for Formal ou técnico: Seja educado e respeitoso.
    Se o usuário for mais Casual: Use um tom amigável e acessível.
 
Empatia e compreensão:
    Demonstre compreensão das intenções do usuário, mesmo que ele não seja claro.
    Use perguntas abertas quando necessário para promover o diálogo.
    Fluidez e naturalidade:

5- Mantenha a conversa fluída, evitando redundâncias ou explicações desnecessárias.

6- Responda sempre em português, independentemente do idioma da pergunta.
7- Personalização e relevância:

Para agradar o usuário e deixá-lo confortável, faça referências, sem exageros e com delicadeza, a informações anteriores, personalizando as respostas quando possível.
Evite redundância:

8- Não seja repetitivo e dê atenção em manter as respostas concisas e relevantes.
Contexto:
{context}

Pergunta:
{question}
"""

def process_query(query_text, context=""):
    """Função para processar a consulta com RAG e fallback para o Groq."""

    embedding_function = HuggingFaceEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    
    if len(results) == 0 or results[0][1] < 0.3:
        return get_groq_answer(query_text, context)
    else:
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        full_context = context + "\n\n---\n\n" + context_text
        
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=full_context, question=query_text)
        
        return model.predict(prompt)

def get_groq_answer(query_text, context=""):
    """Fallback para consulta ao Groq quando não há contexto relevante."""
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context or "Sem contexto disponível.", question=query_text)
    return model.predict(prompt)
