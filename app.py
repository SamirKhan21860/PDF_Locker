from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfFileWriter, PdfFileReader

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        uploaded_file = request.files['file']
        password = request.form['password']
        
        # Validate file and password
        if not uploaded_file or not password:
            return 'Invalid file or password.'
        
        # Process PDF file
        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(uploaded_file)
        
        for page_num in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page_num))
        
        pdf_writer.encrypt(password)
        
        # Save the new PDF
        output_path = 'Locked_document.pdf'
        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)
            
        return send_file(output_file, as_attachment=True)
            
    except Exception as e:
        return str(e)
    
if __name__ == '__main__':
    app.run(debug=True)