import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    rds = boto3.client('rds')

    sql_file = s3.download_file('erplus-sql', 'erplus.sql')
    rds.execute_sql(sql_file, database='tpchUsecase')

    return 'Successfully executed SQL file'