#!/usr/bin/env python
import sys
import warnings

from marketing_digital.crew import MarketingCrew

warnings.filterwarnings("ignore", category=SyntaxWarning)


def get_inputs() -> dict:
    """Retorna os parâmetros e variáveis de contexto injetados nos templates

    de agentes e tarefas (agents.yaml e tasks.yaml).
    """
    return {
        "produto_ou_servico": "KnitCraft Studio",
        "nicho_ou_mercado": "Vestuário",
        "objetivo_campanha": "Gerar leads qualificados para o funil de vendas",
        "periodo_analise": "últimos 30 dias",
    }


def run():
    """Inicia a execução sequencial completa da MarketingCrew com os inputs definidos."""
    inputs = get_inputs()
    resultado = MarketingCrew().crew().kickoff(inputs=inputs)
    print("\n\n=== RESULTADO FINAL ===\n")
    print(resultado.raw)


def train():
    """Treina os agentes da crew por N iterações para calibração.

    Uso:
        python main.py train <n_iteracoes> <arquivo_saida>
    """
    if len(sys.argv) < 4:
        print("Uso correto: python main.py train <n_iteracoes> <arquivo_saida>")
        sys.exit(1)

    inputs = get_inputs()
    try:
        MarketingCrew().crew().train(
            n_iterations=int(sys.argv[2]),
            filename=sys.argv[3],
            inputs=inputs,
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao treinar a crew: {e}") from e


def replay():
    """Reexecuta a crew a partir de uma tarefa específica informada pelo task_id.

    Uso:
        python main.py replay <task_id>
    """
    if len(sys.argv) < 3:
        print("Uso correto: python main.py replay <task_id>")
        sys.exit(1)

    try:
        MarketingCrew().crew().replay(task_id=sys.argv[2])
    except Exception as e:
        raise RuntimeError(f"Erro ao repetir a execução da crew: {e}") from e


def test():
    """Executa a bateria de testes avaliando a qualidade dos outputs da crew.

    Uso:
        python main.py test <n_iteracoes> <modelo_eval>
    """
    if len(sys.argv) < 4:
        print("Uso correto: python main.py test <n_iteracoes> <modelo_eval>")
        sys.exit(1)

    inputs = get_inputs()
    try:
        MarketingCrew().crew().test(
            n_iterations=int(sys.argv[2]),
            openai_model_name=sys.argv[3],
            inputs=inputs,
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao testar a crew: {e}") from e


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else "run"

    comandos = {
        "run": run,
        "train": train,
        "replay": replay,
        "test": test,
    }

    if comando not in comandos:
        print(f"Comando desconhecido: '{comando}'")
        print("Comandos disponíveis: python main.py [run | train | replay | test]")
        sys.exit(1)

    comandos[comando]()
