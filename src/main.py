import pandas as pd
import geopandas as gpd

# load health unit boundary data
path_to_health_units = '../data/health-units/lhrp000b06a_e_Oct2011.shp'
health_units = gpd.read_file(path_to_health_units)

# load covid data
path_to_covid_data = '../data/covid-data/individual_level/cases_2020.csv'
covid_data = pd.read_csv(path_to_covid_data)

print(covid_data.head())