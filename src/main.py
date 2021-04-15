import pandas as pd
import geopandas as gpd

import folium

import os
import webbrowser

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

# sum over health regions
covid_data_sums = covid_data['HR_UID'].value_counts()
covid_data_sums.index = covid_data_sums.index.astype('O')

# init map
m = folium.Map(location=[56.130, -106.35], tiles='cartodbpositron', zoom_start=4)

# plot total case count by health region
folium.Choropleth(geo_data=health_regions.__geo_interface__,
                  data=covid_data_sums,
                  key_on='feature.id',
                  fill_color="OrRd",
                #   fill_opacity=0.7,
                #   line_opacity=1.0,
                  legend_name='Total COVID-19 Cases',
                  ).add_to(m)

# render map
filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output/map.html')
m.save(filepath)
webbrowser.open('file://' + filepath)
