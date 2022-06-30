import logging
import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd
from io import StringIO
import glob

# security credentials
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
BUCKET_NAME = "ds4a-project-3"

# Interact with the S3 bucket from python
def upload_data(data,bucket_name,key,aws_access_key_id,aws_secret_access_key):
    '''
    Upload data to storage S3, aws_acces_key_id and aws_secret_access_key are provided by AWS.
    key: The object key (or key name) uniquely identifies the object in a bucket
    '''
    s3 = boto3.resource("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(Filename=str(key), Key=str(key), ExtraArgs={"ACL": "public-read", "StorageClass": "STANDARD"})

# Get the files from the directory in EC2
ec2_dir = '/home/ec2-user/zillow_crawled_data/' # zillow_crawled_data is a folder in BUCKET_NAME S3 container
csv_files = glob.glob(ec2_dir + '*.csv')

try:
    for file in csv_files:
        # Read the scraped data on the EC2 instance
        data = pd.read_csv(file)

        # change the filename to be stored on S3
        key = file.replace(ec2_dir[:15],"") # remove '/home/ec2-user/'

        # call the function to upload data to S3
        upload_data(data, BUCKET_NAME, key, AWS_ACCESS_KEY, AWS_SECRET_KEY)
        
    print('Files successfully loaded to the S3 bucket: "' + BUCKET_NAME + '"')
except:
    print('Client error: file(s) could not be uploaded to S3')
    
# Check file is uploaded by accessing the Object URL available on S3
# object_URL = 'https://myds4a-data-store.s3.amazonaws.com/data/crimes.csv'
# data_aws = pd.read_csv(object_URL)
# data_aws.head(10)

#-------------------------------------------------------------------------------------------------------------------------------------------
# CODE TO RUN ON EC2 INSTANCE for CRON JOBS SCRAPING!
# # change modifications
# !chmod 400 project_3_key.pem

# # SSH to the running EC2 instance
# !ssh -i project_3_key.pem ec2-user@ec2-54-175-233-102.compute-1.amazonaws.com

# Install all updates on the instance
# !sudo yum update

# # or install only pip for python
# !sudo yum install python3-pip

# # then install python3 dependencies
# !pip install --user pandas matplotlib

# using SCP to transfer file from local path to EC2
# !scp -i project_3_key.pem ../zillow_crawled_data/*.csv ec2-user@ec2-54-175-233-102.compute-1.amazonaws.com:/home/ec2-user/