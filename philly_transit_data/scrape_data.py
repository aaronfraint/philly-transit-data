"""
Use the geojson URLs from SEPTA's open data portal to download spatial data.
"""
import pandas as pd
import geopandas as gpd
import urllib


class TransitData:
    """Provide a single method for downloading one or all
    transit datasets in the Philly region
    """

    URL_CODES = {
        "SEPTA regional rail": {
            # Latest data published 12/17/21 (as of 2/3/2022)
            "stops": "cf49c62fbc17430aa818e900556d207e_0",
            "lines": "7ebff6bc356d4fa28d4a7e4147d03b32_0",
        },
        "SEPTA trolley": {
            # Latest data published 12/17/21 (as of 2/3/2022)
            "stops": "20e09781b71c4800a413796662646129_0",
            "lines": "33944ef79d2249aca38561a68dc3e06f_0",
        },
        "SEPTA bus": {
            # Latest data published 9/25/2023 (as of 3/18/2024)
            "stops": "51d1eb2a85a742eaa28ee2407c4e8b6f_0",
            "lines": "51d1eb2a85a742eaa28ee2407c4e8b6f_0",
        },
        "SEPTA highspeed": {
            # Latest data published 2/2/22 (as of 2/3/2022)
            "stops": "af52d74b872045d0abb4a6bbbb249453_0",
            "lines": "1e7754ca5f7d47e480a628e282466428_0",
        },
        "NJT bus": {
            # Latest data published 1/16/2024 (as of 3/18/2024)
            "stops": "fcb66a1ea358460bad1113e2d4ec2ec5_11",
            "lines": "c79f24daf6a84b9d9d0cbb400631db3d_7",
        },
        "NJT rail": {
            # Latest data published 9/29/21 (as of 2/3/2022)
            "stops": "4809dada94c542e0beff00600ee930f6_0",
            "lines": "e6701817be974795aecc7f7a8cc42f79_0",
        },
        "NJT light rail": {
            # Latest data published 8/25/21 (as of 2/3/2022)
            "stops": "7877bb73757d4b1586338ccf2168705d_0",
            "lines": "b432bf3bf40f40da9d43fa955b834274_0",
        },
    }

    def _make_url(self, code: str):
        """Make the URL by placing the code into the ArcGIS opendata pattern"""
        return f"https://opendata.arcgis.com/datasets/{code}.geojson"

    def options(self):
        """Return a list of all modes that can be scraped"""
        return list(self.URL_CODES.keys())

    def add_data_source(self, mode_name: str, url_type: str, url_or_code: str):
        """Allow users to add their own URLS to ArcGIS open data.

        :param mode_name: name of the provider and mode, eg. 'SEPTA bus'
        :type mode_name: str
        :param url_type: type of transit data. Must be 'stops' or 'lines'
        :type url_type: str
        :param url_or_code: the full URL or just the code portion
        :type url_or_code: str
        :return: None, updates the internal dictionary in-place
        :rtype: None
        """

        # Ensure the user passes a stop or line URL
        if url_type not in ["stops", "lines"]:
            print("URL type must either be 'stops' or 'lines'")
            return None

        # Let the user know if they're going to overwrite an existing code
        if mode_name in self.URL_CODES and url_type in self.URL_CODES[mode_name]:
            print(f"{mode_name} - {url_type} already exists: Overwriting URL")

        # Add the mode if it's not already in the dictionary
        if mode_name not in self.URL_CODES:
            self.URL_CODES[mode_name] = {}

        # Strip out the URL prefix and suffix (if passed in)
        code = url_or_code
        for text in ["https://opendata.arcgis.com/datasets/", ".geojson"]:
            if text in code:
                code = code.replace(text, "")

        # Save the code with the rest of the data sources
        self.URL_CODES[mode_name][url_type] = code

    def get_data_from_portal(self, mode: str = "SEPTA bus"):
        """Extract stop and line data from .geojson URLs
        Return two geodataframes: stops and lines
        """

        try:
            url_codes = self.URL_CODES[mode]
        except KeyError:
            print(
                f"Mode '{mode}' is not defined. Check your spelling or add a new entry with add_data_source() "
            )
            return None

        stop_url = self._make_url(url_codes["stops"])
        line_url = self._make_url(url_codes["lines"])

        # Use geopandas to read geojson data from the web
        try:
            stops = gpd.read_file(stop_url)
            lines = gpd.read_file(line_url)
        except urllib.error.HTTPError:
            print("BAD URL")
            print(stop_url)
            print(line_url)
            print(mode)

        # Add new column to each with the name of the mode
        stops["src"] = mode
        lines["src"] = mode

        return stops, lines

    def all_spatial_data(self):
        """Download data for all modes.
        Return single stop and line geodataframes
        with all SEPTA modes merged together.
        """

        stops = []
        lines = []

        for mode in self.URL_CODES:
            gdf_stop, gdf_line = self.get_data_from_portal(mode=mode)

            stops.append(gdf_stop)
            lines.append(gdf_line)

        # Convert stop data into a singlepart geodataframe
        stop_gdf = pd.concat(stops)
        singleparts = stop_gdf[stop_gdf.geom_type != "MultiPoint"]
        multiparts = stop_gdf[stop_gdf.geom_type == "MultiPoint"]
        stops_singlepart = pd.concat([singleparts, multiparts.explode(index_parts=True)])

        return stops_singlepart, pd.concat(lines)

if __name__ == '__main__':
    transit_data = TransitData()
    stops, lines = transit_data.all_spatial_data()

