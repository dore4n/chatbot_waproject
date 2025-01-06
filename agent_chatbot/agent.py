import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from agent_chatbot.chroma_config import load_or_create_chroma, add_message_to_chroma
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
message_history = []
user_preferences = {}


vectorstore = load_or_create_chroma(persist_directory="./chroma")


llm_generic = ChatGroq(
    model="llama-3.2-90b-vision-preview",
    temperature=0,
    max_tokens=500,
    timeout=None,
    max_retries=2
)

def load_history_from_chroma(vectorstore):
    """
    Carrega o histórico de mensagens do ChromaDB.
    Retorna o histórico completo, se solicitado.
    """
    try:
        results = vectorstore._collection.get()
        history = []

        if "documents" in results: 
            for result in results["documents"]:
                if isinstance(result, dict) and "text" in result:
                    history.append(result["text"])
                else:
                    history.append(str(result))
        else:
            logging.warning("A chave 'documents' não foi encontrada em 'results'.")

        logging.info(f"Histórico de mensagens carregado: {len(history)} mensagens")
        return history 
    except Exception as e:
        logging.error(f"Erro ao carregar histórico de mensagens: {e}")
        return []

def manage_message_history(input_message: str) -> None:
    """
    Gerencia o histórico de mensagens, adicionando a mensagem do usuário
    ao histórico e garantindo que o limite de 10 mensagens não seja ultrapassado.
    """
    global message_history

    message_history.append(HumanMessage(content=input_message))


    if len(message_history) > 10:
        message_history = message_history[-10:]

    logging.info(f"Histórico de mensagens atualizado: {len(message_history)} mensagens")

research_agent = create_react_agent(
    llm_generic,
    tools=[],  
    state_modifier="""
        Você é especializado em fornecer respostas com base no histórico de mensagens.
    """
)

def execute_agent(input_message: str) -> str:
    global message_history, user_preferences

    vectorstore = load_or_create_chroma(persist_directory="./chroma")
    loaded_history = load_history_from_chroma(vectorstore)


    for past_message in loaded_history:
        message_history.append(AIMessage(content=past_message))


    manage_message_history(input_message)


    if "tom mais formal" in input_message.lower():
        user_preferences["tone"] = "formal"
        message_history.append(AIMessage(content="Entendido! A partir de agora, usarei um tom mais formal."))
        return "Entendido! A partir de agora, usarei um tom mais formal."
    elif "tom mais informal" in input_message.lower():
        user_preferences["tone"] = "informal"
        message_history.append(AIMessage(content="Entendido! A partir de agora, usarei um tom mais informal."))
        return "Entendido! A partir de agora, usarei um tom mais informal."


    response = research_agent.invoke({"messages": message_history})


    if "messages" in response and len(response["messages"]) > 0:
        response_content = response["messages"][-1].content
    else:
        response_content = "Não consegui processar sua solicitação. Pode fornecer mais informações?"


    if response_content == message_history[-1].content:
        response_content = "Parece que você está perguntando sobre algo que já discutimos. Vamos tentar algo novo!"


    message_history.append(AIMessage(content=response_content))

    add_message_to_chroma(input_message, vectorstore)

    logging.info(f"Histórico de mensagens atualizado: {len(message_history)} mensagens")
    return response_content