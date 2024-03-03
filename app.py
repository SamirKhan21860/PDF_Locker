from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfWriter, PdfReader

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
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(uploaded_file)
        
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.addPage(pdf_reader.getPage(page_num))
        
        pdf_writer.encrypt(password)
        
        # Save the new PDF
        output_path = 'Locked_document.pdf'
        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_path)
        output_file.close() # Close the output file explicitly
            
        return send_file(output_file, as_attachment=True)
     
    except IOError as e:
        return f"Error saving the file: {str(e)}"
    except PermissionError as e:
        return f"Permission error: {str(e)}"       
    except Exception as e:
        return str(e)
    
if __name__ == '__main__':
    app.run(debug=True)