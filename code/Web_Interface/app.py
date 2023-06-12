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

    # get user inputs through a sidebar
    name = st.sidebar.text_input("Student Name: ")
    email = st.sidebar.text_input("Email Address: ")
    st.sidebar.subheader("Your Documents")
    pdf_docs = st.sidebar.file_uploader("Upload your Images here and click on 'Process'",accept_multiple_files=True)

    st.header("Handwritten Essay Marking Software")
        
    # Page title
    st.markdown("## <span style='font-size: 24px; font-weight: normal;'>Student Result Card</span>", unsafe_allow_html=True)

    # Process button
    if st.button("Process"):
        processed_result = process_data(name, email)
        st.session_state.results.append([name, email, processed_result])

        display_data() 

    

if __name__ == '__main__':
    main()

        