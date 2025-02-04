---

# **Documentação do Projeto Chatbot Waproject**

## **Resumo**
O projeto **Chatbot Waproject** é um chatbot interativo e educacional, utilizando tecnologias como LangChain, LangGraph, ChromaDB, e Streamlit. O agente é especializado em responder perguntas sobre o livro "O Pequeno Príncipe", utilizando um mecanismo de Recuperação de Dados por Busca (RAG). Ele pode realizar buscas no banco de dados ChromaDB, analisar o contexto e fornecer respostas relevantes com base nas mensagens anteriores.

<img src="/public/readme/home-conversas-pequeno.png">
<img src="/public/readme/home-conversas-pequeno-iniciada.png">

---

## **Índice**
1. [Pré-requisitos](#pré-requisitos)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Como Executar](#como-executar)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Principais Dependências](#principais-dependências)
6. [Uso](#uso)
7. [Debugging e Logs](#debugging-e-logs)
8. [Contribuições](#contribuições)
9. [Licença](#licença)

---

## **Pré-requisitos**
Certifique-se de ter as seguintes ferramentas instaladas antes de configurar o projeto:
- **Python 3.10+**
- **Docker** e **Docker Compose**
- **Git**

---

## **Configuração do Ambiente**

1. Clone o repositório:
   ```bash
   git clone <https://github.com/dore4n/chatbot_waproject.git>
   cd chatbot_waproject
   ```

2. Configure o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   GROQ_API_KEY=<sua_api_key>
   HUGGING_FACE_API_KEY=<sua_api_key>
   ```

---

## **Como Executar**

### **Usando o Docker**
1. Construa e inicie os contêineres:
   ```bash
   docker-compose up --build
   ```

2. Acesse o Streamlit no navegador em:
   ```
   http://localhost:8501
   ```

### **Sem Docker**
1. Execute o Streamlit diretamente:
   ```bash
   streamlit run app.py
   ```

2. O chatbot estará disponível na interface do Streamlit.

---

## **Estrutura do Projeto**

### **Raiz do Projeto**
- `langgraph.json`: Configurações e definições do LangGraph para roteamento do agente.
- `dockerfile`: Configuração para criar a imagem Docker.
- `docker-compose.yml`: Orquestração dos contêineres Docker.
- `app.py`: Arquivo principal do Streamlit para interface do usuário.
- `.env.example`: Exemplo de como você vai criar seu .env com variáveis de ambiente sensíveis.
- `requirements.txt`: Lista de dependências.

### **Diretório `agent_chatbot/`**
- `agent.py`: Implementação principal do agente e integração com LangGraph.
- `graph.py`: Configuração e manipulação do grafo do LangGraph.

---

## **Principais Dependências**
- **LangChain**: Framework para construção de agentes LLM.
- **LangGraph**: Integração com gráficos para roteamento dinâmico.
- **ChromaDB**: Banco de dados vetorial para armazenamento e recuperação.
- **Streamlit**: Interface gráfica interativa.
- **Hugging Face**: Para embeddings vetoriais.

Veja a lista completa de dependências em `requirements.txt`.

---

## **Uso**

### **Interação com o Agente**
1. Acesse o Streamlit:
   ```
   http://localhost:8501
   ```
2. Interaja com o chatbot enviando mensagens sobre "O Pequeno Príncipe". O agente responderá com base no contexto do livro e nas interações anteriores.

### **Adicionar Novos Dados ao Chroma (Caso Necessário)**
Se você precisar adicionar novos chunks ao banco de dados Chroma (por exemplo, para atualizar o conteúdo com mais informações ou incluir novos tópicos), será necessário rodar o script chroma_config.py para gerar novamente o banco de dados com os novos dados.

 1. Rodar o chroma_config.py para adicionar novos chunks:

  Caso deseje atualizar o Chroma com novos dados, execute o script chroma_config.py, que irá processar os novos chunks e atualizar o banco de dados:

```bash
python agent_chatbot/chroma_config.py
```
 2. Rodar o Streamlit novamente:

Após rodar o chroma_config.py e atualizar o banco de dados Chroma, execute novamente o Streamlit:

```bash
streamlit run app.py
```
O chatbot agora estará usando o banco de dados atualizado, pronto para interagir com os novos dados.

---

## **Debugging e Logs**
### **Logs**
Os logs são gerados automaticamente e exibidos no terminal. Para maior detalhamento, ative o modo `DEBUG`:
```bash
export DEBUG=true
streamlit run app.py
```

### **Problemas Comuns**
- **Erro no Docker Compose**:
  - Verifique o arquivo `requirements.txt`.
  - Confirme se as variáveis no `.env` estão configuradas corretamente.
- **Respostas vazias do chatbot**:
  - Certifique-se de que o ChromaDB está ativo e funcional.

---

## **Contribuições**
1. Faça um fork do projeto.
2. Crie uma branch para suas alterações:
   ```bash
   git checkout -b minha-nova-feature
   ```
3. Envie suas alterações e crie um Pull Request.

---

## **Licença**
Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---
