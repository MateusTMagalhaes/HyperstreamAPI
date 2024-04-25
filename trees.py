# Função para gerar visualização de pastas
def generate_pastas_dict(df):
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

def generate_apps_dict(df):
  tree = {"name": "flare", "children": []}

  def is_origin(pasta_origem, df):
    if df['PastaDestino'].isin([pasta_origem]).any() or df['PastaBackup'].isin([pasta_origem]).any():
        print(False)
        return False
    print(True)
    return True


  # Tem filhos?
  def has_children(pasta_origem, df, current_dict, isBackup):
    for _, row in df.iterrows():
      nome_ch = row["Nome"]
      pasta_origem_ch = row["PastaOrigem"] if row["PastaOrigem"] else None
      pasta_destino_ch = row["PastaDestino"] if row["PastaDestino"] else None
      pasta_backup_ch = row["PastaBackup"] if row["PastaBackup"] else None

      if pasta_origem == pasta_origem_ch:
        # Adiciona o children
        if 'children' in current_dict:
          current_dict['children'].append({'name': nome_ch})
        else:
          current_dict['children'] = [{'name': nome_ch}]
        current_dict["children"][-1]['isBackup'] = isBackup
        has_children(pasta_destino_ch, df, current_dict['children'][-1], False)
        has_children(pasta_backup_ch, df, current_dict['children'][-1], True)

  for _, row in df.iterrows():
    nome = row["Nome"]
    pasta_origem = row["PastaOrigem"] if row["PastaOrigem"] else None
    pasta_destino = row["PastaDestino"] if row["PastaDestino"] else None
    pasta_backup = row["PastaBackup"] if row["PastaBackup"] else None

    if is_origin(pasta_origem, df):
      # Adiciona o children

      tree['children'].append({'name': nome})
      tree["children"][-1]['isBackup'] = False

      # Começa o depth
      has_children(pasta_destino, df, tree["children"][-1], False)
      has_children(pasta_backup, df, tree["children"][-1], True)

  return tree