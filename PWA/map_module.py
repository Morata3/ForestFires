import folium
from matplotlib import colors
from matplotlib import cm
import requests
import flask

colormap = cm.get_cmap('Spectral_r')

coord = [(41.906131, -6.631415),
         (41.894612, -6.639913),
         (41.911177, -6.601031),
         (41.902809, -6.611932),
         (41.899487, -6.596397),
         (41.895973, -6.606882),
         (41.891309, -6.616996),
         (41.933097, -6.671018),
         (41.922593, -6.651428),
         (41.879638, -6.669783),
         (41.875039, -6.653193),
         (41.887015, -6.645027),
         (41.876881, -6.631911),
         (41.919800, -6.636365),
         (41.912907, -6.640077),
         (41.916117, -6.587119),
         (41.919984, -6.687096),
         (41.881672, -6.622507),
         (41.905189, -6.674421)]
center = (41.901210, -6.620919)


def normalize_temp(temp):
    min_temp = 20
    max_temp = 80
    normalized_temp = (temp-min_temp)/(max_temp-min_temp)
    return normalized_temp

def getCoordDict():
    coord_dict = dict()
    for s in range(len(coord)):
        coord_dict["s"+str(s+1)] = coord[s]
    return coord_dict

def updateMap(sensor_data):
    circle_map = folium.Map(location=center, zoom_start = 13)
    coord_dict = getCoordDict()
    for key,value in sensor_data.items():
        temp = f'{key}: {value["temp"]:.1f}C'
        folium.CircleMarker(location=coord_dict[key],
                            radius=30,
                            color=colors.rgb2hex(colormap(normalize_temp(value["temp"]))[:3]),
                            tooltip=temp,
                            fill=True
                           ).add_to(circle_map)
        if(value["fire"]==1):
            icon = folium.features.CustomIcon("./static/images/fire-icon.png",icon_size=(24, 33))
            folium.Marker(location=coord_dict[key],icon=icon).add_to(circle_map)
    circle_map.save('./templates/dist/folium_map.html')