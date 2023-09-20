# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 11:24:10 2023

@author: nfama
"""

# import warnings

# # Suprimindo todos os warnings
# warnings.filterwarnings('ignore')
# # Restaurando as configurações originais de warnings
# warnings.resetwarnings()

import asana
import pandas as pd
import json

# gets taks from a specific project
def get_project(token, worksp_gid, project_gid):
    
    
    # auth
    client = asana.Client.access_token(token)

    # request df principal
    result = client.tasks.get_tasks_for_project(project_gid, {'opt_fields': ['gid','name',
                                                                             'assignee.name',
                                                                             'created_at',
                                                                             'completed',
                                                                             'completed_at',
                                                                             'completed_by.name']}, 
                                                              opt_pretty=True)
    
    # normalizando o df principal
    df = pd.json_normalize(result)
    df = df.astype(str) # transformando tudo em str
    df = df.rename(columns=lambda x: x.replace('.', '_')) # padronizando o nome das colunas
    
    # criando lista para data de conclusão da subtask = Fechar parceria
    df['data_fechamento'] = None
    
    # buscando subtasks de cada task
    for index, row in df.iterrows():
        task_gid = row['gid']    
        
        try:
            result = client.tasks.get_subtasks_for_task(task_gid, {'opt_fields': ['gid','name','completed_at']}, 
                                                        opt_pretty=True)
            df_subtask = pd.json_normalize(result)
            date = df_subtask[df_subtask['name'] == 'Fechar parceria']['completed_at'].iloc[0]
            
            # adicionando data ao df
            df.at[index, 'data_fechamento'] = date
        except:
            print(task_gid)
            pass
            
    
    # request section (status/etapa)
    result = client.tasks.get_tasks_for_project(project_gid, {'opt_fields': ['gid','memberships.section.name']}, 
                                                              opt_pretty=True)
    # normalizando
    df_section = pd.json_normalize(result)
    df_section = df_section.explode(['memberships'])
    df_section = pd.json_normalize(json.loads(df_section.to_json(orient='records')))
    df_section = df_section.rename(columns=lambda x: x.replace('.', '_')) # padronizando o nome das colunas
    
    
    # request custom fields
    result = client.tasks.get_tasks_for_project(project_gid, {'opt_fields': ['gid','custom_fields']}, 
                                                              opt_pretty=True)
    # normalizando
    df_custom = pd.json_normalize(result)
    df_custom = df_custom.explode(['custom_fields'])
    df_custom = pd.json_normalize(json.loads(df_custom.to_json(orient='records')))
    
    # selecionando colunas necessarias
    df_custom = df_custom.loc[:, ['gid','custom_fields.name','custom_fields.display_value']]
    df_custom = df_custom.rename(columns=lambda x: x.replace('.', '_')) # padronizando o nome das colunas
    
    
    return(df,df_section,df_custom)