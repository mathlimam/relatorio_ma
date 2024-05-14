import geopandas as gpd
from pyproj import CRS

crs=CRS('EPSG:4326')

data_source = 'shape_map.shp'

data = gpd.read_file(data_source)
gpd.

data.to_file("map_correto.json", driver="GeoJSON")