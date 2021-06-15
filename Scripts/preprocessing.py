# Import de bibliotecas

import sys
sys.path.append('..')
import pandas as pd
from config import *
import math

def preprocessing():
    #Leitura de arquivos

    df_brasil = pd.read_csv(path_arquivo_brasil,encoding = 'latin-1')
    df_mexico = pd.read_csv(path_arquivo_mexico,encoding = 'latin-1')
    df_chile = pd.read_csv(path_arquivo_chile,encoding = 'latin-1')
    df_argentina = pd.read_csv(path_arquivo_argentina,encoding = 'latin-1')
    df_barbados = pd.read_csv(path_arquivo_barbados,encoding = 'latin-1')
    df_uruguai = pd.read_csv(path_arquivo_uruguai,encoding = 'latin-1')

    # Escolha de features

    features = ['folio','marital','yeduca','c18','a01b','a06n','a11a','a18','d01a',
            'd01b','d01c','d02','d03','d04','d05','d06','d07','d08','d09','d10','d11',
            'e07b','f011','f02a','f02b','f02c','f02d','f02e','f02f','f02g','f02h','f02i',
            'f02j','f02k','f04','h01','h04','h07','l01a','l02','l03d','l03i']
    df_brasil = df_brasil[features]
    features = ['folio','marital','yeduca','c18','a01b','a06n','a11a','a18','d01a',
             'd01b','d01c','d02','d03','d04','d05','d06','d07','d08','d09','d10','d11',
             'e07b','f011','f02a','f02b','f02c','f02d','f02e','f02f','f02g','f02h','f02i',
             'f02j','f02k','f04','h01','h04','h07','l01a','l02','l03d','l03i']
    df_chile = df_chile[features]
    features = ['folio','marital','yeduca','c18','a01b','a06n','a11a','a18','d01a',
            'd01b','d01c','d02','d03','d04','d05','d06','d07','d08','d09','d10','d11',
            'e07b','f011','f02a','f02b','f02c','f02d','f02e','f02f','f02g','f02h','f02i',
            'f02j','f02k','f04','h01','h04','h07','l01a','l02','l03d','l03i']

    df_argentina = df_argentina[features]
    df_barbados = df_barbados[features]
    df_uruguai = df_uruguai[features]

    df_barbados['country'] = 'Barbados'
    df_uruguai['country'] = 'Uruguai'
    df_argentina['country'] = 'Argentina'
    df_chile['country'] = 'Chile'
    df_brasil['country'] = 'Brasil'

    # Renomeando features

    rename_colunas = ['folio','marital','y_educa','gender','age','last_level_school','religion','n_children',
                  'diff1','diff2','diff3','diff4','diff5','diff6','diff7','diff8','diff9','diff10',
                  'diff11','diff12','diff13','takes_medicine','kind_health_ins','cover1','cover2',
                  'cover3','cover4','cover5','cover6','cover7','cover8','cover9','cover10','cover11',
                  'times_hospital','payd_job','age_begin_working','age_stop_working','flex1','flex2','flex3','flex4','country']
    df_brasil.columns = rename_colunas
    df_argentina.columns = rename_colunas
    df_chile.columns = rename_colunas
    df_uruguai.columns = rename_colunas
    df_barbados.columns = rename_colunas

    # Concatenando dataframes

    data = pd.concat([df_brasil,df_argentina,df_chile,df_uruguai,df_barbados])

    # Criando feature de score funcional
    for i in range(1,14):    
        data['diff'+str(i)] = data['diff'+str(i)].map({2:0,1:1,3:1,4:1,9:1})
        
    data['functional_score'] = data[['diff1','diff2','diff3','diff4','diff5','diff6','diff7',
                                    'diff8','diff9','diff10','diff11','diff12','diff13']].sum(axis=1)

    data.drop(['diff1','diff2','diff3','diff4','diff5','diff6','diff7',
                                    'diff8','diff9','diff10','diff11','diff12','diff13'],axis=1,inplace=True)

    # Criando feature de cobertura do plano
    for i in range(1,12):
        data['cover'+str(i)] = data['cover'+str(i)].map({1:2,2:1,3:0,8:0,9:0})
        
    data['cover_score'] = data[['cover1','cover2','cover3','cover4','cover5','cover6',
                            'cover7','cover8','cover9','cover10','cover11']].sum(axis=1)

    data.drop(['cover1','cover2','cover3','cover4','cover5','cover6',
                            'cover7','cover8','cover9','cover10','cover11'],axis=1,inplace=True)

    # Criando feature de score de flexibilidade
    data['flex1'] = data['flex1'].map({10:10,95:0,96:0,98:0})
    for i in range(2,4):
        data['flex'+str(i)] = data['flex'+str(i)].map({10:10,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,95:0,96:0,98:0})
        
    data['flexibility_score'] = data[['flex1','flex2','flex3','flex4']].sum(axis=1)

    data.drop(['flex1','flex2','flex3','flex4'],axis=1,inplace=True)

    data['takes_medicine'] = data['takes_medicine'].map({1:1,2:0})

    # Consertando o index e a coluna de id

    data['folio'] = range(len(data))
    data = data.reset_index(drop=True)

    # Consertando valores das features

    # Marital
    data['marital'] = data['marital'].map({9:'Others',0:'Others',1:'Others',2:'Married',3:'Others',4:'Widowed',5:'Others',6:'Others'})
    data.loc[data['marital'].isnull(),['marital']]='Others'

    # Y_educa
    data.dropna(subset=['y_educa'],inplace=True)
    data.loc[data['y_educa']>20,['y_educa']] = math.ceil(data.loc[data['y_educa']<=30,['y_educa']].mean())

    # Last_level_school
    data['last_level_school'] = data['last_level_school'].map({0:1,1:1,2:1,3:2,4:2,5:2,6:2,7:3,8:3,9:3,98:1})
    data.loc[data['last_level_school'].isnull(),['last_level_school']]=1

    # Religion
    data['religion']=data['religion'].map({1:'Roman Catholic',2:'Anglican',3:'Others',
                                       4:'Others',5:'Others',6:'Others',7:'Others',8:'Others',9:'Others'})
    data.loc[data['religion'].isnull(),['religion']] = 'Others'
    
    # n_children
    data.loc[data['n_children']==98,['n_children']]=0
    data.dropna(subset=['n_children'],inplace=True)

    # takes_medicine
    data.loc[data['takes_medicine'].isnull(),['takes_medicine']]=0

    #kind_health_ins
    data['kind_health_ins'] = data['kind_health_ins'].map({1:'Social security',2:'Other public insurance',
                                                       3:'Private security',4:'Others',5:'None',
                                                       6:'Others',7:'Others',8:'Others',9:'Others'})
    data.loc[data['kind_health_ins'].isnull(),['kind_health_ins']] = 'Others'
    
    # times_hospital
    data['times_hospital'] = data['times_hospital'].map({0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,16:16,99:0,98:0})
    data.loc[data['times_hospital'].isnull(),['times_hospital']] = 0

    #payd_job
    data['payd_job'] = data['payd_job'].map({9:0,8:0,1:1,2:0})
    data.dropna(subset=['payd_job'],inplace=True)

    #age_stop_working/age_begin_working
    data.loc[data['age_stop_working']>data['age'],
         ['age_stop_working']] = data.loc[data['age_stop_working']<data['age'],
                                          ['age_stop_working']].mean()
    data.loc[(data['age_begin_working']==98)|(data['age_begin_working']==99),
         ['age_begin_working']] = data.loc[data['age_begin_working']<90,['age_begin_working']].mean()
    data.loc[(data['age_begin_working'].isna())
         &(data['age_stop_working'].notna()),'age_begin_working']=data.loc[(data['age_begin_working'].notna()),
                                                                             'age_begin_working'].mean()
    data.loc[(data['age_begin_working'].notna())
         &(data['age_stop_working'].isna()),['age_stop_working']] = data.loc[(data['age_begin_working'].notna())
                                                                                 &(data['age_stop_working'].isna()),
                                                                                 'age']
    data['work_life'] = data['age_stop_working'] - data['age_begin_working']
    data.loc[(data['age_begin_working'].isna())
         &(data['age_stop_working'].isna()),['work_life']] = 0                                 
    return data

if __name__ == '__main__' :
    data = preprocessing()
    data.to_csv(path_arquivo_pprocessed,index=False)