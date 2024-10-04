from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
import logging

# --- Configuração de logging ---
logger = logging.getLogger(__name__)


# --- Constantes e Configurações ---
TIMEOUT_SECONDS = 10  # Defina o tempo limite em segundos


class AgentService:
    def __init__(self, llm, tools):
        self.agent_executor = self.create_agent(llm, tools)

    @staticmethod
    def create_agent(llm, tools):
        template = '''Answer the following questions as best you can, using the context provided:

        Context: {context}

        Please provide a detailed answer.

        {tools}

        Use the following format:

        Question: {input}
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought: {agent_scratchpad}'''

        prompt = PromptTemplate(input_variables=[
                                "input", "tools", "tool_names", "agent_scratchpad"], template=template)
        # Criar o agente com o LLM e as ferramentas
        agent = create_react_agent(llm, tools, prompt)
        logger.info("Agente REACT criado com sucesso.")
        return AgentExecutor(agent=agent, tools=tools)

    def get_response(self, query, context):
        logger.info(f"Processando consulta: {query}")

        # Função interna para executar o agente
        def execute_agent():
            try:
                response = self.agent_executor.invoke({
                    "input": query,
                    "agent_scratchpad": "",
                    "context": context
                })
                return response
            except Exception as e:
                logger.error(f"Erro ao obter resposta do agente: {e}")
                return {"output": "Erro durante o processamento da solicitação."}

        # Usando ThreadPoolExecutor para aplicar o timeout
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(execute_agent)

            try:
                # Aguarda o resultado com o tempo limite definido
                response = future.result(timeout=TIMEOUT_SECONDS)
                return response
            except FuturesTimeoutError:
                logger.error(
                    f"O tempo limite de {TIMEOUT_SECONDS} segundos foi excedido.")
                return {"output": f"Tempo limite excedido. A operação demorou mais de {TIMEOUT_SECONDS} segundos."}
