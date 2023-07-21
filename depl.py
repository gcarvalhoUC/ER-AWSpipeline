import boto3
import botocore
import pymysql
import os

def read_sql_from_s3(bucket_name, file_name):
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        sql_script = response['Body'].read().decode('utf-8')
        return sql_script
    except botocore.exceptions.ClientError as e:
        print(f"Error reading SQL file from S3: {e}")
        return None

def execute_sql_on_rds(sql_script, rds_host, rds_user, rds_password, rds_database):
    try:
        connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_database)
        cursor = connection.cursor()
        cursor.execute(sql_script)
        connection.commit()
        print("Database deployed successfully!")
    except Exception as e:
        print(f"Error executing SQL script on RDS: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # Set your AWS credentials if not already configured using environment variables or AWS CLI
    #aws_region = 'your-aws-region'
    s3_bucket_name = 'erplus-sql'
    sql_file_name = 'erplus.sql'
    rds_host = 'erplus-withdb-rdsinstance-jpwfterttovm.czgkzxn4tyv0.us-east-2.rds.amazonaws.com'
    rds_user = 'yadmin'
    rds_password = 'admin1234567'
    rds_database = 'tpchUsecase'

    sql_script = read_sql_from_s3(s3_bucket_name, sql_file_name)
    if sql_script:
        execute_sql_on_rds(sql_script, rds_host, rds_user, rds_password, rds_database)
