"""
Convert and CSV to Apache Parquet.

Requires format .json file in same directory.
"""
import json


class CitySchemaFormat(object):
    """City Schema Handler."""

    def __init__(self):
        """Init loader."""
        with open("CitySchemaFormat.json") as city_schema:
            self.json_file = json.load(city_schema)

    def get_city_format(self, city):
        """Handle the get/set for CSV."""
        return self.json_file[city]
