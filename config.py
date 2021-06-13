import os

path_folder_raw = r'C:\Users\Olá\OneDrive - Fundacao Getulio Vargas - FGV\kim\Aulas ML\datasets\bases\raw'
path_folder_pprocessed = r'C:\Users\Olá\OneDrive - Fundacao Getulio Vargas - FGV\kim\Aulas ML\datasets\bases\preprocessed'

path_arquivo_brasil = os.path.join(path_folder_raw,'Brazil.csv')
path_arquivo_argentina = os.path.join(path_folder_raw,'Argentina.csv')
path_arquivo_barbados = os.path.join(path_folder_raw,'Barbados.csv')
path_arquivo_chile = os.path.join(path_folder_raw,'Chile.csv')
path_arquivo_cuba = os.path.join(path_folder_raw,'Cuba.csv')
path_arquivo_mexico = os.path.join(path_folder_raw,'Mexico.csv')
path_arquivo_uruguai = os.path.join(path_folder_raw,'Uruguay.csv')

path_arquivo_pprocessed = os.path.join(path_folder_pprocessed,'preprocessed.csv')