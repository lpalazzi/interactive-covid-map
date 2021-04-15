import pandas as pd
import geopandas as gpd

# load health region boundary data
health_regions = gpd.read_file('./data/health-regions/RegionalHealthBoundaries.shp')[['HR_UID', 'geometry']].set_index('HR_UID')

# load health region mappings
health_region_mappings = pd.read_csv('./data/covid-data/other/hr_map.csv')

# load covid data
covid_data_2020 = pd.read_csv('./data/covid-data/individual_level/cases_2020.csv')
covid_data_2021 = pd.read_csv('./data/covid-data/individual_level/cases_2021.csv')
covid_data = pd.concat([covid_data_2020, covid_data_2021])

# map covid_data.health_region name to health_region_mappings.HR_UID
covid_data = pd.merge(covid_data, health_region_mappings, how='left', on=['health_region', 'province'])

# clean covid data
covid_data = covid_data.drop(['country', 'age', 'sex', 'travel_yn', 'travel_history_country', 'locally_acquired', 'case_source', 'additional_info', 'additional_source', 'method_note', 'pop', 'health_region_esri', 'province', 'province_short'], axis=1)
covid_data = covid_data.rename(columns={'province_full': 'province'})

# parse dates
covid_data['date_report'] = pd.to_datetime(covid_data['date_report'], format='%d-%m-%Y')
covid_data['report_week'] = pd.to_datetime(covid_data['report_week'], format='%d-%m-%Y')