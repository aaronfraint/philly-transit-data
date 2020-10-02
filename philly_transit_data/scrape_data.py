"""
Use the geojson URLs from SEPTA's open data portal to download spatial data.
"""
import pandas as pd
import geopandas as gpd


class TransitData:
    """ Provide a single method for downloading one or all
        transit datasets in the Philly region
    """

    URL_CODES = {
        "SEPTA regional rail": {
            # Latest data published 7/9/2018 (as of 10/1/2020)
            "stops": "64eaa4539cf4429095c2c7bf25c629a2_0",
            "lines": "48b0b600abaa4ca1a1bacf917a31c29a_0"
        },
        "SEPTA trolley": {
            # Latest data published 8/18/2020 (as of 10/1/2020)
            "stops": "8aee4ea99d564e50b986e99a4669418a_0",
            "lines": "2a4a268c0c2b4b04bcf1b2f1755d939a_0"
        },
        "SEPTA bus": {
            # Latest data published 5/6/2020 (as of 10/1/2020)
            "stops": "897f2b081daf442bbcab66e9485b91b0_0",
            "lines": "39f74b6d8b1b4b608933b5358d55be1c_0"
        },
        "SEPTA subway - broad": {
            # Latest data published 7/10/2018 (as of 10/1/2020)
            "stops": "2e9037fd5bef406488ffe5bb67d21312_0",
            "lines": "c051c18bb15444b6861a93fd247dde3d_0"

        },
        "SEPTA subway - market": {
            # Latest data published 7/10/2018 (as of 10/1/2020)
            "stops": "8c6e2575c8ad46eb887e6bb35825e1a6_0",
            "lines": "6f4ae63a492c407eb95a9e56a6750e7f_0"

        },
        "SEPTA norristown high speed line": {
            # Latest data published 7/10/2018 (as of 10/1/2020)
            "stops": "f106f00a4ac34885ab35f4ebabb2aee0_0",
            "lines": "8e685b473f4045d899dce7896ee5923a_0"
        },
        "NJT bus": {
            # Latest data published 5/14/2020 (as of 10/2/2020)
            "stops": "d1b2669cd9bf4ab6bb8e04f5326e8d77_9",
            "lines": "8e7d1cc8cb8c473bb0dd0536593e1a80_10"
        },
        "NJT rail": {
            # Latest data published 5/4/2020 (as of 10/2/2020)
            "stops": "acf1aa71053f4bb48a1aad7034f35e48_3",
            "lines": "2117276b2d83440da81970db6a8c6edb_2"
        },
    }

    def _make_url(self, code: str):
        """ Make the URL by placing the code into the ArcGIS opendata pattern """
        return f"https://opendata.arcgis.com/datasets/{code}.geojson"

    def options(self):
        """ Return a list of all modes that can be scraped """
        return list(self.URL_CODES.keys())

    def add_data_source(
            self,
            mode_name: str,
            url_type: str,
            url_or_code: str):
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
        if mode_name in self.URL_CODES \
           and url_type in self.URL_CODES[mode_name]:
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
        """ Extract stop and line data from .geojson URLs
            Return two geodataframes: stops and lines
        """

        if mode not in self.URL_CODES:
            return KeyError

        url_codes = self.URL_CODES[mode]
        stop_url = self._make_url(url_codes["stops"])
        line_url = self._make_url(url_codes["lines"])

        # Use geopandas to read geojson data from the web
        stops = gpd.read_file(stop_url)
        lines = gpd.read_file(line_url)

        # Add new column to each with the name of the mode
        stops["src"] = mode
        lines["src"] = mode

        return stops, lines

    def all_spatial_data(self):
        """ Download data for all modes.
            Return single stop and line geodataframes
            with all SEPTA modes merged together.
        """

        stops = []
        lines = []

        for mode in self.URL_CODES:
            gdf_stop, gdf_line = self.get_data_from_portal(mode=mode)

            stops.append(gdf_stop)
            lines.append(gdf_line)

        return pd.concat(stops), pd.concat(lines)
