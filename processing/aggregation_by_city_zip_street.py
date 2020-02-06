"""Takes in parquet file returns aggregated parquet file."""
import pandas as pd
from collections import defaultdict, namedtuple
from fastparquet import ParquetFile, write


class _aggregation_tuple():
    def __init__(self):
        self.sum_land_value = 0
        self.sum_improvements_value = 0
        self.residential_count = 0
        self.industrial_count = 0
        self.commercial_count = 0
        self.vacant_count = 0
        self.other_count = 0
        return self

    def increment_count(self, use_case):
        if use_case == "RESIDENTIAL":
            self.residential_count += 1
        elif use_case == "INDUSTRIAL":
            self.industrial_count += 1
        elif use_case == "COMMERCIAL":
            self.commercial_count += 1
        elif use_case == "VACANT":
            self.vacant_count += 1
        else:
            self.other_count += 1

    def add_to_value(self, land_value, improvements_value):
        self.sum_land_value += land_value
        self.sum_improvements_value += improvements_value

    def __repr__(self):
        count = self.residential_count + self.industrial_count \
            + self.commercial_count + self.vacant_count + self.other_count
        return {
            'avg_land_value': self.sum_land_value/count,
            'avg_improvements_value': self.sum_improvements_value/count,
            'residential_count': self.residential_count,
            'industrial_count': self.industrial_count,
            'commercial_count': self.commercial_count,
            'vacant_count': self.vacant_count,
            'other_count': self.other_count}


def aggregation_by_city_zip_street(source_name, source_parquet):
    """Take in cleaned city parquet, returns result parquet.

    file_name: [source_name]_aggregated.parquet
    schema:
        city
        zip
        street
        year
        state
        avg_land_value
        avg_improvements_value
        avg_total_value
        residential_count
        industrial_count
        commercial_count
        vacant_count
        key_to_property_coordinates (FK)
    """
    parquet_file = ParquetFile(source_parquet)
    df = parquet_file.to_pandas()

    aggregated = defaultdict(_aggregation_tuple)
    for index, row in df.iterrows():
        aggregated[row['year'], row['city'], row['zip'], row['street']]\
            .add_to_value(row['land_value'], row['improvement_value'])\
            .increment_count(str(row['use']))

    # TODO: Work on processing
    return aggregated
