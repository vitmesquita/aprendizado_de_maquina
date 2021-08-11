import sys
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
sys.path.append('..')
import pandas as pd
from config import *

# Leitura de dados
df = pd.read_csv(path_arquivo_pprocessed)

# Separação de variáveis
features = ['marital', 'y_educa', 'gender', 'age','n_children', 'takes_medicine', 'kind_health_ins',
            'functional_score','cover_score', 'flexibility_score','work_life']

cat_col = ['marital','gender','kind_health_ins']

# Transformando em colunas dummy
df_cluster = pd.get_dummies(df[features],columns=cat_col,drop_first=True)

# Normalizando scores (via divisao pelo maximo)
dic = {'max_func_score':df_cluster['functional_score'].max(),
       'max_cover_score':df_cluster['cover_score'].max(),
       'max_flex_score':df_cluster['flexibility_score'].max()}

df_cluster.loc[:,'functional_score'] = df_cluster['functional_score']/df_cluster['functional_score'].max()
df_cluster.loc[:,'cover_score'] = df_cluster['cover_score']/df_cluster['cover_score'].max()
df_cluster.loc[:,'flexibility_score'] = df_cluster['flexibility_score']/df_cluster['flexibility_score'].max()

# Normalizando via standartscaler
X = df_cluster.loc[:,['y_educa','age','n_children','work_life']]
scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

df_cluster.loc[:,['y_educa','age','n_children','work_life']] = X_scaled

# Clusterização
kmeans = KMeans(n_clusters=6, random_state=0).fit(df_cluster)
df['labels'] = kmeans.labels_

df.to_csv(path_arquivo_cluster)