import os
from PIL import Image
import streamlit as st
import google.generativeai as genai

# ---------------- API KEY CONFIG ----------------
# Read API key from environment variable
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    st.error("API key not set! Please add GENAI_API_KEY in environment variables.")
    st.stop()

genai.configure(api_key=GENAI_API_KEY)

# ---------------- UI STYLING ----------------
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1677442136019-21780ecad995");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.6);
        z-index: -1;
    }
    h1,h2,h3,h4,h5,h6,p,label {
        color: white !important;
        font-family: 'Segoe UI', sans-serif;
    }
    [data-testid="stFileUploader"] {
        background-color: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 12px;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border-radius: 8px;
        height: 45px;
        width: 200px;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("AI Image Analyzer")
st.write("Upload an image and get AI-powered description")

# ---------------- User Counter ----------------
counter_file = "counter.txt"
if not os.path.exists(counter_file):
    with open(counter_file, "w") as f:
        f.write("0")

with open(counter_file, "r") as f:
    count = int(f.read())
count += 1
with open(counter_file, "w") as f:
    f.write(str(count))

st.success(f"Total Users Visited: {count}")

# ---------------- Session History ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- File Upload ----------------
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=400)

# ---------------- Prompt Input ----------------
prompt = st.text_input(
    "Enter your prompt",
    placeholder="Example: Describe this image in simple English"
)

# ---------------- Generate Response ----------------
if st.button("GET RESPONSE"):
    if uploaded_file is not None and prompt:
        # Gemini currently only supports text input for model.generate_content
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content([prompt])
        
        answer_text = response[0].content[0].text if response else "No response from AI."
        
        st.subheader("AI Description")
        st.write(answer_text)
        
        st.session_state.history.append((prompt, answer_text))
    else:
        st.warning("Please upload an image and enter a prompt")

# ---------------- Display History ----------------
st.subheader("Previous Results")
if not st.session_state.history:
    st.write("No history yet")

for q, a in reversed(st.session_state.history):
    st.markdown(f"""
    **Question:** {q}  
    **Answer:** {a}  
    ---
    """)
