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

@mock_aws
def test_response_body_contains_count():
    table = boto3.resource('dynamodb').create_table(
        TableName = 'resume-visitor-count',
        KeySchema = [{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode = 'PAY_PER_REQUEST'
    )
    table.put_item(Item={'id': 'visitors', 'count': 0})
    response = lambda_handler({}, {})
    assert response ['body'] == '1'

@mock_aws
def test_CORS_headers():
    table = boto3.rousrce('dynamodb').create_table(
        TableName = 'resume-visitor-count',
        KeySchema = [{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode = 'PAY_PER_REQUEST'
    )
    table.put_item(Item={'id': 'visitors', 'count': 0})
    response = lambda_handler({}, {})
    assert response['headers']['Access-Control-Allow-Origin'] == '*'
    assert response['headers']['Access-Control-Allow-Methods'] == 'GET'
    assert response['headers']['Access-Control-Allow-Headers'] == 'Content-Type'