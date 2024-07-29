!pip install PyPDF2 google-generativeai ipywidgets

import PyPDF2
import google.generativeai as palm
import ipywidgets as widgets
from IPython.display import display

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    print(f"Extracting text from: {pdf_path}")  # Debugging
    text = ''
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    print("Extraction complete.")  # Debugging
    return text

# Function to handle file upload event
def on_upload_change(change):
    for filename, file_info in upload_widget.value.items():
        print(f"File uploaded: {filename}")  # Debugging
        with open(filename, 'wb') as f:
            f.write(file_info['content'])
        pdf_text = extract_text_from_pdf(filename)
        start_chatbot(pdf_text)

# Function to start the chatbot with a text input widget
def start_chatbot(pdf_text):
    print("Configuring Bot...")  # Debugging
    palm.configure(api_key='API KEY') #Add your own :)

    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name

    def chat_with_palm(prompt, context):
        response = palm.generate_text(
            model=model,
            prompt=f"{context}\n\nUser: {prompt}",
            temperature=0,
            max_output_tokens=800,
        )
        return response.result

    print("Welcome to Doc ChatBot! Type 'exit' to end the conversation.")
    pdf_context = pdf_text  # Use the extracted text from the uploaded PDF

    # Create text input widget for user interaction
    input_box = widgets.Text(placeholder='Type your message here...')
    output_box = widgets.Output()

    display(input_box, output_box)

    def on_text_submit(change):
        user_input = input_box.value
        input_box.value = ''  # Clear the input box
        if user_input.lower() == 'exit':
            with output_box:
                print("Bot: Goodbye!")
        else:
            response = chat_with_palm(user_input, pdf_context)
            with output_box:
                print(f"You: {user_input}")
                print(f"Bot: {response}")

    input_box.on_submit(on_text_submit)

# Create file upload widget
upload_widget = widgets.FileUpload(accept='.pdf', multiple=False)
upload_widget.observe(on_upload_change, names='value')
display(upload_widget)

