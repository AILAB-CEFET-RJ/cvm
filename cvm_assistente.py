from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from sqlalchemy import create_engine, text
import os
import json
import pandas as pd

# --- Configurações iniciais ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # ou defina diretamente
DATABASE_URL = "postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco"

# Inicializar conexão com o banco
engine = create_engine(DATABASE_URL)

# Inicializar modelo LLM
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

# --- TOOL: Validar Percentual de Representação ---
def validar_percentual_representacao(percentual_alvo: float, mais_de_cem: bool = True):
    """Consulta o banco para validar se o percentual mínimo de representação está conforme."""
    if mais_de_cem:
        sql = text("""
            SELECT nome_fundo, nome_classe, numero_cotistas, percentual_minimo_representacao
            FROM fundos
            JOIN fundos_cotas ON fundos.id = fundos_cotas.fundo_id
            WHERE numero_cotistas > 100
        """)
    else:
        sql = text("""
            SELECT nome_fundo, nome_classe, numero_cotistas, percentual_minimo_representacao
            FROM fundos
            JOIN fundos_cotas ON fundos.id = fundos_cotas.fundo_id
            WHERE numero_cotistas <= 100
        """)
    with engine.connect() as conn:
        result = conn.execute(sql).fetchall()
    relatorio = []
    for linha in result:
        nome_fundo, nome_classe, numero_cotistas, percentual_atual = linha
        status = "Conforme" if round(percentual_atual, 2) == round(percentual_alvo, 2) else "Divergente"
        relatorio.append({
            "Fundo": nome_fundo,
            "Classe": nome_classe,
            "Cotistas": numero_cotistas,
            "Percentual Atual": percentual_atual,
            "Percentual Esperado": percentual_alvo,
            "Status": status
        })
    return relatorio

# --- Definir as Tools ---
def _parse_and_call_percent_validation(input_text):
    """Função auxiliar para parsear input da Tool."""
    data = json.loads(input_text)
    return validar_percentual_representacao(
        percentual_alvo=data['percentual'],
        mais_de_cem=data['mais_de_cem']
    )

validate_percent_tool = Tool(
    name="validar_percentual_representacao",
    func=lambda input_text: _parse_and_call_percent_validation(input_text),
    description="Use esta ferramenta para validar percentuais mínimos de representação de cotistas. Input: JSON {percentual: float, mais_de_cem: bool}"
)

# --- Inicializar Agente ---
tools = [validate_percent_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    entrada = """
    A eleição de representante dos cotistas pode ser aprovada pela maioria dos cotistas presentes e que representem, no mínimo:
    - 3% do total de cotas emitidas, quando a classe tiver mais de cem cotistas;
    - 5% do total de cotas emitidas, quando a classe tiver até cem cotistas.
    """

    # Extrai e valida a regra de 3% (>100 cotistas)
    resultado_mais_100 = validar_percentual_representacao(percentual_alvo=3.0, mais_de_cem=True)
    # Extrair e validar a regra de 5% (<=100 cotistas)
    resultado_menos_100 = validar_percentual_representacao(percentual_alvo=5.0, mais_de_cem=False)

    # Combina os resultados
    relatorio_completo = resultado_mais_100 + resultado_menos_100

    # Converte para DataFrame para visualizar melhor
    df = pd.DataFrame(relatorio_completo)

    # Exibe o relatório
    print("\n=== RELATÓRIO DE CONFORMIDADE ===")
    print(df.to_string(index=False))

    # Salva o relatório em CSV
    df.to_csv("relatorio_conformidade_cvm.csv", index=False)
