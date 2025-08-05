import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
import re

st.set_page_config(layout="wide")

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("ytu-ce-cosmos/turkish-gpt2")
    model = AutoModelForCausalLM.from_pretrained("ytu-ce-cosmos/turkish-gpt2").to("cpu")
    return tokenizer, model

tokenizer, model = load_model()

user_name = st.session_state.get("user_name", "Misafir")
user_burc = st.session_state.get("zodiac", "Koç")
user_gender = st.session_state.get("gender", "Kadın")
user_image_path = st.session_state.get("image_path", None)

col1, col2 = st.columns([5, 1])

with col1:
    st.title(f"👋 Merhaba, {user_name}!")
    st.subheader(f"✨ Burcun: {user_burc} • Cinsiyet: {user_gender}")

    base_prompt = f"{user_burc} burcu {user_gender.lower()} hakkında içten ve özgün bir burç yorumu yap."
    inputs = tokenizer(base_prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=180,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            do_sample=True,
            no_repeat_ngram_size=3,
            early_stopping=True
        )

    yorum = tokenizer.decode(outputs[0], skip_special_tokens=True)
    yorum = yorum.replace(base_prompt, "").strip()

    st.markdown("### 🤖 Yapay Zekâ Yorumu:")
    st.info(yorum)

with col2:
    if user_image_path and os.path.exists(user_image_path):
        st.image(user_image_path, width=120, caption=f"{user_burc} Burcu")

st.markdown("---")

st.subheader("🔮 Burcuna Özel Sorular Sorabilirsin")

kategori = st.selectbox("Kategori Seç:", ["Aşk", "Kariyer", "Sağlık", "Genel"])
soru = st.text_input("Sorunuz:")

if st.button("Yanıtla"):
    if not soru.strip():
        st.warning("Lütfen bir soru yazın.")
    else:
        soru_prompt = (
            f"{user_burc} burcu {user_gender.lower()} için {kategori} konusunda kısa, özgün ve tekrarsız bir yanıt ver.\n"
            f"Soru: {soru}\nYanıt:"
        )

        inputs_soru = tokenizer(soru_prompt, return_tensors="pt")

        with torch.no_grad():
            outputs_soru = model.generate(
                **inputs_soru,
                max_length=150,
                temperature=0.7,
                top_p=0.9,
                top_k=40,
                do_sample=True,
                no_repeat_ngram_size=3,
                early_stopping=True
            )

        cevap_raw = tokenizer.decode(outputs_soru[0], skip_special_tokens=True)
        cevap_clean = re.split(r"Yanıt:\s*", cevap_raw)[-1].strip()
        cevap_clean = re.sub(r"\s+", " ", cevap_clean)
        st.success(f"🧠 Yapay Zekâ Yanıtı:\n\n{cevap_clean}")
