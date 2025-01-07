import streamlit as st
from agent_chatbot.agent import process_query
from streamlit_chat import message

def main():
    st.set_page_config(page_title="Chat Interativo", page_icon=":speech_balloon:")

    st.title("Chatbot WaProject")

    if "messages" not in st.session_state:
        st.session_state.messages = []


    query_text = st.text_input("Digite sua pergunta:", placeholder="Exemplo: Me ajude a pesquisar sobre tecnologias de IA.")

    if query_text:
        with st.spinner("Digitando..."):

            st.session_state.messages.append({"sender": "user", "content": query_text})

            context = "\n".join(
                f"{msg['sender'].capitalize()}: {msg['content']}"
                for msg in st.session_state.messages[:-1] 
            )

            response = process_query(query_text, context)

            st.session_state.messages.append({"sender": "agent", "content": response})

            for i, msg in enumerate(reversed(st.session_state.messages)):
                if msg["sender"] == "user":
                    message(msg["content"], is_user=True, key=str(i) + "_user")
                else:
                    message(msg["content"], is_user=False, key=str(i) + "_bot")


if __name__ == "__main__":
    main()
