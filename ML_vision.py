import fitz  # PyMuPDF
import pytesseract
import json

def pdf_or_image_to_json(file_path):
    # Initialize empty text variable
    
    list_data = []  # List to store the text of the first row on each page
    first_row_text = []
    
    # Check if the input file is a PDF or an image
    if file_path.endswith('.pdf'):
        # Open the PDF file
        with fitz.open(file_path) as pdf_document:
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
                    
    elif file_path.endswith('.png'):
        # For PNG image
        text = pytesseract.image_to_string(file_path)
    else:
        print("Unsupported file format.")
        return
    
    # print(list_data)
    
    # Process the extracted text as needed
    # processed_text = list_data # Example: removing leading/trailing whitespaces
    
    json_format = into_json_format(first_row_text, list_data)
    # print(json_format)
    
    # # Convert processed text to JSON payload
    # json_payload = {'data_from_pdf': first_row_text, 'text': processed_text}
    
    # # Convert dictionary to JSON string
    # json_string = json.dumps(json_payload)
    # print(type(json_format))
    return json_format

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
        
    for data_ in data:        
        if len(key) == len(data_):
            items = json.loads("{}")
            for index in range(len(key)):
                items[key[index]] = data_[index]
            json_format.append(items)  
        else:
            print("size of header is not equal to size of data") 
    json_data = json.dumps(json_format) 
    # print(type(json_data))   
    
    return json_data
            
def main():
    # Example usage
    file_path = 'test_pdf.pdf'  # Replace with your file path
    json_data = pdf_or_image_to_json(file_path)
    json_data = json.loads(json_data)
# print(json_data[0].keys())

if __name__=="__main__": 
    main() 
