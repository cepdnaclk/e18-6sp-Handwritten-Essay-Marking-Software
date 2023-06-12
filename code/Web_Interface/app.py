import streamlit as st 
from PyPDF2 import PdfReader
import random

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text = page.extract_text()
    return text

def process_data(name, email):
    # Perform necessary processing on the data
    # For example, you could save the data to a database or perform calculations
    result = random.randint(0, 100)

    # Return the processed result
    return result

# @st.cache_resource(persist=True)
def display_data():
    for i, result in enumerate(st.session_state.results):
            st.subheader(f"Result Card {i+1}")
            st.write(f"Name: {result[0]}")
            st.write(f"Email: {result[1]}")
            st.write(f"Result: {result[2]}%")
            st.write("---")



def main():
    st.set_page_config(page_title="Handwritten Essay Marker", page_icon=":books:")

    if "results" not in st.session_state:
        st.session_state.results = list()

    # st.header("Chat with multiple PDFs :books:")
    # st.text_input("Ask a question about your documents:")

    # put things inside sidebar
    # swith st.sidebar:
    st.header("Handwritten Essay Marking Software")

    name = st.text_input("Student Name: ")
    email = st.text_input("Email Address: ")
    st.subheader("Your Documents")
    pdf_docs = st.file_uploader("Upload your Images here and click on 'Process'",accept_multiple_files=True)
    
    # Page title
    st.subheader("Student Result Card")

    # Process button
    if st.button("Process"):
        processed_result = process_data(name, email)
        st.session_state.results.append([name, email, processed_result])

        display_data()
        # Display result cards
        # for i, result in enumerate(st.session_state.results):
        #     st.subheader(f"Result Card {i+1}")
        #     st.write(f"Name: {result[0]}")
        #     st.write(f"Email: {result[1]}")
        #     st.write(f"Result: {result[2]}%")
        #     st.write("---")


if __name__ == '__main__':
    main()