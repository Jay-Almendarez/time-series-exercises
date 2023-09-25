import pandas as pd
import numpy as np
from acquire import read_or_write_csv, acquire_store
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def prep_ops():
    ops = read_or_write_csv('opsd.csv')
    ops.columns = ops.columns.str.lower()
    ops = ops.rename(columns= {'wind+solar':'wind_and_solar'})
    ops.date = pd.to_datetime(ops.date)
    ops = ops.set_index('date').sort_index()
    ops['month'] = ops.index.month_name()
    ops['year'] = ops.index.year
    ops.solar[ops.solar.isnull()] = 0
    ops.wind[ops.wind.isnull()] = 0
    ops.wind_and_solar = ops['wind'] + ops['solar']
    ops.wind_and_solar[ops.wind_and_solar.isnull()] = 0
    return ops


def prep_store():
    store = acquire_store()
    store.sale_date = pd.to_datetime(store.sale_date)
    store = store.set_index('sale_date').sort_index()
    store['month'] = store.index.month_name()
    store['day_of_week'] = store.index.day_of_week
    store['sales_total'] = (store['sale_amount'] * store['item_price'])
    return store