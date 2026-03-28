import streamlit as st
from io import BytesIO
import google.generativeai as genai

# --- Your API key here ---
GENAI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=GENAI_API_KEY)

# --- Page Config ---
st.set_page_config(page_title="Image Analyzer", layout="wide")

# --- Background & header styling ---
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1612831661897-3f52d9f24d6c');
        background-size: cover;
        background-position: center;
        color: white;
    }
    .card {
        background-color: rgba(0,0,0,0.6);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .card img {
        border-radius: 10px;
    }
    h1, h2, h3, p {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🖼️ Professional Image Q&A</h1>", unsafe_allow_html=True)

# --- Upload section ---
uploaded_file = st.file_uploader("Upload your image", type=["png","jpg","jpeg"])
prompt = st.text_input("Ask a question about the image:")

# --- Session history ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Analyze Button ---
if st.button("Analyze"):
    if not uploaded_file or not prompt:
        st.warning("Please upload an image and enter a question.")
    else:
        img_bytes = uploaded_file.read()
        parts = [
            prompt,
            {"mime_type": uploaded_file.type, "data": img_bytes}
        ]
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(parts)
            answer = response[0].content[0].text

            st.session_state.history.append({
                "prompt": prompt,
                "image_bytes": img_bytes,
                "answer": answer
            })
        except Exception as e:
            st.error(f"API error: {e}")

# --- Display History in cards ---
st.markdown("## History")
for item in reversed(st.session_state.history):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"**Q:** {item['prompt']}")
    st.image(item["image_bytes"], width=300)
    st.markdown(f"**A:** {item['answer']}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown(f"<p style='text-align:center;'>Total queries this session: {len(st.session_state.history)}</p>", unsafe_allow_html=True)