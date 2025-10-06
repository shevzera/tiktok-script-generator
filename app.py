import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="TikTok Script Generator", page_icon="🎬", layout="wide")

st.markdown("""
<style>
    .script-box {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #FF0050;
        margin: 10px 0;
    }
    .prompt-box {
        background-color: #2D2D2D;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #00D9FF;
        margin: 10px 0;
    }
    .description-box {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #00FF88;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 TikTok Script Generator")
st.markdown("**Gere roteiros virais em inglês + Image Prompts + Descrição + Hashtags**")

with st.sidebar:
    st.header("⚙️ Configuração")
    api_key = st.text_input("Google Gemini API Key", type="password", help="Cole sua API key aqui")
    st.markdown("[📖 Como pegar API Key](https://aistudio.google.com/apikey)")
    st.markdown("---")
    st.markdown("### 📏 Especificações")
    st.info("✅ Script: 1300-1500 caracteres\n\n✅ Estilo: Viral\n\n✅ Público: Americano\n\n✅ Duração: ~60 segundos")

col1, col2 = st.columns([1, 1])

with col1:
    tema = st.text_area("📝 Tema (em português)", placeholder="Ex: A história sombria por trás do McDonald's", height=100)

with col2:
    roteiro_exemplo = st.text_area("📄 Roteiro Pronto (opcional)", placeholder="Se já tem um roteiro em português, cole aqui.", height=100)

if st.button("🚀 Gerar Conteúdo Completo", type="primary", use_container_width=True):
    
    if not api_key:
        st.error("⚠️ Por favor, insira sua API Key na barra lateral!")
        st.stop()
    
    if not tema and not roteiro_exemplo:
        st.error("⚠️ Insira um tema OU um roteiro pronto!")
        st.stop()
    
    try:
        st.write("🔍 DEBUG 1: Iniciando configuração...")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        st.write("🔍 DEBUG 2: Modelo configurado")
        
        base_content = roteiro_exemplo if roteiro_exemplo else tema
        content_type = "ROTEIRO ORIGINAL (português)" if roteiro_exemplo else "TEMA (português)"
        
        st.write(f"🔍 DEBUG 3: Conteúdo = {base_content[:50]}...")
        
        prompt = f"""Você é um especialista em criar conteúdo VIRAL para TikTok voltado para o público AMERICANO.

{content_type}: {base_content}

REGRAS IMPORTANTES:
- O SCRIPT deve ter EXATAMENTE entre 1300-1500 caracteres (OBRIGATÓRIO)
- NO SCRIPT: NÃO incluir marcações de segundos, APENAS [PAUSE], [EMPHASIS], [BREATH]

ENTREGUE NO FORMATO:

SCRIPT|||
[Script completo em inglês formatado para ElevenLabs APENAS com [PAUSE], [EMPHASIS], [BREATH]. SEM [0-3s]. 1300-1500 CARACTERES]

PROMPTS|||
0-3s: Cinematic [descrição ultra detalhada: composição, lighting, camera angle, mood, cores, texturas, movimento]. Hyper-realistic, 4K.
3-7s: Cinematic [descrição ultra detalhada]. Hyper-realistic, 4K.
7-12s: Cinematic [descrição ultra detalhada]. Hyper-realistic, 4K.
12-17s: Cinematic [descrição ultra detalhada]. Hyper-realistic, 4K.
17-22s: Cinematic [descrição ultra detalhada]. Hyper-realistic, 4K.
22-27s: Cinematic [descrição ultra detalhada]. Hyper-realistic, 4K.
27-32s: Cinematic [descrição ultra detalhada]. Hyper-realistic, 4K.
32-37s: Cinematic [descrição ultra detalhada]. Hyper-realistic, 4K.
37-42s: Cinematic [descrição ultra detalhada]. Hyper-realistic, 4K.
42-45s: Cinematic [descrição ultra detalhada]. Hyper-realistic, 4K.
45-50s: Cinematic [descrição ultra detalhada]. Hyper-realistic, 4K.

DESCRIPTION|||
[Descrição 150-200 caracteres com call-to-action americano]

[8-10 hashtags trending EUA incluindo #fyp #viral]
"""
        
        st.write("🔍 DEBUG 4: Enviando prompt para Gemini...")
        
        with st.spinner("🤖 Gerando seu conteúdo viral..."):
            response = model.generate_content(prompt)
            resultado = response.text
        
        st.write("🔍 DEBUG 5: Resposta recebida!")
        st.write(f"🔍 DEBUG 6: Tamanho da resposta = {len(resultado)} caracteres")
        st.write(f"🔍 DEBUG 7: Primeiros 300 chars = {resultado[:300]}")
        
        partes = resultado.split("|||")
        st.write(f"🔍 DEBUG 8: Número de partes após split = {len(partes)}")
        
        if len(partes) < 4:
            st.error(f"❌ Formato inválido. Esperava 4 partes, recebi {len(partes)}")
            st.write("Resposta completa:")
            st.code(resultado)
            st.stop()
        
        script_text = partes[1].strip()
        prompts_text = partes[2].strip()
        description_text = partes[3].strip()
        
        st.write(f"🔍 DEBUG 9: Script extraído com {len(script_text)} caracteres")
        
        char_count = len(script_text)
        
        if char_count < 1300:
            st.warning(f"⚠️ Script muito curto ({char_count} caracteres). Gerando novamente...")
            st.rerun()
        elif char_count > 1500:
            script_text = script_text[:1500].rsplit('.', 1)[0] + '.'
            char_count = len(script_text)
        
        st.success("✅ Conteúdo gerado com sucesso!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Caracteres", f"{char_count}")
        with col2:
            st.metric("⏱️ Duração", "~60s")
        with col3:
            st.metric("Status", "✅ Aprovado" if 1300 <= char_count <= 1500 else "⚠️ Revisar")
        
        st.markdown("---")
        
        st.markdown("### 🎙️ Roteiro (ElevenLabs Ready)")
        st.markdown("")
        st.markdown('<div class="script-box">', unsafe_allow_html=True)
        st.markdown(script_text.replace("[PAUSE]", "**[PAUSE]**").replace("[EMPHASIS]", "**[EMPHASIS]**").replace("[BREATH]", "**[BREATH]**"))
        st.markdown('</div>', unsafe_allow_html=True)
        st.code(script_text, language="text")
        
        st.markdown("---")
        
        st.markdown("### 🎨 Prompts das Imagens")
        st.markdown("")
        
        prompts_lines = [line.strip() for line in prompts_text.split('\n') if line.strip()]
        
        for prompt_line in prompts_lines:
            if ':' in prompt_line:
                parts = prompt_line.split(':', 1)
                timestamp = parts[0].strip()
                content = parts[1].strip()
                
                st.markdown(f"**⏱️ {timestamp}**")
                st.markdown('<div class="prompt-box">', unsafe_allow_html=True)
                st.markdown(content)
                st.markdown('</div>', unsafe_allow_html=True)
                st.code(content, language="text")
        
        st.markdown("---")
        
        st.markdown("### 📝 Descrição + Hashtags")
        st.markdown("")
        st.markdown('<div class="description-box">', unsafe_allow_html=True)
        st.markdown(description_text)
        st.markdown('</div>', unsafe_allow_html=True)
        st.code(description_text, language="text")
        
        texto_completo = f"""ROTEIRO:
{script_text}

PROMPTS DAS IMAGENS:
{prompts_text}

DESCRIÇÃO + HASHTAGS:
{description_text}
"""
        
        st.download_button("📥 Download Completo", data=texto_completo, file_name=f"tiktok_{char_count}chars.txt", mime="text/plain")
    
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

st.markdown("---")
st.markdown("Made with ❤️ | Powered by Google Gemini 2.0 Flash")
