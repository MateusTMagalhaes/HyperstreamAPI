from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from typing import List
import io

app = FastAPI()

@app.post("/uploadcsv/")
async def create_upload_file(file: UploadFile):
    if file.filename.endswith('.csv'):
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), sep=';')
        # Replace NaN values with None, which is JSON serializable
        df = df.where(pd.notnull(df), None)
        data = df.to_dict('records')
        return {'data': data}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
#run?