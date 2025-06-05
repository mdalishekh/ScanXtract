
# 🚀 ScanXtract v1.1 – Fast & Lightweight OCR API

**ScanXtract** is a blazing-fast, lightweight OCR engine built with FastAPI and Docker. It extracts text from PDFs and images in seconds — no clutter, no bloat. Whether you're automating workflows or building tools, **ScanXtract** is your plug-and-play microservice.

---

## ✨ What's New in v1.1

- ⚡ **Faster Text Extraction**: Optimized processing pipeline for quicker results.
- 🧠 **Reduced Memory Usage**: Enhanced efficiency, especially with large scanned PDFs.

---

## 🔁 Refer to Our Previous Version

For reference, you can check out our earlier version here:  
🔗 [ScanXtract v1.0 Documentation](https://hackmd.io/@mdalishekh/B1k8hpCbll)

---

## ❓ Why Use ScanXtract?

- ⭐ 100% Free to use
- ⚡ Lightweight, fast, and efficient
- 🚫 No usage limits or throttling
- 👨‍💻 Built with developers and students in mind

---

## 👥 Who Is It For?

ScanXtract is perfect for:

- Developers building document processing pipelines
- Students working on ML/Data Science projects
- Backend engineers needing quick OCR integration
- Anyone tired of bulky, bloated OCR tools

It’s built to **save your time, effort, and system resources** — with minimal setup.

---

## 🐳 How To Use (Run with Docker)

You can get started instantly with Docker. No installation. No setup. Just plug and play.


### Pull the Image

```bash
docker pull mdalishekh/scanxtract:v1.1
```

### Run the Container

```bash
docker run -d --name scanxtract-engine -p 8000:8000 mdalishekh/scanxtract:v1.1
```

Or customize the container name and port:

```bash
docker run -d --name <your-container-name> -p <your-port>:8000 mdalishekh/scanxtract:v1.1
```

---

## ⚙️ Features / API Endpoints

### 1. Extract Text from PDF

**`POST /ocr-api/pdf-to-text`**

- **Body Type:** `form-data`
- **Key:** `file` (PDF only)

**✅ Response (JSON):**

```json
{
  "fileId": "f0cfe9c4-0d65-4d69-82f8-275f44dee41d",
  "text": "Your extracted text goes here"
}
```

---

### 2. Extract Text from Image

**`POST /ocr-api/image-to-text`**

- **Body Type:** `form-data`
- **Key:** `file` (image formats like PNG, JPG, etc.)

**✅ Response (JSON):**

```json
{
  "fileId": "fe9c4-0d65-4d69-82f8-275f44dee41d",
  "text": "Your extracted text goes here"
}
```

---

### 3. Delete Uploaded File

**`DELETE /delete-file/<your-file-id>`**

- **Path Param:** UUID (`fileId` returned by upload APIs)

**✅ Response (JSON):**

```json
{
  "success": true,
  "message": "File 'Scanned Air.pdf' deleted successfully",
  "fileId": "9b81b4ce-327f-4f95-9799-c41f50d0b519"
}
```

---

## 🧪 Example Code to Call APIs Using Python

```python
import requests

BASE_URL = "http://localhost:8000"  # Change this if hosted elsewhere

def extract_text_from_pdf(pdf_path: str):
    url = f"{BASE_URL}/ocr-api/pdf-to-text"
    with open(pdf_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    return response.json()

def extract_text_from_image(image_path: str):
    url = f"{BASE_URL}/ocr-api/image-to-text"
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    return response.json()

def delete_uploaded_file(file_id: str):
    url = f"{BASE_URL}/delete-file/{file_id}"
    response = requests.delete(url)
    return response.json()
```
----
```python
if __name__ == "__main__":
    # 1. Extract from PDF
    pdf_result = extract_text_from_pdf("your-path/sample.pdf")
    print("PDF Result:", pdf_result)

    # 2. Extract from Image
    image_result = extract_text_from_image("your-path/sample.png")
    print("Image Result:", image_result)

    # 3. Delete File using fileId (from any of above results)
    file_id = pdf_result.get("fileId")
    if file_id:
        delete_result = delete_uploaded_file(file_id)
        print("Delete Result:", delete_result)
```

---

## 🔮 Coming Soon

- 📄 PDF page selection
- 📊 Usage analytics
- ⚙️ Enhanced speed and smarter extraction engine

---

#### Made by @mdalishekh 😊
