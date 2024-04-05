# example code from: https://plotly.com/python/scattermapbox/

from typing import Literal

import pandas as pd
import plotly.express as px


HOTSPOTS_FILE_PATH = "./hotspots.csv"
SIZE_COLUMN: Literal['fwi', 'ros', 'hfi', 'estarea'] = 'estarea'

df = pd.read_csv(HOTSPOTS_FILE_PATH)
fig = px.scatter_mapbox(df, lat="lat", lon="lon", size=SIZE_COLUMN, size_max=15,
                        color=SIZE_COLUMN, color_continuous_scale=px.colors.cyclical.IceFire,
                        center={"lat": 50, "lon": -100}, zoom=3,
                        mapbox_style="open-street-map")
fig.show()
