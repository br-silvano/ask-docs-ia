# AskDocs

O **AskDocs** é uma aplicação que utiliza o poder de LLMs (Modelos de Linguagem Grandes) e agentes inteligentes para responder perguntas com base em documentos carregados. Este projeto inclui um sistema de agente REACT, indexação de documentos utilizando FAISS, e integração com OpenAI para criar respostas contextuais.

## Estrutura do Projeto

O projeto é composto por vários serviços modulares que se comunicam entre si para oferecer uma experiência completa de perguntas e respostas. Abaixo está uma breve explicação de cada arquivo:

### `agent_service.py`
Este arquivo contém o `AgentService`, que configura e gerencia um agente REACT utilizando ferramentas e um modelo de linguagem. Ele usa `ThreadPoolExecutor` para aplicar limites de tempo nas execuções das consultas, assegurando que o agente responda dentro do prazo estabelecido.

### `document_service.py`
Este serviço carrega documentos a partir de um caminho especificado. O carregamento é feito com um timeout usando `ThreadPoolExecutor` para evitar travamentos se o arquivo for muito grande ou demorar muito para ser lido.

### `faiss_service.py`
O serviço FAISS é responsável por criar um índice FAISS para permitir buscas eficientes de similaridade nos documentos carregados. Ele também implementa um timeout para a criação do índice e para as pesquisas de similaridade.

### `interaction_history_service.py`
Gerencia o histórico de interações entre o usuário e o sistema, garantindo que um número máximo de interações seja mantido, removendo as mais antigas quando necessário.

### `llm_service.py`
Gerencia a inicialização do modelo de linguagem (LLM) da OpenAI. O serviço utiliza `ThreadPoolExecutor` para garantir que o modelo seja carregado com um timeout definido.

### `document_responder.py`
Função simples que simula uma resposta baseada em documentos.

### `app.py`
Arquivo principal que orquestra o carregamento de documentos, criação de embeddings, indexação FAISS, criação de agentes e interação com o usuário.

## Como executar o projeto

### Pré-requisitos

- Python 3.9 ou superior
- Instalar as dependências utilizando o `pip`:
  ```bash
  pip install -r requirements.txt
  ```

### Configuração de ambiente

Antes de executar o projeto, crie um arquivo `.env` na raiz do projeto e adicione a chave da API da OpenAI:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Execução

Após configurar as dependências e variáveis de ambiente, você pode executar o sistema com o seguinte comando:

```bash
python app.py
```

#### Exemplo de pergunta
```shell
Faça sua pergunta (ou digite 'sair' para encerrar): O que é Dify.AI?
```

### Funcionalidades

- **Agente REACT**: Responde perguntas utilizando informações de documentos carregados.
- **Carregamento de Documentos**: Carrega documentos de texto para busca de informações relevantes.
- **Indexação FAISS**: Indexa os documentos para facilitar buscas de similaridade.
- **Histórico de Interações**: Mantém o histórico das interações do usuário com o sistema, oferecendo uma experiência contextualizada.

### Timeout

Para evitar travamentos ou demoras excessivas, os seguintes tempos limites foram configurados:
- **Agente REACT**: 10 segundos
- **Carregamento de Documentos**: 10 segundos
- **Criação de Índice FAISS**: 10 segundos
- **Busca FAISS**: 10 segundos

## Contribuição

Este projeto está em desenvolvimento contínuo, e contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença

Este projeto é licenciado sob os termos da [MIT License](LICENSE).
