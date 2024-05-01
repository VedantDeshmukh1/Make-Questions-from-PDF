import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

def generate_questions(pdf_path, api_key):
    # ... (code remains the same)

# Streamlit app
def main():
    st.set_page_config(page_title="Question Generator", page_icon=":question:", layout="wide")

    # Custom CSS styles
    st.markdown(
        """
        <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #2E86C1;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 24px;
            color: #34495E;
            margin-bottom: 10px;
        }
        .question {
            font-size: 18px;
            color: #2C3E50;
            margin-bottom: 10px;
        }
        .divider {
            border-top: 1px solid #ccc;
            margin: 20px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="title">Question Generator</div>', unsafe_allow_html=True)

    # API key input
    api_key = st.text_input("Enter your Google API key", type="password")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None and api_key:
        # Save the uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())

        # Generate questions
        with st.spinner("Generating questions..."):
            questions = generate_questions("temp.pdf", api_key)

        # Display the generated questions
        st.markdown('<div class="subtitle">Generated Questions</div>', unsafe_allow_html=True)
        for i, question in enumerate(questions):
            st.markdown(f'<div class="question"><strong>Questions for Text Chunk {i+1}:</strong></div>', unsafe_allow_html=True)
            st.write(question)
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
