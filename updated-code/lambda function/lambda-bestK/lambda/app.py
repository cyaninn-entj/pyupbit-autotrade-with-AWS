import pyupbit
import numpy as np
import boto3


def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-ETH", count=7) #재배포 필요 230619확인
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror



def update_dynamodb_table(bestk):
    dynamodb = boto3.client('dynamodb')
    
    # define the table name and the key of the item to be updated
    table_name = 'table-for-Ethereum-Autotrade'
    item_key = {'Env': {'S': 'Dev'}}
    
    # define the attribute to be updated and its new value
    attribute_name = 'k-value'
    new_value = bestk
    
    # update the item with the new attribute value
    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key=item_key,
            UpdateExpression='SET #attr = :val',
            ExpressionAttributeNames={'#attr': attribute_name},
            ExpressionAttributeValues={':val': {'N': str(new_value)}}
        )
        print("success : updating dynamoDB talbe")
    except Exception as e:
        print("Exception : ", e)

    return response


def handler(event, context):
    dict={}
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(k)
        print("%.1f %f" % (k, ror))
        dict[k]=ror
    bestk=max(dict, key=dict.get)
    bestk=round(bestk, 1)

    print("best-k-value : "+str(bestk)+" !!!")

    result=update_dynamodb_table(bestk)

    return result