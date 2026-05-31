import PyPDF2
import docx

def read_resume(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() for page in reader.pages)

    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        text = "\n".join(para.text for para in doc.paragraphs)

    return text