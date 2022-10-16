# Imports
import PyPDF2 


# Main function
def to_text(pdf):
    with open(pdf, 'rb') as pdfFileObj:
      pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
      full_pdf_text = ""
      for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page) 
        full_pdf_text += pageObj.extractText()
    return full_pdf_text