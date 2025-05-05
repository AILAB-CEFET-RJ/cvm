import re
from typing import List, Dict
import spacy

nlp = spacy.load("pt_core_news_sm")

# Exemplo de trecho de texto legal (poderia vir de um PDF)
texto = """
Deliberação sobre demonstrações contábeis: A assembleia especial de cotistas deve deliberar sobre as demonstrações contábeis da classe de cotas, e a assembleia geral de cotistas deve deliberar sobre as demonstrações contábeis do fundo, no prazo de até 60 dias após o encaminhamento das demonstrações contábeis à CVM, contendo relatório do auditor independente.

V – salvo na hipótese de iliquidez excepcional de que trata o art. 44, é devida ao cotista uma multa de 0,5% (meio por cento) do valor de resgate, a ser paga pelo administrador, por dia de atraso no pagamento do resgate de cotas.

§ 1º Caso a classe de cotas seja exclusivamente destinada a investidores qualificados, os limites previstos no art. 45, §§ 1º e 2º; ficam majorados para, respectivamente, até 60% (sessenta por cento) e até 40% (quarenta por cento), preservado o requisito de existência de formador de mercado para as cotas que excederem ao limite ordinário.
"""

# Expressões regulares para capturar padrões
regex_percent = r"\d+(,\d+)?\s*%|\(.*?por cento\)"
regex_dias = r"\d+\s*dias"
regex_multa = r"\d+(,\d+)?%\s+do valor de resgate"

# Função para extrair frases com contexto

def extrair_valores_com_contexto(texto: str) -> List[Dict[str, str]]:
    resultados = []
    doc = nlp(texto)
    for sent in doc.sents:
        frase = sent.text.strip()
        valores = []
        valores += re.findall(regex_percent, frase)
        valores += re.findall(regex_dias, frase)
        valores += re.findall(regex_multa, frase)
        if valores:
            resultados.append({
                "frase": frase,
                "valores_detectados": valores
            })
    return resultados

# Teste do protótipo
if __name__ == "__main__":
    extracoes = extrair_valores_com_contexto(texto)
    for i, item in enumerate(extracoes):
        print(f"[Regra {i+1}]")
        print("Frase:", item['frase'])
        print("Valores detectados:", item['valores_detectados'])
        print("---")
