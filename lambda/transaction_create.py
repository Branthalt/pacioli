import boto3
from time import time
from datetime import datetime
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Transactions')

def create_item():
    item = {
        'id': 1,
        'timestamp': int(datetime(2018, 11, 7).timestamp()),
        'modified': int(time.time()),
        'description': 'awesome weekend'}

    return table.put_item(Item=item)

def lambda_handler(event, context):
    # TODO implement
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
