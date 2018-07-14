import pandas as pd
import requests
import json
import numpy as np
import pickle

#Load Google Maps API key
with open('../data/apikey.txt', 'r') as fd:
    api_key = fd.read()
          
def get_lng_lat(address, town):
    """Return a dict with longitude and latitude"""
    
    querry_adresse = 'https://maps.googleapis.com/maps/api/geocode/json?address={0},+{1}&key={2}'.format(address, town, api_key)
    rsp = requests.get(querry_adresse)
    js = json.loads(rsp.content.decode('utf8'))
    if 'results' in js.keys() and js['results']:
        ret = js['results'][0]['geometry']['location']
    else:
        ret = np.nan
    return ret

#Open a file with some addresses
print("loading file")
df = pd.read_csv('../data/scraping_darty.csv', index_col = False, sep = ';')

#use Google Maps API to get longitude and latitude for each address
addresses = df['adresse'].tolist()
towns = df['code postal'].tolist()

print("requesting geographic coordinates")
lng_lat_lst = [get_lng_lat(address, town) for address, town in zip(addresses, towns)]

#save the result just in case
with open("../data/lng_lat.pickle", 'wb') as fd:
    pickle.Pickler(fd).dump(lng_lat_lst)

#Extract longitude and latitude from the dict_list
lng_lst = [dic['lng'] if type(dic) == dict else dic for dic in lng_lat_lst]
lat_lst = [dic['lat'] if type(dic) == dict else dic for dic in lng_lat_lst]

#save geographic coordinates in your file
df['longitude'] = lng_lst
df['latitude'] = lat_lst

df.to_csv('../data/localisation_darty.csv', sep = ';', index = False)
print("localisation_darty.csv saved in data")