import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO
import time

st.set_page_config(page_title="TikTok Script Generator", page_icon="🎬", layout="wide")

st.markdown("""
<style>
    .stCodeBlock {
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 TikTok Script Generator")
st.markdown("**Gere roteiros virais em inglês + Image Prompts + Descrição + Hashtags + Imagens com IA**")

with st.sidebar:
    st.header("⚙️ Configuração")
    
    st.markdown("### 📏 Especificações")
    st.info("✅ Script: 1300-1500 caracteres\n\n✅ Estilo: Viral\n\n✅ Público: Americano\n\n✅ Duração: ~60 segundos")
    
    st.markdown("---")
    st.markdown("### 🎨 Geração de Imagens")
    gerar_imagens = st.checkbox("Gerar imagens automaticamente", value=True)
    
    estilo_imagem = st.selectbox(
        "Estilo Visual",
        [
            "Cinematic Film (Recomendado)",
            "Documentary Photography",
            "Dark Moody Cinematic",
            "Netflix Documentary",
            "True Crime Aesthetic"
        ]
    )
    
    if gerar_imagens:
        st.info("🎨 Imagens com **Flux** (alta qualidade)")

col1, col2 = st.columns([1, 1])

with col1:
    tema = st.text_area("📝 Tema (em português)", placeholder="Ex: A história sombria por trás do McDonald's", height=100)

with col2:
    roteiro_exemplo = st.text_area("📄 Roteiro Pronto (opcional)", placeholder="Se já tem um roteiro em português, cole aqui.", height=100)

if st.button("🚀 Gerar Conteúdo Completo", type="primary", use_container_width=True):
    
    if not tema and not roteiro_exemplo:
        st.error("⚠️ Insira um tema OU um roteiro pronto!")
        st.stop()
    
    try:
        api_key = "AIzaSyC7_BhPwmurF0Wo8bNF3r-R20jmlCSJNGs"
        genai.configure(api_key=api_key)
        model_text = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        base_content = roteiro_exemplo if roteiro_exemplo else tema
        content_type = "ROTEIRO ORIGINAL (português)" if roteiro_exemplo else "TEMA (português)"
        
        prompt = f"""Você é um especialista em criar conteúdo VIRAL para TikTok voltado para o público AMERICANO.

{content_type}: {base_content}

REGRAS IMPORTANTES:
- O SCRIPT deve ter entre 1300-1500 caracteres
- NO SCRIPT: NÃO incluir marcações de segundos, APENAS [PAUSE], [EMPHASIS], [BREATH]
- Seja criativo e detalhado para atingir o tamanho ideal
- Para os IMAGE PROMPTS: seja MUITO detalhado, descrevendo composição, lighting (tipo específico como golden hour, neon glow, rim lighting), camera angle preciso (low angle, bird's eye, dutch tilt), mood claro (tense, eerie, dramatic), cores dominantes, texturas visíveis, movimento de câmera, contexto temporal/espacial

ENTREGUE EXATAMENTE NO FORMATO (com os delimitadores |||):

SCRIPT|||
[Script completo em inglês formatado para ElevenLabs APENAS com [PAUSE], [EMPHASIS], [BREATH]. SEM [0-3s]. 1300-1500 caracteres. Estilo viral com gancho forte nos primeiros 3 segundos. Linguagem simples para público americano.]

PROMPTS|||
0-3s: [Descrição visual detalhada e precisa da cena, incluindo: o que aparece exatamente, composição específica, lighting detalhado, camera angle preciso, mood/atmosfera, cores dominantes, texturas visíveis, movimento, contexto espacial/temporal]. Cinematic, hyper-realistic, 4K quality, professional color grading.

3-7s: [Descrição visual detalhada e precisa com todos os elementos acima]. Cinematic, hyper-realistic, 4K quality.

7-12s: [Descrição visual detalhada e precisa com todos os elementos acima]. Cinematic, hyper-realistic, 4K quality.

12-17s: [Descrição visual detalhada e precisa com todos os elementos acima]. Cinematic, hyper-realistic, 4K quality.

17-22s: [Descrição visual detalhada e precisa com todos os elementos acima]. Cinematic, hyper-realistic, 4K quality.

22-27s: [Descrição visual detalhada e precisa com todos os elementos acima]. Cinematic, hyper-realistic, 4K quality.

27-32s: [Descrição visual detalhada e precisa com todos os elementos acima]. Cinematic, hyper-realistic, 4K quality.

32-37s: [Descrição visual detalhada e precisa com todos os elementos acima]. Cinematic, hyper-realistic, 4K quality.

37-42s: [Descrição visual detalhada e precisa com todos os elementos acima]. Cinematic, hyper-realistic, 4K quality.

42-47s: [Descrição visual detalhada e precisa com todos os elementos acima]. Cinematic, hyper-realistic, 4K quality.

47-52s: [Descrição visual detalhada e precisa com todos os elementos acima]. Cinematic, hyper-realistic, 4K quality.

DESCRIPTION|||
[Descrição engajante de 150-200 caracteres com call-to-action americano forte]

[8-10 hashtags trending nos EUA incluindo #fyp #viral e específicos do tema]
"""
        
        with st.spinner("🤖 Gerando roteiro e prompts..."):
            response = model_text.generate_content(prompt)
            resultado = response.text
        
        partes = resultado.split("|||")
        
        if len(partes) < 4:
            st.error(f"❌ Erro no formato. Tentando novamente...")
            st.rerun()
        
        script_text = partes[1].strip()
        prompts_text = partes[2].strip()
        description_text = partes[3].strip()
        
        script_text = script_text.replace("PROMPTS", "").replace("PROMPT", "").strip()
        
        char_count = len(script_text)
        
        if char_count < 1200:
            st.warning(f"⚠️ Script muito curto ({char_count} caracteres). Gerando novamente...")
            st.rerun()
        elif char_count > 1600:
            script_text = script_text[:1550].rsplit('.', 1)[0] + '.'
            char_count = len(script_text)
        
        st.success("✅ Conteúdo gerado com sucesso!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Caracteres", f"{char_count}")
        with col2:
            st.metric("⏱️ Duração", "~60s")
        with col3:
            if 1300 <= char_count <= 1500:
                st.metric("Status", "✅ Perfeito")
            elif 1200 <= char_count < 1300:
                st.metric("Status", "✅ Bom")
            else:
                st.metric("Status", "✅ Ok")
        
        st.markdown("---")
        
        st.markdown("### 🎙️ Roteiro (ElevenLabs Ready)")
        st.code(script_text, language="text")
        
        st.markdown("### 🎨 Prompts das Imagens")
        
        prompts_lines = [line.strip() for line in prompts_text.split('\n') if line.strip()]
        prompts_list = []
        
        for prompt_line in prompts_lines:
            if ':' in prompt_line:
                parts = prompt_line.split(':', 1)
                timestamp = parts[0].strip()
                content = parts[1].strip()
                
                prompts_list.append({"timestamp": timestamp, "prompt": content})
                
                st.markdown(f"**⏱️ {timestamp}**")
                st.code(content, language="text")
        
        st.markdown("### 📝 Descrição + Hashtags")
        st.code(description_text, language="text")
        
        texto_completo = f"""ROTEIRO:
{script_text}

PROMPTS DAS IMAGENS:
{prompts_text}

DESCRIÇÃO + HASHTAGS:
{description_text}
"""
        
        st.markdown("---")
        st.download_button("📥 Download Completo", data=texto_completo, file_name=f"tiktok_{char_count}chars.txt", mime="text/plain", use_container_width=True)
        
        if gerar_imagens and prompts_list:
            st.markdown("---")
            st.markdown("### 🖼️ Imagens Geradas com IA")
            st.info(f"🎨 Gerando {len(prompts_list)} imagens em estilo **{estilo_imagem}**... Aguarde.")
            
            # Estilos otimizados
            style_mappings = {
                "Cinematic Film (Recomendado)": "cinematic film still, shot on ARRI ALEXA, shallow depth of field, film grain, professional color grading, volumetric lighting, 8K UHD",
                "Documentary Photography": "documentary photography, photojournalism style, natural lighting, authentic, National Geographic quality",
                "Dark Moody Cinematic": "dark moody cinematic, film noir aesthetic, dramatic shadows, high contrast, atmospheric",
                "Netflix Documentary": "Netflix documentary cinematography, professional film quality, natural lighting, 4K",
                "True Crime Aesthetic": "true crime documentary aesthetic, forensic photography style, cold color temperature, stark lighting"
            }
            
            style_suffix = style_mappings.get(estilo_imagem, style_mappings["Cinematic Film (Recomendado)"])
            negative_prompt = "low quality, blurry, distorted, ugly, bad anatomy, watermark, text"
            
            for idx, prompt_data in enumerate(prompts_list):
                timestamp = prompt_data["timestamp"]
                prompt_img = prompt_data["prompt"]
                
                prompt_final = f"{prompt_img}, {style_suffix}"
                
                st.markdown(f"#### 📸 {timestamp}")
                
                with st.spinner(f"🎨 Gerando imagem {idx+1}/{len(prompts_list)}..."):
                    try:
                        prompt_encoded = requests.utils.quote(prompt_final)
                        negative_encoded = requests.utils.quote(negative_prompt)
                        
                        image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=1344&height=768&model=flux&nologo=true&enhance=true&negative={negative_encoded}&seed={42+idx}"
                        
                        response_img = requests.get(image_url, timeout=60)
                        
                        if response_img.status_code == 200:
                            image = Image.open(BytesIO(response_img.content))
                            st.image(image, caption=f"Imagem para {timestamp}", use_container_width=True)
                            
                            buf = BytesIO()
                            image.save(buf, format="PNG")
                            st.download_button(
                                label=f"📥 Download {timestamp}",
                                data=buf.getvalue(),
                                file_name=f"tiktok_{timestamp.replace(':', '-')}.png",
                                mime="image/png",
                                key=f"download_{idx}"
                            )
                        else:
                            st.warning(f"⚠️ Erro ao gerar. Use o prompt:")
                            st.code(prompt_final, language="text")
                        
                        time.sleep(3)
                        
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
                        st.code(prompt_final, language="text")
            
            st.success(f"✅ Todas as imagens geradas!")
    
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")

st.markdown("---")
st.markdown("Made with ❤️ | Powered by Google Gemini 2.0 Flash + Flux")
