import os
import numpy as np
import pandas as pd
import geopandas as gpd
import branca.colormap as cm

root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

# load health region mappings
hr_map = pd.read_csv(os.path.join(root_dir, 'data/covid-data/other/hr_map.csv'))
hr_map['HR_UID'] = hr_map['HR_UID'].astype('int64')

# load health region boundary data
health_regions = gpd.read_file(os.path.join(root_dir, 'data/health-regions/RegionalHealthBoundaries.shp'))
health_regions = health_regions[health_regions.Province != 'SK']
health_regions = health_regions[['HR_UID', 'geometry']].set_index('HR_UID')
health_regions.index = health_regions.index.astype('int64')

# load original SK health region boundary data
health_regions_sk = gpd.read_file(os.path.join(root_dir, 'data/health-regions-sk/SaskHealthBoundaries.shp')).rename(columns={'REGIONNAME': 'health_region'})
health_regions_sk = pd.merge(health_regions_sk, hr_map[hr_map.province == 'Saskatchewan'], how='left', on=['health_region'])
health_regions_sk = health_regions_sk[['HR_UID', 'geometry']].set_index('HR_UID')
health_regions_sk.index = health_regions_sk.index.astype('int64')

# add original SK boundaries to full boundary data
health_regions = health_regions.append(health_regions_sk)

# load the COVID-19 cases timeseries
covid_timeseries = pd.read_csv(os.path.join(root_dir, 'data/covid-data/timeseries_hr/cases_timeseries_hr.csv'))

# map covid_timeseries.health_region name to health_region_mappings.HR_UID
covid_timeseries = pd.merge(covid_timeseries, hr_map, how='left', on=['health_region', 'province'])
covid_timeseries = covid_timeseries.drop(['province_full', 'province_short', 'health_region_esri'], axis=1)

# parse dates
covid_timeseries['date_report'] = pd.to_datetime(covid_timeseries['date_report'], format='%d-%m-%Y')

# sort based on health region
covid_timeseries = covid_timeseries.sort_values(['HR_UID', 'date_report']).reset_index(drop=True)

# use log of cases to plot colours
covid_timeseries['cases_log'] = np.log10(covid_timeseries['cases'])

# convert date to string
covid_timeseries['date_report_sec'] = covid_timeseries['date_report'].astype(int) / 10**9
covid_timeseries['date_report_sec'] = covid_timeseries['date_report_sec'].astype(int).astype(str)

# map daily cases to colour
cmap = cm.linear.YlOrRd_09.scale(0, max(covid_timeseries['cases_log']))
covid_timeseries['colour'] = covid_timeseries['cases_log'].map(cmap)
cmap = cm.linear.YlOrRd_09.scale(0, max(covid_timeseries['cases']))

# generate style dictionary for time slider
style_dict = {}
for HR_UID in hr_map.HR_UID:
    df = covid_timeseries[covid_timeseries['HR_UID'] == HR_UID]
    inner_dict = {}
    for _, row in df.iterrows():
        inner_dict[row['date_report_sec']] = {'color': row['colour'], 'opacity': 0.8}
    style_dict[str(HR_UID)] = inner_dict
