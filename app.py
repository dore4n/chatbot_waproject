import streamlit as st
from agent_chatbot.main import execute_agent
from streamlit_chat import message

def main():
    st.set_page_config(page_title='Chat Interativo', page_icon=':speech_balloon:')

    st.title("Agente Interativo com LangChain")


    if "messages" not in st.session_state:
        st.session_state.messages = []


    user_input = st.text_input("Digite sua pergunta:", placeholder="Exemplo: Me ajude a pesquisar sobre tecnologias de IA.")


    if user_input:
        with st.spinner("Processando..."):

            st.session_state.messages.append({"sender": "user", "content": user_input})


            response = execute_agent(user_input)
            

            st.session_state.messages.append({"sender": "agent", "content": response})
            

            for i, msg in enumerate(reversed(st.session_state.messages)):
                if msg["sender"] == "user":
                    message(msg["content"], is_user=True, key=str(i) + "_user")
                else:
                    message(msg["content"], is_user=False, key=str(i) + "_bot")
            
    else:
        st.warning("Por favor, digite uma pergunta válida.")

if __name__ == "__main__":
    main()
