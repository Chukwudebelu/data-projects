import pandas as pd
import numpy as np

df_boston = pd.read_csv('zillow_crawled_data/raw_housing_data_baltimore_06_23_2022__21_52_58.csv')

def clean_data(df):
    '''# Drop row of records with NaN values in any column'''
    # Iterate through the rows
    for i in list(df.index):
        if df.loc[i,:].isnull().values.any(): # if any row is 'NaN'
            df.drop(i, axis=0, inplace=True) # remove row
            
    '''Drop "-" values in the # of bedroom column'''
    for j in list(df.index):
        for k in ['beds']:
            if df.loc[j,k] == '-':
                df.drop(j, axis=0, inplace=True)
    
    '''Drop "-" values in the # of bathroom column'''
    for l in list(df.index):
        for m in ['baths']:
            if df.loc[l,m] == '-':
                df.drop(l, axis=0, inplace=True)
                
    '''Drop "--" values in the square footage column'''
    for n in list(df.index):
        for p in ['area_sq_ft']:
            if df.loc[n,p] == '--':
                df.drop(n, axis=0, inplace=True)
    
    # Convert the Zip codes, number of beds & baths and square footage to integers
    df[['zip_code','beds','baths']] = df[['zip_code','beds','baths']].astype('int')
    
    # Remove the $ values and ','
    df['price']=df['price'].str.replace(',','').str.strip('$').astype('int')
    
    # Remove ',' from square footage column
    df['area_sq_ft']=df['area_sq_ft'].str.replace(',','').astype('int')
    
    # Reset the index of the new dataframe
    df = df.reset_index()
    del df['index']
    
    return df