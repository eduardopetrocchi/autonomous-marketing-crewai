"""Testes unitários e de integração estrutural para a MarketingCrew."""

import unittest
from marketing_digital.crew import MarketingCrew


class TestMarketingCrew(unittest.TestCase):
    """Bateria de testes de integridade estrutural da Crew de Marketing."""

    def setUp(self):
        """Instancia a MarketingCrew antes de cada teste."""
        self.marketing_crew = MarketingCrew()

    def test_crew_initialization(self):
        """Valida se a classe MarketingCrew pode ser instanciada corretamente."""
        self.assertIsNotNone(self.marketing_crew)

    def test_agents_defined(self):
        """Garante que todos os agentes esperados estão configurados."""
        agent_names = ["strategy_analyst", "copywriter", "visual_designer", "media_buyer"]
        for agent_name in agent_names:
            agent_method = getattr(self.marketing_crew, agent_name, None)
            self.assertTrue(callable(agent_method), f"Agente '{agent_name}' não encontrado.")

    def test_tasks_defined(self):
        """Garante que todas as tasks esperadas estão configuradas."""
        task_names = [
            "analise_estrategica_funil",
            "criacao_copy_persuasiva",
            "direcao_visual_criativos",
            "planejamento_campanha_trafego",
        ]
        for task_name in task_names:
            task_method = getattr(self.marketing_crew, task_name, None)
            self.assertTrue(callable(task_method), f"Tarefa '{task_name}' não encontrada.")

    def test_crew_assembly(self):
        """Valida se a equipe (Crew) é montada com 4 agentes e 4 tarefas."""
        crew_instance = self.marketing_crew.crew()
        self.assertEqual(len(crew_instance.agents), 4)
        self.assertEqual(len(crew_instance.tasks), 4)


if __name__ == "__main__":
    unittest.main()
