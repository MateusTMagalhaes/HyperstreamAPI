from fastapi import FastAPI, UploadFile, HTTPException
import pandas as pd
import io
from pydantic import ValidationError

from modelos import MyModel
import validações


app = FastAPI()

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

        # Criar um dicionário para armazenar a estrutura de árvore
        tree = {"children": []}

        # Função para adicionar um nó à árvore
        def add_node(parent, node):
            for child in parent['children']:
                if child['name'] == node:
                    return child
            if node:
                new_child = {"name": node, "children": []}
                parent['children'].append(new_child)
                return new_child

        # Adicionar todos os nós à árvore
        for _, row in df.iterrows():
            parent_node = add_node(tree, row['PastaOrigem'])
            add_node(parent_node, row['PastaDestino'])

        return {'data': tree}
    else:
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido")