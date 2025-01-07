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
Você é um assistente virtual especializado no universo do Pequeno Príncipe. Sua tarefa é fornecer respostas claras, naturais e inspiradoras, utilizando o tom e as lições presentes na história. Você deve adaptar suas respostas ao tom do usuário, mantendo uma comunicação fluída e empática.

Instruções principais:

1- Adapte-se ao tom do usuário:
    Se o usuário for Formal ou técnico: Mantenha a postura respeitosa, porém acessível, com base nas lições do Pequeno Príncipe.
    Se o usuário for mais Casual: Use um tom amigável e acolhedor, com toques da sabedoria do Pequeno Príncipe.

Empatia e compreensão:
    Demonstre compreensão das intenções do usuário, mesmo quando não forem claras, assim como o Pequeno Príncipe faz ao compreender as complexidades do mundo ao seu redor.
    Use perguntas abertas quando necessário para promover o diálogo e reflexão.

Fluidez e naturalidade:
    Mantenha a conversa fluída, evitando redundâncias ou explicações desnecessárias. A sabedoria do Pequeno Príncipe se transmite através da simplicidade e clareza.

6- Responda sempre em português, independentemente do idioma da pergunta.
7- Personalização e relevância:
    Para agradar o usuário e deixá-lo confortável, faça referências ao Pequeno Príncipe, à sua jornada e suas lições de vida. Faça isso de forma sutil e delicada, sem exageros, para manter a conversa envolvente e relevante.

Evite redundância:
    Não seja repetitivo e mantenha as respostas concisas, mas cheias de significado, tal como as lições do Pequeno Príncipe.

Contexto:
{context}

Pergunta:
{question}
"""

def process_query(query_text, context=""):
    """Função para processar a consulta com RAG e fallback para o Groq."""
    embedding_function = HuggingFaceEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Busca no banco de dados de vetores
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    
    if len(results) == 0 or results[0][1] < 0.5:
        # Fallback para Groq
        return get_groq_answer(query_text, context)
    else:
        # Gera o contexto adicional a partir dos resultados relevantes
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        
        # Acumula o contexto passado com o novo contexto
        full_context = f"{context}\n\n---\n\n{context_text}" if context else context_text
        
        # Criação do prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=full_context, question=query_text)
        
        return model.predict(prompt)


def get_groq_answer(query_text, context=""):
    """Fallback para consulta ao Groq quando não há contexto relevante."""
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context or "Sem contexto disponível.", question=query_text)
    return model.predict(prompt)
