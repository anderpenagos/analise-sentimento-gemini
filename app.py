import os
import json
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# ------------------------------------------------------------
# 1. Configuração
# ------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(" GEMINI_API_KEY não encontrada no .env")

genai.configure(api_key=API_KEY)

# Configuração para garantir resposta em JSON
generation_config = {
    "response_mime_type": "application/json"
}

# Verifique se o nome do modelo está correto conforme seu teste anterior

model = genai.GenerativeModel("gemini-2.0-flash-lite", generation_config=generation_config)

# ------------------------------------------------------------
# 2. AGENTE 1: Gerador de Dados (Substitui a lista manual)
# ------------------------------------------------------------
def gerar_mensagens_fake(quantidade=6):
    print(f"Agente 1: Criando {quantidade} interações de clientes fictícios...")
    
    prompt = f"""
    Aja como um gerador de dados sintéticos para testes de CRM.
    Crie uma lista JSON com exatamente {quantidade} mensagens de clientes variados.
    
    Requisitos:
    - Varie os canais: WhatsApp, Email, Instagram, ReclameAqui, Telefone.
    - Varie o tom: Clientes furiosos, clientes felizes, dúvidas técnicas, perguntas sobre entrega.
    - Varie os produtos: Eletrônicos, Móveis, Eletrodomésticos.
    
    O formato de cada item deve ser EXATAMENTE:
    {{
        "canal": "Nome do Canal",
        "cliente_id": "ID aleatório (ex: C999)",
        "texto": "A mensagem do cliente aqui"
    }}
    """

    try:
        resposta = model.generate_content(prompt)
        dados = json.loads(resposta.text)
        
        # O Gemini as vezes devolve um dict {"dados": [...]}, as vezes a lista direta [...]
        # Vamos garantir que pegamos a lista
        if isinstance(dados, dict) and "dados" in dados:
            return dados["dados"]
        elif isinstance(dados, list):
            return dados
        else:
            # Tenta achar qualquer lista dentro do json
            for key, value in dados.items():
                if isinstance(value, list):
                    return value
            return []
            
    except Exception as e:
        print(f" Erro no Agente 1: {e}")
        return []

# ------------------------------------------------------------
# 3. AGENTE 2: Analista de Sentimento
# ------------------------------------------------------------
def analisar_texto(texto):
    prompt = f"""
    Você é um especialista em Customer Experience (CX). Analise a mensagem:
    "{texto}"

    Retorne um JSON ÚNICO (não uma lista) com:
    - sentimento (positivo, negativo, neutro)
    - emocao (ex: raiva, gratidão, confusão, ansiedade)
    - tema (ex: defeito, atraso, elogio, dúvida técnica)
    - urgencia (baixa, média, alta)
    - resumo (resumo curto da situação)
    """

    try:
        resposta = model.generate_content(prompt)
        dados = json.loads(resposta.text)

        # CORREÇÃO AQUI: Verifica se o Gemini devolveu uma lista
        if isinstance(dados, list):
            # Se for lista e tiver itens, pega o primeiro
            if len(dados) > 0:
                return dados[0]
            else:
                return None # Lista vazia
        
        return dados # Se já for um dicionário, retorna direto

    except Exception as e:
        print(f"Erro no Agente 2 para o texto '{texto[:20]}...': {e}")
        return None

# ------------------------------------------------------------
# 4. Execução do Fluxo (Pipeline)
# ------------------------------------------------------------

# PASSO A: Gerar os dados
mensagens = gerar_mensagens_fake(6)

if not mensagens:
    print("Falha ao gerar mensagens. Encerrando.")
    exit()

print(f"✔ Dados gerados com sucesso! ({len(mensagens)} mensagens)\n")

# PASSO B: Analisar os dados
resultados = []
print(" Agente 2: Iniciando análise de sentimentos...\n")

for msg in mensagens:
    # Pequeno print para ver o que está acontecendo em tempo real
    print(f"   Processando Cliente {msg.get('cliente_id')} ({msg.get('canal')})...")
    
    analise = analisar_texto(msg.get("texto"))
    
    if analise:
        linha = {
            "canal": msg.get("canal"),
            "cliente_id": msg.get("cliente_id"),
            "texto": msg.get("texto"),
            "sentimento": analise.get("sentimento"),
            "emocao": analise.get("emocao"),
            "tema": analise.get("tema"),
            "urgencia": analise.get("urgencia"),
            "resumo": analise.get("resumo")
        }
        resultados.append(linha)

print("\n✔ Todas as análises concluídas!")

# ------------------------------------------------------------
# 5. Exportar
# ------------------------------------------------------------
if resultados:
    df = pd.DataFrame(resultados)
    nome_arquivo = "resultados_gerados_ia.csv"
    df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
    
    print(f"\n Arquivo salvo: {nome_arquivo}")
    print("\n--- Amostra dos Resultados ---")
    print(df[['canal', 'sentimento', 'urgencia']].head(6)) 
else:
    print("Nenhum resultado gerado.")