"""Cleaning just LA."""
import pyarrow
from pyarrow import csv
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import CitySchemaFormat


def removed_useless_cols():
    DF = pd.read_csv("../../LA_Assessor_Roll_2016-2019.csv")
    city_schema = CitySchemaFormat.CitySchemaFormat()
    la_schema = city_schema.get_city_format("Los Angeles")
    df_cleaned = DF[list(la_schema.values())]
    df_cleaned.rename(columns={
                    str(val): str(key) for key, val in la_schema.items()},
                    inplace=True)
    df_cleaned.to_csv("../../LA_Roll_2006_2019_new.csv", index=False)
    pass


def converted_to_parquet():
    DF = pd.read_csv("../../LA_Roll_2006_2019_new.csv")
    TABLE = pa.Table.from_pandas(DF)
    pq.write_table(TABLE, '../../LA_Roll_2006_2019.parquet')


if __name__ == "__main__":
