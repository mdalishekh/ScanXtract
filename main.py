import os
import uuid
import logging
import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from file_reader import TextExtractor

# Initiating FastAPI instance
app = FastAPI()

BASE_UPLOAD_DIR = "uploads"

# Ensure uploads folder exists
os.makedirs(BASE_UPLOAD_DIR, exist_ok=True)
# Setting logging levels
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# REST API only for PDF files OCR
@app.post("/ocr-api/pdf-to-text")
async def upload_pdf(file: UploadFile = File(...)) -> JSONResponse:
    # Validate PDF mime type
    logging.info(f"Uploading Your PDF :- {file.filename}")
    if file.content_type != "application/pdf":
        logging.error("Invalid file type uploaded.")
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
    logging.info(f"File saved at: {unique_folder}\n")
    logging.info(pdf_text)
    # Return the unique file name and extracted text  
    return JSONResponse(content={
        "fileId": unique_folder, 
        "text": pdf_text})


# REST API only for Image files OCR
@app.post("/ocr-api/image-to-text")
async def upload_image(file: UploadFile = File(...)) -> JSONResponse:
    # Validate image mime type
    logging.info(f"Uploading Your Image :- {file.filename}")
    allowed_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only JPEG and PNG image files are allowed.")
    # Generate a unique folder name using UUID
    unique_folder = str(uuid.uuid4())
    folder_path = os.path.join(BASE_UPLOAD_DIR, unique_folder)
    os.makedirs(folder_path, exist_ok=True)
    # Define full file path
    file_path = os.path.join(folder_path, file.filename)  # type: ignore
    # Save the uploaded image file
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Performing OCR on Image file
    text_extractor = TextExtractor() 
    image_text = " ".join(text_extractor.extract_text(file_path).split())
    logging.info(f"File saved at: {unique_folder}\n")
    logging.info(image_text)
    # Return the unique file name and extracted text
    return JSONResponse(content={
        "fileId": unique_folder,
        "text": image_text})


# REST API for Image files and PDF OCR
@app.post("/ocr-api/extract-text")
async def upload_scanned_file(file: UploadFile = File(...)) -> JSONResponse:
    """
    Unified OCR API for scanned files.
    Supports: PDF, JPEG, PNG

    Returns:
        JSON: File ID, file name, type, and extracted text
    """
    # logging.info(f"Uploading File: {file.filename}")

    allowed_pdf = "application/pdf"
    allowed_images = ["image/jpeg", "image/png", "image/jpg"]
    all_allowed_types = [allowed_pdf] + allowed_images

    # Validate file type
    if file.content_type not in all_allowed_types:
        raise HTTPException(status_code=400, detail="Only PDF, JPEG, or PNG files are allowed.")

    # Generate a unique folder
    unique_folder = str(uuid.uuid4())
    folder_path = os.path.join(BASE_UPLOAD_DIR, unique_folder)
    os.makedirs(folder_path, exist_ok=True)

    # Save the uploaded file
    file_path = os.path.join(folder_path, file.filename)  # type: ignore
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Determine file type for logging only
    file_type = "PDF" if file.content_type == allowed_pdf else "Image"
    logging.info(f"Processing as {file_type}")
    # Extract text
    text_extractor = TextExtractor()
    extracted_text = text_extractor.extract_text(file_path)
    clean_text = " ".join(extracted_text.split())
    # Logging
    logging.info(f"File saved at: {folder_path}")
    logging.info(clean_text)
    # Response
    return JSONResponse(content={
        "fileId": unique_folder,
        "fileName": file.filename,
        "fileType": file.content_type,
        "text": clean_text
    })



# Delete Specific file / folder 
@app.delete("/delete-file/{file_id}")
def delete_uploaded_file(file_id: str):
    UPLOAD_DIR = Path("uploads")
    target_folder = UPLOAD_DIR / file_id

    if not target_folder.exists() or not target_folder.is_dir():
        logging.error(f"No such file found with file_id: {file_id}")
        raise HTTPException(status_code=404, detail="File not found")
    files = os.listdir(target_folder)
    try:
        shutil.rmtree(target_folder)
        logging.info(f"File deleted succesfully :- {files[0]}")
        return JSONResponse({
        "sucess" : True, 
        "message": f"File '{files[0]}' deleted successfully",
        "fileId" : file_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")