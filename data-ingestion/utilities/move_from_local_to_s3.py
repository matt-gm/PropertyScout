'''
Module to move file from local to S3
'''
import s3_file_manager

S3FM = s3_file_manager.s3_file_manager()
S3FM.set_bucket_name("assessor-data-bucket")
S3FM.put_file("LA_2019.parquet")
