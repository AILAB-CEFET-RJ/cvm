import re

def extrair_artigos_de_resolucao(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        texto = f.read()

    # Expressão regular para capturar os artigos (ex: Art. 1º)
    padrao_artigos = re.finditer(r'(Art\. ?\d+º.*?)((?=Art\. ?\d+º)|\Z)', texto, re.DOTALL)

    artigos = {}
    for match in padrao_artigos:
        cabecalho = match.group(1)
        corpo = match.group(2)
        
        # Extrai o número do artigo para ser a chave
        numero_artigo = re.search(r'Art\. ?(\d+)º', cabecalho)
        if numero_artigo:
            chave = int(numero_artigo.group(1))
            artigos[chave] = (cabecalho + corpo).strip()

    return artigos

if __name__ == "__main__": 
    arquivo = "resol175consolid.md"
    artigos = extrair_artigos_de_resolucao(arquivo)

    # salva o resultado em um arquivo CSV com duas colunas: artigo e texto
    with open("artigos_extracao.csv", "w", encoding="utf-8") as f:
        f.write("Artigo,Texto\n")
        for k, v in artigos.items():
            f.write(f"{k},\"{v}\"\n")

    # Exemplo: imprimir os cinco primeiros artigos
    for k in sorted(artigos.keys())[:5]:
        print(f"Artigo {k}:\n{artigos[k][:500]}...\n")
