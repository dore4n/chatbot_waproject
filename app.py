import streamlit as st
from agent_chatbot.agent import process_query
from streamlit_chat import message

def main():
    st.set_page_config(page_title="Chat Interativo", page_icon=":speech_balloon:")

    st.title("Chatbot WaProject")

    # Inicializa o estado da sessão para armazenar mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Campo de entrada para a pergunta do usuário
    query_text = st.text_input("Digite sua pergunta:", placeholder="Exemplo: Me ajude a pesquisar sobre tecnologias de IA.")

    if query_text:
        with st.spinner("Digitando..."):
            # Adiciona a mensagem do usuário no histórico
            st.session_state.messages.append({"sender": "user", "content": query_text})

            # Chama a função process_query para obter a resposta do chatbot
            response = process_query(query_text)

            # Adiciona a resposta do chatbot no histórico
            st.session_state.messages.append({"sender": "agent", "content": response})

    # Exibição do histórico de mensagens
            for i, msg in enumerate(reversed(st.session_state.messages)):
                if msg["sender"] == "user":
                    message(msg["content"], is_user=True, key=str(i) + "_user")
                else:
                    message(msg["content"], is_user=False, key=str(i) + "_bot")

    else:
        st.warning("Por favor, digite uma pergunta válida.")

if __name__ == "__main__":
    main()
