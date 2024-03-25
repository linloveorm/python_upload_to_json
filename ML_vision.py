# ML_vision.py
import io
import json
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import sys


def pdf_or_image_to_json(file_bytes):
    list_data = []  # List to store the text of the first row on each page
    first_row_text = []

    # Check if the input file is a PDF or an image
    if file_bytes.startswith(b'%PDF'):  # Check if the bytes data represents a PDF
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
        # json_format = into_json_format(first_row_text, list_data)
    else:
        # For other formats assuming it's an image (e.g., PNG)
        text = pytesseract.image_to_string(Image.open(io.BytesIO(file_bytes)))
        data_list = text.split('\n')
        data_list = list(filter(lambda item: item, data_list))
        first_row_text = data_list[0].split(' ')
        
        list_data = [data_list[i].split(' ') for i in range(1, len(data_list))]
        print(list_data)

    json_format, error_data = into_json_format(first_row_text, list_data)
    
    return json_format, error_data

def extract_first_row(page):
    first_row_text = []
    blocks = page.get_text('dict')['blocks']
    if blocks:
        for line in blocks[0]['lines']:  # Extract the lines from the first block
            for span in line['spans']:  # Extract text from each span in the line
                first_row_text.append(span["text"])
    return first_row_text  # Remove leading/trailing whitespaces

def into_json_format(key_texts, list_data):
    key = key_texts
    data = list_data
    json_format = []    
    error_data = []
        
    for data_ in data:        
        if len(key) == len(data_):
            items = json.loads("{}")
            for index in range(len(key)):
                items[key[index]] = data_[index]
            json_format.append(items)  
        else:
            error_data.append(data_)
            # print(data_ )
            print("size of header is not equal to size of data") 
    json_data = json.dumps(json_format) 
    # print(json_data)  
    
    return json_data, error_data
            
def main(file_path):
    # file_path = "e:/python_uploadto_json/test_pdf_Page_1.png"
    json_data, error_data = pdf_or_image_to_json(file_path)
    json_data = json.loads(json_data)
    # print(error_data)
    # Print the keys of the first JSON object
    # print(json_data[0].keys())
    
    # Pass json_data as a command-line argument
    # print(json_data)  # Print for verification
    return json_data, error_data

if __name__ == "__main__":
    # main()
    if len(sys.argv) > 1:
        json_data = main(sys.argv[1])
        # print(json_data)  # Print for verification
