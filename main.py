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

        def generate_json(df=df):
            tree = {"children": []}
            for index, row in df.iterrows():
                pasta_origem = row["PastaOrigem"].strip()
                pasta_destino = row["PastaDestino"].strip() if row["PastaDestino"] else None
                pasta_backup = row["PastaBackup"].strip() if row["PastaBackup"] else None

                if not any([pasta_origem, pasta_destino, pasta_backup]):
                    continue 

                node_origem = {"name": pasta_origem}

                if pasta_destino:
                    node_destino = {"name": pasta_destino}
                    node_origem["children"] = [node_destino]

                if pasta_backup:
                    node_backup = {"name": pasta_backup}
                    if "children" not in node_origem:
                        node_origem["children"] = []
                    node_origem["children"].append(node_backup)

                tree["children"].append(node_origem)
            return tree
        
        tree = generate_json()

        print(tree)
        return tree
    else:
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido")