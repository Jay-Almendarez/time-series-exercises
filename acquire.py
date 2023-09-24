import requests
import pandas as pd


def df_from_api(criteria):
    '''
    df_from_api will request an API filtered by the criteria we desire (ex: people, planets, starships) and finally return our entries into a dataframe for later use.
    '''
    response = requests.get(f'https://swapi.dev/api/{criteria}/')
    df_name = response.json()
    num = range(2, df_name['count']+1)
    count = df_name['count']
    response = requests.get(f'https://swapi.dev/api/{criteria}/1/')
    df_name = response.json()
    df_name = pd.Series(df_name)
    df_name = pd.DataFrame(df_name).T
    for i in num:
        response = requests.get(f'https://swapi.dev/api/{criteria}/{i}/')
        df_name_new = response.json() 
        df_name_new = pd.Series(df_name_new)
        df_name_new = pd.DataFrame(df_name_new).T
        df_name = pd.concat([df_name, df_name_new], axis=0, ignore_index=True)
    return df_name


def read_or_write_csv():
    '''
    
    '''
    if 'opsd.csv' exists:
        return pd.read_csv('opsd.csv')
    else:
        
    