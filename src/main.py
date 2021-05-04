import os
import webbrowser
import folium

from load_data import health_regions, covid_timeseries

# init map
m = folium.Map(location=[56.130, -106.35], tiles='cartodbpositron', zoom_start=4, prefer_canvas=True)

# plot total case count by health region
folium.Choropleth(geo_data=health_regions.__geo_interface__,
                  # data=covid_data_sums,
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
