from dotenv import load_dotenv
from langchain.agents import Tool
from langchain_openai import OpenAIEmbeddings
import logging
import os

from services.agent_service import AgentService
from services.document_service import DocumentService
from services.faiss_service import FAISSService
from services.interaction_history_service import InteractionHistoryService
from services.llm_service import LLMService
from utils.document_responder import document_responder_function

# --- Configuração de logging ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('error_log.txt')
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# --- Carregar variáveis de ambiente ---
load_dotenv()

# --- Constantes e Configurações ---
FILE_PATH = 'data/artigo.txt'


def main():
    # Carregar chaves
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logger.error(
            "OPENAI_API_KEY não foi encontrada. Verifique o arquivo .env.")
        return

    # Carregar documentos
    try:
        documents = DocumentService.load_documents(FILE_PATH)
    except Exception as e:
        logger.error(f"Erro ao carregar documentos: {e}")
        return

    # Criar embeddings e índice FAISS
    logger.info("Criando embeddings e índice FAISS, por favor aguarde...")
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    faiss_service = FAISSService(embeddings)
    faiss_service.create_index(documents)

    # Inicializar modelo LLM
    llm_service = LLMService(openai_api_key)

    # Ferramentas para o agente
    document_responder_tool = Tool(
        name="DocumentResponder",
        func=document_responder_function,
        description="Esta ferramenta responde perguntas usando documentos carregados."
    )
    tools = [document_responder_tool]

    # Criar agente
    agent_service = AgentService(llm_service.llm, tools)

    # Inicializar o serviço de histórico de interações
    session_id = os.urandom(16).hex()  # Gerar um ID de sessão único
    interaction_history_service = InteractionHistoryService(
        max_interactions=10)

    # Instrução para uso do agente
    print("Bem-vindo ao sistema de perguntas! Você pode fazer uma pergunta baseada nos documentos.")
    print("Digite 'sair' para encerrar o programa.")

    # Loop para perguntas e respostas
    while True:
        query = input(
            "Faça sua pergunta (ou digite 'sair' para encerrar): ").strip().lower()
        if query == 'sair':
            logger.info("Encerrando o programa.")
            break

        docs = faiss_service.search(query, k=5)
        if not docs:
            print("Nenhum documento relevante encontrado.")
            continue
        
         # Adicionar a interação do usuário ao histórico
        interaction_history_service.add_interaction(
            session_id, f"Usuário: {query}")

        # Concatenar o histórico de interações e os documentos encontrados
        context = "\n".join([doc.page_content for doc in docs]) + "\n"
        context += "\n".join(interaction_history_service.get_history(session_id))

        # Obter a resposta do agente
        response = agent_service.get_response(query, context)

        # Adicionar a resposta do agente ao histórico
        interaction_history_service.add_interaction(
            session_id, f"Agente: {response.get('output', 'Sem resposta disponível no momento.')}")

        print("Resposta do Agente:\n")
        print(response.get('output', 'Sem resposta disponível no momento.'))


if __name__ == "__main__":
    main()
