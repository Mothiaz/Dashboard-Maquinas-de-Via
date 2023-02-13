import pandas as pd

class DataSchema:
    EQUIP = 'equip'
    REPAIRTIME = 'repairTime'
    FALHA = 'falha'
    DATE = 'date'
    TIPO = 'tipo'
    DESCRICAO = 'descricao'
    OM = 'om'
    YEAR = 'year'
    MONTH = 'month'
    FLEET = 'fleet'
    SYSTEM = 'sistema'
    SET = 'conjunto'
    ITEM = 'item'
    PROBLEM = 'problema'


def load_data(path: str) -> pd.DataFrame:
    #carregar documento
    data = pd.read_excel(path, 'ClasseDeFalhas', skiprows=1, dtype={'OM': str}, parse_dates=['Dia'])
    data.columns = data.columns.str.lower()  # colunas minusculas
    data.rename(columns={'equip.': DataSchema.EQUIP, 'retenção': DataSchema.REPAIRTIME,
                         'falha?': DataSchema.FALHA, 'dia': DataSchema.DATE,
                         'tipo': DataSchema.TIPO, 'descrição': DataSchema.DESCRICAO,
                         'om': DataSchema.OM, 'frota': DataSchema.FLEET},
                inplace=True)  # renomeia colunas
    data = data.iloc[:, 0:18]  # seleciona as primeiras 19 colunas: ate 'problema'
    data.drop(columns=['ano', 'mês'], inplace=True)  # dropa colunas inuteis
    # data.loc[:, 'om'] = data['om'].astype(str)  # redefine o tipo de dado da coluna 'om' para string
    # data['date'] = pd.to_datetime(data['date'], format='%d/%m/%y')  # formato da coluna data
    data['repairTime'] = data['repairTime'] * 24  # repairTime como valor
    # data = data[data['sistema'].notnull()]  # retira celulas vazias
    # data = data[data['sistema'] != '***']
    data.dropna(subset='om', inplace=True)
    data.fillna(value='Em Diagnostico', inplace=True)

    #GERANDO COLUNAS YEAR E MONTH

    data[DataSchema.YEAR] = data[DataSchema.DATE].dt.year.astype(str)
    data[DataSchema.MONTH] = data[DataSchema.DATE].dt.month.astype(str)

    return data