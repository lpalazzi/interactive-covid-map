import pandas as pd
import geopandas as gpd

# load health region boundary data
health_regions = gpd.read_file('./data/health-units/lhrp000b06a_e_Oct2011.shp')

# load health region mappings
health_region_mappings = pd.read_csv('./data/covid-data/other/hr_map.csv')

# load covid data
covid_data_2020 = pd.read_csv('./data/covid-data/individual_level/cases_2020.csv')
covid_data_2021 = pd.read_csv('./data/covid-data/individual_level/cases_2021.csv')
covid_data = pd.concat([covid_data_2020, covid_data_2021])

# clean covid data
covid_data = covid_data.drop(['country', 'travel_yn', 'travel_history_country', 'locally_acquired', 'case_source', 'additional_info', 'additional_source', 'method_note'], axis=1)

# map covid_data.health_region name to health_region_mappings.HR_UID
covid_data = pd.merge(covid_data, health_region_mappings, how='left', on=['health_region', 'province'])
