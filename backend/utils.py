# backend/utils.py
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def submit_to_n8n(files: dict, metadata: dict, webhook_url: str) -> dict:
    """
    Sends uploaded files and metadata to an n8n webhook endpoint.
    """
    data = {"metadata": json.dumps(metadata)}

    # Build multipart/form-data payload
    files_to_send = []
    for name, file in files.items():
        if not file:
            continue
        try:
            files_to_send.append((name, (file.name, file, file.type)))
        except Exception as e:
            logger.error(f"Error preparing file '{name}': {e}")

    try:
        resp = requests.post(webhook_url, data=data, files=files_to_send, timeout=30)
        if resp.status_code == 200:
            logger.info("✅ Successfully sent loan data to n8n.")
            return {"status": "success", "message": "Data sent successfully", "response": resp}
        else:
            logger.warning(f"⚠️ n8n responded with {resp.status_code}: {resp.text}")
            return {"status": "error", "message": f"n8n error: {resp.status_code}", "response": resp}

    except requests.Timeout:
        logger.error("⏰ Request to n8n timed out.")
        return {"status": "error", "message": "Request timed out", "response": None}

    except Exception as e:
        logger.exception(f"❌ Unexpected error sending data to n8n: {e}")
        return {"status": "error", "message": str(e), "response": None}
