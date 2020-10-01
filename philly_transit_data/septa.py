import pandas as pd
import geopandas as gpd


class SEPTA:

    def __init__(self):
        self.URLS = {
            "regional rail": {
                # Latest data published 7/9/2018 (as of 10/1/2020)
                "stops": "https://opendata.arcgis.com/datasets/64eaa4539cf4429095c2c7bf25c629a2_0.geojson",
                "lines": "https://opendata.arcgis.com/datasets/48b0b600abaa4ca1a1bacf917a31c29a_0.geojson"
            },
            "trolley": {
                # Latest data published 8/18/2020 (as of 10/1/2020)
                "stops": "https://opendata.arcgis.com/datasets/8aee4ea99d564e50b986e99a4669418a_0.geojson",
                "lines": "https://opendata.arcgis.com/datasets/2a4a268c0c2b4b04bcf1b2f1755d939a_0.geojson"
            },
            "bus": {
                # Latest data published 5/6/2020 (as of 10/1/2020)
                "stops": "https://opendata.arcgis.com/datasets/897f2b081daf442bbcab66e9485b91b0_0.geojson",
                "lines": "https://opendata.arcgis.com/datasets/39f74b6d8b1b4b608933b5358d55be1c_0.geojson"
            },
            "subway - broad": {
                # Latest data published 7/10/2018 (as of 10/1/2020)
                "stops": "https://opendata.arcgis.com/datasets/2e9037fd5bef406488ffe5bb67d21312_0.geojson",
                "lines": "https://opendata.arcgis.com/datasets/c051c18bb15444b6861a93fd247dde3d_0.geojson"

            },
            "subway - market": {
                # Latest data published 7/10/2018 (as of 10/1/2020)
                "stops": "https://opendata.arcgis.com/datasets/8c6e2575c8ad46eb887e6bb35825e1a6_0.geojson",
                "lines": "https://opendata.arcgis.com/datasets/6f4ae63a492c407eb95a9e56a6750e7f_0.geojson"

            },
            "norristown high speed line": {
                # Latest data published 7/10/2018 (as of 10/1/2020)
                "stops": "https://opendata.arcgis.com/datasets/f106f00a4ac34885ab35f4ebabb2aee0_0.geojson",
                "lines": "https://opendata.arcgis.com/datasets/8e685b473f4045d899dce7896ee5923a_0.geojson"
            },
        }

    def get_data_from_portal(self, mode: str = "bus"):
        if mode not in self.URLS:
            return KeyError

        urls = self.URLS[mode]

        # Use geopandas to read geojson data from the web
        stops = gpd.read_file(urls["stops"])
        lines = gpd.read_file(urls["lines"])

        # Add new column to each with the name of the mode
        stops["src"] = mode
        lines["src"] = mode

        return stops, lines

    def all_spatial_data(self):
        stops = []
        lines = []
        for mode in self.URLS:
            gdf_stop, gdf_line = self.get_data_from_portal(mode=mode)

            stops.append(gdf_stop)
            lines.append(gdf_line)

        return pd.concat(stops), pd.concat(lines)
