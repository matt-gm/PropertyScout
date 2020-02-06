'''
Convert and CSV to Apache Parquet
Requires format .ini file
'''
import json


class city_schema_format():
    '''Handles the get/set for CSV'''
    def __init__(self):
        with open("city_schema_format.json") as city_schema:
            self.json_file = json.load(city_schema)

    '''
    Input: City name as str
    Output: Dictionary mapping unified_label:citys_label'''
    def get_city_format(self, city):
        return(self.json_file[city])
