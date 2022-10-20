import geopandas as gpd
import glob
import matplotlib.pyplot as plt
import os
import pathlib

# get the geojsons
geojson_dir = "data/"
path2geojsons = geojson_dir + "*.geojson"
to_map = glob.glob(path2geojsons)
print(f"We are going to map {len(to_map)} geojsons. They are:")
for geojson in to_map:
    print(f"  * {geojson}")


# create the output path:
output_path = "mymaps/"
pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

# load data and plot
for i, geojson in enumerate(to_map):
    gdf = gpd.read_file(geojson, driver="GeoJSON")
    gdf.plot()
    plt.savefig(os.path.join(output_path, f"{i}.jpg"))
