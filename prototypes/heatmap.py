# example code from: https://plotly.com/python/mapbox-density-heatmaps/

from typing import Literal

import pandas as pd
import plotly.express as px


HOTSPOTS_FILE_PATH = "./hotspots.csv"
Z_COLUMN: Literal['fwi', 'ros', 'hfi', 'estarea'] = 'estarea'

df = pd.read_csv(HOTSPOTS_FILE_PATH)

fig = px.density_mapbox(df, lat='lat', lon='lon', z=Z_COLUMN, radius=10,
                        center={"lat": 50, "lon": -100}, zoom=3,
                        mapbox_style="open-street-map")
fig.show()

# %%
