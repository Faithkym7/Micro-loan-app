# backend/Data/data_logic.py
import pandas as pd
import requests
import json
import streamlit as st
import io
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

def process_uploaded_file(file_dict):
    """Process and validate multiple uploaded files (CSV + PDF OCR)."""
    results = {}

    for name, file in file_dict.items():
        if file is None:
            continue

        try:
            filename = file.name.lower()

            # --- CSV Handling ---
            if filename.endswith(".csv"):
                df = pd.read_csv(file)
                if df.empty:
                    results[name] = {
                        "status": "error",
                        "message": "File is empty.",
                        "data": None,
                        "preview": "empty csv"
                    }
                else:
                    results[name] = {
                        "status": "success",
                        "data": df,
                        "preview": f"CSV with {len(df)} rows and {len(df.columns)} columns"
                    }

            # --- PDF Handling (OCR) ---
            elif filename.endswith(".pdf"):
                try:
                    # Convert PDF pages to images
                    pdf_bytes = file.read()
                    images = convert_from_bytes(pdf_bytes)

                    # Run OCR on each page
                    extracted_text = ""
                    for page_number, img in enumerate(images, start=1):
                        text = pytesseract.image_to_string(img)
                        extracted_text += f"\n\n--- Page {page_number} ---\n{text.strip()}"

                    if extracted_text.strip():
                        results[name] = {
                            "status": "success",
                            "data": extracted_text,
                            "preview": f"Extracted text from {len(images)} page(s)"
                        }
                    else:
                        results[name] = {
                            "status": "error",
                            "message": "No text detected via OCR.",
                            "data": None,
                            "preview": "blank pdf"
                        }

                except Exception as ocr_err:
                    results[name] = {
                        "status": "error",
                        "message": f"OCR failed: {ocr_err}",
                        "data": None,
                        "preview": "ocr error"
                    }

            else:
                results[name] = {
                    "status": "error",
                    "message": "Unsupported file type.",
                    "data": None,
                    "preview": "unsupported"
                }

        except Exception as e:
            results[name] = {
                "status": "error",
                "message": str(e),
                "data": None,
                "preview": "error"
            }

    return results


def submit_loan_application(files, metadata):
    """
    Send files + metadata to n8n webhook with progress feedback.
    Stores response JSON in st.session_state['latest_loan_data'] for chat usage.
    Returns a dict with status, message, and optionally response data.
    """
    webhook_url = st.secrets.get("n8n", {}).get("webhook_url")
    if not webhook_url:
        return {"status": "error", "message": "Missing webhook URL in secrets.toml"}

    # Prepare multipart fields
    fields = {"metadata": json.dumps(metadata)}

    for name, file in files.items():
        if not file:
            continue
        try:
            mime_type = getattr(file, "type", "application/octet-stream")
            # Convert Streamlit UploadedFile to proper file-like object
            file_bytes = io.BytesIO(file.getbuffer())
            fields[name] = (file.name, file_bytes, mime_type)
        except Exception as e:
            st.warning(f"⚠️ Skipping file {name}: {e}")

    # Create MultipartEncoder
    m = MultipartEncoder(fields=fields)

    # Progress bar for Streamlit
    progress_bar = st.progress(0)

    def monitor_callback(monitor):
        progress = min(int((monitor.bytes_read / monitor.len) * 100), 100)
        progress_bar.progress(progress)

    monitor = MultipartEncoderMonitor(m, monitor_callback)

    # Spinner while sending
    with st.spinner("Submitting loan application..."):
        try:
            response = requests.post(
                webhook_url,
                data=monitor,
                headers={"Content-Type": monitor.content_type},
                timeout=60  # increase timeout for large uploads
            )

            if response.status_code == 200:
                try:
                    # Parse JSON response
                    response_json = response.json() if response.headers.get("Content-Type", "").startswith("application/json") else None
                    
                    # Store in session state for chat
                    if response_json:
                        st.session_state["latest_loan_data"] = response_json

                    return {
                        "status": "success",
                        "message": "Loan data sent successfully.",
                        "data": response_json
                    }
                except Exception:
                    return {"status": "success", "message": "Loan data sent successfully."}
            else:
                return {
                    "status": "error",
                    "message": f"n8n responded with {response.status_code}: {response.text}"
                }

        except requests.Timeout:
            return {"status": "error", "message": "Request timed out."}
        except Exception as e:
            return {"status": "error", "message": str(e)}