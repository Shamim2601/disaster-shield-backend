import requests
import os
from dotenv import load_dotenv
import schemas
load_dotenv()

weather_api_key=os.getenv('WEATHER_API_KEY')

def get_current_weather(lat:float,long:float)->schemas.Weather:
    url = "http://api.weatherapi.com/v1/current.json"
    lat_long=lat.__str__()+','+long.__str__()
    params = {'key':weather_api_key,'q':lat_long,'aqi' :'yes'}
    r = requests.get(url,params=params)
    data = r.json()
    
    location = schemas.Location(**data['location'])
    air_quality = schemas.Air_Quality(**data['current']['air_quality'],\
        us_epa_index=list(schemas.Us_Epa_Index)[data['current']['air_quality']['us-epa-index']])
    # condition = schemas.Weather_Condition(**data['current']['condition'])
    weather_data:dict=data['current']
    weather_data.pop('air_quality')
    weather = schemas.Weather(**data['current'],location=location,air_quality=air_quality)
    return weather
    
        

