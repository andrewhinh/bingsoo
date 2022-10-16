# Imports
import PyPDF2 
from pathlib import Path


# Variables
inference_context_file = Path(__file__).resolve().parents[0] / 'syllabus.pdf'


# Main function
def to_text(self):
    with open(inference_context_file, 'rb') as pdfFileObj:
      pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
      full_pdf_text = ""
      for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page) 
        full_pdf_text += pageObj.extractText()
    return full_pdf_text