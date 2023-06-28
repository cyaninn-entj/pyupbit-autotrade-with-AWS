import pyupbit
import datetime
import upbit_defs as m_upbit
import log_defs as m_log
import time
import schedule
import boto3

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

global best_k
global predicted_end_price
def read_dynamoDB_table() :
    global best_k
    global predicted_end_price
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


def main():
    global best_k
    global predicted_end_price

    d = datetime.datetime.now()
    year=str(d.strftime("%Y"))
    month=str(d.strftime("%m"))
    day=str(d.strftime("%d"))
    log_file_name="output"+year+month+day+".log"

    logfile=m_log.open_logfile(log_file_name)

    try :
        upbit_access_key, upbit_secret_key = get_parameter_fromSSM()
        bestk,predicted_end_price= read_dynamoDB_table()
        logs="success : get_parameter_fromSSM, read_dynamoDB_table"
        m_log.write_and_flush_logs(logfile, logs)
    except Exception as e:
        logs="failure : get_parameter_fromSSM, read_dynamoDB_table"
        m_log.write_and_flush_logs(logfile, logs)
        logs="Exception : "+str(e)
        m_log.write_and_flush_logs(logfile, logs)
    schedule.every().hour.do(lambda: read_dynamoDB_table())

    try :
        upbit_login = pyupbit.Upbit(upbit_access_key, upbit_secret_key)
        logs="success : login"
        m_log.write_and_flush_logs(logfile, logs)
    except Exception as e:
        logs="failure : login"
        m_log.write_and_flush_logs(logfile, logs)
        logs="Exception : "+str(e)
        m_log.write_and_flush_logs(logfile, logs)
    
    try :
        '''자동매매'''
        dt_today=datetime.datetime.now()
        logs="start daily autotrade : "+str(dt_today)
        m_log.write_and_flush_logs(logfile, logs)

        # trading start
        log_cup=0
        while True:
            try:
                now = datetime.datetime.now()
                start_time = m_upbit.get_start_time("KRW-ETH")
                end_time = start_time + datetime.timedelta(days=1)
                dt_now = datetime.datetime.now()

                if start_time < now < end_time - datetime.timedelta(minutes=5):
                    target_price = m_upbit.get_target_price("KRW-ETH", float(bestk))
                    current_price = m_upbit.get_current_price("KRW-ETH")
                    if target_price < current_price and current_price < predicted_end_price:
                        krw = m_upbit.get_balance("KRW", upbit_login)
                        if krw > 5000:
                            upbit_login.buy_market_order("KRW-ETH", krw*0.9995)
                            logs="buy_market_order : "+str(dt_now)
                            m_log.write_and_flush_logs(logfile, logs)
                    else :
                        if log_cup==10 :
                            logs="running :"+str(dt_now)
                            m_log.write_and_flush_logs(logfile, logs)
                            log_cup=0
                else:
                    eth = m_upbit.get_balance("ETH", upbit_login)
                    if eth > 0.00008:
                        upbit_login.sell_market_order("KRW-ETH", eth*0.9995)
                    break
                time.sleep(1); log_cup=log_cup+1
            except Exception as e:
                logs="Exception : "+str(e)
                m_log.write_and_flush_logs(logfile, logs)
                time.sleep(1)

        dt_today=datetime.datetime.now()
        logs="shutdown daily autotrade : "+str(dt_today)
        m_log.write_and_flush_logs(logfile, logs)

        m_log.close_logfile(logfile)
        m_log.send_logs_to_s3(log_file_name)

    except Exception as e:
        logs="failure : trading"
        m_log.write_and_flush_logs(logfile, logs)
        logs="Exception : "+str(e)
        m_log.write_and_flush_logs(logfile, logs)

main()
