import boto3
from moto import mock_aws
import json
import os
os.environ['TABLE_NAME'] = 'resume-visitor-count'
from lambda_function import lambda_handler

@mock_aws
def test_count_increments():
    table = boto3.resource('dynamodb').create_table(
        TableName = 'resume-visitor-count',
        KeySchema = [{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode = 'PAY_PER_REQUEST'
    )
    table.put_item(Item={'id': 'visitors', 'count': 0})
    response = lambda_handler({}, {})
    assert response['statusCode'] == 200