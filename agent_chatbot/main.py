import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from agent_chatbot.graph import create_graph
from agent_chatbot.agent import research_agent
from agent_chatbot.tools import python_repl

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

message_history = [] 
user_preferences = {}  


graph = create_graph(research_agent)

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
    elif "tom mais informal" in input_message.lower():
        user_preferences["tone"] = "informal"
        message_history.append(AIMessage(content="Entendido! A partir de agora, usarei um tom mais informal."))
    elif "verdadeiro" in input_message.lower():
        user_preferences["verified_data"] = input_message
        message_history.append(AIMessage(content="Obrigado por confirmar a informação. Vamos continuar."))


    state = {"messages": message_history}
    final_state = graph.invoke(state)


    if "messages" in final_state and len(final_state["messages"]) > 1:
        response = final_state["messages"][-1].content
    else:
        response = "Não consegui processar sua solicitação. Pode fornecer mais informações?"

    message_history.append(AIMessage(content=response))

    return response
