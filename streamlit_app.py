import streamlit as st
import io
import json
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import cv2
import numpy as np
import requests

def pdf_or_image_to_json(file_bytes):
    list_data = []  # List to store the text of the first row on each page
    first_row_text = []

    # Check if the input file is a PDF or an image
    if isinstance(file_bytes, bytes) and file_bytes.startswith(b'%PDF'):  # Check if the bytes data show a PDF
        # Open the PDF file
        with fitz.open(stream=io.BytesIO(file_bytes)) as pdf_document:
            # Iterate through each page of the PDF
            for page_number in range(len(pdf_document)):
                page = pdf_document.load_page(page_number)
                
                # Extract text from the first row on the page
                first_row_text = extract_first_row(page)
                
                # Skip the first row in each page
                skip_first_row = True
                
                # Iterate through the text blocks on the page
                for text_block in page.get_text('dict')['blocks']:
                    # Skip the first row
                    if skip_first_row:
                        skip_first_row = False
                        continue
                    
                    list_data_in_line = []
                    # Extract text from each line in the block
                    for line in text_block['lines']: 
                        text = [] 
                        # Extract text from each span in the line
                        for span in line['spans']:
                            text.append(span['text'])
                        list_data_in_line.append(text[0])
                    
                    list_data.append(list_data_in_line)
    elif isinstance(file_bytes, np.ndarray):  # Check if the input is a NumPy array (image)
        processed_image = preprocess_image(file_bytes)
        # Use Tesseract OCR to extract text from PNG file
        text = pytesseract.image_to_string(processed_image)
        
        list_data = [line.split() for line in text.split('\n') if line.strip()]  # Split text into lines and words
        first_row_text = list_data[0] if list_data else []

    json_format, error_data = into_json_format(first_row_text, list_data)
    
    return json_format, error_data

def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive to obtain a binary image
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # Perform morphological operations to enhance text extraction
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    binary = cv2.erode(binary, kernel, iterations=1)
    
    return binary

def extract_first_row(page):
    first_row_text = []
    blocks = page.get_text('dict')['blocks']
    if blocks:
        for line in blocks[0]['lines']:  # Extract the lines from the first block
            for span in line['spans']:  # Extract text from each span in the line
                first_row_text.append(span["text"])
    return first_row_text  # Remove leading/trailing whitespaces

def into_json_format(key_texts, list_data):
    #set header as Key
    key = key_texts
    
    #get data
    data = list_data
    json_format = []    
    error_data = []
        
    for data_ in data:        
        if len(key) == len(data_):
            items = {}
            for index in range(len(key)):
                items[key[index]] = data_[index]
            json_format.append(items)  
        else:
            error_data.append(data_)
            
    json_data = json.dumps(json_format) 
    
    return json_data, error_data

def main():
    st.title("File Browser")

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        st.write("You have uploaded:")
        st.write(uploaded_file)

        # Convert uploaded file        
        if uploaded_file.type == 'image/png':
            image_bytes = uploaded_file.read()
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            file_bytes = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        elif uploaded_file.type == 'application/pdf':
            file_bytes = uploaded_file.getvalue()
        else:
            st.write("Unsupported file format.")
            return

        # Preview uploaded file
        if uploaded_file.type.startswith('image'):
            st.image(file_bytes, caption='Uploaded Image', use_column_width=True)
        elif uploaded_file.type == 'application/pdf':
            st.write("PDF preview is not supported yet.")
            
        # data from uploaded file to pdf_or_image_to_json function
        json_data, error_data = pdf_or_image_to_json(file_bytes)
            
        # the buttons will display after get json data
        # "Correct" will connect to API for store uploaded file and json payload to database
        if st.button("Correct"):
            # Pretend to connect to a mock API to store data in the database
            mock_api_url = "https://api.example.com/store_data"
            payload = {"file": uploaded_file.getvalue(), "json_data": json_data}
            response = requests.post(mock_api_url, json=payload)
            if response.status_code == 200:
                st.success("Data stored successfully.")
            else:
                st.error("Failed to store data.")
                
        if st.button("Cancel"):
            st.write("Cancel action was performed.")

        

        st.write("JSON Data:")
        st.json(json_data)

        

        st.write("Error Data:")
        st.write(error_data)

if __name__ == "__main__":
    main()
