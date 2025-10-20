import pandas as pd

def process_uploaded_file(file_dict):
    """Process and validate multiple uploaded files"""
    results = {}

    for name, file in file_dict.items():
        if file is None:
            continue

        try:
            if file.name.lower().endswith(".csv"):
                df = pd.read_csv(file)
                if df.empty:
                    results[name] = {"status": "error", "message": "File is empty.", "data": None}
                else:
                    results[name] = {"status": "success", "data": df}
            elif file.name.lower().endswith(".pdf"):
                # For now, we won’t parse PDF; just acknowledge upload.
                results[name] = {"status": "success", "data": None}
            else:
                results[name] = {"status": "error", "message": "Unsupported file type.", "data": None}
        except Exception as e:
            results[name] = {"status": "error", "message": str(e), "data": None}

    return results
