# Análise de Sentimento Omnicanal com IA (Google Gemini)

Este projeto é uma pipeline de **Engenharia de Prompt** que utiliza a API do Google Gemini para simular e analisar o atendimento ao cliente (CX).

O sistema opera com dois Agentes de IA autônomos:
1.  **Agente Gerador:** Cria dados sintéticos de clientes fictícios (reclamações, elogios, dúvidas) simulando canais como WhatsApp, Email e Instagram.
2.  **Agente Analista:** Processa as mensagens, classificando sentimento, emoção, urgência e gerando resumos automáticos.

## Tecnologias Utilizadas
- **Python** (Linguagem principal)
- **Google Gemini 1.5 Flash** (LLM para geração e análise)
- **Pandas** (Manipulação e exportação de dados)

## Funcionalidades
- [x] Geração automática de cenários de teste (Fake Data).
- [x] Análise de sentimento (Positivo, Negativo, Neutro).
- [x] Detecção de emoção e categorização de urgência.
- [x] Exportação dos resultados para CSV estruturado.

## Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/anderpenagos/analise-sentimento-gemini.git
cd analise-sentimento-gemini
```
### 2. Crie um ambiente virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```
### 3. Instale as dependências
```bash
pip install -r requirements.txt
```
### 4. Configure a API Key
Este projeto precisa de uma chave de API do Google Gemini.
1. Crie um arquivo chamado .env na raiz do projeto.
2. Adicione sua chave neste formato:
```Env
pip install -r requirements.txt
```
### 5. Execute o script
```bash
python app.py
```
### Exemplo de Saída (CSV)

O script gera um arquivo resultados_gerados_ia.csv com colunas como:

Canal	Sentimento	Emoção	Urgência	Resumo
WhatsApp	Negativo	Raiva	Alta	Cliente com geladeira vazando água.
Email	Positivo	Gratidão	Baixa	Elogio ao atendimento técnico rápido.

Desenvolvido por Anderson Penagos