import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# --- Configuração Inicial ---
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura a chave de API do Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    # Mostra um erro na página se a chave não for encontrada
    st.error("Chave de API do Gemini não encontrada! Por favor, configure seu arquivo .env.")
    st.stop() # Interrompe a execução do script

# --- Funções da Aplicação ---

def carregar_modelo():
    """Carrega o modelo GenerativeModel do Gemini."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        return model
    except Exception as e:
        st.error(f"Erro ao carregar o modelo do Gemini: {e}")
        return None

def analisar_imagem(modelo, imagem, prompt):
    """Envia a imagem e o prompt para o Gemini e retorna a resposta."""
    if not modelo:
        return "Modelo não foi carregado corretamente."
    
    try:
        # Prepara o conteúdo para o modelo (prompt e imagem)
        conteudo = [prompt, imagem]
        response = modelo.generate_content(conteudo)
        return response.text
    except Exception as e:
        return f"Ocorreu um erro durante a análise: {e}"

# --- Interface da Página Web (Streamlit) ---

# st.title() define o título principal da página
st.title("🤖 Analisador de Imagens com Gemini AI")

# st.write() escreve textos na página, suportando Markdown
st.write("Faça o upload de uma imagem e peça ao Gemini para descrevê-la ou responder a uma pergunta sobre ela.")

# Carrega o modelo de IA
model = carregar_modelo()

# st.file_uploader() cria um widget para o usuário fazer upload de arquivos
uploaded_file = st.file_uploader(
    "Escolha uma imagem...", 
    type=["jpg", "jpeg", "png"] # Define os tipos de arquivo permitidos
)

# Verifica se um arquivo foi enviado pelo usuário
if uploaded_file is not None and model:
    # Abre a imagem usando a biblioteca Pillow (PIL)
    image = Image.open(uploaded_file)

    # st.image() exibe a imagem na página web
    st.image(image, caption="Imagem enviada.", use_column_width=True)

    # st.text_area() cria um campo de texto para o usuário digitar
    prompt_usuario = st.text_area(
        "O que você quer saber sobre a imagem?", 
        "Descreva esta imagem em detalhes." # Texto padrão
    )

    # st.button() cria um botão. O código dentro do 'if' só executa quando o botão é clicado.
    if st.button("Analisar Imagem"):
        # st.spinner() mostra uma animação de "carregando" enquanto o código dentro do 'with' executa
        with st.spinner("Analisando a imagem, por favor aguarde..."):
            resultado = analisar_imagem(model, image, prompt_usuario)
            
            # st.subheader() cria um subtítulo
            st.subheader("Resultado da Análise:")
            # st.markdown() exibe o texto da resposta, permitindo formatação
            st.markdown(resultado)