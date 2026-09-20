from docx import Document
from pathlib import Path

def replace_text(document, old_text, new_text):
    for paragraph in document.paragraphs:
        if old_text in paragraph.text:
            paragraph/text = paragraph.text.replace(old_text, new_text)

def export_to_word(text, file_path, template_path):
    document = Document(template_path)
    replace_text(document, '{{date}}', date)
    document.save(file_path)