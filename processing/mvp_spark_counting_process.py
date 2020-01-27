import sys
import os
import pandas as pd
import numpy as np
from pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext()
sqlContext = SQLContext(sc)
sqlContext.read.parquet("la_2019.parquet")
# 4) Make Spark calculate the aggregation in this format:
# [City, ZIP Code, Street] = [Count of Properties, Average Value]

# 5) Put the results in a results.txt

# 6) Write results to the bucket
