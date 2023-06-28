import boto3
import os

def open_logfile(n):
    log_file_name=n
    f=open(log_file_name, 'a')
    return f

def write_and_flush_logs(f, log_string):
    logs=log_string+"\n"
    f.write(logs); f.flush()

def close_logfile(f):
    f.close()

def send_logs_to_s3(n):
    bucket_name="logs-ethereum-autotrade"
    file_path=n
    session = boto3.Session(profile_name='default')

    s3=session.client('s3')
    f=open(file_path, 'rb')
    s3.upload_fileobj(f, bucket_name, file_path)
