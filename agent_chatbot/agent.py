import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage
from agent_chatbot.chroma_config import load_or_create_chroma, add_message_to_chroma


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


vectorstore = load_or_create_chroma(persist_directory="./chroma")

search_tool = DuckDuckGoSearchRun(backend='auto')


message_history = []
user_preferences = {}


llm_generic = ChatGroq(
    model="llama-3.2-90b-vision-preview",
    temperature=0,
    max_tokens=500,
    timeout=None,
    max_retries=2
)


research_agent = create_react_agent(
    llm_generic,
    tools=[search_tool],
    state_modifier="""
        Você é especializado em realizar pesquisas detalhadas sobre um tema.
        Sempre procure fornecer respostas completas e detalhadas.
    """
)

def search_in_chroma(query: str, vectorstore, top_k=3) -> list:
    """
    Busca no Chroma as mensagens mais relevantes com base na consulta do usuário.
    Retorna uma lista de resultados.
    """
    results = vectorstore.similarity_search(query, k=top_k)
    return [result['text'] for result in results]

def execute_agent(input_message: str) -> str:
    """
    Executa o grafo do LangGraph com a mensagem fornecida, armazena o histórico
    e adapta-se com base nas interações do usuário.
    """
    global message_history, user_preferences


    message_history.append(HumanMessage(content=input_message))


    if "tom mais formal" in input_message.lower():
        user_preferences["tone"] = "formal"
        message_history.append(AIMessage(content="Entendido! A partir de agora, usarei um tom mais formal."))
        return "Entendido! A partir de agora, usarei um tom mais formal."
    elif "tom mais informal" in input_message.lower():
        user_preferences["tone"] = "informal"
        message_history.append(AIMessage(content="Entendido! A partir de agora, usarei um tom mais informal."))
        return "Entendido! A partir de agora, usarei um tom mais informal."


    chroma_results = search_in_chroma(input_message, vectorstore)
    if chroma_results:

        response = "Encontrei as seguintes informações relevantes no meu histórico:\n"
        response += "\n".join(f"- {result}" for result in chroma_results)
        message_history.append(AIMessage(content=response))
        return response


    search_result = None
    if "como" in input_message.lower():
        search_result = search_tool.run(input_message)
        message_history.append(AIMessage(content=search_result))  
        

        add_message_to_chroma(search_result, vectorstore)


    state = {"messages": message_history}
    final_state = research_agent.invoke(state)


    if "messages" in final_state and len(final_state["messages"]) > 1:
        response = final_state["messages"][-1].content
    else:
        response = "Não consegui processar sua solicitação. Pode fornecer mais informações?"


    message_history.append(AIMessage(content=response))

    add_message_to_chroma(input_message, vectorstore)
    add_message_to_chroma(response, vectorstore)

    return response
