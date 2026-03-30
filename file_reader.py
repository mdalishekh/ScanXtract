import PyPDF2
import docx
from ocr import ocr_image, ocr_pdf


class FileExtractor:
    """
    Contains methods for extracting text from various file formats.
    """
    def extract_pdf_text(self, file_path: str) -> str:
        """Extracts text from a PDF file."""
        try:
            text = ""
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = "".join(
                    (page.extract_text() or "") + "\n"
                    for page in reader.pages
                )
            if not text.strip():
                return ocr_pdf(file_path) or ""  # type: ignore
            return text.strip()
        except Exception as e:
            return ""

    def extract_docx_text(self, file_path: str) -> str:
        """Extracts text from a DOCX file using python-docx."""
        doc = docx.Document(file_path)
        return "".join(para.text for para in doc.paragraphs)

    def extract_txt_text(self, file_path: str) -> str:
        """Extracts text from a TXT file."""
        with open(file_path, "r", encoding="utf-8") as txt_file:
            return txt_file.read().strip()
        
    def extract_image_text(self, file_path: str) -> str:
        return ocr_image(file_path) or ""  # type: ignore
            

class TextExtractor(FileExtractor):
    """
    Derived class that handles file format checking and calls appropriate extraction methods.
    """
    def extract_text(self, file_path: str) -> str:
        """Reads text from various file formats (PDF, DOCX, TXT, Images)."""
        if file_path.endswith(".pdf"):
            return self.extract_pdf_text(file_path)
        elif file_path.endswith(".docx"):
            return self.extract_docx_text(file_path)
        elif file_path.endswith(".txt"):
            return self.extract_txt_text(file_path)
        elif file_path.endswith((".png", ".jpg", ".jpeg")):
            return self.extract_image_text(file_path)
        else:
            return "Unsupported file format."