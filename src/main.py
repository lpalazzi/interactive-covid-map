import os
import webbrowser
import folium
from folium.plugins import TimeSliderChoropleth

from load_data import health_regions, style_dict, cmap

m = folium.Map(location=[56.130, -106.35], tiles='cartodbpositron', zoom_start=4, max_bounds=True)

s = TimeSliderChoropleth(data=health_regions.to_json(), styledict=style_dict).add_to(m)

cmap.caption = 'Number of daily confirmed cases'
l = cmap.add_to(m)

# render map
filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output/map.html')
m.save(filepath)
webbrowser.open('file://' + filepath)
