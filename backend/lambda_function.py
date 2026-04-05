import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])
ALLOWED_ORIGIN = os.environ.get('ALLOWED_ORIGIN')

def lambda_handler(event, context):
    response = table.update_item(
        ExpressionAttributeNames={'#count': 'count'},
        ExpressionAttributeValues={':inc': 1},
        Key={'id': 'visitors'},
        UpdateExpression='ADD #count :inc',
        ReturnValues='UPDATED_NEW',   
    )
    return {
        'headers': {
            'Access-Control-Allow-Origin': ALLOWED_ORIGIN,
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'statusCode': 200,
        'body': json.dumps(int(response['Attributes']['count']))
    }