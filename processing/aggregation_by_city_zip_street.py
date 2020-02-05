'''
Takes in parquet file
Does the counting
Returns aggregated parquet file
'''
import s3fs
from fastparquet import ParquetFile, write

def aggregation_by_city_zip_street(source_name, source_parquet):
