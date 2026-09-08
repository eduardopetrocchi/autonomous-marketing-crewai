from typing import Tuple, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.tools import BaseTool as LangChainBaseTool
from langchain_ollama import ChatOllama


def _build_toolkit(
    db_path: str, llm_model: str, base_url: str
) -> Tuple[SQLDatabase, LangChainBaseTool]:
    """Inicializa a conexão com o banco SQLite via LangChain e instancia

    o toolkit SQL com a ferramenta de inspeção de schema.

    Args:
        db_path: Caminho para o arquivo SQLite do e-commerce.
        llm_model: Nome do modelo para o toolkit do LangChain.
        base_url: URL base da API do Ollama.

    Returns:
        Tupla com a instância de SQLDatabase e a tool LangChain sql_db_schema.
    """
    db = SQLDatabase.from_uri(
        f"sqlite:///{db_path}",
        include_tables=[
            "customers",
            "order_line_items",
            "sku_catalog",
            "inventory_snapshots",
            "orders",
            "website_daily",
            "meta_ads_campaigns",
            "purchase_orders",
            "website_sessions",
        ],
    )

    llm = ChatOllama(model=llm_model, base_url=base_url, temperature=0)

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools_sql = toolkit.get_tools()
    get_schema_tool = next(t for t in tools_sql if t.name == "sql_db_schema")

    return db, get_schema_tool


class SQLQueryInput(BaseModel):
    """Schema de entrada para a tool executar_query_sql."""

    query: str = Field(
        ...,
        description=(
            "Query SQL (SELECT) a ser executada no banco de dados do e-commerce. "
            "Use a tool 'consultar_schema' antes, se precisar saber os nomes "
            "das colunas de uma tabela."
        ),
    )


class SQLQueryTool(BaseTool):
    """Ferramenta que executa consultas SELECT no banco de dados SQLite do e-commerce.

    Garante execução segura bloqueando operações de escrita e retornando
    diagnósticos amigáveis caso ocorram erros de sintaxe ou schema.
    """

    name: str = "executar_query_sql"
    description: str = (
        "Executa uma consulta SQL (somente SELECT) no banco de dados do "
        "e-commerce (tabelas: customers, order_line_items, sku_catalog, "
        "inventory_snapshots, orders, website_daily, meta_ads_campaigns, "
        "purchase_orders, website_sessions). Em caso de erro de sintaxe ou "
        "coluna inexistente, a mensagem retornada indica o problema — "
        "reescreva a query e tente novamente."
    )
    args_schema: Type[BaseModel] = SQLQueryInput

    def __init__(
        self,
        db_path: str = "ecommerce.db",
        llm_model: str = "qwen3:8b",
        base_url: str = "http://localhost:11434",
        **kwargs,
    ):
        """Inicializa a ferramenta de execução SQL conectando ao banco de dados."""
        super().__init__(**kwargs)
        self._db, _ = _build_toolkit(db_path, llm_model, base_url)

    def _run(self, query: str) -> str:
        """Executa a query SELECT informada contra o banco de dados."""
        query_normalizada = query.strip().lower()
        if not query_normalizada.startswith("select"):
            return (
                "Erro: só são permitidas queries SELECT. "
                "Reescreva a consulta usando apenas SELECT."
            )

        resultado = self._db.run_no_throw(query)
        return (
            resultado
            if resultado
            else "Erro: a consulta falhou. Reescreva a query e tente novamente."
        )


class SQLSchemaInput(BaseModel):
    """Schema de entrada para a tool consultar_schema."""

    tabelas: str = Field(
        ...,
        description=(
            "Nome de uma ou mais tabelas separadas por vírgula "
            "(ex: 'orders, order_line_items') para retornar colunas e "
            "tipos de dados."
        ),
    )


class SQLSchemaTool(BaseTool):
    """Ferramenta que retorna o schema (tabelas, colunas e tipos de dados)

    do banco de dados relacional do e-commerce.
    """

    name: str = "consultar_schema"
    description: str = (
        "Retorna o schema (colunas e tipos) das tabelas informadas do "
        "banco de dados do e-commerce. Use antes de montar uma query SQL "
        "para confirmar os nomes exatos das colunas."
    )
    args_schema: Type[BaseModel] = SQLSchemaInput

    def __init__(
        self,
        db_path: str = "ecommerce.db",
        llm_model: str = "qwen3:8b",
        base_url: str = "http://localhost:11434",
        **kwargs,
    ):
        """Inicializa a ferramenta de consulta de schema conectando ao banco."""
        super().__init__(**kwargs)
        _, self._get_schema_tool = _build_toolkit(db_path, llm_model, base_url)

    def _run(self, tabelas: str) -> str:
        """Consulta e retorna a estrutura e colunas das tabelas solicitadas."""
        return self._get_schema_tool.invoke({"table_names": tabelas})
