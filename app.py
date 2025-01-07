import streamlit as st
from agent_chatbot.agent import process_query
from streamlit_chat import message

def main():
    st.set_page_config(page_title="Conversas sobre o pequeno príncipe", page_icon=":rose:")

    st.title("Conversas sobre o Pequeno Príncipe")
    
    st.markdown("""
    **Bem-vindo ao mundo do Pequeno Príncipe!**

    "Aqui, você pode conversar sobre o Pequeno Príncipe, suas aventuras pelo universo, suas reflexões filosóficas e seus encontros com personagens únicos.
    Pergunte sobre sua amizade com a rosa, suas lições de vida, ou o que ele aprendeu com o aviador no deserto.
    Sinta-se à vontade para conversar sobre outros tópicos, mas a minha expertise é no Pequeno Príncipe!"
    """)

    if "messages" not in st.session_state:
        st.session_state.messages = []


    query_text = st.text_input("O que você gostaria de saber?", placeholder= "Exemplo: O que o Pequeno Príncipe aprendeu sobre a amizade?")

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
