from typing import List
from dotenv import load_dotenv

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.llm import LLM
from crewai.project import CrewBase, agent, crew, task

from marketing_digital.tools.custom_tool import SQLQueryTool, SQLSchemaTool

load_dotenv()


@CrewBase
class MarketingCrew:
    """Crew de marketing digital para análise de dados de funil, copy persuasiva,

    direção visual e planejamento estratégico de tráfego pago.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Modelos LLM configurados para cada perfil de agente
    llm_estrategista = LLM(
        model="ollama/qwen3:8b",
        base_url="http://localhost:11434",
        temperature=0.2,
    )
    llm_copywriter = LLM(
        model="ollama/mistral",
        base_url="http://localhost:11434",
        temperature=0.7,
    )
    llm_designer = LLM(
        model="ollama/qwen3:8b",
        base_url="http://localhost:11434",
        temperature=0.5,
    )
    llm_media_buyer = LLM(
        model="gemini/gemini-2.5-flash",
        temperature=0.1,
    )

    # Ferramentas SQL para consulta e inspeção de schema do e-commerce
    sql_query_tool = SQLQueryTool()
    sql_schema_tool = SQLSchemaTool()

    # Agentes

    @agent
    def strategy_analyst(self) -> Agent:
        """Cria o agente analista de estratégia e dados de funil."""
        return Agent(
            config=self.agents_config["strategy_analyst"],  # type: ignore[index]
            llm=self.llm_estrategista,
            tools=[self.sql_schema_tool, self.sql_query_tool],
            verbose=True,
        )

    @agent
    def copywriter(self) -> Agent:
        """Cria o agente copywriter e redator de resposta direta."""
        return Agent(
            config=self.agents_config["copywriter"],  # type: ignore[index]
            llm=self.llm_copywriter,
            verbose=True,
        )

    @agent
    def visual_designer(self) -> Agent:
        """Cria o agente diretor de arte e designer de experiência visual."""
        return Agent(
            config=self.agents_config["visual_designer"],  # type: ignore[index]
            llm=self.llm_designer,
            verbose=True,
        )

    @agent
    def media_buyer(self) -> Agent:
        """Cria o agente gestor de tráfego pago e aquisição de mídia."""
        return Agent(
            config=self.agents_config["media_buyer"],  # type: ignore[index]
            llm=self.llm_media_buyer,
            verbose=True,
        )

    # Tasks

    @task
    def analise_estrategica_funil(self) -> Task:
        """Define a tarefa de diagnóstico e análise de dados do funil."""
        return Task(
            config=self.tasks_config["analise_estrategica_funil"],  # type: ignore[index]
            output_file="resultados_tasks/1analise_estrategica_funil.md",
        )

    @task
    def criacao_copy_persuasiva(self) -> Task:
        """Define a tarefa de redação de copy e roteiros persuasivos."""
        return Task(
            config=self.tasks_config["criacao_copy_persuasiva"],  # type: ignore[index]
            output_file="resultados_tasks/2criacao_copy_persuasiva.md",
        )

    @task
    def direcao_visual_criativos(self) -> Task:
        """Define a tarefa de direção visual e layout de criativos."""
        return Task(
            config=self.tasks_config["direcao_visual_criativos"],  # type: ignore[index]
            output_file="resultados_tasks/3direcao_visual_criativos.md",
        )

    @task
    def planejamento_campanha_trafego(self) -> Task:
        """Define a tarefa de planejamento de mídia paga e orçamento."""
        return Task(
            config=self.tasks_config["planejamento_campanha_trafego"],  # type: ignore[index]
            output_file="resultados_tasks/4planejamento_campanha_trafego.md",
        )

    # Crew

    @crew
    def crew(self) -> Crew:
        """Compõe a equipe sequencial de agentes de marketing digital."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


