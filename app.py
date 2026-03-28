import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
import streamlit as st

load_dotenv()

gemini_api_key = os.getenv("API_KEY")
genai.configure(api_key=gemini_api_key)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #e3f2fd, #ffffff);
    }

    h1, h2, h3 {
        color: #0d47a1;
        text-align: center;
    }

    .stButton>button {
        background-color: #1976d2;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }

    .stTextInput>div>div>input {
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("AI Image Analytics App")

counter_file = "counter.txt"

if not os.path.exists(counter_file):
    with open(counter_file, "w") as f:
        f.write("0")

with open(counter_file, "r") as f:
    count = int(f.read())

count += 1

with open(counter_file, "w") as f:
    f.write(str(count))

st.write("Users visited:", count)

if "history" not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

st.markdown("""
<style>

.stApp {
    background-image: url("https://images.unsplash.com/photo-1677442136019-21780ecad995");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* dark transparent overlay */
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

/* text styling */
h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
    font-family: 'Segoe UI', sans-serif;
}

/* upload box style */
[data-testid="stFileUploader"] {
    background-color: rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 12px;
}

/* button style */
.stButton>button {
    background-color: #007BFF;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 200px;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.title("AI Image Analyzer")
st.write("Upload an image and get AI-powered description")

st.success(f"Total Users Visited: {count}")



if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=400)

prompt = st.text_input(
    "Enter your prompt",
    placeholder="Example: Describe this image in simple English"
)

if st.button("GET RESPONSE"):

    if uploaded_file is not None and prompt:

        img = Image.open(uploaded_file)

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content([prompt, img])

        st.subheader("AI Description")

        st.write(response.text)

        st.session_state.history.append((prompt, response.text))

    else:
        st.warning("Please upload image and enter prompt")

st.subheader("Previous Results")

if len(st.session_state.history) == 0:
    st.write("No history yet")

for q, a in reversed(st.session_state.history):

    st.markdown(f"""
    Question: {q}

    Answer: {a}
    
    ---
    """)
