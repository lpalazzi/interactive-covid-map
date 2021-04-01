import pandas as pd
import geopandas as gpd

# load health unit boundary data
health_units = gpd.read_file('./data/health-units/lhrp000b06a_e_Oct2011.shp')

# load covid data
covid_data_2020 = pd.read_csv('./data/covid-data/individual_level/cases_2020.csv')
covid_data_2021 = pd.read_csv('./data/covid-data/individual_level/cases_2021.csv')
covid_data = pd.concat([covid_data_2020, covid_data_2021])

