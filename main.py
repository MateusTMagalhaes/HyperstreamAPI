from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from pydantic import ValidationError

from modelos import MyModel
import validações


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/uploadcsv/")
async def create_upload_file(file: UploadFile):
    if file.filename.endswith('.csv'):
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), sep=';')
        validações.check_header(df)

        # Retira espaços iniciais e finais de todos os valores
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        # Substitui valores inválidos por None
        df = df.applymap(lambda x: None if pd.isnull(x) or x == "" else x)
        
        data = df.to_dict('records')

        # Valida os dados
        for item in data:
            try:
                MyModel(**item)
            except ValidationError as e:
                # Raise a new exception with the ID included in the message
                raise HTTPException(status_code=400, detail=f"Erro na linha de ID {item['ID']}: {str(e)}")

        return {'data': data}
    else:
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido")
    #boot