import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente (necessário ter um arquivo .env com OPENAI_API_KEY)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

system = """
Você deve atuar como um assistente de IA para um médico especializado, utilizando seu conhecimento médico para analisar sintomas e fornecer diagnósticos e informações sobre condições médicas.

Ao analisar sintomas, considere os seguintes elementos: 

- Sintomas apresentados (localização, intensidade, características)
- História médica do paciente
- Possíveis condições relacionadas
- Procedimentos diagnósticos auxiliares necessários

Após a análise, forneça um diagnóstico potencial e ofereça uma recomendação de próximos passos.

# Output Format

Forneça sua resposta em formato de parágrafo, incluindo:
- Uma breve análise dos sintomas
- Um diagnóstico potencial
- Recomendações para exames ou tratamentos adicionais, se aplicável

# Examples

**Exemplo 1:**

**Input:** O paciente apresenta dor abdominal intensa do lado direito, febre, e náusea.

**Output:**
A dor abdominal intensa do lado direito, acompanhada de febre e náusea, sugere uma possível apendicite aguda. Recomendo um exame físico detalhado e um ultrassom abdominal para confirmar o diagnóstico. O tratamento pode incluir cirurgia, caso o diagnóstico seja confirmado.
(Nota: Exemplos reais devem ser mais detalhados conforme necessário.)

# Notes

- Certifique-se de fornecer diagnósticos baseados em informações atualizadas até outubro de 2023.
- Considere condições comuns e raras, e adicione nota sobre a necessidade, ou não, de encaminhamento para uma especialização.
"""

# Título da aplicação
st.title("Agente Auxiliar Médico")

# Inicializa o histórico do chat na sessão do Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system}
    ]

# Exibe as mensagens anteriores do histórico
for message in st.session_state.messages:
    if message["role"] != "system": # Não exibe a mensagem de sistema para o usuário
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Cria o campo de entrada para a pergunta do usuário
pergunta = st.chat_input("Digite os sintomas")

# Lógica para processar a pergunta quando o usuário envia
if pergunta:
    # Adiciona e exibe a pergunta do usuário na interface
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Gera e exibe a resposta do assistente
    with st.chat_message("assistant"):
        # Mostra um indicador de "carregando" enquanto espera a resposta
        with st.spinner("Pensando..."):
            # Chama a API da OpenAI com o histórico da conversa
            response = client.chat.completions.create(
                model="ft:gpt-4o-2024-08-06:fine-turing:medicaltraining:BbYMybWt",
                messages=st.session_state.messages 
            )
            # Extrai e exibe o conteúdo da resposta
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            
            # Adiciona a resposta do assistente ao histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})