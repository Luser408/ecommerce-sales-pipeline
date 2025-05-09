import json
import boto3

glue = boto3.client('glue')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"New file: {key} in {bucket}")
        glue.start_job_run(JobName='sales_cleaning_job')
    return {
        'statusCode': 200,
        'body': json.dumps('Glue job triggered')
    }