import requests
import pandas as pd
import numpy as np
import env
import os

def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
    get_connection will determine the database we are wanting to access, and load the database along with env stored values like username, password, and host
    to create the url needed for SQL to read the correct database.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


def acquire_zillow():
    file_name = 'zillow_cluster.csv'
    if os.path.isfile(file_name):
        return pd.read_csv(file_name)
    else:
        query = 'SELECT DISTINCT predictions_2017.id, typeconstructiontypeid, storytypeid, propertylandusetypeid, heatingorsystemtypeid, buildingclasstypeid,  architecturalstyletypeid, airconditioningtypeid, basementsqft,  bathroomcnt, bedroomcnt, buildingqualitytypeid, calculatedbathnbr,  decktypeid, finishedfloor1squarefeet, calculatedfinishedsquarefeet,  finishedsquarefeet12, finishedsquarefeet13, finishedsquarefeet15,  finishedsquarefeet50, finishedsquarefeet6, fips, fireplacecnt,  fullbathcnt, garagecarcnt, garagetotalsqft, hashottuborspa, latitude,  longitude, lotsizesquarefeet, poolcnt, poolsizesum, pooltypeid10,  pooltypeid2, pooltypeid7, propertycountylandusecode, propertyzoningdesc,  rawcensustractandblock, regionidcity, regionidcounty, regionidneighborhood,  regionidzip, roomcnt, threequarterbathnbr, unitcnt, yardbuildingsqft17,  yardbuildingsqft26, yearbuilt, numberofstories, fireplaceflag,  structuretaxvaluedollarcnt, taxvaluedollarcnt, assessmentyear, landtaxvaluedollarcnt,  taxamount, taxdelinquencyflag, taxdelinquencyyear, censustractandblock,  airconditioningdesc, architecturalstyledesc, buildingclassdesc,  heatingorsystemdesc, propertylandusedesc, storydesc, typeconstructiondesc,  logerror, parcelid FROM predictions_2017 LEFT JOIN properties_2017 USING (parcelid) LEFT JOIN airconditioningtype USING (airconditioningtypeid) LEFT JOIN architecturalstyletype USING (architecturalstyletypeid) LEFT JOIN buildingclasstype USING (buildingclasstypeid) LEFT JOIN heatingorsystemtype USING (heatingorsystemtypeid) LEFT JOIN propertylandusetype USING (propertylandusetypeid) LEFT JOIN storytype USING (storytypeid) LEFT JOIN typeconstructiontype USING (typeconstructiontypeid) LEFT JOIN unique_properties USING (parcelid) WHERE transactiondate BETWEEN "2017-01-01" AND "2017-12-31" AND latitude NOT LIKE "null" AND longitude NOT LIKE "null"'
        connection = get_connection('zillow')
        df = pd.read_sql(query, connection)
        df.to_csv('zillow_cluster.csv', index=False)
        return df
    
    
def acquire_store():
    '''
    Returns a dataframe of all store data in the tsa_item_demand database and saves a local copy as a csv file.
    '''
    file_name = 'tsa_item_demand.csv'
    if os.path.isfile(file_name):
        return pd.read_csv(file_name)
    else:
        query = '''
            SELECT *
            FROM items
            JOIN sales USING(item_id)
            JOIN stores USING(store_id)
            '''
        connection = get_connection('tsa_item_demand')
        df = pd.read_sql(query, connection)
        df.to_csv('tsa_item_demand.csv', index=False)
        return df
    
    
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


def read_or_write_csv(file_name):
    '''
    
    '''
    file_name = file_name
    return pd.read_csv(file_name)
