import os
import uuid
import logging
import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from file_reader import TextExtractor

app = FastAPI()

BASE_UPLOAD_DIR = "uploads"

# Ensure uploads folder exists
os.makedirs(BASE_UPLOAD_DIR, exist_ok=True)
# Setting logging levels
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@app.post("/ocr-api/pdf-to-text")
async def upload_pdf(file: UploadFile = File(...)):
    # Validate PDF mime type
    logging.info("Uploading Your PDF")
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    # Generate a unique folder name using UUID
    unique_folder = str(uuid.uuid4())
    folder_path = os.path.join(BASE_UPLOAD_DIR, unique_folder)
    # Create the unique folder
    os.makedirs(folder_path, exist_ok=True)
    # Define full file path inside the unique folder
    file_path = os.path.join(folder_path, file.filename) # type: ignore
    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text_extractor = TextExtractor() 
    pdf_text = " ".join(text_extractor.extract_text(file_path).split())
    logging.info(pdf_text)
    logging.info(f"File saved at: {unique_folder}")
    return JSONResponse(content={"fileId": unique_folder, 
                                "text": pdf_text
                                })


@app.delete("/delete-file/{file_id}")
def delete_uploaded_ffile(file_id: str):
    UPLOAD_DIR = Path("uploads")
    target_folder = UPLOAD_DIR / file_id

    if not target_folder.exists() or not target_folder.is_dir():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        shutil.rmtree(target_folder)
        return JSONResponse({
            "sucess" : True, 
            "message": f"File '{file_id}' deleted successfully",
            })
    # File ka naam bhi return karna hai , jo delete hua.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting folder: {str(e)}")