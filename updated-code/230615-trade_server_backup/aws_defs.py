import boto3

def read_dynamoDB_table() :
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('table-for-Ethereum-Autotrade')

    response = table.get_item(
        Key={
            'Env': 'Dev'
        }
    )

    item = response['Item']
    best_k = item['k-value']
    predicted_end_price = item['endprice']

    return best_k, predicted_end_price



def get_parameter_fromSSM() :
    ssm = boto3.client('ssm')

    parameters=['/ethereum-autotrade/upbit-key/access-key',
                '/ethereum-autotrade/upbit-key/secret-key']
    upbit_keys=list()

    for i in parameters:
        response = ssm.get_parameter(
            Name=i,
            WithDecryption=True
        )
        upbit_keys.append(response['Parameter']['Value'])
    
    return upbit_keys[0],upbit_keys[1]