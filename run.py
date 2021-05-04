# from fastapi import FastAPI
from datetime import datetime
from botocore.exceptions import ClientError
import etcd3
import json
import os
import sqlite3
import boto3
import logging
from decouple import config

etcd_ip = config("ETCD_IP_ADDR")
etcd_port =config("ETCD_PORT")
env_endpoint_url = config("ENDPOINT_URL")
env_aws_access_key_id = config("AWS_ACCESS_KEY_ID")
env_aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY")



def backup_from_etcd(etcd_port, etcd_ip,file_name):
    etcd = etcd3.client(etcd_ip,etcd_port)
    con = sqlite3.connect(f'{file_name}.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS etcd (key TEXT, value TEXT)")
    json_dic ={}
    for val, metadata in etcd.get_all():
        json_dic.update({metadata.key.decode('utf-8'):val.decode('utf-8')})
        cur.execute("INSERT INTO etcd (key , value) VALUES (?, ?)",(metadata.key.decode('utf-8'),val.decode('utf-8')))
    with open(f'{file_name}.json', 'w') as json_file:
        json.dump(json_dic, json_file)
def upload(env_endpoint_url,env_aws_access_key_id,env_aws_secret_access_key,env_file_path,env_object_name):
    logging.basicConfig(level=logging.INFO)
    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url=env_endpoint_url,
            aws_access_key_id=env_aws_access_key_id,
            aws_secret_access_key=env_aws_secret_access_key
        )

    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket = s3_resource.Bucket('etcd-backup')
            file_path = env_file_path
            object_name = env_object_name
            with open(file_path, "rb") as file:
                bucket.put_object(
                    ACL='private',
                    Body=file,
                    Key=object_name
                )
        except ClientError as e:
            logging.error(e)


datetime_name= datetime.now().strftime("%d. %B %Y %I:%M%p")
backup_from_etcd(etcd_port,etcd_ip,datetime_name)
upload(env_endpoint_url,env_aws_access_key_id,env_aws_secret_access_key,f"{datetime_name}.db",f"/{datetime_name}.db")
upload(env_endpoint_url,env_aws_access_key_id,env_aws_secret_access_key,f"{datetime_name}.json",f"/{datetime_name}.json")
# app = FastAPI()
# @app.get('/')
# async def send_data():
#     return get_data_from_etcd(etcd_ip,etcd_port)



