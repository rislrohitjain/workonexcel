import os
import json
import logging
import polars as pl
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import traceback

# --- LOGGING CONFIGURATION ---
logging.basicConfig(
    filename='error_logs.txt',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_ROOT = "uploads"
EXPORT_ROOT = "exports"

def get_dated_path(root):
    path = os.path.join(root, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(path, exist_ok=True)
    return path

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        dir_path = get_dated_path(UPLOAD_ROOT)
        
        # Rename logic: datetime_timestamp
        ext = os.path.splitext(file.filename)[1]
        now = datetime.now()
        new_filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{int(now.timestamp())}{ext}"
        file_path = os.path.join(dir_path, new_filename)
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        df = pl.read_excel(file_path) if new_filename.endswith(('.xlsx', '.xls')) else pl.read_csv(file_path)
        
        return {
            "filename": new_filename,
            "path": file_path,
            "columns": df.columns,
            "total_rows": len(df)
        }
    except Exception as e:
        logging.error(f"Upload Error:\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/filter")
async def filter_data(file_path: str = Form(...), filters: str = Form(...), sorts: str = Form(...)):
    try:
        df = pl.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) else pl.read_csv(file_path)
        
        # 1. Apply Filters
        filter_list = json.loads(filters)
        for f in filter_list:
            col_name = f['col']
            op = f['op']
            val = f['val']
            if not val: continue
            
            selector = pl.col(col_name)
            clean_val = str(val).strip()
            
            if op == "=":
                df = df.filter(selector.cast(pl.Utf8).str.strip_chars() == clean_val)
            elif op == "like":
                df = df.filter(selector.cast(pl.Utf8).str.contains(clean_val))
            elif op == "!=":
                df = df.filter(selector.cast(pl.Utf8).str.strip_chars() != clean_val)
            elif op == ">":
                df = df.filter(selector.cast(pl.Float64) > float(val))
            elif op == "<":
                df = df.filter(selector.cast(pl.Float64) < float(val))

        # 2. Apply Sorting
        sort_list = json.loads(sorts)
        if sort_list:
            cols = [s['col'] for s in sort_list]
            desc = [s['desc'] for s in sort_list]
            df = df.sort(cols, descending=desc)

        # 3. Add Serial Number
        if len(df) > 0:
            # Check if S.No already exists to avoid "Duplicate Column" errors
            if "S.No" in df.columns:
                df = df.drop("S.No")
            
            # CORRECT SYNTAX: pl.Series (Capital S)
            df = df.insert_column(0, pl.Series("S.No", list(range(1, len(df) + 1))))
        
        return df.to_dicts()

    except Exception as e:
        logging.error(f"Filter Error at {file_path}:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export")
async def export_data(data: str = Form(...)):
    try:
        df = pl.from_dicts(json.loads(data))
        dir_path = get_dated_path(EXPORT_ROOT)
        filename = f"export_{datetime.now().strftime('%H%M%S')}.xlsx"
        path = os.path.join(dir_path, filename)
        df.write_excel(path)
        return {"path": path}
    except Exception as e:
        logging.error(f"Export Error:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)