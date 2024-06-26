import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

def generate_questions(pdf_path, api_key):
    # Load the PDF document
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split the text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Define the prompt template
    prompt_template = """
    Given the following text, generate multiple questions of three or more types as follows:
    1. True or False question
    2. Multiple Choice Question (MCQ) with four options
    3. One-word answer question

    Text:
    {text}

    Questions:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    # Initialize the Google Language Model
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

    # Create the question generation chain
    question_chain = LLMChain(llm=llm, prompt=prompt)

    # Generate questions for each text chunk
    questions = []
    for i, text in enumerate(texts):
        response = question_chain.run(text=text.page_content)
        questions.append(f"Questions for Text Chunk {i+1}:\n{response}")

    return questions

# Streamlit app
def main():
    page_bg_img = '''
<style>
body {
background-image: url("https://wallpapers.com/images/featured/dark-forest-shsyax3tzax42p9o.jpg");
background-size: cover;
}
</style>
'''

    st.markdown(page_bg_img, unsafe_allow_html=True)
    #image_url = "dark-forest-shsyax3tzax42p9o.jpg"
    #set_background_image(image_url)
    st.title("Question Generator \U0001F929")
    st.write("Upload your PDF enter API-KEY and automatically process it to generate MCQ, one-word, and true or false questions.")
    # API key input
    api_key = st.text_input("Enter your Google API key")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None and api_key:
        # Save the uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())

        # Generate questions
        questions = generate_questions("temp.pdf", api_key)

        # Display the generated questions
        for question in questions:
            st.write(question)
            st.write("---")

if __name__ == "__main__":
    main()
