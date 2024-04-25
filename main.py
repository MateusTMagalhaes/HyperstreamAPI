from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from pydantic import ValidationError

from modelos import MyModel
import validações, trees


app = FastAPI()

app.add_middleware(
    # Abrindo apenas para essa situação de hackaton
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/uploadcsv/")
async def create_upload_file(file: UploadFile):
    # Checa formato do arquivo
    if file.filename.endswith('.csv'):
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), sep=';')
        # Checa os headers
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



        return {
            'tree': trees.generate_apps_dict(df),
            'network': trees.generate_pastas_dict(df)
            }
    else:
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido")

@app.get("/testdata/")
async def get_test_data():
    return {
    "tree": {
        "name": "",
        "children": [
            {
                "name": "Cliente-FATURA-HSJ",
                "isBackup": False
            },
            {
                "name": "Cliente-FATURA-WFD-EMAIL",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-ACTION-EMAIL 1a VIA",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-CARGAECM-DIGITAL",
                                "isBackup": True,
                                "children": [
                                    {
                                        "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                                        "isBackup": True,
                                        "children": [
                                            {
                                                "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                                "isBackup": True
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Cliente-FATURA-ACTION-EMAIL 2a VIA",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-CARGAECM-DIGITAL",
                                "isBackup": True,
                                "children": [
                                    {
                                        "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                                        "isBackup": True,
                                        "children": [
                                            {
                                                "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                                "isBackup": True
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-WFD-EMAIL-ALEATORIO",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-INPUBLOG-DIGITAL",
                        "isBackup": True
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-WFD-ARMAZENAMENTO",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-CARGAECM-DIGITAL",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                                "isBackup": True,
                                "children": [
                                    {
                                        "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                        "isBackup": True
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-WFD-ARMAZENAMNTO-ALEATORIO",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-INPUBLOG-DIGITAL",
                        "isBackup": True
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-QUEBRAPDF-EMAIL",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-ACTION-EMAIL 1a VIA",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-CARGAECM-DIGITAL",
                                "isBackup": True,
                                "children": [
                                    {
                                        "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                                        "isBackup": True,
                                        "children": [
                                            {
                                                "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                                "isBackup": True
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Cliente-FATURA-ACTION-EMAIL 2a VIA",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-CARGAECM-DIGITAL",
                                "isBackup": True,
                                "children": [
                                    {
                                        "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                                        "isBackup": True,
                                        "children": [
                                            {
                                                "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                                "isBackup": True
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-QUEBRAPDF-ARMAZENAMENTO",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-CARGAECM-DIGITAL",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                                "isBackup": True,
                                "children": [
                                    {
                                        "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                        "isBackup": True
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-WFD-IMPRESSO-ALEATORIO",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-INPUBLOG-DIGITAL",
                        "isBackup": True
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-MOVERSPOOL-GRAFICA",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-WFD-IEEN",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-ACTION-EMAIL 1a VIA",
                                "isBackup": True,
                                "children": [
                                    {
                                        "name": "Cliente-FATURA-CARGAECM-DIGITAL",
                                        "isBackup": True,
                                        "children": [
                                            {
                                                "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                                                "isBackup": True,
                                                "children": [
                                                    {
                                                        "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                                        "isBackup": True
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "Cliente-FATURA-ACTION-EMAIL 2a VIA",
                                "isBackup": True,
                                "children": [
                                    {
                                        "name": "Cliente-FATURA-CARGAECM-DIGITAL",
                                        "isBackup": True,
                                        "children": [
                                            {
                                                "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                                                "isBackup": True,
                                                "children": [
                                                    {
                                                        "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                                        "isBackup": True
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Cliente-FATURA-WFD-IMPRESSO-ECM",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-CARGAECM-DIGITAL",
                                "isBackup": True,
                                "children": [
                                    {
                                        "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                                        "isBackup": True,
                                        "children": [
                                            {
                                                "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                                "isBackup": True
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Cliente-FATURA-MOVERSPOOL-ARQ. IMPI",
                        "isBackup": True
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-QUEBRAPDF-IMPRESSO",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-CARGAECM-DIGITAL",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                                "isBackup": True,
                                "children": [
                                    {
                                        "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                        "isBackup": True
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-MOVERSPOOL-ARQ.-EXCLUSAO",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-DPREPORT-FIMPROCESSO",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-DPREPORT-INDEXAR DADOS ANALITICO",
                                "isBackup": True
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-MOVERSPOOL-ARQ.-CSV-DVA",
                "isBackup": False
            },
            {
                "name": "Cliente-FATURA-START",
                "isBackup": False
            },
            {
                "name": "Cliente-FATURA-2VIA-HSJ",
                "isBackup": False
            },
            {
                "name": "Cliente-FATURA-2VIA-ACTION-EMAIL",
                "isBackup": False,
                "children": [
                    {
                        "name": "Cliente-FATURA-2VIA-DPREPORT-FIMPROCESSAMENTO",
                        "isBackup": True,
                        "children": [
                            {
                                "name": "Cliente-FATURA-2VIA-DPREPORT-INDEXAR-DADOS-ANALITICO",
                                "isBackup": True
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Cliente-FATURA-DVA-FILE-UPLOAD",
                "isBackup": False
            }
        ]
    },
    "network": {
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
}