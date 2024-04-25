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

@app.get("/testdata/")
async def get_test_data():
    return {
    "children": [
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\HSJ\\ENTRADA\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\BV\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\HSJ\\ENTRADA\\BKP\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA\\",
            "children": [
                {
                    "name": "\\\\HSLAN028-0\\SAIDAS_BV_FAT\\PDF_UNICO\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\ACTION\\ENTRADA\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA\\",
            "children": [
                {
                    "name": "\\\\HSLAN028-0\\SAIDAS_BV_FAT\\ALEATORIOS\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\INPUTBLOG\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA\\",
            "children": [
                {
                    "name": "\\\\HSLAN028-0\\SAIDAS_BV_FAT\\PDF_UNICO\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\CARGA_ECM\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA\\",
            "children": [
                {
                    "name": "\\\\HSLAN028-0\\SAIDAS_BV_FAT\\ALEATORIOS\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\INPUTBLOG\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\SAIDAS\\PDF_UNICO\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\BV\\FATURA\\SAIDAS\\ECM\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\ACTION\\ENTRADA\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\SAIDAS\\PDF_UNICO\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\BV\\FATURA\\SAIDAS\\ECM\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\CARGA_ECM\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\ACTION\\ENTRADA\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\CARGA_ECM\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\INPUTBLOG\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\BV\\FATURA\\SAIDAS\\ALEATORIOS\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\PROCESSADOS\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\CARGA_ECM\\",
            "children": [
                {
                    "name": "E:\\APLICATIVO\\BV\\FATURA\\ECM_LOAD\\Configs\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\DPREPORT\\DPR_FIM_PROCESSAMENTO\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\DPREPORT\\DPR_FIM_PROCESSAMENTO\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\DPREPORT\\DPR_INDEXAR_DADOS_ANALITICO\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA\\",
            "children": [
                {
                    "name": "\\\\HSLAN028-0\\SAIDAS_BV_FAT\\ALEATORIOS\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\INPUTBLOG\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA_PNET_IEEN\\",
            "children": [
                {
                    "name": "\\\\HSLAN028-0\\SAIDAS_BV_FAT\\PDF_UNICO\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\ACTION\\ENTRADA\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA_PNET_IEEN\\",
            "children": [
                {
                    "name": "\\\\HSLAN028-0\\SAIDAS_BV_FAT\\PDF_UNICO\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\CARGA_ECM\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\MOVERSPOOL\\MOV_ARQGRAFICA\\",
            "children": [
                {
                    "name": "\\\\ft001\\VALID\\BV\\PRD\\upload\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA_PNET_IEEN\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA_PNET_IEEN\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA_PNET_IMPI_ECM\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\SAIDAS\\PDF_UNICO\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\BV\\FATURA\\SAIDAS\\ECM\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\CARGA_ECM\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\DPREPORT\\DPR_FIM_PROCESSAMENTO\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\ARMAZEM\\relatorios-regras",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\ARMAZEM\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\START\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\BV\\FATURA\\FORMATAR_FATURA\\PRINTNET\\ENTRADA\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\START\\BKP\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA_2VIA\\HSJ\\ENTRADA\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\BV\\FATURA_2VIA\\ACTION\\ENTRADA\\"
                },
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA_2VIA\\HSJ\\ENTRADA\\BKP\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA_2VIA\\ACTION\\ENTRADA\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA_2VIA\\DPREPORT\\DPR_FIMPRCESSAMENTO\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA_2VIA\\DPREPORT\\DPR_FIMPRCESSAMENTO\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA_2VIA\\DPREPORT\\DPR_INDEXAR_DADOS_ANALITICO\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA_2VIA\\DPREPORT\\DPR_INDEXAR_DADOS_ANALITICO\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA_2VIA\\PROCESSADOS\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\DPREPORT\\DPR_INDEXAR_DADOS_ANALITICO\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\PROCESSADOS\\"
                }
            ]
        },
        {
            "name": "\\\\FT002\\PARCEIROS\\Cliente\\PRD\\DOWNLOAD\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\ARMAZEM\\"
                }
            ]
        },
        {
            "name": "E:\\PRODUCAO\\Cliente\\FATURA\\ACTION\\ENTRADA\\",
            "children": [
                {
                    "name": "E:\\PRODUCAO\\Cliente\\FATURA\\CARGA_ECM\\"
                }
            ]
        }
    ]
}