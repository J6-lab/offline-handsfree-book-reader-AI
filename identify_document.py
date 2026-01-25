import os

def identify_document_type(file_path):
    if not os.path.exists(file_path):
        return "File not found"

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        return "PDF Document"
    elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]:
        return "Image Document"
    elif ext in [".doc", ".docx"]:
        return "Word Document"
    elif ext == ".txt":
        return "Text Document"
    else:
        return "Unknown Document Type"
