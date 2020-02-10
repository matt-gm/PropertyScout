from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *


if __name__ == "__main__":

    spark = SparkSession.builder \
        .master("local") \
        .appName("CSV_to_Parquet") \
        .getOrCreate()


    file_name = "/Users/matthewmaatubang/Development/test/test.parquet"
    df = spark.read.load(file_name,format="parquet")
    df.show(n=10)
